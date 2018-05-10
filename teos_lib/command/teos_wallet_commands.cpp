#include <teoslib/command/wallet_commands.hpp>

const char* walletSubcommands = R"(
ERROR: RequiredError: Subcommand required
Interact with local wallet
Usage : . / teos [OPTIONS] wallet SUBCOMMAND [OPTIONS]

Subcommands:
    create          Create a new wallet locally
    open            Open an existing wallet
    lock            Lock wallet
    lock_all        Lock all unlocked wallets
    unlock          Unlock wallet
    import          Import private key into wallet
    list            List opened wallets, *= unlocked
    keys            List of private keys from all unlocked wallets in wif format.
)";

const std::string walletCommandPath = "/v1/wallet/";