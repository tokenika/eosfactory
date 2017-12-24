#ifdef _MSC_VER
#include <boost/config/compiler/visualc.hpp>
#endif
#include <boost/property_tree/ptree.hpp>
#include <boost/property_tree/json_parser.hpp>
#include <boost/foreach.hpp>
#include <cassert>
#include <exception>
#include <iostream>
#include <sstream>
#include <string>

#define NSON "NSON"

int main1()
{
  try
  {
    std::stringstream ss;
    ss << "[\"NSON *\", \"cartman_wallet *\", \"eos_is_scheise_wallet *\", \"hacker_wallet *\", \"szymon_wallet *\" ]";

    boost::property_tree::ptree pt;
    boost::property_tree::read_json(ss, pt);


    std::stringstream ss1;
    boost::property_tree::json_parser::write_json(ss1, pt, true);
    std::cout << ss1.str();

    BOOST_FOREACH(boost::property_tree::ptree::value_type &v, pt)
    {
      assert(v.first.empty()); // array elements have no names
      std::cout << v.second.data() << std::endl;
    }
    return EXIT_SUCCESS;
  }
  catch (std::exception const& e)
  {
    std::cerr << e.what() << std::endl;
  }
  return EXIT_FAILURE;

}