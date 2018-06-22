/**
 * @file build_contract.hpp
 * @copyright defined in LICENSE.txt
 * @author Tokenika
 * @date 30 May 2018
*/

/**
 * @defgroup teoslib_raw Raw function classes
 */

using namespace std;

namespace teos {
  namespace control {

    class Cleos : public TeosControl
    {
      public:
        Cleos(
        vector<string> args, string first, string second,
        bool isVerbose = 1, 
        pair<string, string> okSubstring("", "") );
    }

  }
}