#pragma once

#include "../eosc_config.h"
#include "eosc_command.hpp"

namespace tokenika
{
  namespace eosc
  {
    class VersionClient : public EoscCommand
    {
    public:

      VersionClient(ptree reqJson, bool raw = false) : EoscCommand(
        "", reqJson, raw) {
        stringstream ss;
        ss << PROJECT_NAME << " " <<VERSION_MAJOR << "." << VERSION_MINOR;
        respJson.put("version", ss.str());
      }
    };

    class VersionClientOptions : public CommandOptions
    {
    public:
      VersionClientOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
#ifdef WIN32
        return R"EOF(
Retrieve version information of the client
Usage: ./eosc version client [Options]
Usage: ./eosc version client [-j "{}"] [OPTIONS]
)EOF";
#else
        return R"EOF(
Retrieve version information of the client
Usage: ./eosc version client [Options]
Usage: ./eosc version client [-j '{}'] [OPTIONS]
)EOF";
#endif
      }

      bool setJson(variables_map &vm) {
        return true;
      }

      EoscCommand getCommand(bool is_raw) {
        return VersionClient(reqJson, is_raw);
      }

      void getOutput(EoscCommand command) {
        output("Version", "%s", GET_STRING(command, "version"));
      }

      void getExample() {
        cout << R"EOF(
boost::property_tree::ptree reqJson;
VersionClient versionClient(reqJson);
cout << versionClient.toStringRcv() << endl;
)EOF" << endl;

        boost::property_tree::ptree reqJson;
        VersionClient versionClient(reqJson);
        cout << versionClient.toStringRcv() << endl;
      }
    };

  }
}