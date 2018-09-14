import os
import re
import sys

def save_code():
    '''Copy the current file without heredoc comments.
    '''
    if len(sys.argv) < 2 or sys.argv[1] != "-s" and sys.argv[1] != "--save":
        return

    source = os.path.abspath(__file__)
    print(source)
    result = os.path.splitext(source)[0] + ".1.py"

    data = open(source, "r").read()
    prog = re.compile(r'\'\'\'.*?\'\'\'', flags=re.DOTALL)

    open(result, "w").write(re.sub(prog, '', data))
    exit()

if __name__ == "__main__":
    save_code()

