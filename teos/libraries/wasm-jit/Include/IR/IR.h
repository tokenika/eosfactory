#pragma once

#include "Platform/Platform.h"

#ifndef IR_API
/*
///blockone:
	#define IR_API DLL_IMPORT
///blockone
*/
///tokenika:
  #define IR_API
///tokenika
#endif

namespace IR
{
	enum { maxMemoryPages = (Uptr)65536 };
	enum { numBytesPerPage = (Uptr)65536 };
	enum { numBytesPerPageLog2 = (Uptr)16 };

	enum { requireSharedFlagForAtomicOperators = false };
}
