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
Invoke 'get_info' command:
get_info get_info;

{
    "head_block_num": "9939",
    "last_irreversible_block_num": "9924",
    "head_block_id": "000026d378f90b5d25dcf962fc44d637872218e5f826420a342f05a534d50bfc",
    "head_block_time": "2017-12-01T18:57:42",
    "head_block_producer": "initr",
    "recent_slots": "0000000000000000000000000000000000000000000000000011111111111111",
    "participation_rate": "0.21875000000000000"
}


Use reference to the last block:
GetBlock GetBlock(
  get_info.get<int>("last_irreversible_block_num"));

{
    "previous": "000026c35fb5d442be6d4e81a1347cce2c0184c4c2047d9e6dfc78b3bb325ac2",
    "timestamp": "2017-12-01T17:01:09",
    "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "producer": "initn",
    "producer_changes": "",
    "producer_signature": "1f6984d14ee40ed9806ae14aa96531d874fc3417bf3f1b66c4b1d9c9402f3f90ef07c4523eb9a639ad632c181580aeb051385d718dc59ecc54d0f0e5de012b540f",
    "cycles": "",
    "id": "000026c44a2e8075a5b92813869bfb67b72b79ccb3f2e40ad815603c04d2fafd",
    "block_num": "9924",
    "refBlockPrefix": "321436069"
}
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
  tokenika::eosc::get_info get_info; /* Call 'eosd' for 'get info'. */
  tokenika::eosc::GetBlock GetBlock( /* Call 'eosd' for 'get block', the last one. */
    get_info.get<int>("last_irreversible_block_num"));

  std::cout << GetBlock.toStringRcv() << std::endl;/* Print the response. */

  return 0;
}
```
Here is the print-out:
```{
    "previous": "000028716589219b442afe9d140bc28eff4335aecd37d519b0105fca4c8e4a3f",
    "timestamp": "2017-12-01T19:18:27",
    "transaction_merkle_root": "0000000000000000000000000000000000000000000000000000000000000000",
    "producer": "inith",
    "producer_changes": "",
    "producer_signature": "1f510dec0bcd85847b7bead61f6deee7a5fb4108745e6ceaaa81804fe4700b561f7ca3f3f26f56fbfaf1e10fd3ba2999f8cbe165fd391b023334badcf894ba54dc",
    "cycles": "",
    "id": "00002872be99d0133ea104b42b771f3c7c2ea3736263dc9db3719728a2776976",
    "block_num": "10354",
    "refBlockPrefix": "3020202302"
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

<a name="windows"></a>
### [Windows](#toc)

There is an MS Visual Studio 17 solution in `eos_visual_studio` folder. You can start
Visual Studio with file `eosc.sln` there, and you compile both the command library and 
`eosc' executable.
```
msbuild.exe ALL_BUILD.vcxproj
msbuild.exe INSTALL.vcxproj
...

The VS solution has set both boost includes and libraries in relation to the `BOOST_ROOT` environmental variable: Configuration Properties > VC++ Directories. Perhaps, you will have to adjust settings.

Now, the blockchain may be accessed from a Windows Command Prompt, if the `eosd` blockchain program is configured to be called from 


Edit > Virtual Network Editor: Host-only
Virtual Machine Settings > Network Adapter: Host-only
```
ifconfig
## inet 192.168.229.141  netmask 255.255.255.0  broadcast 192.168.229.255
```
eosd config.ini: http-server-endpoint = 192.168.229.141:8888 # Host-only

* Wallet NOT on localhost  -- *
* - Password and/or Private Keys - *
* - are transferred unencrypted.

OK, now trying the tunnel.

