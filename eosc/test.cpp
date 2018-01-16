#include <stdlib.h>
#include <string>
#include <iostream>

#include <eosc_helper.hpp>

using namespace std;

int main()
{
  tokenika::eosc::KeyPair keyPair;
  cout << "private key: " << keyPair.privateKey << endl;
  cout << "public key: " << keyPair.publicKey << endl;
}