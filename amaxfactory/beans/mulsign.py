import json
from time import sleep

from base.amcli import convert, runaction, gettable
from amaxfactory.beans.base.baseClass import baseClass


class Mulsign(baseClass):
    contract = 'amax.mulsign'
    def cancel(self, issuer='user1', proposal_id=1, suber='user1'):
        self.response = runaction(self.contract + f""" cancel '["{issuer}",{proposal_id}]' -p {suber}""")
        return self

    def collectfee(self, fromx='user1', to='user1', quantity="0.10000000 AMAX", suber='user1'):
        self.response = runaction(self.contract + f""" collectfee '["{fromx}","{to}","{quantity}"]' -p {suber}""")
        return self

    def delmulsigner(self, issuer='user1', wallet_id=1, mulsigner='user1', suber='user1'):
        self.response = runaction(
            self.contract + f""" delmulsigner '["{issuer}",{wallet_id},"{mulsigner}"]' -p {suber}""")
        return self

    def pk_delmulsigner(self, issuer='user1', wallet_id=1, mulsigner='user1'):
        self.response = convert(
            self.contract + f""" delmulsigner '["{issuer}",{wallet_id},"{mulsigner}"]'""")
        return self.response

    def execute(self, issuer='user1', proposal_id=1, suber='user1'):
        self.response = runaction(self.contract + f""" execute '["{issuer}",{proposal_id}]' -p {suber}""")
        return self

    def init(self, fee_collector='user1',fee="0.10000000 AMAX", suber='user1'):
        self.response = runaction(self.contract + f""" init '["{fee_collector}","{fee}"]' -p {suber}""")
        return self

    def propose(self, issuer='user1', wallet_id=1, type='user1',contract_name=contract, params=1, excerpt='x', meta_url='x', duration=1,
                suber='user1'):
        params = str(params).replace("'", '"')
        self.response = runaction(
            self.contract + f""" propose '["{issuer}",{wallet_id},"{type}","{contract_name}","{params}","{excerpt}","{meta_url}",{duration}]' -p {suber}""")
        return self

    def setmulsigner(self, issuer='user1', wallet_id=1, mulsigner='user1', weight=1, suber='user1'):
        self.response = runaction(
            self.contract + f""" setmulsigner '["{issuer}",{wallet_id},"{mulsigner}",{weight}]' -p {suber}""")
        return self

    def pk_setmulsigner(self, issuer='user1', wallet_id=1, mulsigner='user1', weight=1):
        self.response = convert(
            self.contract + f""" setmulsigner '["{issuer}",{wallet_id},"{mulsigner}",{weight}]'""")
        return self.response

    def setmulsignm(self, issuer='user1', wallet_id=1, mulsignm=1, suber='user1'):
        self.response = runaction(self.contract + f""" setmulsignm '["{issuer}",{wallet_id},{mulsignm}]' -p {suber}""")
        return self

    def pk_setmulsignm(self, issuer='user1', wallet_id=1, mulsignm=1):
        self.response = convert(self.contract + f""" setmulsignm '["{issuer}",{wallet_id},{mulsignm}]'""")
        return self.response

    def setwapexpiry(self, issuer='user1', wallet_id=1, expiry_sec=1, suber='user1'):
        self.response = runaction(
            self.contract + f""" setwapexpiry '["{issuer}",{wallet_id},{expiry_sec}]' -p {suber}""")
        return self

    def submit(self, issuer='user1', proposal_id=1, vote=1, suber='user1'):
        self.response = runaction(self.contract + f""" respond '["{issuer}",{proposal_id},{vote}]' -p {suber}""")
        return self

    def wallets(self):
        sleep(0.1)
        return gettable(self.contract + " " + self.contract + " wallets -l 10000")
    def getwallet(self, id):
        sleep(0.1)
        return json.loads(gettable(self.contract + " " + self.contract + f" wallets -L {id} -U {id}"))['rows'][0]

    def proposals(self):
        sleep(0.1)
        return gettable(self.contract + " " + self.contract + " proposals -l 10000")

    def getLastWallet(self):
        rows = json.loads(self.wallets())['rows']
        try:
            return rows[-1]
        except:
            return {'id':-1}


    def getLastProposal(self):
        rows = json.loads(self.proposals())['rows']
        try:
            return rows[-1]
        except:
            return {'id':-1}
