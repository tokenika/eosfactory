


import os
from amaxfactory.core.account import CreateAccount
import unittest
from amaxfactory.shell import init

class Testx(unittest.TestCase):
    
    
    def test_4(self):
        dir = os.path.dirname(os.path.abspath(__file__))
        init.create_bean("amax.recover","/root/contracts/joss/amax.contracts/src_tools/build/contracts/amax.recover/amax.token.abi",dir)

    def test_5(self):
 
        wasm_path = os.getenv("FACTORY_DIR") + "/templates/wasm/"
        file_dir = os.path.dirname(os.path.abspath(__file__))
        bean_list = ""
        dir_list = []
        for root, dirs, files in os.walk(wasm_path):
            dir_list = dirs
            break
        print(dir_list, len(dir_list))

        for dir in dir_list:
            dir_list = []
            for root, dirs, files in os.walk(wasm_path+"/"+dir):
                dir_list = dirs
                break
            print(dir_list, len(dir_list))

            for contract_name in dir_list:
                if str(contract_name)[0] != "_":
                    init.create_bean(contract_name,f"{dir}/{contract_name}/{contract_name}.abi",file_dir,abi_in_factory=True)
                    class_name = str(contract_name).replace(".","_")
                    bean_list += f"from amaxfactory.bean.{class_name} import {class_name.upper()}\n"
        
        with open(f'{file_dir}/bean_list.py', 'w', encoding='UTF-8') as file:
            file.write(bean_list)
            

if __name__ == "__main__":
    unittest.main()

