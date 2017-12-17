#include "eosc_get_commands.hpp"

const char* getSubcommands = R"EOF(
ERROR: RequiredError: Subcommand required
Retrieve various items and information from the blockchain
Usage : . / eosc [OPTIONS] get SUBCOMMAND [OPTIONS]

Subcommands:
    info            Get current blockchain information
    block           Retrieve a full block from the blockchain
    account         Retrieve an account from the blockchain
    code            Retrieve the code and ABI for an account
    table           Retrieve the contents of a database table
    accounts        Retrieve accounts associated with a public key
    servants        Retrieve accounts which are servants of a given account
    transaction     Retrieve a transaction from the blockchain
    transactions    Retrieve all transactions with specific account name referenced in their scope
)EOF";

const std::string getCommandPath = "/v1/chain/";