#pragma once

#ifndef EMSCRIPTEN_API
/*
///bloclone:
	#define EMSCRIPTEN_API DLL_IMPORT
///blockone
*/
///tokenika:
	#define EMSCRIPTEN_API
///tokenika
#endif

#include <vector>

namespace IR { struct Module; }
namespace Runtime { struct ModuleInstance; }

namespace Emscripten
{
	EMSCRIPTEN_API void initInstance(const IR::Module& module,Runtime::ModuleInstance* moduleInstance);
	EMSCRIPTEN_API void injectCommandArgs(const std::vector<const char*>& argStrings,std::vector<Runtime::Value>& outInvokeArgs);
}