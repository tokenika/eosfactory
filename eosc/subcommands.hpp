#pragma once

#include <string>
#include <map>

const char* create = R"EOF(
ERROR: RequiredError: Subcommand required
Create various items, on and off the blockchain
Usage : . / eosc [OPTIONS] create SUBCOMMAND [OPTIONS]

Subcommands:
    key             Create a new keypair and print the public and private keys
    account         Create a new account on the blockchain
    producer        Create a new producer on the blockchain
)EOF";

const char* set = R"EOF(
ERROR: RequiredError: Subcommand required
Set or update blockchain state
Usage: ./eosc [OPTIONS] set SUBCOMMAND [OPTIONS]

Subcommands:
    contract        Create or update the contract on an account
    producer        Approve/unapprove producer
    proxy           Set proxy account for voting
    account         set or update blockchain account state
    action          set or update blockchain action state
)EOF";

const char* benchmark = R"EOF(
ERROR: RequiredError: Subcommand required
Configure and execute benchmarks
Usage: ./eosc [OPTIONS] benchmark SUBCOMMAND [OPTIONS]

Subcommands:
    setup           Configures initial condition for benchmark
    transfer        executes random transfers among accounts
)EOF";

const char* push = R"EOF(
ERROR: RequiredError: Subcommand required
Push arbitrary transactions to the blockchain
Usage: ./eosc [OPTIONS] push SUBCOMMAND [OPTIONS]

Subcommands:
    message         Push a transaction with a single message
    transaction     Push an arbitrary JSON transaction
    transactions    Push an array of arbitrary JSON transactions
)EOF";
