"const Eos = require('eosjs'); const eos = Eos().getInfo((error, info) => { console.log(error, info);});"

node -p "const Eos = require('eosjs'); console.log(Eos().getInfo({}));"