import eosf

class Dictionary:

    def __init__(self, sentence):
        acc_map = eosf.account_map()

        for name in acc_map:
            sentence.replace(name, acc_map[name])