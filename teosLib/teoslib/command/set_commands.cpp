#include <teos/command/set_commands.hpp>


const char* setSubcommands = R"EOF(
ERROR: RequiredError: Subcommand required
Set or update blockchain state
Usage: ./teos [OPTIONS] set SUBCOMMAND [OPTIONS]

Subcommands:
    contract        Create or update the contract on an account
    producer        Approve/unapprove producer
    proxy           Set proxy account for voting
    account         set or update blockchain account state
    action          set or update blockchain action state
)EOF";

