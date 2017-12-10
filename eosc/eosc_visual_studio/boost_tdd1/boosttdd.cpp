#define BOOST_TEST_MODULE example
#include <boost/test/included/unit_test.hpp>

BOOST_AUTO_TEST_CASE(free_test_function)
/* Compare with void free_test_function() */
{
  BOOST_TEST(true /* test assertion */);
  BOOST_TEST(false /* test assertion */);
}





