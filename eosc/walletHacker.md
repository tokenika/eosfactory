```
E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create second
##             password: "PW5KPth1CqbGxMyGv5YhhkFYgUPKHxX7ayRuNdb941MiHC3GqL2xU"
## You need to save this password to be able to lock/unlock the wallet!

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create second
ERROR!
status code is 500
 eosd response is Content-Length: 267
Content-type: application/json
Server: WebSocket++/0.7.0

{"code":500,"message":"Internal Service Error","details":"0 exception: unspecified\nWallet with name: 'second' already exists at /home/eos/test2/./second.wallet\n    {\"n\":\"second\",\"path\":\"/home/eos/test2/./second.wallet\"}\n      wallet_manager.cpp:42 create"}

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create -h

Create a new wallet locally
Usage: ./eosc wallet create [name] [Options]
Usage: ./eosc wallet create [-j "{"""NSON""":"""string"""}'] [OPTIONS]

Options:

  -n [ --name ] arg (=default)    The name of the new wallet

  -h [ --help ]                   Help screen
  --wallet-host arg (=localhost)  The host where eos-wallet is running
  --wallet-port arg (=8888)       The port where eos-wallet is running
  -V [ --verbose ]                Output verbose messages on error
  -j [ --json ] arg               Json argument
  -v [ --received ]               Print received json
  -r [ --raw ]                    Not pretty print
  -e [ --example ]                Usage example


E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create
ERROR!
status code is 500
 eosd response is Content-Length: 271
Content-type: application/json
Server: WebSocket++/0.7.0

{"code":500,"message":"Internal Service Error","details":"0 exception: unspecified\nWallet with name: 'default' already exists at /home/eos/test2/./default.wallet\n    {\"n\":\"default\",\"path\":\"/home/eos/test2/./default.wallet\"}\n      wallet_manager.cpp:42 create"}

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create third
##             password: "PW5KASmkhboVeh6WUEvMCJRcVBoFiYWrCnUMXHeWDA7nhJtGEwgPP"
## You need to save this password to be able to lock/unlock the wallet!

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create third
ERROR!
status code is 500
 eosd response is Content-Length: 263
Content-type: application/json
Server: WebSocket++/0.7.0

{"code":500,"message":"Internal Service Error","details":"0 exception: unspecified\nWallet with name: 'third' already exists at /home/eos/test2/./third.wallet\n    {\"n\":\"third\",\"path\":\"/home/eos/test2/./third.wallet\"}\n      wallet_manager.cpp:42 create"}

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create eos_is_scheise_wallet
##             password: "PW5KHkKF18NjdHwEfC6t2MmNJmsWrzRGLdPRBvVwriY26yHYtkHxF"
## You need to save this password to be able to lock/unlock the wallet!

E:\Workspaces\EOS\Pentagon\eosc\eosc_visual_studio\x64\Debug>.\eosc tokenika wallet create eos_is_scheise_wallet
ERROR!
status code is 500
 eosd response is Content-Length: 327
Content-type: application/json
Server: WebSocket++/0.7.0

{"code":500,"message":"Internal Service Error","details":"0 exception: unspecified\nWallet with name: 'eos_is_scheise_wallet' already exists at /home/eos/test2/./eos_is_scheise_wallet.wallet\n    {\"n\":\"eos_is_scheise_wallet\",\"path\":\"/home/eos/test2/./eos_is_scheise_wallet.wallet\"}\n      wallet_manager.cpp:42 create"}
```
