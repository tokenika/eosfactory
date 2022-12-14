from amaxfactory.beans.base.amcli import runaction
from amaxfactory.beans.base.baseClass import baseClass


class AMAX(baseClass):
    contract = 'amax.token'

    def close(self, owner='user1', symbol='8,AMAX', suber='user1'):
        runaction(self.contract + f""" close '["{owner}","{symbol}"]' -p {suber}""")

    def create(self, issuer='user1', maximum_supply="0.10000000 AMAX", suber='user1'):
        runaction(self.contract + f""" create '["{issuer}","{maximum_supply}"]' -p {suber}""")

    def issue(self, to='user1', quantity="0.10000000 AMAX", memo='x', suber='user1'):
        runaction(self.contract + f""" issue '["{to}","{quantity}","{memo}"]' -p {suber}""")

    def open(self, owner='user1', symbol='8,AMAX', ram_payer='user1', suber='user1'):
        runaction(self.contract + f""" open '["{owner}","{symbol}","{ram_payer}"]' -p {suber}""")

    def retire(self, quantity="0.10000000 AMAX", memo='x', suber='user1'):
        runaction(self.contract + f""" retire '["{quantity}","{memo}"]' -p {suber}""")

    def transfer(self, fromx='user1', to='user1', quantity="0.10000000 AMAX", memo='x', suber='user1'):
        self.response = runaction(
            self.contract + f""" transfer '["{fromx}","{to}","{quantity}","{memo}"]' -p {suber}""")
        return self
    
    def pk_transfer(self, fromx='user1', to='user1', quantity="0.10000000 AMAX", memo='x'):
        self.response = convert(
            self.contract + f"""  transfer '["{fromx}","{to}","{quantity}","{memo}"]' """)
        return self.response


