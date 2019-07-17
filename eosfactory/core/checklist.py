'''
'''
import sys
import json
import argparse
import eosfactory.core.utils as utils
import eosfactory.core.config as config

IS_ERROR = 2
IS_WARNING = 1

class Checklist():

    def __init__(self, is_html=False, error_codes=""):
        self.is_html = is_html
        self.html_text = ""
        self.is_error = False
        self.is_warning = False
        self.IS_WINDOWS = utils.is_windows_ubuntu()
        self.os_version = utils.os_version()

        self.print_msg("EOSFactory version {}".format(config.VERSION))

################################################################################
# psutil
################################################################################
        try:
            if  "psutil" in error_codes:
                import psutil1
            else:
                import psutil
        except ImportError:
            command = "pip3 install --user psutil"
            button = '''
<button 
    style="text-align:left;"
    class="btn ${{BASH_COMMAND}}";
    class="btn"; 
    id="Install psutil"; 
    title="Install psutil. Click the button then ENTER in a newly created bash terminal window, to go."
>
    {}
</button>            
'''.format(command)

            self.error_msg('''
Module 'psutil' is not installed. Install it: {}
'''.format(button))
            self.print_error(
'''Module 'psutil' is not installed.
Install it: ''')
            self.print_code("`{}`\n".format(command))


################################################################################
# termcolor
################################################################################
        try:
            if  "termcolor" in error_codes:
                import termcolor1
            else:
                import termcolor
        except ImportError:
            command = "pip3 install --user termcolor"
            button = '''
<button 
    style="text-align:left;"
    class="btn ${{BASH_COMMAND}}";
    class="btn"; 
    id="Install termcolor"; 
    title="Install termcolor. Click the button then ENTER in a newly created bash terminal window, to go."
>
    {}
</button>            
'''.format(command)

            self.error_msg('''
Module 'termcolor' is not installed. Install it: {}
'''.format(button))

            self.print_error(
'''Module 'termcolor' is not installed.
Install it: ''')
            self.print_code("`{}`\n".format(command))


        if self.IS_WINDOWS:

################################################################################
# Ubuntu version
################################################################################
            lsb_release, error = utils.spawn(
                            ["lsb_release", "-r", "-s"], raise_exception=False)
            if error:
                self.error_msg(error)
            else:
                if "ubuntuversion" in error_codes:
                    lsb_release = "16.4.1"

                ubuntu_version = int(lsb_release.split(".")[0])    
                if ubuntu_version < config.UBUNTU_VERSION_MIN:
                    msg = \
'''
WSL Ubuntu version is {}.
EOSIO nodeos can fail with Windows WSL Ubuntu below version 16.
                        '''.format(lsb_release)              
                        
                    self.status_msg(self.warning(msg))
                    self.print_warning(msg)


################################################################################
# WSL root
################################################################################
            root = config.wsl_root()
            if not root or "wslroot" in error_codes:
                self.error_msg(
'''Cannot determine the root of the WSL. Set it: 
<button 
    class="btn ${FIND_WSL}"; 
    id=""; 
    title="Click the button to open file dialog. Navigate to a directory containing the Ubuntu file system."
>
    Indicate WSL root
</button>
''')
                self.print_error(
'''Cannot determine the root of the WSL. To indicate it, use the command:''')
                self.print_code("`python3 -m eosfactory.config --wsl_root`\n")


################################################################################
# eosio
################################################################################
        eosio_version = config.eosio_version()
        if  "eosio" in error_codes:
            eosio_version = ["", "1.8.0"]
        # eosio_version = ["1.3.3", "1.8.0"]    

        if eosio_version[0]:
            self.status_msg(
                        "Found eosio version {}".format(eosio_version[0]))
            self.print_status(
                        "Found eosio version {}".format(eosio_version[0]))

        if not eosio_version[0] or len(eosio_version) > 1\
                and not self.equal(eosio_version[0], eosio_version[1]):
            command = ""
            
            if self.os_version == utils.UBUNTU:
                ubuntu_version = utils.spawn(
                                        ["lsb_release", "-r", "-s"], 
                                        raise_exception=False)[0].split(".")[0]

                if ubuntu_version and ubuntu_version == 16:
                    command = \
'''sudo apt remove eosio &&\\
wget https://github.com/eosio/eos/releases/download/v1.8.0/eosio_1.8.0-1-ubuntu-16.04_amd64.deb &&\\
sudo apt install ./eosio_1.8.0-1-ubuntu-16.04_amd64.deb                
'''
                else:
                    command = \
'''sudo apt remove eosio &&\\
wget https://github.com/eosio/eos/releases/download/v1.8.0/eosio_1.8.0-1-ubuntu-18.04_amd64.deb &&\\
apt install ./eosio_1.8.0-1-ubuntu-18.04_amd64.deb
'''
            elif self.os_version == utils.DARWIN:
                command = \
'''brew remove eosio &&\\
brew tap eosio/eosio &&\\
brew install eosio
'''

            button = '''
<button 
    style="text-align:left;"
    class="btn ${{BASH_COMMAND}}";
    class="btn"; 
    id="Install eosio v{0}"; 
    title="Install eosio v{0}. Click the button then ENTER in a newly created bash terminal window, to go."
>
    {1}
</button>            
'''.format(eosio_version[1], command)

            instructions = '<a href="https://github.com/EOSIO/eos">EOSIO installation instructions</a>'

            if eosio_version[0] and len(eosio_version) > 1 :
                self.warning_msg(
'''
NOTE: EOSFactory was tested with version {0} while installed is {1}. Install eosio v{0}:<br>
{2}
'''.format(
                eosio_version[1], eosio_version[0], 
                button if command else instructions))

                self.print_warning(
'''NOTE: EOSFactory was tested with version {0} while installed is {1}. Install eosio v{0}:
'''.format(
            eosio_version[1], eosio_version[0])
            )
                self.print_code(
'''```
{}
```
'''.format(command if command else instructions))                    

            else:
                if not "ignoreeoside" in error_codes:
                    self.warning_msg('''
Cannot determine that eosio is installed as nodeos does not response.<br>
It hangs up sometimes.<br>
EOSFactory expects eosio version {}. Install eosio, if not installed:<br>
{}<br>
'''.format(eosio_version[1], button if command else instructions))

                    self.print_warning(
'''Cannot determine that eosio is installed as nodeos does not response.
It hangs up sometimes.
EOSFactory expects eosio version {}. Install eosio, if not installed:
'''.format(eosio_version[1]))

                    self.print_code(
'''```
{}
```
'''.format(command if command else instructions))


################################################################################
# eosio_cdt
################################################################################
        eosio_cdt_version = config.eosio_cdt_version()
        if "eosio_cdt" in error_codes:
            eosio_cdt_version = ["", "1.6.0"]
        # eosio_cdt_version = ["1.6.1", "1.6.0"]    
        
        if eosio_cdt_version[0]:
            self.status_msg(
                "Found eosio.cdt version {}.".format(eosio_cdt_version[0]))
            self.print_status(
                "Found eosio.cdt version {}.".format(eosio_cdt_version[0]))
        
        if not eosio_cdt_version[0] or len(eosio_cdt_version) > 1\
                and not self.equal(eosio_cdt_version[0], eosio_cdt_version[1]):
            command = ""

            if self.os_version == utils.UBUNTU:
                command = \
'''sudo apt remove eosio.cdt &&\\
wget https://github.com/eosio/eosio.cdt/releases/download/v1.6.1/eosio.cdt_1.6.1-1_amd64.deb &&\\
sudo apt install ./eosio.cdt_1.6.1-1_amd64.deb
'''
            elif self.os_version == utils.DARWIN:
                command = \
'''brew remove eosio.cdt &&\\
brew tap eosio/eosio.cdt && \\
brew install eosio.cdt
'''
            button = '''
<button 
    style="text-align:left;"
    class="btn ${{BASH_COMMAND}}";
    class="btn"; 
    id="Install eosio.cdt v{0}"; 
    title="Install eosio.cdt v{0}. Click the button then ENTER in a newly created bash terminal window, to go."
>
    {1}
</button>
'''.format(eosio_cdt_version[1], command)

            instructions = '<a href="https://github.com/EOSIO/eosio.cdt">EOSIO.cdt installation instructions</a>'

            if eosio_cdt_version[0] and len(eosio_cdt_version) > 1 \
                    and not eosio_cdt_version[0] == eosio_cdt_version[1]:
                self.warning_msg(
'''
NOTE: EOSFactory was tested with version {0} while installed is {1}. Install eosio.cdt v{0}:<br>
{2}
'''.format(
                eosio_cdt_version[1], eosio_cdt_version[0], 
                button if command else instructions))

                self.print_warning(
'''NOTE: EOSFactory was tested with version {0} while installed is {1}. Install eosio v{0}:
'''.format(
                eosio_cdt_version[1], eosio_cdt_version[0]))

                self.print_code(
'''```
{}
```
'''.format(command if command else instructions))

            else:
                self.error_msg('''
    Cannot determine that eosio.cdt is installed as eosio-cpp does not response.<br>
    EOSFactory expects eosio.cdt version {}. Install it, if not installed.
    {}<br>
'''.format(eosio_cdt_version[1], button if command else instructions))

                self.print_error(
'''Cannot determine that eosio.cdt is installed as eosio-cpp does not response.
EOSFactory expects eosio.cdt version {}. Install it, if not installed.
'''.format(eosio_cdt_version[1]))

                self.print_code(
'''```
{}
```
'''.format(command if command else instructions))


################################################################################
# Default workspace
################################################################################
        try:
            contract_workspace_dir = config.contract_workspace_dir()
        except:
            contract_workspace_dir = None

        button = '''
<button 
    class="btn ${CHANGE_WORKSPACE}";
    id="${CHANGE_WORKSPACE}"; 
    title="Set workspace"
>
    Set workspace.
</button>            
'''
        if not contract_workspace_dir or "workspace" in error_codes:
            self.error_msg('''
Default workspace is not set, or it does not exist.{}
'''.format(button))

        else:
            self.status_msg(
'''Default workspace is {}.{}
'''.format(contract_workspace_dir, button))


################################################################################
#
################################################################################
    
    def just_msg(self, msg):
        if self.is_html:
            msg = msg.replace("&&\\", "&&\\<br>")
            print("{}\n".format(msg))


    def print_msg(self, msg):
        if not self.is_html:
            print(msg)    

    
    def status_msg(self, msg):
        if self.is_html:
            msg = msg.replace("&&\\", "&&\\<br>")
            print("<li>{}</li>\n".format(msg))


    def print_status(self, msg):
        if not self.is_html:
            msg = msg.replace("<br>", "")
            print(msg)            


    def warning(self, msg):
        self.is_warning = True
        if self.is_html:
            msg = msg.replace("&&\\", "&&\\<br>")
            return '<em style="color: ${{WARNING_COLOR}}"> {} </em>'.format(msg)


    def warning_msg(self, msg):
        self.is_warning = True
        if self.is_html:
            msg = msg.replace("&&\\", "&&\\<br>")
            print('<em style="color: ${{WARNING_COLOR}}"> {} </em>'.format(msg))


    def print_warning(self, msg):
        if not self.is_html:
            msg = msg.replace("<br>", "")
            msg = "WARNING:\n" + msg
            try:
                import termcolor
                msg = termcolor.colored(msg, "yellow")
            except:
                pass

            print(msg)        


    def error_msg(self, msg):
        if self.is_html:
            self.is_error = True
            msg = msg.replace("&&\\", "&&\\<br>")
            print(
                '<p style="color: ${{ERROR_COLOR}}">ERROR: {}</p>'.format(msg))


    def print_error(self, msg):
        if not self.is_html:
            self.is_error = True
            msg = msg.replace("<br>", "")
            msg = "ERROR:\n" + msg
            try:
                import termcolor
                msg = termcolor.colored(msg, "magenta")
            except:
                pass

            print(msg)


    def print_code(self, msg):
        if not self.is_html:
            msg = msg.replace("<br>", "")
            try:
                import termcolor
                msg = termcolor.colored(msg, "blue")
            except:
                pass

            print(msg)        

    def equal(self, version1, version2):
        return version1.split(".")[0] == version2.split(".")[0] \
            and version1.split(".")[1] == version2.split(".")[1]

def main():
    parser = argparse.ArgumentParser(description='''
    Check whether installation conditions are fulfilled.
    ''')
    parser.add_argument(
                    "--html", help="Print html output.", action="store_true")
    parser.add_argument("--error", help="Error code", default="")

    parser.add_argument(
        "--wsl_root",  help="Show set the root of the WSL and exit.", 
        action="store_true")
    parser.add_argument(
        "--dont_set_workspace", help="Ignore empty workspace directory.", 
        action="store_true")    
    parser.add_argument(
        "--json", help="Bare config JSON and exit.", 
        action="store_true")
    parser.add_argument(
        "--workspace", help="Set contract workspace and exit.",
        action="store_true")
    parser.add_argument(
        "--dependencies", help="Set dependencies and exit.",
        action="store_true")
    
    args = parser.parse_args()

    if args.json:
        print(json.dumps(
            config.current_config(dont_set_workspace=args.dont_set_workspace), 
            sort_keys=True, indent=4))
    elif args.wsl_root:
        config.wsl_root()
    elif args.workspace:
        config.set_contract_workspace_dir()
    elif args.html:
        checklist = Checklist(args.html, args.error)
        if checklist.is_error:
            sys.exit(IS_ERROR)
        elif checklist.is_warning:
            sys.exit(IS_WARNING)
    elif args.dependencies:
        checklist = Checklist(False, args.error)

    else:
        print("Checking dependencies of EOSFactory...")
        checklist = Checklist(False, args.error)
        if not checklist.is_error and not checklist.is_warning:
            print("... all the dependencies are in place.\n\n")
        else:
            print(
'''Some functionalities of EOSFactory may fail if the indicated errors are not 
corrected.
''')
        config.config()


if __name__ == '__main__':
    main()


