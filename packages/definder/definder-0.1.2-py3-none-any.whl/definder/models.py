# dependencies_finder.py
from pathlib import Path
import ast
from typing import Set, Dict, Tuple
from concurrent.futures import ProcessPoolExecutor
import asyncio
import os
from .package_mapping import get_package_name

class DependencyFinder:
    def __init__(self, src_paths: list[str], workers: int = None, no_save: bool = False):
        self.src_paths = src_paths
        self.workers = workers or os.cpu_count()
        self.third_party_imports: Set[str] = set()
        self.no_save = no_save
        self.local_modules: Set[str] = set()
        self.builtin_modules: Set[str] = set()
        self.required_modules: Set[str] = set()
        self.questionable_modules: Set[str] = set()
        self.relative_modules: Set[str] = set()
        
    def find_imports_in_file(self, file_path: Path) -> Set[str]:
        """Analyze imports in a single file."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except (IOError, OSError) as e:
            print(f"Failed to read {file_path}: {str(e)}")
            return set()
            
        imports = set()
        try:
            tree = ast.parse(content)
            for node in ast.walk(tree):
                # Handle 'import xxx' statements
                if isinstance(node, ast.Import):
                    for name in node.names:
                        imports.add(name.name.split('.')[0])
                
                # Handle 'from xxx import yyy' statements
                elif isinstance(node, ast.ImportFrom):
                    if node.module:
                        imports.add(node.module.split('.')[0])
        except SyntaxError as e:
            print(f"Failed to parse {file_path}: {str(e)}")
            
        return imports

    async def process_files(self) -> Dict[str, Set[str]]:
        """Process all files in parallel."""
        loop = asyncio.get_event_loop()
        with ProcessPoolExecutor(max_workers=self.workers) as executor:
            # Get all Python files
            python_files = self.get_python_files()
            
            print(f"\nScanning {len(python_files)} Python files... 🔍")
            
            # Process files in parallel
            tasks = []
            for file_path in python_files:
                task = loop.run_in_executor(
                    executor,
                    self.find_imports_in_file,
                    file_path
                )
                tasks.append(task)
                
            # Wait for all tasks to complete
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Merge results
            all_imports = set()
            for result in results:
                if isinstance(result, Exception):
                    continue
                all_imports.update(result)
            
            # Categorize imports
            self.builtin_modules = self.get_stdlib_modules()
            
            for imp in all_imports:
                if imp in self.builtin_modules:
                    continue
                elif imp in self.local_modules:
                    self.relative_modules.add(imp)
                elif any(q in imp.lower() for q in ['test', 'example', 'utils', 'tools']):
                    self.questionable_modules.add(imp)
                else:
                    self.required_modules.add(get_package_name(imp))
            
            return {
                'builtin': sorted(self.builtin_modules),
                'required': sorted(self.required_modules),
                'questionable': sorted(self.questionable_modules),
                'relative': sorted(self.relative_modules)
            }

    def get_python_files(self) -> Set[Path]:
        """Get all Python file paths and record local module names."""
        python_files = set()
        for src in self.src_paths:
            path = Path(src)
            if not path.exists():
                print(f"Warning: Path does not exist: {path}")
                continue
                
            if path.is_file():
                if path.suffix != '.py':
                    print(f"Warning: Skipping non-Python file: {path}")
                    continue
                python_files.add(path)
                self.local_modules.add(path.stem)
            elif path.is_dir():
                for py_file in path.rglob('*.py'):
                    python_files.add(py_file)
                    self.local_modules.add(py_file.stem)
        return python_files

    @staticmethod
    def get_stdlib_modules() -> Set[str]:
        """Get Python standard library modules list."""
        import sys
        import distutils.sysconfig as sysconfig
        
        stdlib_path = sysconfig.get_python_lib(standard_lib=True)
        stdlib_modules = set()
        
        # Add all builtin modules
        stdlib_modules.update(sys.builtin_module_names)
        
        # Add all modules from standard library path
        try:
            for path in Path(stdlib_path).rglob('*.py'):
                if path.stem != '__init__':
                    stdlib_modules.add(path.stem)
        except Exception as e:
            print(f"Warning: Error while scanning stdlib path: {str(e)}")
            
        return stdlib_modules

    def save_requirements(self, dependencies: Set[str]) -> str:
        """Save dependencies to requirements file and return the filename used"""
        if self.no_save:
            return None
            
        # Determine which requirements file to use
        if not Path('requirements.txt').exists():
            filename = 'requirements.txt'
        elif not Path('requirements-definder.txt').exists():
            filename = 'requirements-definder.txt'
        else:
            filename = 'requirements-definder.txt'
            
        # Write dependencies to file
        with open(filename, 'w') as f:
            for dep in sorted(dependencies):
                f.write(f"{dep}\n")
                
        return filename

def main():
    import argparse
    from pprint import pprint
    
    parser = argparse.ArgumentParser()
    parser.add_argument('src', nargs='+', help='Source file(s) or directory')
    parser.add_argument('--workers', type=int, help='Number of workers')
    parser.add_argument('--no-save', action='store_true', help='Do not save requirements file')
    args = parser.parse_args()
    
    try:
        finder = DependencyFinder(args.src, args.workers, args.no_save)
        
        loop = asyncio.get_event_loop()
        results = loop.run_until_complete(finder.process_files())
        
        # Pretty print results
        pprint(results)
        
        # Save requirements file
        if not args.no_save and results['required']:
            try:
                filename = finder.save_requirements(results['required'])
                print(f"\nSaved dependencies to {filename} 💾")
            except Exception as e:
                print(f"Error: Failed to save requirements: {str(e)}")
        
        print(f"\nAll done! ✨ 🔍 ✨")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()