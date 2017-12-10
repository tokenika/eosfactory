/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */

#include "currency.hpp" /// defines transfer struct (abi)

namespace currency
{
using namespace eosio;

///  When storing accounts, check for empty balance and remove account
void store_account(account_name account_to_store, const account &a)
{
   if (a.is_empty())
   {
      ///               value, scope
      accounts::remove(a, account_to_store);
   }
   else
   {
      ///              value, scope
      accounts::store(a, account_to_store);
   }
}

void apply_currency_transfer(const currency::transfer &transfer_msg)
{
   require_notice(transfer_msg.to, transfer_msg.from);
   require_auth(transfer_msg.from);

   auto from = get_account(transfer_msg.from);
   auto to = get_account(transfer_msg.to);

   from.balance -= transfer_msg.quantity; /// token subtraction has underflow assertion
   to.balance += transfer_msg.quantity;   /// token addition has overflow assertion

   store_account(transfer_msg.from, from);
   store_account(transfer_msg.to, to);
}

} // namespace currency

using namespace currency;

extern "C" {
void init()
{
   eosio::print(
       "init currency contract: ",
       "N(currency): ",
       N(currency),
       "\n");
   store_account(N(currency), account(currency_tokens(1000ll * 1000ll * 1000ll)));
}

void apply(eosio::uint64_t code, eosio::uint64_t action)
{
   eosio::print(
       "code: ", code, "; name(code): ", name(code),
       "; name(code).value: ", name(code).value,
       "; N(name(code).value): ", N(name(code).value),
       "\n",
       "action: ", action, "; name(action): ", name(action),
       "\n");

   if (code == N(currency))
   {
      if (action == N(transfer))
      {
         currency::transfer message;
         message.quantity = currency_tokens(50);
         message.from = account_name(5093418677655568384);
         message.to = account_name(8421048506461978624);

         eosio::print(
             "Transfer ", message.quantity,
             " from ", message.from,
             " to ", message.to,
             "\n");

         currency::apply_currency_transfer(message);
      }
   }
}

void applyOrig(eosio::uint64_t code, eosio::uint64_t action)
{
   eosio::print(
       "code: ", code, "; name(code): ", name(code),
       "; name(code).value: ", name(code).value,
       "; N(name(code).value): ", N(name(code).value),
       "\n",
       "action: ", action, "; name(action): ", name(action),
       "\n");

   if (code == N(currency))
   {
      if (action == N(transfer))
      {
         auto message = eosio::current_message<currency::transfer>();
         eosio::print(
             "Transfer ", message.quantity,
             " from ", message.from,
             " to ", message.to,
             "\n");

         currency::apply_currency_transfer(current_message<currency::transfer>());
      }
   }
}
}
