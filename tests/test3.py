import node
import sess
from eosf import *

def run():
    node.reset()
    sess.init()

    #c = Contract("currency")
    #c = Contract("/mnt/d/Workspaces/EOS/eosfactory/contracts/currency")
    #c.get_code()

    #t = Template("test5")
    t = Template("/mnt/d/Workspaces/EOS/eosfactory/contracts/test6")
    #t.get_code()
    
    #print("Test OK")
    node.stop()

if __name__ == "__main__":
    run()
    