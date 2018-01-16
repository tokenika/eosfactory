#include <stdlib.h>
#include <string>
#include <iostream>

#include <teos_helper.hpp>

using namespace std;

int main()
{
  tokenika::teos::KeyPair keyPair;
  cout << "private key: " << keyPair.privateKey << endl;
  cout << "public key: " << keyPair.publicKey << endl;
}