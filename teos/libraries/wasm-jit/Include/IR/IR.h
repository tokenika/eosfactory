#pragma once

#include "Platform/Platform.h"

#ifndef IR_API
/*
<BlockOne>
	#define IR_API DLL_IMPORT
</BlockOne>
*/
//<Tokenika>
  #define IR_API
//</Tokenika>
#endif

namespace IR
{
	enum { maxMemoryPages = (Uptr)65536 };
	enum { numBytesPerPage = (Uptr)65536 };
	enum { numBytesPerPageLog2 = (Uptr)16 };

	enum { requireSharedFlagForAtomicOperators = false };
}
