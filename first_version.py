def act():
    a = input("kostyaKoder@mireahost:~$ ")
    b = a.split()
    if a == 'exit':
        exit()
    if (len(b)) == 0:
        return ""
    if b[0] == "ls":
        return b
    elif b[0] == 'cd':
        return b
    elif b[0] == 'pwd':
        return b
    else:
        return f"{b[0]}: command not found"

# if __name__ == '__main__':
#     args = sys.argv
#
#     path = args[1]
#     prompt = args[2]
#     script_path = args[3]
#
#     while True:
#         a = input(f"{prompt}> ")
#         print(act(a))

while True:
    print(act())