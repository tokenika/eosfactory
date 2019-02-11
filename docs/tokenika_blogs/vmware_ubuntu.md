# Installing VMware Workstation Player 12 Ubuntu

### [Installing VSCode](https://linuxize.com/post/how-to-install-visual-studio-code-on-ubuntu-18-04/)


### Share folders between Windows and Ubuntu
While Virtual Ubuntu is powered:
`Player => Manage => Virtual Machine Settings => Options => Shared Folders`

Set `Always enabled`

Add ...

As a result, `mnt/hgfs/EOS` folder in the Files window.

toolbox version:
```bash
vmware-toolbox-cmd
bash

You should first run update, then upgrade. Neither of them automatically runs the other.

apt-get update updates the list of available packages and their versions, but it does not install or upgrade any packages.
apt-get upgrade actually installs newer versions of the packages you have. After updating the lists, the package manager knows about available updates for the software you have installed. This is why you first want to update.

```bash
sudo apt update
sudo apt upgrade

# https://linuxize.com/post/how-to-install-visual-studio-code-on-ubuntu-18-04/
sudo apt install software-properties-common apt-transport-https wget

wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -

sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

sudo apt install code

sudo apt install python3-pip
pip3 install termcolor
pip3 install setuptools
pip3 install wheel
```

```bash
wget https://github.com/eosio/eos/releases/download/v1.6.1/eosio_1.6.1-1-ubuntu-18.04_amd64.deb

sudo apt install ./eosio_1.6.1-1-ubuntu-18.04_amd64.deb

wget https://github.com/eosio/eosio.cdt/releases/download/v1.5.0/eosio.cdt-1.5.0-1_amd64.deb

sudo apt install ./eosio.cdt-1.4.1.x86_64.deb  
```
```bash
sudo apt install git
```

### Files missing in /mnt/hgfs on Ubuntu VM

[See](https://xpressubuntu.wordpress.com/2015/05/11/resolving-no-shared-folders-with-vmware-player-7-and-ubuntu-15-04-guest/comment-page-1/#comment-708)

```bash
git clone https://github.com/rasa/vmware-tools-patches.git
cd vmware-tools-patches
sudo ./patched-open-vm-tools.sh
```

### mutable globals cannot be imported

ERROR /mnt/hgfs/Workspaces/EOS/eosfactory/eosfactory/core/errors.py 44:
Reading WASM from /mnt/hgfs/Workspaces/EOS/eosfactory/contracts_linux/_wslqwjvacdyugodewiyd/build/_wslqwjvacdyugodewiyd.wasm...
Publishing contract...
Error 3070003: Serialization Error Processing WASM
Error Details:
mutable globals cannot be imported: globalImport.type.isMutable
pending console output:

### 
wget https://github.com/eosio/eosio.cdt/releases/download/v1.5.0/eosio.cdt-1.5.0-1_amd64.deb ## wrong, has to be .com/EOSIO/eosio not .com/eosio/eosio
wget https://github.com/EOSIO/eosio.cdt/releases/download/v1.5.0/eosio.cdt_1.5.0-1_amd64.deb
sudo apt install /mnt/c/Workspaces/EOS/eosio.cdt_1.5.0-1_amd64.deb