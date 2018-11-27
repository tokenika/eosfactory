const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_table(
        code, scope, table, json=true, limit=10, table_key="", 
        lower_bound="", upper_bound="") {
    __namedParameters = {
        code: code,
        json: json,
        limit: limit,
        lower_bound: lower_bound,
        scope: scope,
        table: table,
        table_key: table_key,
        upper_bound: upper_bound
    }
    result = await rpc.get_table_rows__namedParameters()
        console.log(result)
}

// get_block(...)




