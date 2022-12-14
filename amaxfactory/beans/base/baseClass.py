import json
from random import randint, random
from time import sleep

from base.amcli import gettable


class baseClass:
    contract = 'amax.token'
    response = 'a'

    def assetResponsePass(self):
        assert self.response != ''
    def assetResponseFail(self):
        assert self.response == ''

    def getLastRow(self, scope, tableName, L = 0):
        sleep(0.1)
        rows = json.loads(gettable(self.contract + " " + scope + f" {tableName} -l 10000 -L {L}"))['rows']
        try:
            return rows[-1]
        except:
            return {'id':0}

    def getLastRowByIndex(self, scope, tableName,key,low,up,limit):
        sleep(0.1)
        rows = json.loads(gettable(self.contract + f" {scope} {tableName} -k {key} -L {low} -U {up} -l {limit}"))['rows']
        try:
            return rows[-1]
        except:
            return {'id':0}
        
    def getCode(self):
        keys = "ABCDEFGHIJKLMNOPQRSDUVWXYZ"
        code = ''
        for i in range(7):
            index = randint(0,len(keys)-1)
            code += keys[index]
        return code