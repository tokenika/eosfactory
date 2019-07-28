const { Api, JsonRpc, JsSignatureProvider } = require(`eosjs`)
const fetch = require(`node-fetch`) // node only; not needed in browsers
const { TextEncoder, TextDecoder } = require(`util`) // node only; native TextEncoder/Decoder
const signatureProvider = new JsSignatureProvider(['',])
const rpc = new JsonRpc(`http://127.0.0.1:8888`, { fetch })
const api = new Api({
    rpc,
    signatureProvider,
    textDecoder: new TextDecoder(),
    textEncoder: new TextEncoder(),
})

const fs = require(`fs`)
const path = require(`path`)
const { Serialize } = require(`eosjs`)

const account = '';
const wasm_file = '';
const abi_file = ''

// 1. Prepare SETCODE
// read the file and make a hex string out of it
const wasm = fs.readFileSync(wasm_file).toString(`hex`)

// 2. Prepare SETABI
const buffer = new Serialize.SerialBuffer({
    textEncoder: api.textEncoder,
    textDecoder: api.textDecoder,
})

var abi = JSON.parse(fs.readFileSync(abi_file, `utf8`))
const abiDefinition = api.abiTypes.get(`abi_def`)
// need to make sure abi has every field in abiDefinition.fields
// otherwise serialize throws
abi = abiDefinition.fields.reduce(
    (acc, { name: fieldName }) =>
    Object.assign(acc, { [fieldName]: acc[fieldName] || [] }),
    abi
)
abiDefinition.serialize(buffer, abi)

const permissionDefault = {actor: account_name, permission: 'active',}

//Send transaction with both setcode and setabi actions
(async () => {
    const result = await api.transact(
        {
            actions: [
                {
                    account: 'eosio',
                    name: 'setcode',
                    authorization: [
                        permissionDefault,
                    ],
                    data: {
                        account: account,
                        vmtype: 0,
                        vmversion: 0,
                        code: wasm,
                    },
                },
                {
                    account: 'eosio',
                    name: 'setabi',
                    authorization: [
                        permissionDefault,
                    ],
                    data: {
                        account: account,
                        abi: Buffer.from(buffer.asUint8Array()).toString(`hex`),
                    },
                },
            ],
        },
        {
            blocksBehind: 3,
            expireSeconds: 30,
        }
    );
    console.log(JSON.stringify(result))
})();


