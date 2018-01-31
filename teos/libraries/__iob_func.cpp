#ifdef _MSC_VER
#include <stdio.h>
#include <stdexcept>

static FILE arr[3];
extern "C" FILE*  __cdecl __iob_func(void) {
  throw std::runtime_error(
    "See https://stackoverflow.com/questions/30412951/unresolved-external-symbol-imp-fprintf-and-imp-iob-func-sdl2");
  return arr;
}
#endif // _MSC_VER 