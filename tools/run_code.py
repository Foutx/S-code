import sys

import os

import subprocess

from langchain.tools import tool


@tool
def run_code(path: str):
    """
    Запускает файл по указанной директории
    Args:
        path - путь до файла
    """

    try:

        with open(path, 'r', encoding='utf-8') as f:

            code = f.read()
            
    except:

        code = ''
    
    is_gui = any(lib in code for lib in ['tkinter', 'pygame', 'PyQt', 'wx'])
    
    if is_gui:

        subprocess.Popen([sys.executable, path])

        return "Success: GUI приложение запущено"
    
    result = subprocess.run(
        [sys.executable, path],
        capture_output=True,
        text=True,
        encoding='utf-8',
        errors='replace',
        env={**os.environ, 'PYTHONIOENCODING': 'utf-8'}
    )

    if result.stderr:

        return f"Error: {result.stderr}"

    return f"Success: {result.stdout}"