```
eosio-cpp 
-contract=helloq 
-R=/mnt/c/Workspaces/EOS/contracts/helloq/src/../resources 
-abigen 
-abigen_output=/mnt/c/Workspaces/EOS/contracts/helloq/build/helloq.abi 
-I=/mnt/c/Workspaces/EOS/contracts/helloq 
-I=/mnt/c/Workspaces/EOS/eosfactory/includes 
/mnt/c/Workspaces/EOS/contracts/helloq/src/helloq.cpp

eosio-cpp 
-contract=hello 
-R=/mnt/c/Workspaces/EOS/contracts/hello/src/../resources
-abigen 
-o /mnt/c/Workspaces/EOS/contracts/hello/build/hello.wasm 
-I=/mnt/c/Workspaces/EOS/contracts/hello 
-I=/mnt/c/Workspaces/EOS/eosfactory/includes 
/mnt/c/Workspaces/EOS/contracts/hello/src/hello.cpp


error message:
==============
/usr/opt/eosio.cdt/1.6.1/bin/wasm-ld: error: duplicate symbol: apply
>>> defined in /tmp/helloq.cpp.o
>>> defined in /tmp/helloq.cpp.o

```

eosio-cpp -contract=helloq -R=/mnt/c/Workspaces/EOS/contracts/helloq/src/../resources -abigen -abigen_output=/mnt/c/Workspaces/EOS/contracts/helloq/build/helloq.abi /mnt/c/Workspaces/EOS/contracts/helloq/src/helloq.cpp


eosio-cpp -contract=hello -R=/mnt/c/Workspaces/EOS/contracts/hello/src/../resources -abigen -o /mnt/c/Workspaces/EOS/contracts/hello/build/hello.wasm -I=/mnt/c/Workspaces/EOS/contracts/hello -I=/mnt/c/Workspaces/EOS/eosfactory/includes /mnt/c/Workspaces/EOS/contracts/hello/src/hello.cpp


eosio-cpp -contract=hello -R=/mnt/c/Workspaces/EOS/contracts/hello/src/../resources -abigen_output /mnt/c/Workspaces/EOS/contracts/hello/build/hello.abi -I=/mnt/c/Workspaces/EOS/contracts/hello -I=/mnt/c/Workspaces/EOS/eosfactory/includes /mnt/c/Workspaces/EOS/contracts/hello/src/hello.cpp

