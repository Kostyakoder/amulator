import getpass
import sys
import os
from pathlib import Path


class Node:
    def __init__(self, file_type, data='', real_path=None, parent=None):
        self.file_type = file_type
        self.data = data
        self.real_path = real_path
        self.parent = parent  # явное хранение родителя вместо '..'


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
        # Если это файл, создаем файловый узел
        node = Node('file', parent=parent)
        node.real_path = real_path
        try:
            with open(real_path, 'r', encoding='utf-8') as f:
                node.data = f.read()
        except:
            node.data = f"<binary file: {real_path}>"
        return node

    # Если это директория, создаем директорию и рекурсивно загружаем содержимое
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


def cd(node, name):
    if name in node.data and node.data[name].file_type == 'dir':
        return node.data[name]

    if node.real_path:
        new_path = os.path.join(node.real_path, name)
        if os.path.exists(new_path) and os.path.isdir(new_path):
            return load_real_directory(new_path, node)

    print("No such file or directory")
    return node


def who():
    return getpass.getuser()


def uniq():
    previous_line = None
    for line in sys.stdin:
        line = line.rstrip('\n')
        if line == "exit":
            break
        if line != previous_line:
            print(line)
            previous_line = line


def pwd(node):
    if node.real_path:
        return node.real_path + ('/' if not node.real_path.endswith(os.sep) else '')

    # Альтернативный способ для виртуальных узлов
    parts = []
    current = node
    while current and current.parent:
        for name, child in current.parent.data.items():
            if child == current:
                parts.append(name)
                break
        current = current.parent
    return '/' + '/'.join(reversed(parts)) + '/'


def mkdir(node, names):
    for name in names:
        new_node = Node('dir', {}, parent=node)
        node.data[name] = new_node
        if node.real_path:
            real_dir_path = os.path.join(node.real_path, name)
            os.makedirs(real_dir_path, exist_ok=True)
            new_node.real_path = real_dir_path




def ls(node):
    for name in sorted(node.data):
        file_type = 'd' if node.data[name].file_type == 'dir' else '-'
        print(f"{file_type} {name}", end='  ')
    print()



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
                case ["cd", name]:
                    new_node = cd(node, name)
                    if new_node != node:  # только если успешно сменили директорию
                        node = new_node
                case ['echo', *args]:
                    print(*args)
                case ['pwd']:
                    print(pwd(node))
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
