import os
import re
import argparse

def save_code(path):
    '''Copy the current file without heredoc comments.
    '''
    md_file = os.path.abspath(path)
    python_file = os.path.splitext(md_file)[0] + ".py"

    with open(md_file, "r") as f:
        data = f.read()

    regex = re.compile(r'```python(.+?)```', flags=re.DOTALL)
    chunks = re.findall(regex, data)

    with open(python_file, "w") as output:
        output.write("".join(chunks))

    print('''
Python chunks from Markdown file
{}
saved in Python file
{}
    '''.format(md_file, python_file))

    os.system('python3 {}'.format(python_file))

parser = argparse.ArgumentParser(description='''
Given a path to a markdown file, having python code chunks, extract the chunks
and save them in a file of the same name but extended '.py'.

Example:
    python3 save_code set_account_permission.md
''')

parser.add_argument("path")

args = parser.parse_args()
save_code(args.path)