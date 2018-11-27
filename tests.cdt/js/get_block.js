const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });

async function get_block(block_num_or_id, json=true) {
    result = await rpc.get_block(block_num_or_id)
    if(json) {
        console.log(result)
    } else {
        console.log(`timestamp: ${result["timestamp"]}`)
        console.log(`block_num: ${result["block_num"]}`)
        console.log(`id: ${result["id"]}`)
    }
    
}

get_block("0000000c1666a47289ef5850a97e99a9891c8096d2426c24b92018f02ef2fa25", false)


(async (block_num_or_id) => {
    result = await rpc.get_block(block_num_or_id)
    console.log(JSON.stringify(result))

})("0000000c1666a47289ef5850a97e99a9891c8096d2426c24b92018f02ef2fa25")