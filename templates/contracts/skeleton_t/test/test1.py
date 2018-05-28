# python3 ./tests/test3.py

import sys
import node
import sess
import eosf

def run(contract_dir):
    print('test node.reset():')
    node.reset()

    print('test node.info():')
    node.info()

    print('test sess.setup():')
    sess.setup()

    print('Contract based on the template definitions, possibly modified:')
    c = eosf.Contract(contract_dir)

    print('test c.deploy():')
    c.deploy()

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"alice"}', sess.alice)

    print('\n', 'c.get_console():')
    print(c.get_console(), "\n")

    print('test c.push_action("hi", sess.alice):')
    c.push_action("hi", '{"user":"carol"}', sess.carol)
    
    print('\n', 'c.get_console():')
    print(c.get_console(), "\n")
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run(str(sys.argv[1]))