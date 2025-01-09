import sys
import traceback
from langchain_groq import ChatGroq
from IPython.core.interactiveshell import InteractiveShell
from rich.console import Console
from rich.panel import Panel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.syntax import Syntax
import inspect
import os

class PyDebugger:
    def __init__(self, langchain_model=None, api_key=None):
        self.langchain_model = ChatGroq(model=langchain_model, temperature=0.2, api_key=api_key)
        self.shell = InteractiveShell.instance() if 'IPython' in sys.modules else None
        self.original_showtraceback = self.shell.showtraceback if self.shell else None
        self.original_excepthook = sys.excepthook
        self.console = Console()
        self.environment = "notebook" if self.is_notebook() else "script"

    def is_notebook(self):
        try:
            from IPython import get_ipython
            if get_ipython() is not None and 'IPKernelApp' in get_ipython().config:
                return True  # Running in a Jupyter Notebook
        except ImportError:
            pass
        return False  # Running in a Python script (.py)

    def enable(self):
        if self.environment == "notebook":
            self.original_showtraceback = self.shell.showtraceback
            self.shell.showtraceback = self.handle_notebook_error
        else:
            sys.excepthook = self.handle_script_error

    def disable(self):
        if self.environment == "notebook" and self.original_showtraceback:
            self.shell.showtraceback = self.original_showtraceback
        elif self.environment == "script":
            sys.excepthook = self.original_excepthook

    def extract_error_details(self, exc_type, exc_value, exc_traceback):
        """
        Extract error details such as code and line number from the traceback.
        """
        formatted_error = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))
        tb_lines = traceback.format_tb(exc_traceback)

        # Extract line number and filename
        last_tb_line = tb_lines[-1] if tb_lines else ''
        line_number = None
        file_name = None
        for line in last_tb_line.splitlines():
            if 'line' in line and ', in ' in line:
                parts = line.split(',')
                line_number = int(parts[1].split('line')[1].strip())
                file_name = parts[0].split('File')[1].strip().strip('"')

        return {
            "code_error": formatted_error,
            "line_number": line_number,
            "file_name": file_name
        }

    def get_file_content(self, file_name):
        """
        Retrieve the content of the .py file for error context.
        """
        if file_name and os.path.exists(file_name):
            with open(file_name, 'r') as f:
                return f.read()
        return None

    def handle_notebook_error(self, *args, **kwargs):
        exc_type, exc_value, exc_traceback = sys.exc_info()
        if self.original_showtraceback:
            self.original_showtraceback(*args, **kwargs)
        self.process_error(exc_type, exc_value, exc_traceback)

    def handle_script_error(self, exc_type, exc_value, exc_traceback):
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        self.process_error(exc_type, exc_value, exc_traceback)


    def process_error(self, exc_type, exc_value, exc_traceback):
        error_details = self.extract_error_details(exc_type, exc_value, exc_traceback)

        # Get file content if it's a .py file
        file_content = self.get_file_content(error_details.get("file_name"))
        # Generate explanation and solution using LangChain
        system_template = """
        Analyze the following Python code error. Identify the cause and suggest a possible correction for the error part only. Answer in short and do not over-explain.

        Error Details:
        - Code Error: {code_error}
        - Line Number: {line_number}
        - File Name: {file_name}
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{code_error}")]
        )
        output_parser = StrOutputParser()
        chain = prompt_template | self.langchain_model | output_parser

        try:
            response = chain.invoke(error_details)

            # Display the explanation and solution in a professional format
            solution_panel = Panel(
                f"[bold white]{response}[/bold white]",
                title="[bold cyan]🤖 PyDebugger[/bold cyan]",
                border_style="cyan",
                expand=True
            )
            self.console.print(solution_panel)
        except Exception as langchain_error:
            # Handle any issues with LangChain itself
            error_handling_panel = Panel(
                f"[bold white]{str(langchain_error)}[/bold white]",
                title="[bold yellow]⚠️ PyDebugger Error[/bold yellow]",
                border_style="yellow",
                expand=True
            )
            self.console.print(error_handling_panel)
