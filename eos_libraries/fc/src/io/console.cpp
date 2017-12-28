#include <iostream>
#include <string>

namespace fc {

#ifdef _MSC_VER
#include <windows.h>

void set_console_echo( bool enable_echo )
{
   auto stdin_handle = GetStdHandle( STD_INPUT_HANDLE );
   DWORD mode = 0;
   GetConsoleMode( stdin_handle, &mode );
   if( enable_echo )
   {
      SetConsoleMode( stdin_handle, mode | ENABLE_ECHO_INPUT );
   }
   else
   {
      SetConsoleMode( stdin_handle, mode & (~ENABLE_ECHO_INPUT) );
   }
}

#else // NOT _MSC_VER
#include <termios.h>
#include <unistd.h>

void set_console_echo( bool enable_echo )
{
   termios oldt;
   tcgetattr(STDIN_FILENO, &oldt);
   termios newt = oldt;
   if( enable_echo )
   {
      newt.c_lflag |= ECHO;
   }
   else
   {
      newt.c_lflag &= ~ECHO;
   }
   tcsetattr(STDIN_FILENO, TCSANOW, &newt);
}

#endif // _MSC_VER

} // namespace fc
