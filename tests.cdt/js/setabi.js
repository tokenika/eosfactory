const Eos = require('eosjs')
eos = Eos()
http_endpoint = 'http://127.0.0.1:8888'
key_provider = [
    '5JfjYNzKTDoU35RSn6BpXei8Uqs1B6EGNwkEFHaN8SPHwhjUzcX', 
    '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3', 
    '5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3', 
    '5HvG218JtkheXWThDKkRnpvBFK3hjbSsgD7AbmWdHK5dQvtqTc3', 
    '5JTCmvrV4WwpGGwkBximniE5wwMp3CywdHZJmhWQS1DmsDhRoJ3', 
    '5JsD5QAfnpAXwr1qdQa8GNsEEidZvee5SHBzdti6PWM8FWYdBgs', 
    '5KieZJGFnTSCaGm2QCS1SDqEFbccwVyMvpJdzq5g9jFxVAhUCdR', 
    '5JkZxkLw5UPCHbbA8EfgvXUgf6iTN4LdVwe3FGNCX6Nj4mf99h4', 
    '5KEEJD1R9NvHSYiykTJTc3vE2CkAvSjH7NSiJEsyCXXnUhFCHd9', 
    '5JUEJ9yxT4mQRstFXNkfoy8Kw1SCU7BiWMMk9A5xJdL94SpzJuu', 
    '5JnUaiuDxDih416ZGmWkZhUwqenBBxHsUZjB6AD4DQUTNEpg8SG'
]
verbose = false
broadcast = true
sign = true
expireInSeconds = 30
no_error_tag = 'OK'

eos.getInfo({}).then(result => id(result, api))

function id(result, api) {
    chain_id = result.chain_id
    config = {
        chainId: chain_id,
        keyProvider: key_provider,
        httpEndpoint: http_endpoint,
        expireInSeconds: expireInSeconds,
        broadcast: broadcast,
        verbose: verbose,
        sign: sign
    }
    eos = Eos(config)
    api()
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
    // For example:
    // eos.getAccount('eosio').then(print_result)
}

function process_result(result) {
    return result
}

//////////////////////////////////////////////////////////////////////////////

const fs = require("fs");
const abi = JSON.parse(fs.readFileSync("/mnt/c/Workspaces/EOS/contracts/_wslqwjvacdyugodewiyd/build/_wslqwjvacdyugodewiyd.abi"));

options = {
    authorization: ["ytcohantju3s@active"],
    broadcast: true,
        sign: true,
}

function api() {
    eos.setabi("ytcohantju3s", abi, options).then(print_result)
}