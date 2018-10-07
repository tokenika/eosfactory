
const eosjs = require('eosjs');
const fetch = require('node-fetch');
const { TextDecoder, TextEncoder } = require('text-encoding');
const defaultPrivateKey = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
const signatureProvider = new eosjs.SignatureProvider([defaultPrivateKey]);
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });
const api = eosjs.Api({ rpc, signatureProvider, textDecoder: new TextDecoder, textEncoder: new TextEncoder });

(async () => {
    const result = await api.transact(
    {
        actions: [
            {
                account: 'eosio',
                name: 'newaccount',
                // authorization: [{
                //     actor: 'eosio',
                //     permission: 'active',
                // }],
                data: {
                    creator: 'eosio',
                    name: 'mynewaccount',
                    owner: {
                        threshold: 1,
                        keys: [{
                            key: 'EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
                            weight: 1
                        }],
                        accounts: [],
                        waits: []
                    },
                        active: {
                        threshold: 1,
                        keys: [{
                            key: 'EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV',
                            weight: 1
                        }],
                        accounts: [],
                        waits: []
                    },
                },
            }
            //,
            // {
            //     account: 'eosio',
            //     name: 'buyrambytes',
            //     authorization: [{
            //         actor: 'useraaaaaaaa',
            //         permission: 'active',
            //     }],
            //     data: {
            //         payer: 'useraaaaaaaa',
            //         receiver: 'mynewaccount',
            //         bytes: 8192,
            //     },
            // },
            // {
            //     account: 'eosio',
            //     name: 'delegatebw',
            //     authorization: [{
            //         actor: 'useraaaaaaaa',
            //         permission: 'active',
            //     }],
            //     data: {
            //         from: 'useraaaaaaaa',
            //         receiver: 'mynewaccount',
            //         stake_net_quantity: '1.0000 SYS',
            //         stake_cpu_quantity: '1.0000 SYS',
            //         transfer: false,
            //     }
            // }
    ]
  }, {
    blocksBehind: 1,
    expireSeconds: 30,
  });

  console.log(result)
})()