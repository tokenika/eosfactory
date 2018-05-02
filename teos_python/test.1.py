import session as s

c1 = Contract("eosio.token")
c1.deploy()

c1.push("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}')
c1.push("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', s.eosio)

c1.push("transfer", '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"}', s.alice)
c1.push("transfer", '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"}', s.carol)
c1.push("transfer", '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"}', s.bob)

c1t1=c1.get("accounts", s.alice)
c1t2=c1.get("accounts", s.bob)
c1t3=c1.get("accounts", s.carol)

assert c1t1.json["rows"][0]["balance"] == '77.0000 EOS'
assert c1t2.json["rows"][0]["balance"] == '11.0000 EOS'
assert c1t3.json["rows"][0]["balance"] == '12.0000 EOS'

print("Test OK")