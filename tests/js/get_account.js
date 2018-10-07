const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_account(account_name, json=true) {
    result = await rpc.get_account(account_name)
    if(json) {
        console.log(JSON.stringify(result))
    } else {
        console.log(`chain_id: ${result["chain_id"]}`)
        console.log(`head_block_num: ${result["head_block_num"]}`)
    } 
}

get_account("eosio")