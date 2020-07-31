from kabu.cli.command import cmd
#from kabu.cli.edgar import Edgar
#from kabu.cli.consensus import Consensus

def main():
    cmd()

#main.add_command(Edgar)
#main.add_command(Consensus)

# `python -m edgar` という形で呼び出されたときのことを考慮
if __name__ == "__main__":
    main()
