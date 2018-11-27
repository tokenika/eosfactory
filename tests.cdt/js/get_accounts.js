const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_accounts(public_key, json=true) {
    result = await rpc.history_get_key_accounts(public_key)
    if(json) {
        console.log(JSON.stringify(result))
    } else {
        console.log(`${result["account_names"]}`)
    } 
}

get_accounts("EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV", false)


(async (public_key) => {
    result = await rpc.history_get_key_accounts(public_key)
    console.log(JSON.stringify(result))

})("EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV")