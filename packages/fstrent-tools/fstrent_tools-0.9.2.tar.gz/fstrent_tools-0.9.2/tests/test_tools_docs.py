import pytest
from src.tools_docs import (
    generate_module_docs,
    get_module_functions,
    update_readme
)

def test_get_module_functions(tmp_path):
    """Test function extraction from Python file"""
    test_file = tmp_path / "test_module.py"
    test_file.write_text('''
def test_func():
    """Test docstring"""
    pass
''')
    
    functions = get_module_functions(str(test_file))
    assert "test_func" in functions
    assert functions["test_func"] == "Test docstring"

@pytest.mark.skip(reason="Requires actual module files")
def test_generate_docs():
    """Test documentation generation"""
    docs = generate_module_docs()
    assert isinstance(docs, str)
    assert "## Modules" in docs 