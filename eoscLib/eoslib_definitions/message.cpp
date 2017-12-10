#include <stdexcept>
#include <eoslib/message.hpp>

/**
 *  Copy up to @ref len bytes of current message to the specified location
*  @brief Copy current message to the specified location
*  @param msg - a pointer where up to @ref len bytes of the current message will be copied
*  @param len - len of the current message to be copied
*  @return the number of bytes copied to msg
*/
eosio::uint32_t read_message(void *msg, eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

/**
 * Get the length of the current message's data field
* This method is useful for dynamically sized messages
* @brief Get the length of current message's data field
* @return the length of the current message's data field
*/
eosio::uint32_t messageSize()
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

/**
 *  Add the specified account to set of accounts to be notified
*  @brief Add the specified account to set of accounts to be notified
*  @param name - name of the account to be verified
*/
void require_notice(account_name name)
{
   fprintf(stdout, "require_notice: not implemented yet!");
}

/**
 *  Verifies that @ref name exists in the set of provided auths on a message. Throws if not found
*  @brief Verify specified account exists in the set of provided auths
*  @param name - name of the account to be verified
*/
void require_auth(account_name name)
{
   throw std::runtime_error("Not implemented yet!");
}

/**
 *  Get the account which specifies the code that is being run
*  @brief Get the account which specifies the code that is being run
*  @return the account which specifies the code that is being run
*/
account_name currentCode()
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}