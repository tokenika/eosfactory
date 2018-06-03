
## 1. bootstrap contract --vsc
Doesn't work on MacOS

## 2. bootstrap contract --vsc
Doesn't work on Ubuntu

## 3. make & ctest
Doesn't work on Ubuntu

## 4. test output is always duplicated


---

# PS C:\Users\cartman> $WSLREGKEY="HKCU:\Software\Microsoft\Windows\CurrentVersion\Lxss"
# PS C:\Users\cartman> $WSLDEFID=(Get-ItemProperty "$WSLREGKEY").DefaultDistribution
# PS C:\Users\cartman> $WSLFSPATH=(Get-ItemProperty "$WSLREGKEY\$WSLDEFID").BasePath
# PS C:\Users\cartman> New-Item -ItemType Junction -Path "$env:LOCALAPPDATA\lxss" -Value "$WSLFSPATH\rootfs"
