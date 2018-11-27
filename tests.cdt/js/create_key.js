const ecc = require('eosjs-ecc')

async function create_key(json=true) {
    private_key = await ecc.randomKey()
    public_key = ecc.privateToPublic(private_key)
    const result = {
        private_key: private_key,
        public_key: public_key
    }
    if(json){
        console.log(JSON.stringify(result))
    } else {
        console.log(private_key)
        console.log(public_key)
    }
    
    
}

create_key()
