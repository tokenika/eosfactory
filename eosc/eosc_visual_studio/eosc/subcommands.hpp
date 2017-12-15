#pragma once

#include <map>


const char* wallet = R"EOF(
Subcommands for 'wallet' command:
  create          Create a new wallet locally
  open            Open an existing wallet
  lock            Lock wallet
  lock_all        Lock all unlocked wallets
  unlock          Unlock wallet
  import          Import private key into wallet
  list            List opened wallets, *= unlocked
  keys            List of private keys from all unlocked wallets in wif format.
)EOF";

std::map<const char*, const char*> subcommands = { 
  { "wallet", wallet } 

};