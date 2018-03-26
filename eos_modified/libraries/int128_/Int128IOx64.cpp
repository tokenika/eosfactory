// File:Int128IOx64.cpp
//#include "pch.h"

#ifdef _M_X64

#include <cassert>
#include <string.h>
#include <wchar.h>
#include <ctype.h>
#include <stdexcept>
#include "include/int128/Int128.h"

using namespace std;

static const _int128 _0(0);
static const _int128 _10(10);
static const _int128 _16(16);
static const _int128 _8(16);

char *_i128toa(_int128 value, char *str, int radix) {
  assert(radix >= 2 && radix <= 36);
  char *s = str;
  const bool negative = value < _0;
  if (negative && (radix == 10)) {
    value = -value;
    while (value != _0) {
      const unsigned int c = value % _10;
      *(s++) = radixLetter(c);
      value /= _10;
    }
    *(s++) = '-';
    *s = 0;
    return _strrev(str);
  }

  _uint128 v(value);
  const _uint128 r(radix);
  while (v != _0) {
    const unsigned int c = v % r;
    *(s++) = radixLetter(c);
    v /= r;
  }
  if (s == str) {
     strcpy_s(str, sizeof str, "0");
     return str;
  }
  else {
    *s = 0;
    return _strrev(str);
  }
  return str;
}

wchar_t *_i128tow(_int128 value, wchar_t *str, int radix) {
  wchar_t *s = str;
  const bool negative = value < _0;
  if (negative && (radix == 10)) {
    value = -value;
    while (value != _0) {
      const unsigned int c = value % _10;
      *(s++) = wradixLetter(c);
      value /= _10;
    }
    *(s++) = '-';
    *s = 0;
    return _wcsrev(str);
  }

  _uint128 v(value);
  const _uint128 r(radix);
  while (v != _0) {
    const unsigned int c = v % r;
    *(s++) = radixLetter(c);
    v /= r;
  }
  if (s == str) {
    wcscpy_s(str, sizeof str, L"0");
    return str;
  }
  else {
    *s = 0;
    return _wcsrev(str);
  }
  return str;
}

const char *_int128::parseDec(const char *str) { // return pointer to char following the number
  bool negative = false;
  bool gotDigit = false;
  switch (*str) {
  case '+':
    str++;
    break;
  case '-':
    str++;
    negative = true;
  }
  *this = _0;
  while (isdigit(*str)) {
    gotDigit = true;
    const unsigned int d = *(str++) - '0';
    *this *= _10;
    *this += d;
  }
  if (!gotDigit) {
    throw "_int128:string is not a number";
  }
  if (negative) {
    *this = -*this;
  }
  return str;
}

const char *_int128::parseHex(const char *str) {
  *this = 0;
  while (isxdigit(*str)) {
    const unsigned int d = convertNumberChar(*(str++));
    *this *= _16;
    *this += d;
  }
  return str;
}

const char *_int128::parseOct(const char *str) {
  *this = 0;
  while (isodigit(*str)) {
    const unsigned int d = convertNumberChar(*(str++));
    *this *= _8;
    *this += d;
  }
  return str;
}

_int128::_int128(const char *str) {
  if (*str == '-') {
    parseDec(str);
  }
  else {
    if (!isdigit(*str)) {
      throw exception("_int128:string is not an integer");
    }
    if (*str == '0') {
      switch (str[1]) {
      case 'x':
        parseHex(str + 2);
        break;
      case 0:
        *this = 0;
        break;
      default:
        parseOct(str + 1);
      }
    }
    else {
      parseDec(str);
    }
  }
}
#endif // _M_X64

