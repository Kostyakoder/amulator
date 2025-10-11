import getpass
import sys
import os
from pathlib import Path


class Node:
    def __init__(self, file_type, data='', real_path=None, parent=None):
        self.file_type = file_type
        self.data = data
        self.real_path = real_path
        self.parent = parent


def load_real_directory(real_path, parent=None, visited=None):
    if visited is None:
        visited = set()

    path = Path(real_path)
    if not path.exists():
        raise ValueError(f"Path {real_path} does not exist")

    # Защита от циклических ссылок
    real_path = os.path.abspath(real_path)
    if real_path in visited:
        return None
    visited.add(real_path)

    if path.is_file():
        node = Node('file', parent=parent)
        node.real_path = real_path
        try:
            with open(real_path, 'r', encoding='utf-8') as f:
                node.data = f.read()
        except:
            node.data = f"<binary file: {real_path}>"
        return node

    node = Node('dir', {}, real_path, parent)

    try:
        for item in path.iterdir():
            if item.name.startswith('.'):  # пропускаем скрытые файлы
                continue
            child_node = load_real_directory(str(item), node, visited.copy())
            if child_node:
                node.data[item.name] = child_node

    except PermissionError:
        node.data = {"error": "Permission denied"}

    return node


def mkdir(node, names):
    for name in names:
        new_node = Node('dir', {}, parent=node)
        node.data[name] = new_node
        if node.real_path:
            real_dir_path = os.path.join(node.real_path, name)
            os.makedirs(real_dir_path, exist_ok=True)
            new_node.real_path = real_dir_path



def reload_from_disk(node):
    if node.real_path and os.path.exists(node.real_path):
        return load_real_directory(node.real_path, node.parent)
    return node


def get_user_directory():
    default_path = os.getcwd()
    return default_path


def repl(node):
    while True:
        try:
            command = input(f'{pwd(node)}> ').split()
            if not command:
                continue

            match command:
                case ["exit"]:
                    return
                case ['mkdir', *names]:
                    mkdir(node, names)
                case ['uniq']:
                    uniq()
                case ['ls']:
                    ls(node)
                case ['pwd']:
                    print(pwd(node))
                case ["cd", name]:
                    new_node = cd(node, name)
                    if new_node != node:
                        node = new_node
                case ['echo', *args]:
                    print(*args)
                case ['rmdir', *names]:
                    rmdir(node, names)
                case ['who']:
                    print(who())
                case ['reload']:
                    node = reload_from_disk(node)
                    print("Reloaded from disk")
                case _:
                    print(f"Unknown command: {command[0]}")
        except KeyboardInterrupt:
            print("\nUse 'exit' to quit")
        except Exception as e:
            print(f"Error: {e}")


# Основная программа
if __name__ == "__main__":
    try:
        user_path = get_user_directory()
        root = load_real_directory(user_path)
        repl(root)
    except Exception as e:
        root = Node('dir', {})
        mkdir(root, ['home'])
        repl(root)