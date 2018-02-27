#include <stdexcept>
#include <eoslib/db.h>
// to list exported functions in a static library: nm libdb.a

eosio::int32_t store_i64(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t update_i64(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t load_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t front_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t next_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t previous_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   return 0;
}

eosio::int32_t lower_bound_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t remove_i64(
    account_name scope,
    table_name table,
    void *data)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t store_str(
    account_name scope,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t update_str(
    account_name scope,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_str(
    account_name scope,
    account_name code,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_str(
    account_name scope,
    account_name code,
    table_name table,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_str(
    account_name scope,
    account_name code,
    table_name table,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_str(
    account_name scope,
    account_name code,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_str(
    account_name scope,
    account_name code,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_str(
    account_name scope,
    account_name code,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_str(
    account_name scope,
    account_name code,
    table_name table,
    char *key,
    eosio::uint32_t keylen,
    char *value,
    eosio::uint32_t valuelen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t remove_str(
   account_name scope, 
   table_name table, 
   char *key, 
   eosio::uint32_t keylen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_primary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_secondary_i128i128(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t remove_i128i128(
    account_name scope,
    table_name table,
    const void *data)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t store_i128i128(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t update_i128i128(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_secondary_i64i64i64(
   account_name scope,
   account_name code,
   table_name table,
   void *data,
   eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_secondary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t datalen)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_primary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t load_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t front_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t back_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t next_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t previous_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t upper_bound_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t lower_bound_tertiary_i64i64i64(
    account_name scope,
    account_name code,
    table_name table,
    void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t remove_i64i64i64(
    account_name scope,
    table_name table,
    const void *data)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t store_i64i64i64(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}

eosio::int32_t update_i64i64i64(
    account_name scope,
    table_name table,
    const void *data,
    eosio::uint32_t len)
{
   throw std::runtime_error("Not implemented yet!");
   return 0;
}
