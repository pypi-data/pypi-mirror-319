# PyDebugger

**PyDebuggerTools** is a Python library designed to enhance error debugging in both `.ipynb` and `.py` scripts. It provides a detailed explanation of errors and suggests possible corrections using the power of LangChain and advanced traceback analysis.

## Features

- **Environment-Aware Debugging**: Automatically detects whether the code is running in a `.py` file or a Jupyter Notebook and adapts its behavior accordingly.
- **Error Analysis and Correction**: Extracts error details (like line number, file name, and traceback) and generates concise explanations with possible solutions.
- **Code Context Display**: For `.py` files, displays the code context where the error occurred, highlighting the relevant lines.
- **Seamless Integration with LangChain**: Uses LangChain's AI capabilities to provide intelligent error solutions.

## Installation

Install the package using pip:
```bash
pip install PyDebugTools
```

## Usage

### Basic Example

```python
from PyDebugTool.debug import PyDebugger

debugger = PyDebugger(langchain_model="llama3-8b-8192", api_key="your_groq_api_key")
debugger.enable()

```

### How It Works
1. **Initialization**: Create an instance of `PyDebugTool` by specifying your LangChain model and API key.
2. **Enable Debugger**: Call `enable()` to activate error handling.
3. **Error Handling**: When an error occurs, PyDebugger will intercept it and display detailed insights along with possible fixes.

## Detailed Behavior
- **In `.ipynb` files**: Overrides the default IPython traceback display to show enhanced error details and solutions.
- **In `.py` Scripts**: Replaces the default Python exception hook to provide enriched error handling in the console.

## Example Code

When an error occurs, PyDebugger might display something like this:

```python
from PyDebugTool.debug import PyDebugger

debugger = PyDebugger(langchain_model="llama3-8b-8192", api_key="your_groq_api_key")
debugger.enable()

import tensorflow as tf

```
```
Traceback (most recent call last):
  File "C:\Users\Sambit Mallick\Desktop\mlops\LLM_TOOL_SOFTWARE\test.py", line 6, in <module>
    import tensorflow as tf
ModuleNotFoundError: No module named 'tensorflow'

┌─────────────────────────────── 🤖 PyDebugger ───────────────────────────────┐
│ The error is caused by the Python interpreter not being able to find the    │
│ TensorFlow module. This is likely because TensorFlow is not installed in    │
│ the Python environment being used to run the script.                        │
│                                                                             │
│ To correct this error, you can install TensorFlow using pip:                │
│                                                                             │
│ `pip install tensorflow`                                                    │
│                                                                             │
│ Alternatively, you can install it using conda if you are using Anaconda:    │
│                                                                             │
│ `conda install tensorflow`                                                  │
└─────────────────────────────────────────────────────────────────────────────┘

```

## Dependencies
- `langchain_groq`
- `IPython`
- `rich`

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Contributions are welcome! Please submit issues and pull requests to improve the library.

## Author
Sambit Mallick - Feel free to reach out for collaboration or queries.

## Acknowledgments
- Powered by LangChain and Groq LLM.

