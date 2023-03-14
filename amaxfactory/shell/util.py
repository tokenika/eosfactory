
def assertAvailableBalance(contract,user,quantity):
    rs = contract.table("accounts",user).json
    for asset in rs["rows"]:
        if quantity in str(asset):
            assert asset["available_balance"]==quantity
            return
    raise Exception(f"quantity:{quantity} not match")

def assertFrozenBalance(contract,user,quantity):
    rs = contract.table("accounts",user).json
    for asset in rs["rows"]:
        if quantity in str(asset):
            assert asset["frozen_balance"]==quantity
            return
    raise Exception(f"quantity:{quantity} not match")
