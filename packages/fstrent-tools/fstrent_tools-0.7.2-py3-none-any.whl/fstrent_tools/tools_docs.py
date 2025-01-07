import inspect
import os
import ast

def get_module_functions(file_path):
    """Extract functions and their docstrings from a Python file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        module_content = f.read()
    
    functions = []
    try:
        tree = ast.parse(module_content)
        
        # First, try to get __all__ list
        all_list = []
        for node in ast.walk(tree):
            if isinstance(node, ast.Assign):
                for target in node.targets:
                    if isinstance(target, ast.Name) and target.id == '__all__':
                        if isinstance(node.value, ast.List):
                            all_list = [n.value for n in node.value.elts if isinstance(n, ast.Constant)]
        
        # Then get functions that are in __all__
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                if not all_list or node.name in all_list:  # Include if in __all__ or if __all__ is empty
                    doc = ast.get_docstring(node) or "No description available"
                    # Get first line of docstring
                    description = doc.split('\n')[0]
                    functions.append((node.name, description))
                    
    except SyntaxError as e:
        print(f"Error parsing {file_path}: {e}")
    
    return functions

def generate_module_docs():
    """Generate markdown documentation for all tools modules and their functions."""
    
    # Get the src directory path
    src_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Find all tools_*.py files
    module_files = []
    for file in os.listdir(src_dir):
        if file.startswith('tools_') and file.endswith('.py'):
            module_files.append(file)
    
    docs = ["# fstrent_tools\n\nA comprehensive collection of Python utility functions.\n\n## Modules\n"]
    
    for module_file in sorted(module_files):
        # Get module name without .py extension
        module_name = module_file[:-3]
        
        # Get module title (remove 'tools_' prefix and capitalize)
        title = module_name[6:].capitalize()
        docs.append(f"\n### {title}\n")
        
        # Get functions from the module file
        file_path = os.path.join(src_dir, module_file)
        functions = get_module_functions(file_path)
        
        # Add function documentation
        for func_name, desc in sorted(functions):
            docs.append(f"- **{func_name}**: {desc}")
    
    return '\n'.join(docs)

def update_readme():
    """Update the README.md file with generated documentation."""
    docs = generate_module_docs()
    
    # Get path to README.md (one directory up from src)
    readme_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'README.md')
    
    # Write to README.md
    with open(readme_path, 'w', encoding='utf-8') as f:
        f.write(docs)

if __name__ == '__main__':
    update_readme() 