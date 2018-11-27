const ecc = require('eosjs-ecc')

function private_to_public(private_key) {
    result = ecc.privateToPublic(private_key)
    console.log(result)
}

private_to_public("5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3")
