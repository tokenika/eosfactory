#pragma once

#ifndef WEBASSEMBLY_API
/*
///blockone:
	#define WEBASSEMBLY_API DLL_IMPORT
///blockone
*/
///tokenika:
#define WEBASSEMBLY_API
///tokenika
#endif

#include "Inline/BasicTypes.h"

namespace IR { struct Module; struct DisassemblyNames; }
namespace Serialization { struct InputStream; struct OutputStream; }

namespace WASM
{
   WEBASSEMBLY_API void serialize(Serialization::InputStream& stream,IR::Module& module);
   WEBASSEMBLY_API void serializeWithInjection(Serialization::InputStream& stream,IR::Module& module);
   WEBASSEMBLY_API void serialize(Serialization::OutputStream& stream,const IR::Module& module);
}
