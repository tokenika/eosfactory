#pragma once

#ifdef DEBUG 

void print_time()
{
  int time = now();
  int hour = (time/3600)%24;
  time = time%3600;
  int min = time/60;
  time = time%60;
  int sec = time;
  eosio::print(hour, ":", min, ":", sec);
}

#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)
#define logger_info(...) \
  { \
    print("INFO "); \
    print(__VA_ARGS__, " \n\t "); \
    print_time(); \
    print(" ", __FILENAME__, "[", __LINE__, "]", "(", __FUNCTION__, ")\n"); \
  }

#else

#define logger_info(...){}

#endif