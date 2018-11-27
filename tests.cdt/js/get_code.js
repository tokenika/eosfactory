const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

// async function get_code(account_name) {
//     result = await rpc.get_code(account_name)
//         console.log(JSON.stringify(result))
// }

// get_code("wqpum1uoaadf")

(async (account_name) => {
    result = await rpc.get_code(account_name);
    console.log(JSON.stringify(result))
})("eosio")