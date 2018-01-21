#include <eos/types/types.hpp>
#include <eos/types/public_key.hpp>
#include <fc/crypto/base58.hpp>

#include <fc/io/raw.hpp>
#include <fc/crypto/hmac.hpp>
#include <fc/crypto/openssl.hpp>
#include <fc/crypto/ripemd160.hpp>

#include <eos/utilities/key_conversion.hpp>
#include <fc/crypto/base58.hpp>
#include <fc/variant.hpp>

#include <teos_helper.hpp>

#ifdef _MSC_VER
static FILE arr[3];
extern "C" FILE*  __cdecl __iob_func(void) {
	throw std::runtime_error(
		"See https://stackoverflow.com/questions/30412951/unresolved-external-symbol-imp-fprintf-and-imp-iob-func-sdl2");
	return arr;
}
#endif // _MSC_VER 

using namespace std;

namespace tokenika {
  namespace teos {

    KeyPair::KeyPair() {
      fc::ecc::private_key pk = fc::ecc::private_key::generate();
      publicKey = string(eosio::types::public_key(pk.get_public_key()));
      privateKey = eosio::utilities::key_to_wif(pk.get_secret());
    }

    string KeyPair::privateK() {
      KeyPair kp;
      return kp.privateKey;
    }
    
    string KeyPair::prk = KeyPair::privateK();
  }
}