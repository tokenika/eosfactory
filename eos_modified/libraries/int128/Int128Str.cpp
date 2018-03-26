#include <cstdlib>
#include <windows.h>
#include "include/int128/Int128.h"

#pragma once
#pragma warning(disable : 4073)
#pragma init_seg(lib)

const int_128  _I128_MIN( 0x8000000000000000, 0x0000000000000000);
const int_128  _I128_MAX( 0x7fffffffffffffff, 0xffffffffffffffff);
const uint_128 _UI128_MAX(0xffffffffffffffff, 0xffffffffffffffff);

// Conversion from int_128/uint_128 to string

// Number of digits that should be appended to the string for each loop.
// Also used as maximal number of digits to scan, that fits in 32 bit UINT
// digitCount[R] = floor(logR(_UI32_MAX+1))
// (index = radix = [2..36])
static const BYTE digitCount[37] = {
   0, 0,32,20,16,13,12,11
 ,10,10, 9, 9, 8, 8, 8, 8
 , 8, 7, 7, 7, 7, 7, 7, 7
 , 6, 6, 6, 6, 6, 6, 6, 6
 , 6, 6, 6, 6, 6
};

// Highest power of radix that fits in 32 bit (index = radix)
// For radix 2,4,8,16,32 special code is used which doesn't use this table.
// For all other values the element is used to get as many digits as possible
// by modulus and division. (powRadix[r] == pow(r,digitCount[r])
static const uint_128 powRadix[] = {
  0          //  not used
 ,0          //  not used
 ,0          //  not used
 ,0xcfd41b91 //  3486784401 =  3^20
 ,0          //  not used
 ,0x48c27395 //  1220703125 =  5^13
 ,0x81bf1000 //  2176782336 =  6^12
 ,0x75db9c97 //  1977326743 =  7^11
 ,0          //  not used
 ,0xcfd41b91 //  3486784401 =  9^10
 ,0x3b9aca00 //  1000000000 = 10^9
 ,0x8c8b6d2b //  2357947691 = 11^9
 ,0x19a10000 //   429981696 = 12^8
 ,0x309f1021 //   815730721 = 13^8
 ,0x57f6c100 //  1475789056 = 14^8
 ,0x98c29b81 //  2562890625 = 15^8
 ,0          //  not used
 ,0x18754571 //   410338673 = 17^7
 ,0x247dbc80 //   612220032 = 18^7
 ,0x3547667b //   893871739 = 19^7
 ,0x4c4b4000 //  1280000000 = 20^7
 ,0x6b5a6e1d //  1801088541 = 21^7
 ,0x94ace180 //  2494357888 = 22^7
 ,0xcaf18367 //  3404825447 = 23^7
 , 0xb640000 //   191102976 = 24^6
 , 0xe8d4a51 //   244140625 = 25^6
 ,0x1269ae40 //   308915776 = 26^6
 ,0x17179149 //   387420489 = 27^6
 ,0x1cb91000 //   481890304 = 28^6
 ,0x23744899 //   594823321 = 29^6
 ,0x2b73a840 //   729000000 = 30^6
 ,0x34e63b41 //   887503681 = 31^6
 ,0          //  not used
 ,0x4cfa3cc1 //  1291467969 = 33^6
 ,0x5c13d840 //  1544804416 = 34^6
 ,0x6d91b519 //  1838265625 = 35^6
 ,0x81bf1000 //  2176782336 = 36^6
};

#define ULTOSTR(v, str, radix)        \
{ if(sizeof(Ctype) == sizeof(char))   \
    _ultoa(v, (char*)str, radix);     \
  else                                \
    _ultow(v, (wchar_t*)str, radix);  \
}

#define STRLEN(str)      ((sizeof(Ctype)==sizeof(char))?strlen((char*)str):wcslen((wchar_t*)str))
#define STRCPY(dst, src) ((sizeof(Ctype)==sizeof(char))?(Ctype*)strcpy((char*)dst, (char*)src):(Ctype*)wcscpy((wchar_t*)dst, (wchar_t*)src))
#define STRREV(str)      ((sizeof(Ctype)==sizeof(char))?(Ctype*)_strrev((char*)str):(Ctype*)_wcsrev((wchar_t*)str))

template<class Int128Type, class Ctype> Ctype *int128toStr(Int128Type value, Ctype *str, UINT radix) {
  if((radix < 2) || (radix > 36)) {
    errno = EINVAL;
    str[0] = 0;
    return str;
  }
  errno = 0;
  bool setSign = false;
  if(value.isZero()) {
    str[0] = '0';
    str[1] = 0;
    return str;
  }

  Ctype *s = str;
  switch(radix) {
  case 2 :
  case 4 :
  case 16:
    { const UINT dc = digitCount[radix];
      for(int i = 3; i >= 0; i--) {
        if(value.s4.i[i]) {
          Ctype tmpStr[40];
          ULTOSTR(value.s4.i[i], tmpStr, radix);
          const size_t l = STRLEN(tmpStr);
          if(s != str) {
            for(size_t i = dc - l; i--;) *(s++) = '0'; // fill up with zeroes, if not leading digits
          }
          STRCPY(s, tmpStr);
          s += l;
        } else if(s != str) {
          for(size_t i = dc; i--;) *(s++) = '0'; // fill up with zeroes, if not leading digits
        }
      }
      *s = 0;
    }
    return str;
  case 8 : // Get 3 bits/digit giving 30 bits/loop, ie 10 digits/loop
  case 32: // Get 5 bits/digit giving 30 bits/loop too! which is 6 digits/loop
    { const UINT shft = (radix==32)?5:3;
      const UINT mask = (1 << shft) - 1;
      const UINT dpl  = 30 / shft;
      uint_128   v    = value;
      for(;;) {
        UINT v30 = v.s4.i[0] & ((1<<30) - 1);
        v >>= 30;
        UINT count;
        for(count = 0; v30; count++, v30 >>= shft) {
          *(s++) = radixLetter(v30 & mask);
        }
        if(v.isZero()) break;
        while(count++ < dpl) *(s++) = '0';
      }
    }
    break;
  case 10:
    if(value.isNegative()) {
      value = -value;
      setSign = true;
    }
    // NB continue case
  default:
    const UINT      dc      = digitCount[radix];
    const uint_128 &divisor = powRadix[radix];
    uint_128        v       = value;
    for(;;) {
      const UINT c = v % divisor;
      Ctype tmpStr[40];
      ULTOSTR(c, tmpStr, radix);
      STRCPY(s, STRREV(tmpStr));
      size_t l = STRLEN(tmpStr);
      s += l;
      v /= divisor;
      if(v) {
        while(l++ < dc) *(s++) = '0'; // append zeroes
      } else {
        break;
      }
    }
    if(setSign) *(s++) = '-';
    break;
  }
  *s = 0;
  return STRREV(str);
}

char *_i128toa(int_128 value, char *str, int radix) {
  return int128toStr<int_128, char>(value, str, radix);
}

wchar_t *_i128tow(int_128 value, wchar_t *str, int radix) {
  return int128toStr<int_128, wchar_t>(value, str, radix);
}

char*_ui128toa(uint_128 value, char *str, int radix) {
  return int128toStr<uint_128, char>(value, str, radix);
}

wchar_t *_ui128tow(uint_128 value, wchar_t *str, int radix) {
  return int128toStr<uint_128, wchar_t>(value, str, radix);
}

// Conversion from string to int_128/uint_128

static inline bool isRadixDigit(wchar_t ch, UINT radix, UINT &value) {
  if(!iswalnum(ch)) return false;
  const UINT v = iswdigit(ch) ? (ch - '0') : (ch - (iswupper(ch)?'A':'a') + 10);
  if(v >= radix) return false;
  value = v;
  return true;
}

template<class Int128Type> Int128Type maxValue() {
  return typeid(Int128Type) == typeid(int_128) ? (uint_128)_I128_MAX : (uint_128)_UI128_MAX;
}

template<class Int128Type, class Ctype, bool withSign> Int128Type strtoint128(const Ctype *s, Ctype **end, UINT radix) {
  if((s == NULL) || ((radix != 0) && ((radix < 2) || (radix > 36)))) {
    errno = EINVAL;
    return 0;
  }
  errno = 0;
  bool negative = false;
  bool gotDigit = false;
  while(iswspace(*s)) s++; // skip whitespace
  if(*s == '-') { // read optional sign
    s++;
    negative = true;
  } else if (*s == '+') {
    s++;
  }
  UINT digit;
  if(radix == 0) { // first determine if radix is 8,10 or 16
    if(*s == '0') {
      gotDigit = true;
      s++;
      if(end) *end = (Ctype*)s;
      if((*s == 'x') || (*s == 'X')) {
        radix = 16; s++;
      } else {
        radix = 8;
      }
      if(!isRadixDigit(*s, radix, digit)) { // we've scanned "0[x]",
        return 0;                           // if no more digits, then 0
      }
    } else if(iswdigit(*s)) {
      radix = 10;
    } else {
      return 0; // nothing recognized
    }
  }
  Int128Type result128;
  bool       overflow        = false;
  const UINT maxDigitCount32 = digitCount[radix];
  if(isRadixDigit(*(s++), radix, digit)) {
    gotDigit           = true;
    while((digit == 0) && isRadixDigit(*s, radix, digit)) s++; // skip leading zeroes
    bool firstChunk    = true;
    UINT result32      = digit;

    if((radix & -(int)radix) == radix) { // is radix 2,4,8,16 or 32
      const UINT maxBitCount   = withSign ? 127 : 128;
      UINT       totalBitCount;
      const UINT bitsPerDigit  = 32 / maxDigitCount32;
      const UINT maxBitCount32 = bitsPerDigit * maxDigitCount32;
      for(UINT bitCount32=bitsPerDigit;;result32=bitCount32=0) {
        while(isRadixDigit(*(s++), radix, digit)) {
          result32 <<= bitsPerDigit;
          result32 |= digit;
          if((bitCount32 += bitsPerDigit) == maxBitCount32) break;
        }
        if(firstChunk) {
          result128     = result32;
          firstChunk    = false;
          totalBitCount = bitCount32;
        } else if(bitCount32) {
          if((totalBitCount += bitCount32) > maxBitCount) {
            const BYTE mask = ~(((withSign&&!negative)?0x7f:0xff)>>(bitCount32&7));
            if(result128.s16.b[15-(bitCount32>>3)] & mask) {
              overflow = true;
              if(bitCount32 == maxBitCount32) {
                while(isRadixDigit(*(s++), radix, digit));
              }
              break;
            }
          }
          result128 <<= bitCount32;
          if(result32) result128 |= result32;
        } else {
          break;
        }
        if(bitCount32 < maxBitCount32) break;
      }
    } else {
      for(UINT digitCount32=1, p32=radix;; p32=1, result32=digitCount32=0) {
        while(isRadixDigit(*(s++), radix, digit)) {
          result32 *= radix;
          result32 += digit;
          p32      *= radix;
          if(++digitCount32 == maxDigitCount32) break;
        }
        if(firstChunk) {
          result128  = result32;
          firstChunk = false;
        } else if(digitCount32) {
          const UINT lastH = result128.s4.i[3];
          result128 *= p32;
          if(result32) result128 += result32;
          if(lastH && ((result128.s4.i[3]==0) || (withSign&&!negative&&result128.isNegative()))) {
            overflow = true;
            if(digitCount32 == maxDigitCount32) {
              while(isRadixDigit(*(s++), radix, digit));
            }
            break;
          }
        } else {
          break;
        }
        if(digitCount32 < maxDigitCount32) break;
      }
    }
  }
  if(!gotDigit) return 0;
  if(end) *end = (Ctype*)s-1;
  if(overflow) {
    errno = ERANGE;
    return withSign ? (negative ? (Int128Type)_I128_MIN : (Int128Type)_I128_MAX) : maxValue<Int128Type>();
  }
  return negative ? -result128 : result128;
}

int_128 _strtoi128(const char *str, char **end, int radix) {
  return strtoint128<int_128 ,char   ,true >(str, end, radix);
}

uint_128 _strtoui128(const char *str, char **end, int radix) {
  return strtoint128<uint_128,char   ,false>(str, end, radix);
}

int_128 _wcstoi128(const wchar_t *str, wchar_t **end, int radix) {
  return strtoint128<int_128 ,wchar_t,true >(str, end, radix);
}

uint_128 _wcstoui128(const wchar_t *str, wchar_t **end, int radix) {
  return strtoint128<uint_128,wchar_t,false>(str, end, radix);
}