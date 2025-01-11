import sys
import traceback
import re
from langchain_groq import ChatGroq
from IPython.core.interactiveshell import InteractiveShell
from rich.console import Console
from rich.panel import Panel
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from rich.syntax import Syntax
import os
import argparse


class PyDebugger:
    def __init__(self, langchain_model=None, api_key=None):
        self.langchain_model = ChatGroq(model=langchain_model, temperature=0.2, api_key=api_key)
        self.shell = InteractiveShell.instance() if 'IPython' in sys.modules else None
        self.original_showtraceback = self.shell.showtraceback if self.shell else None
        self.original_excepthook = sys.excepthook
        self.console = Console()
        self.environment = "notebook" if self.is_notebook() else "script"
        self.error_history = []

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
        self.console.print(
            Panel(
                "[bold green]You can ask a question about this error using `ask_question('Your question')`.[/bold green]",
                title="[bold blue]💡 Tip[/bold blue]",
                border_style="blue",
                expand=True
            )
        )

    def handle_script_error(self, exc_type, exc_value, exc_traceback):
        traceback.print_exception(exc_type, exc_value, exc_traceback)
        self.process_error(exc_type, exc_value, exc_traceback)

    def split_explanation_and_code(self, response):
        """
        Split the response into explanation and corrected code.
        """
        code_match = re.search(r"```\n(.*?)```", response, re.DOTALL)
        if not code_match:
            code_match = re.search(r"```Python\n(.*?)```", response, re.DOTALL)
        if code_match:
            explanation = response[:code_match.start()].strip()
            corrected_code = code_match.group(1).strip()
            return explanation, corrected_code
        return response.strip(), None

    def ask_question(self, question):
        if not self.error_history:
            self.console.print(
                Panel(
                    "[bold yellow]No error history found! Please run a code snippet with errors first.[/bold yellow]",
                    title="[bold red]⚠️ Error History Empty[/bold red]",
                    border_style="red"
                )
            )
            return

        # Retrieve the last error details
        last_error = self.error_history[-1]

        system_template = """
        Answer the user's question based on the following Python error details and traceback. If relevant, include suggestions. Try to correct the traceback based on the code input provided if provided at all.

        Error Details:
        - Code Error: {code_error}
        - Line Number: {line_number}
        - File Name: {file_name}

        User Question: {user_question}
        """
        prompt_template = ChatPromptTemplate.from_messages(
            [("system", system_template), ("user", "{user_question}")]
        )
        output_parser = StrOutputParser()
        chain = prompt_template | self.langchain_model | output_parser

        try:
            response = chain.invoke({
                "code_error": last_error["code_error"],
                "line_number": last_error["line_number"],
                "file_name": last_error["file_name"],
                "user_question": question
            })

            explanation, corrected_code = self.split_explanation_and_code(response)
            # Print the explanation in the response panel
            explanation_panel = Panel(
                explanation.strip(),
                title="[bold cyan]🤖 Explanation[/bold cyan]",
                border_style="cyan",
                expand=True
            )
            self.console.print(explanation_panel)

            # Print the corrected code in a separate panel, if available
            if corrected_code:
                syntax = Syntax(corrected_code.strip(), "python", theme="monokai")
                code_panel = Panel(
                    syntax,
                    title="[bold green]✅ Corrected Code[/bold green]",
                    border_style="green",
                    expand=True
                )
                self.console.print(code_panel)

        except Exception as langchain_error:
            # Handle LangChain errors gracefully
            error_handling_panel = Panel(
                f"[bold white]{str(langchain_error)}[/bold white]",
                title="[bold yellow]⚠️ PyDebugger Question Error[/bold yellow]",
                border_style="yellow",
                expand=True
            )
            self.console.print(error_handling_panel)

    def process_error(self, exc_type, exc_value, exc_traceback):
        error_details = self.extract_error_details(exc_type, exc_value, exc_traceback)
        self.error_history.append(error_details)

        file_content = self.get_file_content(error_details.get("file_name"))
        code_snippet = None
        if file_content and error_details["line_number"]:
            lines = file_content.splitlines()
            start = max(0, error_details["line_number"] - 3)
            end = min(len(lines), error_details["line_number"] + 2)
            code_snippet = "\n".join(lines[start:end])

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

            # Extract corrected code if available
            explanation, corrected_code = self.split_explanation_and_code(response)

            # Print the explanation in the response panel
            explanation_panel = Panel(
                explanation.strip(),
                title="[bold cyan]🤖 Explanation[/bold cyan]",
                border_style="cyan",
                expand=True
            )
            self.console.print(explanation_panel)

            # Print the corrected code in a separate panel, if available
            if corrected_code:
                syntax = Syntax(corrected_code.strip(), "python", theme="monokai")
                code_panel = Panel(
                    syntax,
                    title="[bold green]✅ Corrected Code[/bold green]",
                    border_style="green",
                    expand=True
                )
                self.console.print(code_panel)


        except Exception as langchain_error:
            error_handling_panel = Panel(
                f"[bold white]{str(langchain_error)}[/bold white]",
                title="[bold yellow]⚠️ PyDebugger Error[/bold yellow]",
                border_style="yellow",
                expand=True
            )
            self.console.print(error_handling_panel)