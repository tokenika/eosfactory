Function macro definitions accept two special operators (# and ##) in the replacement sequence:
The operator #, followed by a parameter name, is replaced by a string literal that contains the argument passed (as if enclosed between double quotes):
```
#define str(x) #x
cout << str(test);
```
This would be translated into:
```
cout << "test";
```
The operator ## concatenates two arguments leaving no blank spaces between them:
```
#define glue(a,b) a ## b
glue(c,out) << "test";
```
This would also be translated into:
```
cout << "test";
```
declarations:
/mnt/hgfs/Workspaces/EOS/eos/contracts/eoslib/message.h
/mnt/hgfs/Workspaces/EOS/eos/contracts/currency/currency.cpp

definitions:

some uses:
* /mnt/hgfs/Workspaces/EOS/eos/contracts/test_api/test_api.cpp
```
static constexpr u32 DJBH(const char* cp)
{
  u32 hash = 5381;
  while (*cp)
      hash = 33 * hash ^ (unsigned char) *cp++;
  return hash;
}

static constexpr u64 WASM_TEST_ACTION(const char* cls, const char* method)
{
  return u64(DJBH(cls)) << 32 | u64(DJBH(method));
}

#define WASM_TEST_ERROR_CODE *((unsigned int *)((1<<16) - 2*sizeof(unsigned int)))

#define WASM_TEST_HANDLER(CLASS, METHOD) \
  if( action == WASM_TEST_ACTION(#CLASS, #METHOD) ) { \
     WASM_TEST_ERROR_CODE = CLASS::METHOD(); \
     return; \
  }

WASM_TEST_HANDLER(test_message, require_notice);

```
* /mnt/hgfs/Workspaces/EOS/eos/contracts/test_api/test_api.hpp: 
```
struct test_message {

  static unsigned int read_message_normal();
  static unsigned int read_message_to_0();
  static unsigned int read_message_to_64k();
  static unsigned int require_notice();
  static unsigned int require_auth();
  static unsigned int assert_false();
  static unsigned int assert_true();
  static unsigned int now();

};
```
* /mnt/hgfs/Workspaces/EOS/eos/contracts/test_api/test_message.cpp
```
unsigned int test_message::require_notice() {
   if( current_code() == N(testapi) ) {
      eosio::require_notice( N(acc1) );
      eosio::require_notice( N(acc2) );
      eosio::require_notice( N(acc1), N(acc2) );
      return WASM_TEST_FAIL;
   } else if ( current_code() == N(acc1) || current_code() == N(acc2) ) {
      return WASM_TEST_PASS;
   }
   return WASM_TEST_FAIL;
}
```
* /mnt/hgfs/Workspaces/EOS/eos/libraries/chain/wasm_interface.cpp
```
/*
in /mnt/hgfs/Workspaces/EOS/eos/libraries/wasm-jit/Include/Runtime/Intrinsics.h 
*/

#define DEFINE_INTRINSIC_FUNCTION1(module,cName,name,returnType,arg0Type,arg0Name) \
	NativeTypes::returnType cName##returnType##arg0Type(NativeTypes::arg0Type); \
	static Intrinsics::Function cName##returnType##arg0Type##Function(#module "." #name,IR::FunctionType::get(IR::ResultType::returnType,{IR::ValueType::arg0Type}),(void*)&cName##returnType##arg0Type); \
	NativeTypes::returnType cName##returnType##arg0Type(NativeTypes::arg0Type arg0Name)

DEFINE_INTRINSIC_FUNCTION1(env,require_notice,require_notice,none,i64,account) {
   wasm_interface::get().current_apply_context->require_recipient( account );
}
```
Preprocessing the above, g++ -E require_notice.cpp:
```
NativeTypes::none require_noticenonei64(NativeTypes::i64);

static Intrinsics::Function require_noticenonei64Function(
   "env" "." "require_notice", //"env.require_notice"
   IR::FunctionType::get(
      IR::ResultType::none,
      {IR::ValueType::i64}),
   (void *)&require_noticenonei64
);

NativeTypes::none require_noticenonei64(NativeTypes::i64 account)
{
   wasm_interface::get().current_apply_context->require_recipient(account);
}
```



* /mnt/hgfs/Workspaces/EOS/eos/tests/api_tests/api_tests.cpp
```
BOOST_CHECK_MESSAGE( CALL_TEST_FUNCTION( TEST_METHOD("test_message", "require_notice"), {}, raw_bytes) == WASM_TEST_PASS, "test_message::require_notice()" );

```