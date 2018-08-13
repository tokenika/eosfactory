# push_action account does not have access to data just inserted #32

https://github.com/tokenika/eosfactory/issues/32

## Q

Hello, I am having an issue here. I am not able to read the table data that I just inserted with my account. I am able to see it with the deployer's account, but I shouldn't have to do that, right?

lottery.spec.py
```
cprint(""" Action contract.push_action("addgrade") """, 'magenta')
action = contract.push_action(
            "addgrade", "[" + str(account_admin) + ", 1, 25]", account_admin)
print(action)
self.assertFalse(action.error)
t = contract.table("grade", account_admin)
```
Output:
```
######### 
Create a `Wallet` object with the NODEOS wallet plugin.
Wallet directory is /Users/markmathis/Projects/EOS/eosfactory/build/daemon/data-dir/wallet/
Created wallet `default` with the local testnet.
Password is saved to the file passwords.json in the wallet directory.
######### 
Get master account.
Local testnet is ON: the `eosio` account is master.
 Action contract.push_action("addgrade") 
#  lottery.code <= lottery.code::addgrade       {"account":"4xkqfr2bm5w1","grade_num":1,"openings":25}

executed transaction: e60860579c03bdeb29de75a64b43ab3231ae1da61888e2ae96591b3484242e2a  120 bytes  323 us
warning: transaction executed locally, but may not be confirmed by the network yet

{
  "rows": [],
  "more": false
}
```
Lottery.cpp
```
void addgrade(const account_name account, uint64_t grade_num, uint64_t openings) {
 require_auth(account);
When I query with the deployer I get the row

{
  "rows": [{
      "account_name": "3130073847880961968",
      "grade_num": 1,
      "openings": 25,
      "applicants": 0
    }
  ],
  "more": false
}
```

## Q

Please, do 