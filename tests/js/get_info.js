const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

// async function get_info(json=true) {
//     result = await rpc.get_info()
//     if(json) {
//         console.log(result)
//     } else {
//         console.log(`chain id: ${result["chain_id"]}`)
//         console.log(`head block num: ${result["head_block_num"]}`)
//     }
    
// }

// get_info(false)


(async (json=true) => {
    result = await rpc.get_info()
    if(json) {
        console.log(result)
    } else {
        console.log(`chain id: ${result["chain_id"]}`)
        console.log(`head block num: ${result["head_block_num"]}`)
    }
    
})()