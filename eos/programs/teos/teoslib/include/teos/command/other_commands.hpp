#pragma once

#include <teoslib/config.h>
#include <teos/command/command.hpp>

namespace teos
{
  namespace command
  {
    class VersionClient : public TeosCommand
    {
    public:

      VersionClient(ptree reqJson) : TeosCommand(
        "", reqJson) {
        stringstream ss;
        ss << PROJECT_NAME << " " <<VERSION_MAJOR << "." << VERSION_MINOR;
        respJson_.put("version", ss.str());
      }
    };

    class VersionClientOptions : public CommandOptions
    {
    public:
      VersionClientOptions(int argc, const char **argv)
        : CommandOptions(argc, argv) {}

    protected:
      const char* getUsage() {
        return R"EOF(
Retrieve version information of the client
Usage: ./teos version client [Options]
Usage: ./teos version client [-j '{}'] [OPTIONS]
)EOF";
      }

      bool setJson(variables_map &vm) {
        return true;
      }

      TeosCommand getCommand() {
        return VersionClient(reqJson);
      }

      void getOutput(TeosCommand command) {
        output("Version", "%s", GET_STRING(command, "version"));
      }

    };

  }
}