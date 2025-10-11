import os


def act(a):
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



if __name__ == "__main__":
    prompt = "$~ kostyaKoder@mireahost:~$"
    script_path = "commands.txt"

    with open(script_path, 'r') as file:
        commands = file.readlines()
        for cmd in commands:
            cmd = cmd.strip()
            if cmd:
                print(f"{os.getcwd()} {prompt}> {cmd}") # просто путь в 3 этапе
                print(act(cmd))
                if (act(cmd) == f"{cmd}: command not found"):
                    break
    # while True:
    #     a = input(f"{prompt}> ")
    #     print(act(a))
