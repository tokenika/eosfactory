const fs = require("fs");
const wasm = fs.readFileSync("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world/build/hello_world.wasm");
const abi = JSON.parse(fs.readFileSync("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world/build/hello_world.abi"));

const Eos = require('eosjs')
eos = Eos()
http_endpoint = 'http://127.0.0.1:8888'
key_provider = [

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
    eos.getCode("e4tl11mtxg5f").then(print_result)
}
