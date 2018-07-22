#http://appjar.info/

import sys
sys.path.append("C:\\Workspaces\\EOS\\eosfactory\\pyteos\\appJar")

import appjar
from appjar import gui

app = gui()
app.setSize(700, 700)
app.setIcon("C://Workspaces//EOS//eosfactory//resources//tokenika.gif")
app.setFg("white", override=False)
app.setTitle("EOSFactory")
app.addLabel("get_started", "Get started")
app.setLabelBg("get_started", "black")
app.go()