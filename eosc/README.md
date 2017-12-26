# Tokenika alternative for the EOS *eosc* program

<a name="toc"></a>
## Table of contents

* [Rationale](#rationale)
  * [Richer API](#richer)
    * [EOS](#richereos)
    * [Tokenika](#richertokenika)
* [Building](#building)
  * [Dependencies](#dependencies)
  * [Linux, Mac, ect.](#linux)
  * [Windows](#windows)

<a name="rationale"></a>
## [Rationale](#toc)

For our work with eos small contracts, we have found that the original EOS `eosc` interface program is too much restrictive. First, it is hard to be used programmatically in a C++ code. Next, it is quite heavy as it is tightly connected to the whole of the EOS code. Also, it is not ready to be used in the Windows environment, while we plan to open Windows based contract development possibility.

It could be enough for us to develope a minimal C++ library, implementing the commands of the EOS `eosc`. However, it was a short step to to provide this library with an command line interface.

Finally, to make our work competitive to the original, and for fun, we have added a richer command option list. We dare to hope that this little work of ours could be included to the EOS project.

We already know how to use this richness: it is much ease to make a tool as tokenika [`eoscBash`](#) that wraps the EOS `eosc` for bookkeeping.

<a name="richer"></a>
## [Richer API](#toc)

<a name="richereos"></a>
### [EOS](#toc)
```
./eosc get block -h
```
```
ERROR: RequiredError: block
Retrieve a full block from the blockchain
Usage: ./eosc get block block

Positionals:
  block TEXT                  The number or ID of the block to retrieve
```
```
./eosc get block 25
```
```
{
  "previous": "00000018b5e0ffcd3dfede45bc261e3a04de9f1f40386a69821780e063a41448",
  "timestamp": "2017-11-29T09:50:03",
  "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
  "producer": "initf",
  "producer_changes": [],
  "producer_signature": "2005db1a193cc3597fdc3bd38a4375df2a9f9593390f9431f7a9b53701cd46a1b5418b9cd68edbdf2127d6ececc4d66b7a190e72a97ce9adfcc750ef0a770f5619",
  "cycles": [],
  "id": "000000190857c9fb43d62525bd29dc321003789c075de593ce7224bde7fc2284",
  "block_num": 25,
  "refBlockPrefix": 623236675
}
```

<a name="richtokenika"></a>
### Tokenika

```
./eosc get block -h
```
```
Retrieve a full block from the blockchain
Usage: ./eosc get block [block_num] [Options]
Usage: ./eosc get block [-j {"block_num_or_id":*}] [OPTIONS]

Options:

  -n [ --block_num ] arg  Block number
  -i [ --block_id ] arg   Block id

  -h [ --help ]           Help screen
  -j [ --json ] arg       Json argument
  -v [ --received ]       Print received json
  -r [ --raw ]            Not pretty print
  -e [ --example ]        Usage example
```
```
./eosc get block 25
##         block number: 25
##            timestamp: 2017-11-29T09:50:03
##     ref block prefix: 623236675
```
```
./eosc get block 25 -v
```
```
{
    "previous": "00000018b5e0ffcd3dfede45bc261e3a04de9f1f40386a69821780e063a41448",
    "timestamp": "2017-11-29T09:50:03",
    "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "producer": "initf",
    "producer_changes": "",
    "producer_signature": "2005db1a193cc3597fdc3bd38a4375df2a9f9593390f9431f7a9b53701cd46a1b5418b9cd68edbdf2127d6ececc4d66b7a190e72a97ce9adfcc750ef0a770f5619",
    "cycles": "",
    "id": "000000190857c9fb43d62525bd29dc321003789c075de593ce7224bde7fc2284",
    "block_num": "25",
    "refBlockPrefix": "623236675"
}
```
```
./eosc get block 25 -v -r
```
```
{"previous":"00000018b5e0ffcd3dfede45bc261e3a04de9f1f40386a69821780e063a41448","timestamp":"2017-11-29T09:50:03","transaction_merkle_root":"0000000000000000000000000000000000000000000000000000000000000000","producer":"initf","producer_changes":"","producer_signature":"2005db1a193cc3597fdc3bd38a4375df2a9f9593390f9431f7a9b53701cd46a1b5418b9cd68edbdf2127d6ececc4d66b7a190e72a97ce9adfcc750ef0a770f5619","cycles":"","id":"000000190857c9fb43d62525bd29dc321003789c075de593ce7224bde7fc2284","block_num":"25","refBlockPrefix":"623236675"}
```
```
./eosc get block -j '{"block_num_or_id":"56"}'
##         block number: 56
##            timestamp: 2017-11-29T10:02:18
##     ref block prefix: 273573026
```
```
./eosc get block --example
```
```
// Invoke 'GetInfo' command:
    ptree getInfoJson;
    GetInfo getInfo(getInfoPostJson);
    cout << getInfo.toStringRcv() << endl;

/*
printout:

{
    "server_version": "9703495c",
    "head_block_num": "1707240",
    "last_irreversible_block_num": "1707225",
    "head_block_id": "001a0ce87ca6e2d0fc19b8a02e9241c658bea0365f4e6f035ce6602db04611bd",
    "head_block_time": "2017-12-25T14:11:31",
    "head_block_producer": "inito",
    "recent_slots": "1111111111111111111111111111111111111111111111111111111111111111",
    "participation_rate": "1.00000000000000000"
}

*/

// Use reference to the last block:
    ptree GetBlockJson;
    GetBlock_poGetBlockJsont_json.put("block_num_or_id",
      getInfo.get<int>("last_irreversible_block_num"));
    GetBlock GetBlock(GetBlock_post_json);
    cout << GetBlock.toStringRcv() << endl;

/*
printout:

{
    "previous": "001a0cd8422216f2828ef5056e9371439f80665cee99d72a5f3162ae7c0495fd",
    "timestamp": "2017-12-25T14:11:16",
    "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "producer": "initn",
    "producer_changes": "",
    "producer_signature": "1f382b4fe716f683c8a7ebd15fe5f5266c75a24f75b9b212fc3cc3f7db11f5258b08e5aebc7680784c240e0f8d0ea7540dfb4ab8dcbe5cd8b492876e8f59bb4ea8",
    "cycles": "",
    "id": "001a0cd98eb6f7e0f8e7803b098082b35f1348672561af193ead3d1b1a281bcf",
    "block_num": "1707225",
    "ref_block_prefix": "998303736"
}

*/
```
## Library
For us, real value is the library that runs the `tokenika eosc`, as we see the original eos library as not practical for our work. We need a light-weight thing, a cross-platform (good for windows) one.

Let you see a code snippet:
```
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "EoscCommands/eosc_get_commands.hpp"

int main(int argc, char *argv[])
{
  using namespace tokenika::eosc;

  ptree getInfoJson;

// Invoke 'GetInfo' command:
  GetInfo getInfo(getInfoPostJson);
  cout << getInfo.toStringRcv() << endl;

  ptree getBlockJson;

// Use reference to the last block:
  GetBlockJson.put("block_num_or_id",
    getInfo.get<int>("last_irreversible_block_num"));
  GetBlock GetBlock(GetBlock_post_json);
  cout << GetBlock.toStringRcv() << endl;

  return 0;
}
```
The printout is:
```
{
    "server_version": "9703495c",
    "head_block_num": "1707240",
    "last_irreversible_block_num": "1707225",
    "head_block_id": "001a0ce87ca6e2d0fc19b8a02e9241c658bea0365f4e6f035ce6602db04611bd",
    "head_block_time": "2017-12-25T14:11:31",
    "head_block_producer": "inito",
    "recent_slots": "1111111111111111111111111111111111111111111111111111111111111111",
    "participation_rate": "1.00000000000000000"
}

{
    "previous": "001a0cd8422216f2828ef5056e9371439f80665cee99d72a5f3162ae7c0495fd",
    "timestamp": "2017-12-25T14:11:16",
    "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "producer": "initn",
    "producer_changes": "",
    "producer_signature": "1f382b4fe716f683c8a7ebd15fe5f5266c75a24f75b9b212fc3cc3f7db11f5258b08e5aebc7680784c240e0f8d0ea7540dfb4ab8dcbe5cd8b492876e8f59bb4ea8",
    "cycles": "",
    "id": "001a0cd98eb6f7e0f8e7803b098082b35f1348672561af193ead3d1b1a281bcf",
    "block_num": "1707225",
    "ref_block_prefix": "998303736"
}

```

<a name="building"></a>
## [Building](#toc)

<a name="dependencies"></a>
### [Dependencies](#toc)
The only external dependency is the boost. We use the version 1_65.

<a name="linux"></a>
### [Linux, Mac, ect.](#toc)

CMake build. Starting in the installation directory:

```
mkdir build
cd build
cmake ..
make
```
<a name="windows"></a>l
### [Windows](#toc)

There is an MS Visual Studio 17 solution in `eos_visual_studio` folder. You can start
Visual Studio with file `eosc.sln` there, and you can compile both the command library and 
`eosc' executable.

The VS solution has set both boost includes and libraries in relation to the `BOOST_ROOT` environmental variable: Configuration Properties > VC++ Directories. Perhaps, you will have to adjust settings.

Now, the blockchain may be accessed from a Windows Command Prompt.


