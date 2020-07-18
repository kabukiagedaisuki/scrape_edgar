from .cli.command import cmd

def main():
    cmd()

# `python -m edgar` という形で呼び出されたときのことを考慮
if __name__ == "__main__":
    main()
