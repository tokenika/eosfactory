#include <stdexcept>
#include <eoslib/system.h>

/**
 *  Aborts processing of this message and unwinds all pending changes if the test condition is true
*  @brief Aborts processing of this message and unwinds all pending changes
*  @param test - 0 to abort, 1 to ignore
*  @param cstr - a null terminated message to explain the reason for failure

*/
void eosio::assert(eosio::uint32_t test, const char *cstr)
{
   throw std::runtime_error("Not implemented yet!");
}

/**
 *  Returns the time in seconds from 1970 of the last accepted block (not the block including this message)
*  @brief Get time of the last accepted block
*  @return time in seconds from 1970 of the last accepted block
*/
eosio::time now()
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}