#ifdef _MSC_VER
#include <stdio.h>

static FILE arr[3];
extern "C" FILE*  __cdecl __iob_func(void) {
  return arr;
}
#endif // _MSC_VER 