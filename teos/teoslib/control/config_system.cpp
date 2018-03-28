#include <stdlib.h>
#include <string>

#include <teoslib/control/config.hpp>
/*
  --genesis-json arg (="genesis.json")  File to read Genesis State from
  --resync-blockchain                   clear chain database and block log
  --http-server-address arg (=127.0.0.1:8888)
                                        The local IP and port to listen for
                                        incoming http connections.
  --wallet-dir arg (=".")               The path of the wallet files (absolute
                                        path or relative to application data
                                        dir)

  -d [ --data-dir ] arg                 Directory containing program runtime
                                        data
  --config-dir arg                      Directory containing configuration
                                        files such as config.ini
  -c [ --config ] arg (="config.ini")   Configuration file name relative to
                                        config-dir

daemon_exe: 

config-dir: E:\Workspaces\EOS\eos\build\etc\eosio\node_00/
E:\Workspaces\EOS\eos\build\etc\eosio\node_00/config.ini
E:\Workspaces\EOS\eos\build\etc\eosio\node_00/genesis.json

data-dir: E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00/
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00\blocks
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00\shared_mem

wallet-dir: .
E:\Workspaces\EOS\eos\build\var\lib\eosio\node_00/default.wallet

*/

using namespace std;

namespace teos {
  namespace control {



  }
}