import pyteos.core.teos as teos
import pyteos.setup as setup

setup.is_print_command_line = True
teos.node_stop()
teos.node_start(True)