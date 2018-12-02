#pragma once

#ifdef DEBUG 

#define __FILENAME__ (strrchr(__FILE__, '/') ? strrchr(__FILE__, '/') + 1 : __FILE__)
#define logger_info(...) \
  { \
    print("INFO ", __VA_ARGS__, " @ "); \
    int time = now(); \
    int hour = (time/3600)%24; \
    time = time%3600; \
    int min = time/60; \
    time = time%60; \
    int sec = time; \
    print(hour, ":", min, ":", sec); \
    print(" ", __FILENAME__, "[", __LINE__, "]", "(", __FUNCTION__, ")\n"); \
  }

#else

#define logger_info(...){}

#endif
