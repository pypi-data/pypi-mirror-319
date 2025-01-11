# tests/test_notebook_debugger.py
import unittest
from PyDebugTool.debug import PyDebugger

class TestNotebookDebugger(unittest.TestCase):
    def test_enable_disable(self):
        debugger = PyDebugger()
        debugger.enable(langchain_model="llama3-8b-8192", api_key="test_key")
        self.assertIsNotNone(debugger.langchain_model)
        debugger.disable()
        self.assertIsNone(debugger.shell.showtraceback == debugger.handle_error)

if __name__ == '__main__':
    unittest.main()