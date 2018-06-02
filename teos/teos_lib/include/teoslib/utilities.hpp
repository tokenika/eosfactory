#pragma once

#include <stdlib.h>
#include <string>
#include <boost/property_tree/ptree.hpp>
#include <boost/date_time/posix_time/posix_time.hpp>

using namespace std;
using namespace boost::property_tree;

const string DARWIN = "Darwin";

namespace teos {

    /**
     * @brief Converts EOS time string to 'boost::posix_time'.
     *
     * EOS time is a string, for example `2017-07-18T20:16:36`. For processing,
     * it is converted to the boost `ptime`.
     *
     * @param str EOS time string.
     * @return boost::posix_time::ptime
     */
    extern boost::posix_time::ptime strToTime(const string str);

    /**
     * @brief Given a json tteosCommandJsonree, returns the <Type>value of a given path.
     *
     * @tparam Type type of the called value
     * @param json json tree
     * @param path path of the given tree
     * @return Type
     */
    template<typename Type>
    Type getJsonPath(ptree json,
      const ptree::path_type & path);

    /**
     * @brief Given a text json tree, returns the equivalent `boost ptree`.
     *
     * @param json
     * @return boost::property_tree::ptree
     */
    extern ptree stringToPtree(
      string json);
      
    extern void boostProcessSystem(string commandLine);

    extern string wslMapWindowsLinux(string path);

    extern string wslMapLinuxWindows(string path);

    extern string uname(string options = "-s");

    extern bool isWindowsUbuntu();

}