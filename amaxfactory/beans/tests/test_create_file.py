
import os,json
from amaxfactory.eosf import *


def test_x():
        file_name = 'nftredpackx'
        contract_name = 'nft.redpack'
        master = new_master_account()

    
        nftredpack = new_account(master,contract_name)
        nftredpack_smart = Contract(nftredpack,"/root/contracts/did.contracts")
        nftredpack_smart.build_sh("nft.redpack")
        obj = json.load(open(nftredpack_smart.abi_file))
        
        content = 'from base.amcli import runaction\nfrom base.baseClass import baseClass\n\n'
        demo = 'from amaxfactory.eosf import * \n'
        demo += 'verbosity([Verbosity.INFO, Verbosity.OUT, Verbosity.TRACE, Verbosity.DEBUG]) \n\n'
        demo += f'def test_start():\n\treset()\n\tmaster = new_master_account()\n\t{file_name} = new_account("{contract_name}")\n'
        for action in obj['actions']:
            for struct in obj['structs']:
                struct_name = struct['name']
                if action['name'] == struct_name:
                    print(struct_name)
                    print(struct['fields'])
                    func = '\tdef ' + struct_name + '(self,'
                    body = f'''self.response = runaction(self.contract + f""" {struct_name} '['''
                    kv = ''
                    for key in struct['fields']:
                        key_type = key['type']
                        key_name = key['name']
                        value = ""
                        if key_type == 'name':
                            value = "'user1'"
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'string':
                            value = "'x'"
                            body += '"{' + key_name + '}"' + ','
                        elif str(key_type).find('uint') >= 0:
                            value = 1
                            body += "{" + key_name + "}" + ','
                        elif key_type == 'symbol':
                            value = "'8,AMAX'"
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'asset':
                            value = '"0.10000000 AMAX"'
                            body += '"{' + key_name + '}"' + ','
                        elif key_type == 'bool':
                            value = "'true'"
                            body += '"{' + key_name + '}"' + ','
                        else :
                            value = '1'
                            body += '"{' + key_name + '}"' + ','

                        kv += f'"{key_name}":{value},'
                    kv = "{"+kv+"},"
                    kv += "admin"
                    demo += f'\ndef test_{struct_name}():\n\t{file_name} = new_account("{contract_name}")\n\tadmin = new_account("admin")\n\t{file_name}.pushaction("{struct_name}",{kv}) \n'
                    func += kv
                    body = body[0:-1]
                    content += func + '):\n\t\t'
                    content += body + ''']' -p {suber}""") \n'''
                    content += '\t\treturn self\n\n'
        for table in obj['tables']:
            name = table['name']
            func = '\tdef ' + name + '(self,'
        # os.popen(f"mkdir {contract}case")
        # with open(f'/root/contracts/pythonProject1/{contract}case/{contract}.py', 'w', encoding='UTF-8') as file:
        #     file.write(content)
        dir = os.path.dirname(os.path.abspath(__file__))
        print(dir)
        with open(f'{dir}/test_{file_name}demo.py', 'w', encoding='UTF-8') as file:
            file.write(demo)



