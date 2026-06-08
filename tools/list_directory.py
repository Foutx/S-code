import os

from langchain.tools import tool


@tool
def list_directory(path: str):
    """
    Возвращает список файлов и папок в указанной директории
    Args:
        path - путь до директории
    """

    try:

        items = os.listdir(path)

        return '\n'.join(items) if items else 'Директория пустая'

    except Exception as e:

        return f'Error: {e}'
