const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_code(account_name, json=true) {
    result = await rpc.get_code(account_name)
    if(json) {
        console.log(JSON.stringify(result))
    } else {
        console.log(`code hash: ${result["code_hash"]}`)
    } 
}

get_code("eosio", false)