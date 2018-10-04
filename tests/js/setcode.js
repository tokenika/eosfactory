const fs = require("fs");
const wasm = fs.readFileSync("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world/build/hello_world.wasm");
const abi = JSON.parse(fs.readFileSync("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world/build/hello_world.abi"));

const Eos = require('eosjs')
eos = Eos()
http_endpoint = 'http://127.0.0.1:8888'
key_provider = [
    "5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX",
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5JJUKcmbno3Yhb7d1G2mi4Z3FCX3c7TAZ1kzV2gZ9moLjHTmSkS",
    "5KeWMfTayC6CKcvLRsLigxMmtYn5rLjuER7q4P65X64SXityTWY",
    "5JRZz6q4dpg23bMQkU8jTkn2Y8uQvmpc4fwDwawR8C9tqBbjkUY",
    "5JsFhedYRvnsCKfYm4MjdyaQSNeQ8DX43Ee3EUrgY3oZd6B7x3k",
    "5K3RZuYpb4Rc4hxsV6kLHxjcHURcjVZgmrvfE7JGFNaSQjLqUzf",
    "5KUGvQqjxoe6vgYDnHtnQ4HDGuCn5v3poFEhZmKHHDeGZQaMVWY",
    "5K4xVLAKfb26UZBfyuYYqk9YQrM385LHNs4BaHw5SnesGVYQfTW",
    "5JqKJ7bC9NuyFw81RndVCCfEKEMroyRLbhErXRSrZpRXzcg5d4K"
]
verbose = false
broadcast = true
sign = true
no_error_tag = 'OK'

config = {
    chainId: "6cbecff836a9fa60da53bf97a0a180103b2e76041d4414693d11bf39e2341547",
    keyProvider: key_provider,
    httpEndpoint: http_endpoint,
    expireInSeconds: 60,
    broadcast: broadcast,
    verbose: verbose,
    sign: sign
}
eos = Eos(config)

api()

function process_result(result) {
    return result
}

function print_result(result, err) {
    if (err) {
        console.error(err)
    }
    else {
        result = process_result(result)
        console.error(no_error_tag)
        console.log(JSON.stringify(result))
    }
}

function api() {
    eos.setcode("e4tl11mtxg5f", 0, 0, wasm).then(print_result)
}
