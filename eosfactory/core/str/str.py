"""''__str__`` functions for various ``eosfactory.core.cleos`` and ``eosfactory.core.eosjs`` classes."""

def get_code(self_json):
    """``__str__`` function for classes :class:`.core.cleos.get.GetCode` and :class:`.core.eosjs.get.GetCode`
    """
    return "wasm hash: {}".format(self_json["code_hash"])


def get_table(self_json):
    """``__str__`` function for classes :class:`.core.cleos.get.GetTable` and :class:`.core.eosjs.get.GetTable`
    """
    msg = ""
    first = True
    for row in self_json["rows"]:
        if not first:
            msg = msg + "\n"
        first = False
        msg = msg + str(row)

    return msg
