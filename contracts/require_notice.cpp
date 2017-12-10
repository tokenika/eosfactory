
#define DEFINE_INTRINSIC_FUNCTION1(module, cName, name, returnType, arg0Type, arg0Name)                                                                                                                      \
   NativeTypes::returnType cName##returnType##arg0Type(NativeTypes::arg0Type);                                                                                                                               \
   static Intrinsics::Function cName##returnType##arg0Type##Function(#module "." #name, IR::FunctionType::get(IR::ResultType::returnType, {IR::ValueType::arg0Type}), (void *)&cName##returnType##arg0Type); \
   NativeTypes::returnType cName##returnType##arg0Type(NativeTypes::arg0Type arg0Name)


DEFINE_INTRINSIC_FUNCTION1(env, require_notice, require_notice, none, i64, account)
{
   wasm_interface::get().current_apply_context->require_recipient(account);
}

/*
Pentagon/contracts$ g++ -E test.cpp
*/
NativeTypes::none require_noticenonei64(NativeTypes::i64);
static Intrinsics::Function require_noticenonei64Function(
      "env" "." "require_notice",
      IR::FunctionType::get(
         IR::ResultType::none,
         {IR::ValueType::i64}),
      (void *)&require_noticenonei64);
NativeTypes::none require_noticenonei64(NativeTypes::i64 account)
{
   wasm_interface::get().current_apply_context->require_recipient(account);
}
