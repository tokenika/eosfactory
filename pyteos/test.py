import session as s

def run():
    s.reset()

    c = s.Contract("eosio.token")

    c.push_action("create", '{"issuer":"eosio", "maximum_supply":"1000000000.0000 EOS", "can_freeze":0, "can_recall":0, "can_whitelist":0}')
    c.push_action("issue", '{"to":"alice", "quantity":"100.0000 EOS", "memo":"memo"}', s.eosio)

    c.push_action("transfer", '{"from":"alice", "to":"carol", "quantity":"25.0000 EOS", "memo":"memo"}', s.alice)
    c.push_action("transfer", '{"from":"carol", "to":"bob", "quantity":"13.0000 EOS", "memo":"memo"}', s.carol)
    c.push_action("transfer", '{"from":"bob", "to":"alice", "quantity":"2.0000 EOS", "memo":"memo"}', s.bob)

    t1=c.get_table("accounts", s.alice)
    t2=c.get_table("accounts", s.bob)
    t3=c.get_table("accounts", s.carol)

    assert t1.json["rows"][0]["balance"] == '77.0000 EOS'
    assert t2.json["rows"][0]["balance"] == '11.0000 EOS'
    assert t3.json["rows"][0]["balance"] == '12.0000 EOS'

    print("Test OK")

    s.stop()
    