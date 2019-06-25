# Installing VMware Workstation Player 12 Ubuntu

## VMware player setup

Virtual Machine Settings Hardware
```bash
Memory 4GB
Hard disk 80GB
Processors 4
```
Virtual Machine Settings Options (while Virtual Ubuntu is powered):
```bash
Shared Folders
    Always enabled
    Folders C:\Workspaces
        As a result, mnt/hgfs/Workspaces folder in the Files window.
```

## Ubuntu setup

>You should first run update, then upgrade. Neither of them automatically runs the other.

>apt-get update updates the list of available packages and their versions, but it does not install or upgrade any packages.
apt-get upgrade actually installs newer versions of the packages you have. After updating the lists, the package manager knows about available updates for the software you have installed. This is why you first want to update.

```bash
sudo apt update
sudo apt upgrade
sudo apt install git
```
### [Files missing in /mnt/hgfs on Ubuntu VM](https://xpressubuntu.wordpress.com/2015/05/11/resolving-no-shared-folders-with-vmware-player-7-and-ubuntu-15-04-guest/comment-page-1/#comment-708)

```bash
cd /tmp/
git clone https://github.com/rasa/vmware-tools-patches.git
cd vmware-tools-patches
sudo ./patched-open-vm-tools.sh
```

### [Installing VSCode](https://linuxize.com/post/how-to-install-visual-studio-code-on-ubuntu-18-04/)

```bash
sudo apt install software-properties-common apt-transport-https wget
wget -q https://packages.microsoft.com/keys/microsoft.asc -O- | sudo apt-key add -
sudo add-apt-repository "deb [arch=amd64] https://packages.microsoft.com/repos/vscode stable main"

sudo apt install code

sudo apt install python3-pip
pip3 install termcolor
pip3 install psutil
pip3 install setuptools
pip3 install wheel
```

### Installing eosio system

```bash
sudo apt remove eosio
wget https://github.com/eosio/eos/releases/download/v1.7.1/eosio_1.7.1-1-ubuntu-18.04_amd64.deb
sudo apt install ./eosio_1.7.1-1-ubuntu-18.04_amd64.deb

sudo apt remove eosio.cdt
wget wget https://github.com/eosio/eosio.cdt/releases/download/v1.6.1/eosio.cdt_1.6.1-1_amd64.deb
sudo apt install ./eosio.cdt_1.6.1-1_amd64.deb
```

### Installing EOSFactory

The workspace directory has to be places outside the Windows filesystem.

## Errors

### mutable globals cannot be imported

```bash
ERROR /mnt/hgfs/Workspaces/EOS/eosfactory/eosfactory/core/errors.py 44:
Reading WASM from /mnt/hgfs/Workspaces/EOS/eosfactory/contracts_linux/_wslqwjvacdyugodewiyd/build/_wslqwjvacdyugodewiyd.wasm...
Publishing contract...
Error 3070003: Serialization Error Processing WASM
Error Details:
mutable globals cannot be imported: globalImport.type.isMutable
pending console output:
```

If `~/Workspaces` not `/mnt/hgfs/Workspaces`, the mutable globals error is replaced (masked) with hanging of `eosio_cpp`. If cpu cores increased from 1 to 4, everything is OK.

If the workspace directory is moved from `/mnt/hgfs/Workspaces/EOS/contracts` to `/tmp/eosfactory/contracts`, the mutable globals error vanishes. Then, the problem is in coding of Ubuntu files written to a Windows file system.

### eosio_cpp hangs

[Good remark:](https://github.com/EOSIO/eosio.cdt/issues/123)
Has to be more cpu cores working. 


### Shared folders not available on Linux guests 

sudo vmhgfs-fuse .host:/ /mnt/hgfs -o allow_other