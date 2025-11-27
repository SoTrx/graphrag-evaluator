#!/usr/bin/env python3
"""
Script to validate that all Python imports in Jupyter notebooks are properly organized using isort.
"""

import os
import json
import subprocess
import tempfile
from pathlib import Path


def extract_python_cells_from_notebook(notebook_path):
    """Extract Python code cells from a Jupyter notebook."""
    with open(notebook_path, 'r', encoding='utf-8') as f:
        notebook = json.load(f)
    
    python_code = []
    for cell in notebook.get('cells', []):
        if cell.get('cell_type') == 'code' and cell.get('metadata', {}).get('language') == 'python':
            source = cell.get('source', [])
            if isinstance(source, list):
                code = ''.join(source)
            else:
                code = source
            
            # Skip cells that are just pip installs or shell commands
            if not code.strip().startswith(('!', '%')):
                python_code.append(code)
    
    return '\n\n'.join(python_code)


def check_imports_with_isort(code):
    """Check if the imports in the code are properly organized using isort."""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.py', delete=False) as temp_file:
        temp_file.write(code)
        temp_file.flush()
        
        try:
            # Run isort in check mode
            result = subprocess.run(
                ['isort', '--check-only', '--diff', temp_file.name],
                capture_output=True,
                text=True
            )
            
            if result.returncode == 0:
                return True, "Imports are properly organized"
            else:
                return False, result.stdout
        finally:
            os.unlink(temp_file.name)


def main():
    """Main function to check all Python notebooks."""
    root_dir = Path(__file__).parent
    notebook_files = list(root_dir.rglob('*.ipynb'))
    
    python_notebooks = []
    for notebook_path in notebook_files:
        if 'python' in str(notebook_path):
            python_notebooks.append(notebook_path)
    
    print(f"Found {len(python_notebooks)} Python notebooks to check:")
    
    all_good = True
    for notebook_path in python_notebooks:
        print(f"\nChecking: {notebook_path.relative_to(root_dir)}")
        
        try:
            code = extract_python_cells_from_notebook(notebook_path)
            if not code.strip():
                print("  ✓ No Python code to check")
                continue
                
            is_organized, message = check_imports_with_isort(code)
            if is_organized:
                print("  ✓ Imports are properly organized")
            else:
                print("  ✗ Imports need reorganization:")
                print(f"    {message}")
                all_good = False
                
        except Exception as e:
            print(f"  ✗ Error checking notebook: {e}")
            all_good = False
    
    if all_good:
        print("\n🎉 All Python imports are properly organized!")
    else:
        print("\n❌ Some imports need to be reorganized.")
    
    return 0 if all_good else 1


if __name__ == "__main__":
    exit(main())
