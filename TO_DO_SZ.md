
## 1. bootstrap contract --vsc
Doesn't work on MacOS

## 2. bootstrap contract --vsc
Doesn't work on Ubuntu

## 3. make & ctest
Doesn't work on Ubuntu

## 4. /teos/config.json
```
File "/mnt/d/Workspaces/EOS/eosfactory/pyteos/pyteos.py", line 60, in __init__
    with open(self.__setupFile) as json_data:
FileNotFoundError: [Errno 2] No such file or directory: '/mnt/d/Workspaces/EOS/eosfactory/pyteos/../teos/config.json'
```

---

## 5. test output is always duplicated


---

# PS C:\Users\cartman> $WSLREGKEY="HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss"
# PS C:\Users\cartman> $WSLDEFID=(Get-ItemProperty "$WSLREGKEY").DefaultDistribution
# PS C:\Users\cartman> $WSLFSPATH=(Get-ItemProperty "$WSLREGKEY\$WSLDEFID").BasePath
# PS C:\Users\cartman> New-Item -ItemType Junction -Path "$env:LOCALAPPDATA\lxss" -Value "$WSLFSPATH\rootfs"
