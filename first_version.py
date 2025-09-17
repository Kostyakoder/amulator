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



while True:
    print(act())