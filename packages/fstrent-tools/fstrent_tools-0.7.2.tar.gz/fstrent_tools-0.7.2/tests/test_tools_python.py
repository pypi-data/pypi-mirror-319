import pytest
from src.tools_python import (
    execute_python_script, get_package_version,
    install_package, list_packages,
    run_python_code, uninstall_package
)
import sys
import subprocess

def test_run_python_code():
    """Test running Python code"""
    result = run_python_code("print('test')")
    assert result == 0

def test_execute_python_script(tmp_path):
    """Test executing Python script"""
    script_path = tmp_path / "test.py"
    script_path.write_text("print('test')")
    result = execute_python_script(str(script_path))
    assert result == 0

def test_package_operations():
    """Test package management functions"""
    packages = list_packages()
    assert isinstance(packages, list)
    
    version = get_package_version("pip")
    assert isinstance(version, str)

@pytest.mark.skip(reason="Avoid modifying installed packages during tests")
def test_package_installation():
    """Test package installation/uninstallation"""
    test_package = "pytest"
    install_package(test_package)
    assert test_package in list_packages()
    
    uninstall_package(test_package)
    assert test_package not in list_packages() 