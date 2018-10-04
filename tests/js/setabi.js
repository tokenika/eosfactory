const fs = require("fs");
const abi = JSON.parse(fs.readFileSync("/mnt/c/Workspaces/EOS/eosfactory/contracts/01_hello_world/build/hello_world.abi"));

const Eos = require('eosjs')
eos = Eos()
http_endpoint = 'http://127.0.0.1:8888'
key_provider = [
    "5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX",
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3",
    "5J9oVJy1ReuY7M8HpfPqSZPMqE5XuH96ZKHga1duaa7gzNjXoBG",
    "5JqWeEpnCJs4LNpsbgXWRRzezct2Ki7GK8vmbuUXCaX4dU8Bxt3",
    "5JuYrB7nwfjBL6zGJcpCwkbP2Ao8SGwUsRRjizWDH3EweuBfiYH",
    "5Kfip1ScCjVsGGnpQCc4EU86XM8LevBGykoBKjYpPtZ927g9rMc",
    "5JyqTgFup3aL7qvvFTvZZUBZnVbQq6QP8V8JMSRezyefm5msX3K",
    "5Jt6rCFNeqEqRiCc3vYnTk3mNLCNFCT2akAqwnQDs7nGLhFyGHM",
    "5JkTP6FcXXLkxqvdYSgogYADiU8Q8t4zKPhdFS2NYm4e6w7HrxS",
    "5KkGVWKXFJuPJVMQkgy1L7qJUobBvc7Jv6zbCuQHiuxRYA2DhH8"
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

options = {
    authorization: ["aqpehkxnf5tw@active"],
    broadcast: true,
        sign: true,
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
    eos.setabi("aqpehkxnf5tw", abi, options).then(print_result)
}
