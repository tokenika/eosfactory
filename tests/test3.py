# python3 ./tests/test3.py

import pyteos
import node
import sess
import eosf

def run():
    print('test node.reset():')
    node.reset()

    print('test node.info():')
    node.info()

    print('test sess.setup():')
    sess.setup()

    print('test Template():')
    t = pyteos.Template(
        "_e4b2ffc804529ce9c6fae258197648cc2", "", remove_existing = True)

    print('Contract based on the template definitions, possibly modified:')
    c = eosf.Contract(t.contract_path())
    
    print('test c.build():')
    c.build()

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

    print('test c.delete():')
    c.delete()
    
    print('test node.stop():')
    node.stop()
    
    print("Test OK")


if __name__ == "__main__":
    run()