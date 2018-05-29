### transaction took too long ERROR
```
{"code":500,"message":"Internal Service Error","error":{"code":3080006,"name":"deadline_exception","what":"transaction took too long",
```

Sometimes happens. This can be EOSIO node instability.
Cure: repeat until success.

### Smart contract debugging example

Open eosio.token template. 
`Tasks->Run Task ...->build`
`Tasks->Run Task ...->test`

You can see 
```
2: issue
2: INFO quantity.amount: 1000000  @ 8:43:8 token.cpp[54](issue)
2: eosio balance: 100.0000 EOS
```
Note *INFO* as a result of an entry in the source file:
```c++
//............................

void token::issue( account_name to, asset quantity, string memo )
{
    print( "issue\n" );
    auto sym = quantity.symbol;
    eosio_assert( sym.is_valid(), "invalid symbol name" );

    auto sym_name = sym.name();
    stats statstable( _self, sym_name );
    auto existing = statstable.find( sym_name );
    eosio_assert( existing != statstable.end(), "token with symbol does not exist, create token before issue" );
    const auto& st = *existing;

    require_auth( st.issuer );
    eosio_assert( quantity.is_valid(), "invalid quantity" );
    eosio_assert( quantity.amount > 0, "must issue positive quantity" );
    logger_info("quantity.amount: ", quantity.amount);

//...........................
```
The same with the skeleton template:

```c++
//..............................

class hello : public eosio::contract {
  public:
      using contract::contract; 

      /// @abi action 
      void hi( account_name user ) {
        logger_info("user: ", name{user});
        print( "Hello, ", name{user} );
      }
};

//...............................
```