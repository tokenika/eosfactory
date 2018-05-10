#include <teoslib/command/push_commands.hpp>

const char* pushSubcommands = R"(
ERROR: RequiredError: Subcommand required
Push arbitrary transactions to the blockchain
Usage: ./teos [OPTIONS] push SUBCOMMAND [OPTIONS]

Subcommands:
    message         Push a transaction with a single message
    transaction     Push an arbitrary JSON transaction
    transactions    Push an array of arbitrary JSON transactions
)";

