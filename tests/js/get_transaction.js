const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_transaction(is, block_num_hint, json=true) {
    result = await rpc.history_get_transaction(is, block_num_hint)
    if(json) {
        console.log(JSON.stringify(result))
    } else {
    } 
}

get_transaction("EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")