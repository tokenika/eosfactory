# Tokenika's alternative for EOS command line interface

## Rationale

For those less familiar with EOS codebase, `eosc` is the official CLI (Command Line Interface) for EOS. It interacts with the EOS blockchain by connecting to a full node called `eosd`, which can run either locally or on a remote server.

When working with EOS smart-contracts, we've found that `eosc` has some inconvenient limitations:

* Firstly, it's hard to use `eosc` programmatically, as it doesn't offer an API.
* Secondly, it is quite heavyweight in terms of external dependencies, as it's tightly connected to the entire EOS codebase.
* Also, it is not ready to be used in Windows environment, while our plans include opening up EOS for smart-contract development on Windows.

It could be enough for us to develop a minimal C++ library acting as an EOS API and this way implement all the commands supported by `eosc`. However, it was a short step to provide such a library with a command line interface, and thus create a full-blown `eosc` replacement, which we've named `teos`. 

Here are the benefits of using `teos` instead of `eosc`:

* With `teos` you can do everything available in `eosc` and much more, as we've added a richer & more useful command option list.
* Also, as `teos` is not dependent on the entire EOS codebase, it can be easily compiled on any platform, including Windows, which is not the case with `eosc`.
* And last but not least, `teos` has an underlying library which offers a proper API which you can use to interact programmatically with EOS full node, `eosd`. 

For obvious reasons everything we do is open source. The source code of `teos` is located in [this repository](https://github.com/tokenika/eosc).

## Comparison

As we've mentioned before, `teos` covers the same functionality as `eosc`, but it's more user friendly and offers a wider selection of options.

Let's compare the `get block` command's help:
```
./eosc get block --help
```
The response `eosc` gives looks like this:
```
ERROR: RequiredError: block
Retrieve a full block from the blockchain
Usage: ./eosc get block block
Positionals:
block TEXT                  The number or ID of the block to retrieve
```
Whereas when you type a similar command in `teos`:

```
./teos get block --help
```

You will get something like this:

```
Retrieve a full block from the blockchain
Usage: ./teos get block [block_num_or_id][options]
Usage: ./teos get block [-j {"block_num_or_id":*}][options]

Options:
  -h [ --help ]           Help screen
  -n [ --block_num ] arg  Block number
  -i [ --block_id ] arg   Block id
  -j [ --json ] arg       Json argument
  -v [ --verbose ]        Print the entire received json
  -r [ --raw ]            Raw print
  -e [ --example ]        Usage example
```
And now let's compare the `get block` command usage, e.g.:
```
./eosc get block 25
```
The `eosc` response looks like this:
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
Whereas for a similar command in `teos`:

```
./teos get block 25
```

You will get a response which is less verbose by default, to make it more readable:

```
## block number: 25
## timestamp: 2017-11-29T09:50:03
## ref block prefix: 623236675
```
But you can make it verbose, if you need:
```
./teos get block 25 --verbose
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
./teos get block 25 --verbose --raw
```
```
{"previous":"00000018b5e0ffcd3dfede45bc261e3a04de9f1f40386a69821780e063a41448","timestamp":"2017-11-29T09:50:03","transaction_merkle_root":"0000000000000000000000000000000000000000000000000000000000000000","producer":"initf","producer_changes":"","producer_signature":"2005db1a193cc3597fdc3bd38a4375df2a9f9593390f9431f7a9b53701cd46a1b5418b9cd68edbdf2127d6ececc4d66b7a190e72a97ce9adfcc750ef0a770f5619","cycles":"","id":"000000190857c9fb43d62525bd29dc321003789c075de593ce7224bde7fc2284","block_num":"25","refBlockPrefix":"623236675"}
```
Also, you can supply the arguments in *json* format:
```
./teos get block --json '{"block_num_or_id":"56"}'
```
```
##         block number: 56
##            timestamp: 2017-11-29T10:02:18
##     ref block prefix: 273573026
```
And finally, for each command you can invoke an example showcasing its usage:
```
./teos get block --example
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

## Building on Ubuntu

#### Dependencies

First, make sure you have Boost 1.62 (or higher) installed:
```
dpkg -s libboost-dev | grep 'Version'
```
In case you need to install it, run this command:
```
sudo apt-get install libboost-all-dev
```
Also, in order to be able to manage things like private key generation, `teos` is also dependent on some C++ libraries (namely `fc` and `utilities`), which are part of EOS codebase.

#### Cloning the source code

Navigate to a location of your choice on your machine and clone our *eosc* repository:

```
git clone https://github.com/tokenika/teos.git
```
#### Compilation

Navigate to the `teos` folder and create a new folder named `build`:

```
cd teos
mkdir build
cd build
```
Run CMake:
```
cmake ..
```
Make sure there are no errors, and then proceed with the actual compilation:
```
make
```
As the result of the compilation, you should be able to find those two files in the `build` folder:
* `teoslib\libteoslib.a` is a static library acting as an API for EOS
* `teos` is the CLI executable making use of the above library

#### Testing on remote sever

Open a terminal window, navigate to the `build` folder and run `teos`:
```
./teos 198.100.148.136:8888 get info
```
The above command will connect to one of our testnet servers. Alternatively, you can use the predefined placeholder `tokenika` instead of  `198.100.148.136:8888`:
```
./teos tokenika get info
```

#### Testing on localhost

If you have complied the entire EOS codebase and have `eosd` running on your local machine, you can also test `teos` locally:
```
./teos localhost get info
```

## Building on Windows

#### Dependencies

Make sure you have Boost 1.64 available on your machine. If not, you can download the source code from [the official webpage](http://www.boost.org/users/download/) or use the [pre-built Windows binaries](https://sourceforge.net/projects/boost/files/boost-binaries/) (make sure to use the [boost_1_64_0-msvc-14.1-64](https://sourceforge.net/projects/boost/files/boost-binaries/1.64.0/boost_1_64_0-msvc-14.1-64.exe/download) version, as it's compatible with MS Visual Studio 2017).

Also, in order to be able to manage things like private key generation, `teos` is also dependent on some C++ libraries (namely `fc` and `utilities`), which are part of EOS codebase. We had to introduce slight changes to make them compatible with Windows. In the future we plan to turn those amendments into pull requests against EOS repository, so that everything is going to be unified. For the time being we use slightly modified clones of those libraries.

#### System variables

Set up a system variable named  `BOOST_ROOT` pointing at your *Boost* directory. In our case it looks like this, but yours will most probably be different, depending on your *Boost* library location:

![](img02.png)

#### Cloning the source code

Navigate to a location of your choice on your machine and clone our *teos* repository:

```
git clone https://github.com/tokenika/teos.git
```

#### Compilation

Open the *Power Shell* terminal, navigate to the `teos` folder and then run the following commands:
```
mkdir bulidWindows
cd buildWindows
cmake -G "Visual Studio 15 2017 Win64" ..
msbuild teos.sln
```

#### Testing on remote sever

If there are no errors, switch to the *Debug* folder:

```
cd Debug
```

And now you should be able to run `teos` and access `eosd` running on one of our servers:

```
./teos 198.100.148.136:8888 get info
```

Alternatively, you can use the predefined placeholder `tokenika` instead of  `198.100.148.136:8888`:

```
./teos tokenika get info
```
```
Debug/teos.exe tokenika get block 25
##         block number: 25
##            timestamp: 2017-12-05T19:55:56
##     ref block prefix: 1139663381
Debug/teos tokenika create key
##             key name: default
##          private key: 5JyL28JPQbPTYwTpjKRcXvfj6nwUKgCmHnJaD28nmmWMpHXukVn
##           public key: EOS7TxBhoCwAWXoV8uhtgjz4inTLwiwcySvrVhGNYcjhw75wFJ9uA
```

#### Working with MS Visual Studio

If you want, you can play with `teos` source code using [MS Visual Studio 2017](https://www.visualstudio.com/). The *Community* edition is fully functional and is [available for free](https://www.visualstudio.com/).

We've created a dedicated MS Visual Studio solution project - it's located in the  `teos_visual_studio` folder. Open the `teos.sln` file in MS Visual Studio 2017, and then build those two projects:

* `teosLib` (the library acting as EOS API)
* `teos` (the executable dependent on `teosLib`).

Once both projects are successfully built, open the *Power Shell* terminal, navigate to the `teos_visual_studio` folder and then run the `teos` CLI:

```
./teos tokenika get info
```

## Library

In our view, the real value of our efforts is actually the library that's behind `teos`. As we mentioned before, the `teosLib` library acts as a full-blown API for EOS.

Let's consider a code snippet illustrating its usage:
```
#include <stdio.h>
#include <stdlib.h>
#include <iostream>
#include <string>

#include "teosLib/teos_get_commands.hpp"

int main(int argc, char *argv[])
{
  using namespace tokenika::teos;

  TeosCommand::host = "198.100.148.136";
  TeosCommand::port = "8888";

  ptree getInfoJson;

  // Invoke 'GetInfo' command:
  GetInfo getInfo(getInfoJson);
  cout << getInfo.toStringRcv() << endl;

  if (getInfo.isError()) {
    return -1;
  }

  ptree getBlockJson;

  // Use reference to the last block:
  getBlockJson.put("block_num_or_id",
    getInfo.get<int>("last_irreversible_block_num"));
  GetBlock getBlock(getBlockJson);
  cout << getBlock.toStringRcv() << endl;

  if (getBlock.isError()) {
    return -1;
  }

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

## Conclusion

We dare to hope that this little work of ours could become an interesting alternative to the original `eosc` CLI, and maybe one day be included as part of EOS codebase.