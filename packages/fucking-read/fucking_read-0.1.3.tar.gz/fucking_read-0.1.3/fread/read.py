import sys, os;
from exnd_curses import window;

file = "";

if len(sys.argv) == 2:
    arg = sys.argv[1];
    if (arg == "-h" or arg == "--help"):
        print("fread 'relative path'\nfread -a 'absolute path'");
    else:
        try:
            file = os.path.abspath(arg);       
        except:
            print("-h for help");
            exit();
elif len(sys.argv) == 3:
    arg = sys.argv[1];
    if arg != '-a':
        exit();
    file = sys.argv[2];
else:
    exit();

if (not os.path.isfile(file)): print("File not found!"); exit();

with open(file, 'r') as file:
    window = window.Window();
    window.changeLines(file.read());

if __name__ == "__main__": pass;