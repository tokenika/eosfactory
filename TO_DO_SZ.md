
## name cannot end with a dot
```
{"code":500,"message":"Internal Service Error","error":{"code":3010001,"name":"name_type_exception","what":"Invalid name","details":[{"message":"Name not properly normalized (name: ve2cfmurpve., normalized: ve2cfmurpve) ","file":"name.cpp","line_number":15,"method":"set"}]}}
```
## /teos/config.json
```
File "/mnt/d/Workspaces/EOS/eosfactory/pyteos/pyteos.py", line 60, in __init__
    with open(self.__setupFile) as json_data:
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/d/Workspaces/EOS/eosfactory/pyteos/../teos/config.json'
```

---

## bootstrap contract --vsc
```
Doesn't work on MacOS & Ubuntu
```
## test output is always duplicated in verbose mode
```
test c.push_action("hi", sess.carol):
#        transaction id: b6b8ac846c2f6d98ba014643ef9d11a0f195fcf8d99d55b12e19112e9aa5381b
#  INFO user: carol @ 23:41:22 satire5.cpp[16](hi)
#  Hello, carol

INFO user: carol @ 23:41:22 satire5.cpp[16](hi)
Hello, carol
```
## format time
```
INFO user: carol @ 8:5:3 contract.name.cpp[16](hi)
```
## make compatible with EOSIO v1.0.1
```
git pull
git checkout v1.0.1
git submodule update --init --recursive
./eosio_build.sh
```

---

```
# PS C:\Users\cartman> $WSLREGKEY="HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss"
# PS C:\Users\cartman> $WSLDEFID=(Get-ItemProperty "$WSLREGKEY").DefaultDistribution
# PS C:\Users\cartman> $WSLFSPATH=(Get-ItemProperty "$WSLREGKEY\$WSLDEFID").BasePath
# PS C:\Users\cartman> New-Item -ItemType Junction -Path "$env:LOCALAPPDATA\lxss" -Value "$WSLFSPATH\rootfs"

# powershell.exe -Command "&{$WSLREGKEY='HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss'; $WSLDEFID=(Get-ItemProperty "$WSLREGKEY").DefaultDistribution; $WSLFSPATH=(Get-ItemProperty "$WSLREGKEY\$WSLDEFID").BasePath; echo $WSLFSPATH}"

```