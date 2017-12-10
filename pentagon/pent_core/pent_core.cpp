
#include <stdlib.h>
#include <string>
#include <boost/algorithm/string/trim.hpp>
#include "pent_core.hpp"

using namespace std;

static char char_to_symbol( char c ) {
   if( c >= 'a' && c <= 'z' )
      return (c - 'a') + 6;
   if( c >= '1' && c <= '5' )
      return (c - '1') + 1;
   return 0;
}

/* 
After  eos/contracts/eoslib/types.hpp:
   static constexpr eosio::uint64_t string_to_name(...)
or after eos/libraries/types/include/eos/types/native.hpp:
   static constexpr uint64_t string_to_name(...)
 */
unsigned long long pentagon::eos_name(const char *str)
{
   unsigned len = 0;
   while( str[len] ) ++len;

   unsigned long long value = 0;

   for( unsigned i = 0; i <= 12; ++i ) {
      unsigned long long c = 0;
      if( i < len && i <= 12 ) c = char_to_symbol( str[i] );

      if( i < 12 ) {
         c &= 0x1f;
         c <<= 64-5*(i+1);
      }
      else {
         c &= 0x0f;
      }

      value |= c;
   }
   return value;
}
/*
static constexpr eosio::uint64_t string_to_name( const char* str ) {

      eosio::uint32_t len = 0;
      while( str[len] ) ++len;

      eosio::uint64_t value = 0;

      for( eosio::uint32_t i = 0; i <= 12; ++i ) {
         eosio::uint64_t c = 0;
         if( i < len && i <= 12 ) c = char_to_symbol( str[i] );

         if( i < 12 ) {
            c &= 0x1f;
            c <<= 64-5*(i+1);
         }
         else {
            c &= 0x0f;
         }

         value |= c;
      }

      return value;
   }
*/

/*
After eos/libraries/types/include/eos/types/native.hpp:
   name::explicit operator string()const(...
*/
string pentagon::eos_name(
  const unsigned long long ull)
{
   static const char *charmap = ".12345abcdefghijklmnopqrstuvwxyz";
   string str(13, '.');
   unsigned long long tmp = ull;
   for (unsigned i = 0; i <= 12; ++i)
   {
      char c = charmap[tmp & (i == 0 ? 0x0f : 0x1f)];
      str[12 - i] = c;
      tmp >>= (i == 0 ? 4 : 5);
   }
   boost::algorithm::trim_right_if(str, [](char c) { return c == '.'; });
   return str;
}
