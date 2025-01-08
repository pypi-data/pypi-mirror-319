import os
from pathlib import Path
import ast
import sys
import re
import shutil

CHAR_LIMIT_PER_FILE = 150_000

def ensure_output_dir():
    """Create or clean the output directory."""
    output_dir = Path('./crawler_results')
    if output_dir.exists():
        shutil.rmtree(output_dir)
    output_dir.mkdir()
    return output_dir

def get_file_content(file_path):
    """Read and return full file content."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception as e:
        return f"[Error reading file: {str(e)}]"

def extract_code_structure(file_path):
    """Extract key elements from a Python file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        structure = []
        
        # Extract imports
        import_lines = []
        for line in content.split('\n'):
            if line.strip().startswith(('import ', 'from ')):
                import_lines.append(line.strip())
        
        if import_lines:
            structure.append("IMPORTS:")
            structure.extend(import_lines)
            structure.append("")
        
        # Parse AST for functions and classes
        try:
            tree = ast.parse(content)
            
            for node in ast.walk(tree):
                if isinstance(node, ast.FunctionDef):
                    func_desc = [f"FUNCTION: {node.name}"]
                    args = [arg.arg for arg in node.args.args]
                    func_desc.append(f"Args: {', '.join(args)}")
                    if (ast.get_docstring(node)):
                        func_desc.append("Docstring:")
                        func_desc.append(ast.get_docstring(node))
                    structure.extend(func_desc)
                    structure.append("")
                
                elif isinstance(node, ast.ClassDef):
                    class_desc = [f"CLASS: {node.name}"]
                    if (ast.get_docstring(node)):
                        class_desc.append("Docstring:")
                        class_desc.append(ast.get_docstring(node))
                    structure.extend(class_desc)
                    structure.append("")

        except SyntaxError:
            structure.append("[Could not parse Python code structure - syntax error]")
            
        return "\n".join(structure)
        
    except Exception as e:
        return f"[Error analyzing file: {str(e)}]"

def extract_js_structure(file_path):
    """Extract key elements from a JavaScript file."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
            
        structure = []
        
        # Extract imports
        import_lines = []
        for line in content.split('\n'):
            if re.match(r'^\s*(import|require|export)', line.strip()):
                import_lines.append(line.strip())
        
        if import_lines:
            structure.append("IMPORTS/EXPORTS:")
            structure.extend(import_lines)
            structure.append("")
        
        # Extract functions and classes
        functions = re.finditer(r'(async\s+)?function\s+(\w+)\s*\([^)]*\)|const\s+(\w+)\s*=\s*(async\s*)?\([^)]*\)\s*=>', content)
        for match in functions:
            structure.append(f"FUNCTION: {match.group().strip()}")
            structure.append("")
        
        classes = re.finditer(r'class\s+(\w+)(?:\s+extends\s+(\w+))?\s*\{', content)
        for match in classes:
            structure.append(f"CLASS: {match.group().strip()}")
            structure.append("")
            
        return "\n".join(structure)
        
    except Exception as e:
        return f"[Error analyzing file: {str(e)}]"

def should_ignore(path):
    """Check if path should be ignored."""
    ignore_patterns = {
        '.git', '__pycache__', 'venv', 'env', 'node_modules',
        '.pyc', '.pyo', '.pyd', '.so', '.dll', '.dylib',
        '.idea', '.vscode', '.DS_Store', 'output_', 
        'docs', 'documentation', '_docs', 'crawler_results', 'input_data', 'output_data'
    }
    
    path_str = str(path)
    return any(pattern in path_str for pattern in ignore_patterns) or \
           any(part.lower() == "docs" for part in Path(path_str).parts)

def generate_tree(start_path):
    """Generate tree structure of the project."""
    tree = []
    start_path = Path(start_path)
    print(f"Scanning directory: {start_path.absolute()}")
    
    try:
        for path in sorted(start_path.rglob('*')):
            if should_ignore(path):
                continue
            relative_path = path.relative_to(start_path)
            depth = len(relative_path.parents) - 1
            prefix = '│   ' * depth + '├── '
            tree.append(f"{prefix}{path.name}")
    except Exception as e:
        print(f"Error while generating tree: {str(e)}")
        return "Error generating tree structure"
    
    return '\n'.join(tree)

class OutputManager:
    def __init__(self, base_path, prefix):
        self.base_path = Path(base_path)
        self.prefix = prefix
        self.current_file_num = 1
        self.current_char_count = 0
        self.current_file = None
        self._open_new_file()

    def _open_new_file(self):
        if self.current_file:
            self.current_file.close()
        output_path = self.base_path / f'{self.prefix}_{self.current_file_num}.txt'
        print(f"\nCreating new output file: {output_path}")
        self.current_file = open(output_path, 'w', encoding='utf-8')
        self.current_char_count = 0
        self.current_file_num += 1

    def write(self, content):
        content_length = len(content)
        if self.current_char_count + content_length > CHAR_LIMIT_PER_FILE:
            self._open_new_file()
        self.current_file.write(content)
        self.current_char_count += content_length

    def close(self):
        if self.current_file:
            self.current_file.close()

def main():
    current_dir = Path('.')
    print(f"Starting code analysis in: {current_dir.absolute()}")
    
    # Create output directory
    output_dir = ensure_output_dir()
    
    files_processed = 0
    errors_encountered = 0
    
    try:
        # Create both brief and full output managers
        brief_output = OutputManager(output_dir, 'brief')
        full_output = OutputManager(output_dir, 'full')
        
        # Generate and write tree structure to both outputs
        print("Generating project structure...")
        tree_structure = "PROJECT STRUCTURE\n" + "=" * 80 + "\n\n" + generate_tree(current_dir) + "\n\n"
        brief_output.write(tree_structure)
        full_output.write(tree_structure)
        
        # Process files
        print("Analyzing files...")
        brief_output.write("CODE STRUCTURE\n" + "=" * 80 + "\n\n")
        full_output.write("FILE CONTENTS\n" + "=" * 80 + "\n\n")
        
        for path in sorted(current_dir.rglob('*')):
            if should_ignore(path) or not path.is_file():
                continue
                
            try:
                print(f"Analyzing: {path}")
                header = f"FILE: {path}\n" + "-" * 80 + "\n"
                
                # Write brief structure
                if path.suffix.lower() == '.py':
                    brief_content = extract_code_structure(path)
                elif path.suffix.lower() == '.js':
                    brief_content = extract_js_structure(path)
                else:
                    brief_content = "File type not supported for structure analysis"
                
                brief_output.write(header + brief_content + "\n" + "-" * 80 + "\n\n")
                
                # Write full content
                full_content = get_file_content(path)
                full_output.write(header + full_content + "\n" + "-" * 80 + "\n\n")
                
                files_processed += 1
            except Exception as e:
                print(f"Error processing {path}: {str(e)}")
                errors_encountered += 1
        
        brief_output.close()
        full_output.close()
        
        print("\nAnalysis complete!")
        print(f"Files processed: {files_processed}")
        print(f"Errors encountered: {errors_encountered}")
        print(f"Output files created in: {output_dir.absolute()}")
        
    except Exception as e:
        print(f"Critical error: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()