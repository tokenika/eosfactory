import ef.core.teos as teos
import ef.setup as setup

setup.is_print_command_line = False
# teos.WAST("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world")
# teos.ABI("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world")

teos.template_create("XXXX", remove_existing=True)

