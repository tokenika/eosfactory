# Tokenika's alternative for *eosc* command line interface


## Rationale

For those less familiar with EOS codebase, `eosc` is the official CLI (Command Line Interface) for EOS. It interacts with the EOS blockchain by connecting to a full node called `eosd`, which can run either locally or on a remote server.

When working with EOS smart-contracts, we've found that the original `eosc` has some inconvenient limitations:

* Firstly, it's hard to use `eosc` programmatically, as it doesn't offer an API.
* Secondly, it is quite heavyweight in terms of external dependencies, as it's tightly connected to the entire EOS codebase.
* Also, it is not ready to be used in Windows environment, while our plans include opening up EOS for smart-contract development on Windows.

It could be enough for us to develop a minimal C++ library acting as an EOS API and this way implement the commands supported by `eosc`. However, it was a short step to provide such a library with a command line interface, and thus create a full-blown `eosc` replacement. Furthermore, to make our work competitive to the original `eosc`, we have added a richer & more useful command option list. Also, our `eosc` compiles on any platform, including Windows, which is not the case with the original `eosc`. 

For obvious reasons everything we do is open source. We dare to hope that this little work of ours could become an interesting alternative to the original `eosc` CLI, and maybe one day be included as part of EOS codebase.

## Comparison

Our version of `eosc` covers the same functionality as the original `eosc`, but it's more user friendly and offers a wider selection of options.

Let's compare the `get block` command help:
```
./eosc get block -h
```
The original `eosc` response looks like this:
```
ERROR: RequiredError: block
Retrieve a full block from the blockchain
Usage: ./eosc get block block
Positionals:
block TEXT                  The number or ID of the block to retrieve
```
Whereas our `eosc` response looks like this:
```
Retrieve a full block from the blockchain
Usage: ./eosc get block [block_num_or_id][options]
Usage: ./eosc get block [-j {"block_num_or_id":*}][options]

Options:
  -n [ --block_num ] arg  Block number
  -i [ --block_id ] arg   Block id
  -h [ --help ]           Help screen
  -j [ --json ] arg       Json argument
  -v [ --received ]       Print received json
  -r [ --raw ]            Raw print
  -e [ --example ]        Usage example
```
And now let's compare the `get block` command usage, e.g.:
```
./eosc get block 25
```
The original `eosc` response looks like this:
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
Whereas our `eosc` response is less verbose by default to make it more readable:
```
## block number: 25
## timestamp: 2017-11-29T09:50:03
## ref block prefix: 623236675
```
But you can make it verbose, if you need:
```
./eosc get block 25 --received
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
Furthermore, you can make it both verbose and unformatted:
```
./eosc get block 25 --received --raw
```
```
{"previous":"00000018b5e0ffcd3dfede45bc261e3a04de9f1f40386a69821780e063a41448","timestamp":"2017-11-29T09:50:03","transaction_merkle_root":"0000000000000000000000000000000000000000000000000000000000000000","producer":"initf","producer_changes":"","producer_signature":"2005db1a193cc3597fdc3bd38a4375df2a9f9593390f9431f7a9b53701cd46a1b5418b9cd68edbdf2127d6ececc4d66b7a190e72a97ce9adfcc750ef0a770f5619","cycles":"","id":"000000190857c9fb43d62525bd29dc321003789c075de593ce7224bde7fc2284","block_num":"25","refBlockPrefix":"623236675"}
```
Also, you can supply the arguments in *json* format:
```
./eosc get block --json '{"block_num_or_id":"56"}'
```
```
##         block number: 56
##            timestamp: 2017-11-29T10:02:18
##     ref block prefix: 273573026
```
And finally, for each command you can invoke an example showcasing its usage:
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

# Building

## Ubuntu

#### Dependencies

First, make sure you have Boost 1.62 (or higher) installed:
```
dpkg -s libboost-dev | grep 'Version'
```
In case you need to install it, run this command:
```
sudo apt-get install libboost-all-dev
```
#### Source code

Navigate to a location of your choice on your machine and clone our *eosc* repository:

```
git clone https://github.com/tokenika/eosc.git
```
#### Compilation

Navigate to the `eosc/eosc` folder and create a new folder named `build`:

```
cd eosc/eosc/
mkdir build
cd build
```
Run CMake:
```
cmake ..
```
Make sure there are no errors, and then preceed with the actual compilation:
```
make
```
As the result of the compilation, you should be able to find those two files in the `build` folder:
* `eosclib\libeosclib.a` is a static library acting as an API for EOS
* `eosc` is the CLI executable making use of the above library

#### Testing on remote sever

Open a terminal window, navigate to the `build` folder and run `eosc`:
```
./eosc 198.100.148.136:8888 get info
```
The above command will connect to one of our test-net servers. Alternatively, you can use the placeholder `tokenika` instead of  `198.100.148.136:8888`:
```
./eosc tokenika get info
```

#### Testing on localhost

If you have complied the entire EOS codebase and have `eosd` running on your machine, you can also test our `eosc` locally:
```
./eosc localhost get info
```

### Windows

#### Visual Studio IDE

On Windows we recommend using [MS Visual Studio 2017](https://www.visualstudio.com/). The *Community* edition is fully functional and is [available for free](https://www.visualstudio.com/).

#### Dependencies

Make sure you have Boost 1.66 available on your machine. If not, you can download the source code from [the official webpage](http://www.boost.org/users/download/) or use the [pre-built Windows binaries](https://sourceforge.net/projects/boost/files/boost-binaries/) (make sure to use the [boost_1_66_0-msvc-14.1-64]( https://sourceforge.net/projects/boost/files/boost-binaries/1.66.0/boost_1_66_0-msvc-14.1-64.exe/download) version, as it's compatible with MS Visual Studio 2017).

#### System variable

Set up a system variable named  `BOOST_ROOT` pointing at your Boost directory. In our case it looks like this, but yours will most probably be different, depending on your Boost library location:

![](img01.png)

#### Source code

Navigate to a location of your choice on your machine and clone our *eosc* repository:

```
git clone https://github.com/tokenika/eosc.git
```

#### Compilation

We've created a dedicated MS Visual Studio 2017 solution project - it's located in the  `eos_visual_studio` folder. Open the `eosc.sln` file in Visual Studio, and then build those two projects:

* `eoscLib` (the library acting as EOS API)
* `eosc` (the executable dependent on `eoscLib`).

#### Testing on remote sever

Open the Windows Power Shell, navigate to the `eosc_visual_studio` folder and run `eosc`:
```
./eosc 198.100.148.136:8888 get info
```
The above command will connect to one of our test-net servers. Alternatively, you can use the placeholder `tokenika` instead of  `198.100.148.136:8888`:
```
./eosc tokenika get info
```

## Library

In our view, the real value of our efforts is actually the library that's behind our `eosc`. As we mentioned before, it serves as a full-blown API for EOS.

Let's consider a code snippet illustrating its usage:
```
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "eosclib/eosc_get_commands.hpp"

int main(int argc, char *argv[])
{
  using namespace tokenika::eosc;

  EoscCommand::host = "198.100.148.136";
  EoscCommand::port = "8888";

  ptree getInfoJson;

  // Invoke 'GetInfo' command:
  GetInfo getInfo(getInfoJson);
  cout << getInfo.toStringRcv() << endl;

  ptree getBlockJson;

  // Use reference to the last block:
  getBlockJson.put("block_num_or_id",
    getInfo.get<int>("last_irreversible_block_num"));
  GetBlock getBlock(getBlockJson);
  cout << getBlock.toStringRcv() << endl;

  return 0;
}
```
Here is the outcome of the above code:
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
