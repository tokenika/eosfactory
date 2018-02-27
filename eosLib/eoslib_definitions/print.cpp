
//#include <iostream>

#include <stdio.h>
#include <stdexcept>
#include <string>
#include <eoslib/types.h>
#include <eoslib/print.h>
#include <pent_core.hpp>

// see eos/libraries/chain/wasm_interface.cpp
/**
*  Prints string
*  @brief Prints string
*  @param cstr - a null terminated string
*
*  Example:
*  @code
*  prints("Hello World!"); // Output: Hello World!
*  @endcode
*/
void prints(const char *cstr)
{
   fprintf(stdout, "%s", cstr);
}

/**
*  Prints string up to given length
*  @brief Prints string
*  @param cstr - pointer to string
*  @param len - len of string to be printed
*
*  Example:
*  @code
*  prints_l("Hello World!", 5); // Output: Hello
*  @endcode
*/
void prints_l(const char *cstr, eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
}

/**
* Prints value as a 64 bit unsigned integer
* @brief Prints value as a 64 bit unsigned integer
* @param Value of 64 bit unsigned integer to be printed
*
*  Example:
*  @code
*  printi(1e+18); // Output: 1000000000000000000
*  @endcode
*/
void printi(eosio::uint64_t value)
{
   fprintf(stdout, "%llu", value);
}

/**
* Prints value as a 128 bit unsigned integer
* @brief Prints value as a 128 bit unsigned integer
* @param value 128 bit integer to be printed
*
*  Example:
*  @code
*  eosio::uint128_t large_int(87654323456);
*  printi128(large_int); // Output: 87654323456
*  @endcode
*/
void printi128(const eosio::uint128_t *value)
{
   throw std::runtime_error("Not implemented yet!");
}

/**
* Prints value as double
* @brief Prints value as double
* @param Value of double (interpreted as 64 bit unsigned integer) to be printed
*
*  Example:
*  @code
*  eosio::uint64_t double_value = double_div( i64_to_double(5), i64_to_double(10) );
*  printd(double_value); // Output: 0.5
*  @endcode
*/
void printd(eosio::uint64_t value)
{
   throw std::runtime_error("Not implemented yet!");
}

/**
* Prints a 64 bit names as base32 encoded string
* @brief Prints a 64 bit names as base32 encoded string
* @param Value of 64 bit names to be printed
*
* Example:
* @code
* printn(N(abcde)); // Output: abcde
* @endcode
*/
void printn(eosio::uint64_t ull)
{
   fprintf(stdout, "%s", pentagon::eos_name(ull).c_str());
}

/**
*/
void printhex(void *data, eosio::uint32_t datalen)
{
   throw std::runtime_error("Not implemented yet!");
}