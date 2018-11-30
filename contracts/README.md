# Contract examples compatible with EOSIO.CDT

## How to generate ABI

Let us take `token`, for example:

```
# cd contracts.cdt/token
eosio-abigen -contract=token -p=build -output=build/token.abi -R=resources src/token.cpp
```

```
eosio-abigen -contract=<ricardian contract file name> \
    -p=<build path> -output=<output path> \
    -R=<resources, ricardian contract files> src/token.cpp
```

## How to generate WASM

```
eosio-cpp -o=build/token.wasm src/token.cpp
```

```
eosio-cpp -o=<output path> src/token.cpp
```

## CMAKE

```
cd build/
cmake ..
make
```