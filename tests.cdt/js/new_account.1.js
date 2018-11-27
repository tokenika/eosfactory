
const eosjs = require('eosjs');
const fetch = require('node-fetch');
const rpc = new eosjs.Rpc.JsonRpc('http://127.0.0.1:8888', { fetch });
const { TextDecoder, TextEncoder } = require('text-encoding');
const defaultPrivateKey = "5KQwrPbwdL6PhXujxW37FSSQZ1JiwsST4cqQzDeyXtP79zkvFD3";
const defaultPublicKey = "EOS6MRyAjQq8ud7hVNYcfnVPJqcVpscN5So8BhtHuGYqET5GDW5CV";
const signatureProvider = new eosjs.SignatureProvider([defaultPrivateKey]);
const api = new eosjs.Api({ rpc, signatureProvider, 
    textDecoder: new TextDecoder, textEncoder: new TextEncoder });
    

(async () => {
    const result = await api.transact(
        {
            actions: [
                {
                    account: 'eosio',
                    name: 'newaccount',
                    authorization: [
                        {
                            actor: 'eosio',
                            permission: 'active',
                        }
                    ],
                    data: {
                        creator: 'eosio',
                        name: 'mynewaccount',
                        owner: {
                            threshold: 1,
                            keys: [
                                {
                                    key: defaultPublicKey,
                                    weight: 1
                                }
                            ],
                            accounts: [],
                            waits: []
                        },
                            active: {
                            threshold: 1,
                            keys: [
                                {
                                    key: defaultPublicKey,
                                    weight: 1
                                }
                            ],
                            accounts: [],
                            waits: []
                        }
                    }
                }
            ]
        },
        {
            blocksBehind: 3,
            expireSeconds: 30,
        });

  console.log(result)
})()