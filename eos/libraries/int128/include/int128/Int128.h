// from https://github.com/JesperMikkelsen/Big-Numbers/blob/master/Lib/Include/Math/Int128.h

#pragma once

//#include "StrStream.h"
//#include "PragmaLib.h"
//#include "Random.h"
//#include "MyUtil.h"
#include <iostream>

typedef struct {
  unsigned __int64 i[2];
} _S2;

typedef struct {
  unsigned int i[4];
} _S4;

typedef struct {
  unsigned short s[8];
} _S8;

typedef struct {
  unsigned char b[16];
} _S16;

#define HI64(n) (n).s2.i[1]
#define LO64(n) (n).s2.i[0]

extern "C" {
  void int128add( void *dst, const void *x);
  void int128sub( void *dst, const void *x);
  void int128mul( void *dst, const void *x);
  void int128div( void *dst, void *x);
  void int128rem( void *dst, void *x);
  void int128neg( void *x);
  void int128inc( void *x);
  void int128dec( void *x);
  void int128shr( void *x, int shft);
  void int128shl( void *x, int shft);
  int  int128cmp( const void *x1, const void *x2);
  void uint128div(void *dst, const void *x);
  void uint128rem(void *dst, const void *x);
  void uint128shr(void *x, int shft);
  int  uint128cmp(const void *x1, const void *x2);
};

class _int128 {
public:
  union {
    _S2  s2;
    _S4  s4;
    _S8  s8;
    _S16 s16;
  };

  // constructors
  inline _int128() {}
  inline _int128(const unsigned __int64 &n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _int128(const __int64 &n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _int128(unsigned long n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _int128(long n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _int128(unsigned int n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _int128(int n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _int128(unsigned short n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _int128(short n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  explicit inline _int128(const unsigned __int64 &hi, const unsigned __int64 &lo) {
    HI64(*this) = hi;
    LO64(*this) = lo;
  }

  // type operators
  operator unsigned __int64() const {
    return LO64(*this);
  }
  operator __int64() const {
    return LO64(*this);
  }
  operator unsigned long() const {
    return (unsigned long)LO64(*this);
  }
  operator long() const {
    return (long)LO64(*this);
  }
  operator unsigned int() const {
    return (unsigned int)LO64(*this);
  }
  operator int() const {
    return (int)LO64(*this);
  }
  inline operator bool() const {
    return LO64(*this) || HI64(*this);
  }

  // assign operators
  inline _int128 &operator++() {   // prefix-form
    int128inc(this);
    return *this;
  }
  inline _int128 &operator--() {   // prefix-form
    int128dec(this);
    return *this;
  }

  inline _int128 operator++(int) { // postfix-form
    const _int128 result(*this);
    int128inc(this);
    return result;
  }
  inline _int128 operator--(int) { // postfix-form
    const _int128 result(*this);
    int128dec(this);
    return result;
  }

  inline bool isNegative() const {
    return ((int)s4.i[3] < 0);
  }
  inline bool isZero() const {
    return LO64(*this) == 0 && HI64(*this) == 0;
  }
};

class _uint128 {
public:
  union {
    _S2  s2;
    _S4  s4;
    _S8  s8;
    _S16 s16;
  };

  // constructors
  inline _uint128() {}

  inline _uint128(const _int128 &n) {
    HI64(*this) = HI64(n);
    LO64(*this) = LO64(n);
  }
  inline _uint128(const unsigned __int64 &n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _uint128(const __int64 &n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _uint128(unsigned long n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _uint128(long n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _uint128(unsigned int n) {
    HI64(*this) = 0;
    LO64(*this) = n;
  }
  inline _uint128(int n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _uint128(unsigned short n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _uint128(short n) {
    HI64(*this) = n < 0 ? -1 : 0;
    LO64(*this) = n;
  }
  inline _uint128(const unsigned __int64 &hi, const unsigned __int64 &lo) {
    HI64(*this) = hi;
    LO64(*this) = lo;
  }

  // type operators
  inline operator _int128() const {
    return *(_int128*)(void*)this;
  }
  inline operator unsigned __int64() const {
    return LO64(*this);
  }
  inline operator __int64() const {
    return LO64(*this);
  }
  inline operator unsigned long() const {
    return (unsigned long)LO64(*this);
  }
  inline operator long() const {
    return (long)LO64(*this);
  }
  inline operator unsigned int() const {
    return (unsigned int)LO64(*this);
  }
  inline operator int() const {
    return (int)LO64(*this);
  }
  inline operator bool() const {
    return LO64(*this) || HI64(*this);
  }

  inline _uint128 &operator++() {   // prefix-form
    int128inc(this);
    return *this;
  }
  inline _uint128 &operator--() {   // prefix-form
    int128dec(this);
    return *this;
  }

  inline _uint128 operator++(int) { // postfix-form
    const _uint128 result(*this);
    int128inc(this);
    return result;
  }
  inline _uint128 operator--(int) { // postfix-form
    const _uint128 result(*this);
    int128dec(this);
    return result;
  }

  inline bool isNegative() const {
    return false;
  }
  inline bool isZero() const {
    return LO64(*this) == 0 && HI64(*this) == 0;
  }
};

// 4 version of all 5 binary arithmetic operators,
// 3 binary logical operators and 6 compare-operators
//    signed   op signed
//    signed   op unsigned
//    unsigned op signed
//    unsigned op unsigned
//  For +,-,*,&,|,^,==,!= the called function is the same
//  regardless of signed/unsigned combinations.
//  For /,%,<,>,<=,>= however the signed function is used
//  only for the "signed op signed" combination.
//  For left shift (<<) there is no difference for
//  signed and unsigned function, but for right shift (>>)
//  the leftmost bit (bit 127) indicates the sign, and will
//  be copied to all new bits comming in from left for _int128
//  and 0-bits will be shifted in for _uint128 (because there
//  is no sign).
//  For assign-operators (+=,-=...) the same rules apply.
//  Vesions for built in integral types are then defined
//  on top of these

// 4 basic combination of operator+ (128-bit integers - dont care about signed/unsigned)
inline _int128 operator+(const _int128 &lft, const _int128 &rhs) {
  _int128 result(lft);
  int128add(&result, &rhs);
  return result;
}
inline _int128 operator+(const _int128 &lft, const _uint128 &rhs) {
  _int128 result(lft);
  int128add(&result, &rhs);
  return result;
}
inline _uint128 operator+(const _uint128 &lft, const _int128 &rhs) {
  _uint128 result(lft);
  int128add(&result, &rhs);
  return result;
}
inline _uint128 operator+(const _uint128 &lft, const _uint128 &rhs) {
  _uint128 result(lft);
  int128add(&result, &rhs);
  return result;
}

// 4 basic combination of operator- (128-bit integers - dont care about signed/unsigned)
inline _int128 operator-(const _int128 &lft, const _int128 &rhs) {
  _int128 result(lft);
  int128sub(&result, &rhs);
  return result;
}
inline _int128 operator-(const _int128 &lft, const _uint128 &rhs) {
  _int128 result(lft);
  int128sub(&result, &rhs);
  return result;
}
inline _uint128 operator-(const _uint128 &lft, const _int128 &rhs) {
  _uint128 result(lft);
  int128sub(&result, &rhs);
  return result;
}
inline _uint128 operator-(const _uint128 &lft, const _uint128 &rhs) {
  _uint128 result(lft);
  int128sub(&result, &rhs);
  return result;
}

// 4 basic combination of operator* (128-bit integers - dont care about signed/unsigned)
inline _int128 operator*(const _int128 &lft, const _int128 &rhs) {
  _int128 result(lft);
  int128mul(&result, &rhs);
  return result;
}
inline _int128 operator*(const _int128 &lft, const _uint128 &rhs) {
  _int128 result(lft);
  int128mul(&result, &rhs);
  return result;
}
inline _uint128 operator*(const _uint128 &lft, const _int128 &rhs) {
  _uint128 result(lft);
  int128mul(&result, &rhs);
  return result;
}
inline _uint128 operator*(const _uint128 &lft, const _uint128 &rhs) {
  _uint128 result(lft);
  int128mul(&result, &rhs);
  return result;
}

// 4 basic combination of operator/ - signed division only if both are signed
inline _int128 operator/(const _int128 &lft, const _int128 &rhs) {
  _int128 result(lft), tmp(rhs);
  int128div(&result, &tmp);
  return result;
}
inline _int128 operator/(const _int128 &lft, const _uint128 &rhs) {
  _int128 result(lft);
  uint128div(&result, &rhs);
  return result;
}
inline _uint128 operator/(const _uint128 &lft, const _int128 &rhs) {
  _uint128 result(lft);
  uint128div(&result, &rhs);
  return result;
}
inline _uint128 operator/(const _uint128 &lft, const _uint128 &rhs) {
  _uint128 result(lft);
  uint128div(&result, &rhs);
  return result;
}

// 4 basic combination of operator% - signed % only if both are signed
inline _int128 operator%(const _int128 &lft, const _int128 &rhs) {
  _int128 result(lft), tmp(rhs);
  int128rem(&result, &tmp);
  return result;
}
inline _int128 operator%(const _int128 &lft, const _uint128 &rhs) {
  _int128 result(lft);
  uint128rem(&result, &rhs);
  return result;
}
inline _uint128 operator%(const _uint128 &lft, const _int128 &rhs) {
  _uint128 result(lft);
  uint128rem(&result, &rhs);
  return result;
}
inline _uint128 operator%(const _uint128 &lft, const _uint128 &rhs) {
  _uint128 result(lft);
  uint128rem(&result, &rhs);
  return result;
}

// 2 version of unary - (dont care about signed/unsigned)
inline _int128 operator-(const _int128 &x) { // unary minus
  _int128 result(x);
  int128neg(&result);
  return result;
}
inline _uint128 operator-(const _uint128 &x) {
  _uint128 result(x);
  int128neg(&result);
  return result;
}

// Basic bit operators
// 4 basic combinations of operator&
inline _int128 operator&(const _int128 &lft, const _int128 &rhs) {
  return _int128(HI64(lft) & HI64(rhs), LO64(lft) & LO64(rhs));
}
inline _int128 operator&(const _int128 &lft, const _uint128 &rhs) {
  return _int128(HI64(lft) & HI64(rhs), LO64(lft) & LO64(rhs));
}
inline _uint128 operator&(const _uint128 &lft, const _int128 &rhs) {
  return _uint128(HI64(lft) & HI64(rhs), LO64(lft) & LO64(rhs));
}
inline _uint128 operator&(const _uint128 &lft, const _uint128 &rhs) {
  return _int128(HI64(lft) & HI64(rhs), LO64(lft) & LO64(rhs));
}

// 4 basic combinations of operator|
inline _int128 operator|(const _int128 &lft, const _int128 &rhs) {
  return _int128(HI64(lft) | HI64(rhs), LO64(lft) | LO64(rhs));
}
inline _int128 operator|(const _int128 &lft, const _uint128 &rhs) {
  return _int128(HI64(lft) | HI64(rhs), LO64(lft) | LO64(rhs));
}
inline _uint128 operator|(const _uint128 &lft, const _int128 &rhs) {
  return _uint128(HI64(lft) | HI64(rhs), LO64(lft) | LO64(rhs));
}
inline _uint128 operator|(const _uint128 &lft, const _uint128 &rhs) {
  return _uint128(HI64(lft) | HI64(rhs), LO64(lft) | LO64(rhs));
}

// 4 basic combinations of operator^
inline _int128 operator^(const _int128 &lft, const _int128 &rhs) {
  return _int128(HI64(lft) ^ HI64(rhs), LO64(lft) ^ LO64(rhs));
}
inline _int128 operator^(const _int128 &lft, const _uint128 &rhs) {
  return _int128(HI64(lft) ^ HI64(rhs), LO64(lft) ^ LO64(rhs));
}
inline _uint128 operator^(const _uint128 &lft, const _int128 &rhs) {
  return _uint128(HI64(lft) ^ HI64(rhs), LO64(lft) ^ LO64(rhs));
}
inline _uint128 operator^(const _uint128 &lft, const _uint128 &rhs) {
  return _uint128(HI64(lft) ^ HI64(rhs), LO64(lft) ^ LO64(rhs));
}

// 2 versions of operator~
inline _int128 operator~(const _int128 &n) {
  return _int128(~HI64(n), ~LO64(n));
}
inline _uint128 operator~(const _uint128 &n) {
  return _uint128(~HI64(n), ~LO64(n));
}

// 2 version of operator>> (arithmetic shift for signed, logical shift for unsigned)
inline _int128 operator>>(const _int128 &lft, const int shft) {
  _int128 copy(lft);
  int128shr(&copy, shft);
  return copy;
}
inline _uint128 operator>>(const _uint128 &lft, const int shft) {
  _uint128 copy(lft);
  uint128shr(&copy, shft);
  return copy;
}

// 2 version of operator<< (dont care about signed/unsigned)
inline _int128 operator<<(const _int128 &lft, const int shft) {
  _int128 copy(lft);
  int128shl(&copy, shft);
  return copy;
}
inline _int128 operator<<(const _uint128 &lft, const int shft) {
  _uint128 copy(lft);
  int128shl(&copy, shft);
  return copy;
}


// 4 basic combinations of operator==. (dont care about signed/unsigned)
inline bool operator==(const _int128 &lft, const _int128 &rhs) {
  return (LO64(lft) == LO64(rhs)) && (HI64(lft) == HI64(rhs));
}
inline bool operator==(const _int128 &lft, const _uint128 &rhs) {
  return (LO64(lft) == LO64(rhs)) && (HI64(lft) == HI64(rhs));
}
inline bool operator==(const _uint128 &lft, const _int128 &rhs) {
  return (LO64(lft) == LO64(rhs)) && (HI64(lft) == HI64(rhs));
}
inline bool operator==(const _uint128 &lft, const _uint128 &rhs) {
  return (LO64(lft) == LO64(rhs)) && (HI64(lft) == HI64(rhs));
}

// 4 basic combinations of operator!= (dont care about signed/unsigned)
inline bool operator!=(const _int128 &lft, const _int128 &rhs) {
  return (LO64(lft) != LO64(rhs)) || (HI64(lft) != HI64(rhs));
}
inline bool operator!=(const _int128 &lft, const _uint128 &rhs) {
  return (LO64(lft) != LO64(rhs)) || (HI64(lft) != HI64(rhs));
}
inline bool operator!=(const _uint128 &lft, const _int128 &rhs) {
  return (LO64(lft) != LO64(rhs)) || (HI64(lft) != HI64(rhs));
}
inline bool operator!=(const _uint128 &lft, const _uint128 &rhs) {
  return (LO64(lft) != LO64(rhs)) || (HI64(lft) != HI64(rhs));
}

// 4 basic combinations of operator> (signed compare only if both are signed)
inline bool operator>(const _int128 &lft, const _int128 &rhs) {
  return int128cmp(&lft, &rhs) > 0;
}
inline bool operator>(const _int128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) > 0;
}
inline bool operator>(const _uint128 &lft, const _int128 &rhs) {
  return uint128cmp(&lft, &rhs) > 0;
}
inline bool operator>(const _uint128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) > 0;
}

// 4 basic combinations of operator>= (signed compare only if both are signed)
inline bool operator>=(const _int128 &lft, const _int128 &rhs) {
  return int128cmp(&lft, &rhs) >= 0;
}
inline bool operator>=(const _int128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) >= 0;
}
inline bool operator>=(const _uint128 &lft, const _int128 &rhs) {
  return uint128cmp(&lft, &rhs) >= 0;
}
inline bool operator>=(const _uint128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) >= 0;
}

// 4 basic combinations of operator< (signed compare only if both are signed)
inline bool operator<(const _int128 &lft, const _int128 &rhs) {
  return int128cmp(&lft, &rhs) < 0;
}
inline bool operator<(const _int128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) < 0;
}
inline bool operator<(const _uint128 &lft, const _int128 &rhs) {
  return uint128cmp(&lft, &rhs) < 0;
}
inline bool operator<(const _uint128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) < 0;
}

// 4 basic combinations of operator<= (signed compare only if both are signed)
inline bool operator<=(const _int128 &lft, const _int128 &rhs) {
  return int128cmp(&lft, &rhs) <= 0;
}
inline bool operator<=(const _int128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) <= 0;
}
inline bool operator<=(const _uint128 &lft, const _int128 &rhs) {
  return uint128cmp(&lft, &rhs) <= 0;
}
inline bool operator<=(const _uint128 &lft, const _uint128 &rhs) {
  return uint128cmp(&lft, &rhs) <= 0;
}

// Assign operators
// operator+= (dont care about sign)
inline _int128 &operator+=(_int128 &lft, const _int128 &rhs) {
  int128add(&lft, &rhs);
  return lft;
}
inline _int128 &operator+=(_int128 &lft, const _uint128 &rhs) {
  int128add(&lft, &rhs);
  return lft;
}
inline _uint128 &operator+=(_uint128 &lft, const _int128 &rhs) {
  int128add(&lft, &rhs);
  return lft;
}
inline _uint128 &operator+=(_uint128 &x, const _uint128 &rhs) {
  int128add(&x, &rhs);
  return x;
}

// operator-= (dont care about sign)
inline _int128 &operator-=(_int128 &lft, const _int128 &rhs) {
  int128sub(&lft, &rhs);
  return lft;
}
inline _int128 &operator-=(_int128 &lft, const _uint128 &rhs) {
  int128sub(&lft, &rhs);
  return lft;
}
inline _uint128 &operator-=(_uint128 &lft, const _int128 &rhs) {
  int128sub(&lft, &rhs);
  return lft;
}
inline _uint128 &operator-=(_uint128 &lft, const _uint128 &rhs) {
  int128sub(&lft, &rhs);
  return lft;
}

// operator*= (dont care about sign)
inline _int128 &operator*=(_int128 &lft, const _int128 &rhs) {
  int128mul(&lft, &rhs);
  return lft;
}
inline _int128 &operator*=(_int128 &lft, const _uint128 &rhs) {
  int128mul(&lft, &rhs);
  return lft;
}
inline _uint128 &operator*=(_uint128 &lft, const _int128 &rhs) {
  int128mul(&lft, &rhs);
  return lft;
}
inline _uint128 &operator*=(_uint128 &lft, const _uint128 &rhs) {
  int128mul(&lft, &rhs);
  return lft;
}

// operator/= (use signed div only if both are signed)
inline _int128 &operator/=(_int128 &lft, const _int128 &rhs) {
  _int128 tmp(rhs);
  int128div(&lft, &tmp);
  return lft;
}
inline _int128 &operator/=(_int128 &lft, const _uint128 &rhs) {
  uint128div(&lft, &rhs);
  return lft;
}
inline _uint128 &operator/=(_uint128 &lft, const _int128 &rhs) {
  uint128div(&lft, &rhs);
  return lft;
}
inline _uint128 &operator/=(_uint128 &lft, const _uint128 &rhs) {
  uint128div(&lft, &rhs);
  return lft;
}

// operator%= (use signed % only if both are signed)
inline _int128 &operator%=(_int128 &lft, const _int128 &rhs) {
  _int128 tmp(rhs);
  int128rem(&lft, &tmp);
  return lft;
}
inline _int128 &operator%=(_int128 &lft, const _uint128 &rhs) {
  uint128rem(&lft, &rhs);
  return lft;
}
inline _uint128 &operator%=(_uint128 &lft, const _int128 &rhs) {
  uint128rem(&lft, &rhs);
  return lft;
}
inline _uint128 &operator%=(_uint128 &lft, const _uint128 &rhs) {
  uint128rem(&lft, &rhs);
  return lft;
}

// operator&= (dont care about sign)
inline _int128 &operator&=(_int128 &lft, const _int128 &rhs) {
  LO64(lft) &= LO64(rhs); HI64(lft) &= HI64(rhs);
  return lft;
}
inline _int128 &operator&=(_int128 &lft, const _uint128 &rhs) {
  LO64(lft) &= LO64(rhs); HI64(lft) &= HI64(rhs);
  return lft;
}
inline _uint128 &operator&=(_uint128 &lft, const _int128 &rhs) {
  LO64(lft) &= LO64(rhs); HI64(lft) &= HI64(rhs);
  return lft;
}
inline _uint128 &operator&=(_uint128 &lft, const _uint128 &rhs) {
  LO64(lft) &= LO64(rhs); HI64(lft) &= HI64(rhs);
  return lft;
}

// operator|= (dont care about sign)
inline _int128 &operator|=(_int128 &lft, const _int128 &rhs) {
  LO64(lft) |= LO64(rhs); HI64(lft) |= HI64(rhs);
  return lft;
}
inline _int128 &operator|=(_int128 &lft, const _uint128 &rhs) {
  LO64(lft) |= LO64(rhs); HI64(lft) |= HI64(rhs);
  return lft;
}
inline _uint128 &operator|=(_uint128 &lft, const _int128 &rhs) {
  LO64(lft) |= LO64(rhs); HI64(lft) |= HI64(rhs);
  return lft;
}
inline _uint128 &operator|=(_uint128 &lft, const _uint128 &rhs) {
  LO64(lft) |= LO64(rhs); HI64(lft) |= HI64(rhs);
  return lft;
}

// operator^= (dont care about sign)
inline _int128 &operator^=(_int128 &lft, const _int128 &rhs) {
  LO64(lft) ^= LO64(rhs); HI64(lft) ^= HI64(rhs);
  return lft;
}
inline _int128 &operator^=(_int128 &lft, const _uint128 &rhs) {
  LO64(lft) ^= LO64(rhs); HI64(lft) ^= HI64(rhs);
  return lft;
}
inline _uint128 &operator^=(_uint128 &lft, const _int128 &rhs) {
  LO64(lft) ^= LO64(rhs); HI64(lft) ^= HI64(rhs);
  return lft;
}
inline _uint128 &operator^=(_uint128 &lft, const _uint128 &rhs) {
  LO64(lft) ^= LO64(rhs); HI64(lft) ^= HI64(rhs);
  return lft;
}

inline _int128 &operator>>=(_int128 &lft, int shft) {
  int128shr(&lft, shft);
  return lft;
}
inline _uint128 &operator>>=(_uint128 &lft, int shft) {
  uint128shr(&lft, shft);
  return lft;
}
inline _int128 &operator<<=(_int128 &lft, int shft) {
  int128shl(&lft, shft);
  return lft;
}
inline _uint128 &operator<<=(_uint128 &lft, int shft) {
  int128shl(&lft, shft);
  return lft;
}

// Now all combinations of binary operators for lft = 128-bit and rhs is built in integral type
// operator+ for built in integral types as second argument
inline _int128  operator+(const _int128  &lft, __int64 rhs) {
  return lft + (_int128)rhs;
}
inline _int128  operator+(const _int128  &lft, unsigned __int64 rhs) {
  return lft + (_uint128)rhs;
}
inline _int128  operator+(const _int128  &lft, long rhs) {
  return lft + (_int128)rhs;
}
inline _int128  operator+(const _int128  &lft, unsigned long rhs) {
  return lft + (_uint128)rhs;
}
inline _int128  operator+(const _int128  &lft, int rhs) {
  return lft + (_int128)rhs;
}
inline _int128  operator+(const _int128  &lft, unsigned int rhs) {
  return lft + (_uint128)rhs;
}
inline _int128  operator+(const _int128  &lft, short rhs) {
  return lft + (_int128)rhs;
}
inline _int128  operator+(const _int128  &lft, unsigned short rhs) {
  return lft + (_uint128)rhs;
}

inline _uint128 operator+(const _uint128 &lft, __int64 rhs) {
  return lft + (_int128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, unsigned __int64 rhs) {
  return lft + (_uint128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, long rhs) {
  return lft + (_int128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, unsigned long rhs) {
  return lft + (_uint128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, int rhs) {
  return lft + (_int128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, unsigned int rhs) {
  return lft + (_uint128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, short rhs) {
  return lft + (_int128)rhs;
}
inline _uint128 operator+(const _uint128 &lft, unsigned short rhs) {
  return lft + (_uint128)rhs;
}


// operator- for built in integral types as second argument
inline _int128  operator-(const _int128  &lft, __int64 rhs) {
  return lft - (_int128)rhs;
}
inline _int128  operator-(const _int128  &lft, unsigned __int64 rhs) {
  return lft - (_uint128)rhs;
}
inline _int128  operator-(const _int128  &lft, long rhs) {
  return lft - (_int128)rhs;
}
inline _int128  operator-(const _int128  &lft, unsigned long rhs) {
  return lft - (_uint128)rhs;
}
inline _int128  operator-(const _int128  &lft, int rhs) {
  return lft - (_int128)rhs;
}
inline _int128  operator-(const _int128  &lft, unsigned int rhs) {
  return lft - (_uint128)rhs;
}
inline _int128  operator-(const _int128  &lft, short rhs) {
  return lft - (_int128)rhs;
}
inline _int128  operator-(const _int128  &lft, unsigned short rhs) {
  return lft - (_uint128)rhs;
}

inline _uint128 operator-(const _uint128 &lft, __int64 rhs) {
  return lft - (_int128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, unsigned __int64 rhs) {
  return lft - (_uint128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, long rhs) {
  return lft - (_int128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, unsigned long rhs) {
  return lft - (_uint128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, int rhs) {
  return lft - (_int128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, unsigned int rhs) {
  return lft - (_uint128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, short rhs) {
  return lft - (_int128)rhs;
}
inline _uint128 operator-(const _uint128 &lft, unsigned short rhs) {
  return lft - (_uint128)rhs;
}


// operator* for built in integral types as second argument
inline _int128  operator*(const _int128  &lft, __int64 rhs) {
  return lft * (_int128)rhs;
}
inline _int128  operator*(const _int128  &lft, unsigned __int64 rhs) {
  return lft * (_uint128)rhs;
}
inline _int128  operator*(const _int128  &lft, long rhs) {
  return lft * (_int128)rhs;
}
inline _int128  operator*(const _int128  &lft, unsigned long rhs) {
  return lft * (_uint128)rhs;
}
inline _int128  operator*(const _int128  &lft, int rhs) {
  return lft * (_int128)rhs;
}
inline _int128  operator*(const _int128  &lft, unsigned int rhs) {
  return lft * (_uint128)rhs;
}
inline _int128  operator*(const _int128  &lft, short rhs) {
  return lft * (_int128)rhs;
}
inline _int128  operator*(const _int128  &lft, unsigned short rhs) {
  return lft * (_uint128)rhs;
}

inline _uint128 operator*(const _uint128 &lft, __int64 rhs) {
  return lft * (_int128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, unsigned __int64 rhs) {
  return lft * (_uint128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, long rhs) {
  return lft * (_int128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, unsigned long rhs) {
  return lft * (_uint128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, int rhs) {
  return lft * (_int128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, unsigned int rhs) {
  return lft * (_uint128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, short rhs) {
  return lft * (_int128)rhs;
}
inline _uint128 operator*(const _uint128 &lft, unsigned short rhs) {
  return lft * (_uint128)rhs;
}


// operator/ for built in integral types as second argument
inline _int128  operator/(const _int128  &lft, __int64 rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, unsigned __int64 rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, long rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, unsigned long rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, int rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, unsigned int rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, short rhs) {
  return lft / (_int128)rhs;
}
inline _int128  operator/(const _int128  &lft, unsigned short rhs) {
  return lft / (_int128)rhs;
}

inline _uint128 operator/(const _uint128 &lft, __int64 rhs) {
  return lft / (_int128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, unsigned __int64 rhs) {
  return lft / (_uint128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, long rhs) {
  return lft / (_int128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, unsigned long rhs) {
  return lft / (_uint128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, int rhs) {
  return lft / (_int128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, unsigned int rhs) {
  return lft / (_uint128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, short rhs) {
  return lft / (_int128)rhs;
}
inline _uint128 operator/(const _uint128 &lft, unsigned short rhs) {
  return lft / (_uint128)rhs;
}


// operator% for built in integral types as second argument
inline _int128  operator%(const _int128  &lft, __int64 rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, unsigned __int64 rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, long rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, unsigned long rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, int rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, unsigned int rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, short rhs) {
  return lft % (_int128)rhs;
}
inline _int128  operator%(const _int128  &lft, unsigned short rhs) {
  return lft % (_int128)rhs;
}

inline _uint128 operator%(const _uint128 &lft, __int64 rhs) {
  return lft % (_int128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, unsigned __int64 rhs) {
  return lft % (_uint128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, long rhs) {
  return lft % (_int128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, unsigned long rhs) {
  return lft % (_uint128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, int rhs) {
  return lft % (_int128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, unsigned int rhs) {
  return lft % (_uint128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, short rhs) {
  return lft % (_int128)rhs;
}
inline _uint128 operator%(const _uint128 &lft, unsigned short rhs) {
  return lft % (_uint128)rhs;
}


// operator& for built in integral types as second argument
inline _int128  operator&(const _int128  &lft, __int64 rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, unsigned __int64 rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, long rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, unsigned long rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, int rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, unsigned int rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, short rhs) {
  return lft & (_int128)rhs;
}
inline _int128  operator&(const _int128  &lft, unsigned short rhs) {
  return lft & (_int128)rhs;
}

inline _uint128 operator&(const _uint128 &lft, __int64 rhs) {
  return lft & (_int128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, unsigned __int64 rhs) {
  return lft & (_uint128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, long rhs) {
  return lft & (_int128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, unsigned long rhs) {
  return lft & (_uint128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, int rhs) {
  return lft & (_int128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, unsigned int rhs) {
  return lft & (_uint128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, short rhs) {
  return lft & (_int128)rhs;
}
inline _uint128 operator&(const _uint128 &lft, unsigned short rhs) {
  return lft & (_uint128)rhs;
}


// operator| for built in integral types as second argument
inline _int128  operator|(const _int128  &lft, __int64 rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, unsigned __int64 rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, long rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, unsigned long rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, int rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, unsigned int rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, short rhs) {
  return lft | (_int128)rhs;
}
inline _int128  operator|(const _int128  &lft, unsigned short rhs) {
  return lft | (_int128)rhs;
}

inline _uint128 operator|(const _uint128 &lft, __int64 rhs) {
  return lft | (_int128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, unsigned __int64 rhs) {
  return lft | (_uint128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, long rhs) {
  return lft | (_int128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, unsigned long rhs) {
  return lft | (_uint128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, int rhs) {
  return lft | (_int128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, unsigned int rhs) {
  return lft | (_uint128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, short rhs) {
  return lft | (_int128)rhs;
}
inline _uint128 operator|(const _uint128 &lft, unsigned short rhs) {
  return lft | (_uint128)rhs;
}


// operator^ for built in integral types as second argument
inline _int128  operator^(const _int128  &lft, __int64 rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, unsigned __int64 rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, long rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, unsigned long rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, int rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, unsigned int rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, short rhs) {
  return lft ^ (_int128)rhs;
}
inline _int128  operator^(const _int128  &lft, unsigned short rhs) {
  return lft ^ (_int128)rhs;
}

inline _uint128 operator^(const _uint128 &lft, __int64 rhs) {
  return lft ^ (_int128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, unsigned __int64 rhs) {
  return lft ^ (_uint128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, long rhs) {
  return lft ^ (_int128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, unsigned long rhs) {
  return lft ^ (_uint128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, int rhs) {
  return lft ^ (_int128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, unsigned int rhs) {
  return lft ^ (_uint128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, short rhs) {
  return lft ^ (_int128)rhs;
}
inline _uint128 operator^(const _uint128 &lft, unsigned short rhs) {
  return lft ^ (_uint128)rhs;
}

// Compare operators where second argument is built in integral type
// operator== for built in integral types as second argument
inline bool operator==(const _int128 &lft, __int64 rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, unsigned __int64 rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, long rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, unsigned long rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, int rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, unsigned int rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, short rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _int128 &lft, unsigned short rhs) {
  return lft == _int128(rhs);
}

inline bool operator==(const _uint128 &lft, __int64 rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _uint128 &lft, unsigned __int64 rhs) {
  return lft == _uint128(rhs);
}
inline bool operator==(const _uint128 &lft, long rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _uint128 &lft, unsigned long rhs) {
  return lft == _uint128(rhs);
}
inline bool operator==(const _uint128 &lft, int rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _uint128 &lft, unsigned int rhs) {
  return lft == _uint128(rhs);
}
inline bool operator==(const _uint128 &lft, short rhs) {
  return lft == _int128(rhs);
}
inline bool operator==(const _uint128 &lft, unsigned short rhs) {
  return lft == _uint128(rhs);
}


// operator!= for built in integral types as second argument
inline bool operator!=(const _int128 &lft, __int64 rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, unsigned __int64 rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, long rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, unsigned long rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, int rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, unsigned int rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, short rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _int128 &lft, unsigned short rhs) {
  return lft != _int128(rhs);
}

inline bool operator!=(const _uint128 &lft, __int64 rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _uint128 &lft, unsigned __int64 rhs) {
  return lft != _uint128(rhs);
}
inline bool operator!=(const _uint128 &lft, long rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _uint128 &lft, unsigned long rhs) {
  return lft != _uint128(rhs);
}
inline bool operator!=(const _uint128 &lft, int rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _uint128 &lft, unsigned int rhs) {
  return lft != _uint128(rhs);
}
inline bool operator!=(const _uint128 &lft, short rhs) {
  return lft != _int128(rhs);
}
inline bool operator!=(const _uint128 &lft, unsigned short rhs) {
  return lft != _uint128(rhs);
}


// operator> for built in integral types as second argument
inline bool operator>(const _int128 &lft, __int64 rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _int128 &lft, unsigned __int64 rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _int128 &lft, long rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _int128 &lft, unsigned long rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _int128 &lft, int rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _int128 &lft, unsigned int rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _int128 &lft, short rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _int128 &lft, unsigned short rhs) {
  return lft > _uint128(rhs);
}

inline bool operator>(const _uint128 &lft, __int64 rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _uint128 &lft, unsigned __int64 rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _uint128 &lft, long rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _uint128 &lft, unsigned long rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _uint128 &lft, int rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _uint128 &lft, unsigned int rhs) {
  return lft > _uint128(rhs);
}
inline bool operator>(const _uint128 &lft, short rhs) {
  return lft > _int128(rhs);
}
inline bool operator>(const _uint128 &lft, unsigned short rhs) {
  return lft > _uint128(rhs);
}


// operator>= for built in integral types as second argument
inline bool operator>=(const _int128 &lft, __int64 rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _int128 &lft, unsigned __int64 rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _int128 &lft, long rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _int128 &lft, unsigned long rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _int128 &lft, int rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _int128 &lft, unsigned int rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _int128 &lft, short rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _int128 &lft, unsigned short rhs) {
  return lft >= _uint128(rhs);
}

inline bool operator>=(const _uint128 &lft, __int64 rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _uint128 &lft, unsigned __int64 rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _uint128 &lft, long rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _uint128 &lft, unsigned long rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _uint128 &lft, int rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _uint128 &lft, unsigned int rhs) {
  return lft >= _uint128(rhs);
}
inline bool operator>=(const _uint128 &lft, short rhs) {
  return lft >= _int128(rhs);
}
inline bool operator>=(const _uint128 &lft, unsigned short rhs) {
  return lft >= _uint128(rhs);
}


// operator< for built in integral types as second argument
inline bool operator<(const _int128 &lft, __int64 rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _int128 &lft, unsigned __int64 rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _int128 &lft, long rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _int128 &lft, unsigned long rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _int128 &lft, int rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _int128 &lft, unsigned int rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _int128 &lft, short rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _int128 &lft, unsigned short rhs) {
  return lft < _uint128(rhs);
}

inline bool operator<(const _uint128 &lft, __int64 rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _uint128 &lft, unsigned __int64 rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _uint128 &lft, long rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _uint128 &lft, unsigned long rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _uint128 &lft, int rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _uint128 &lft, unsigned int rhs) {
  return lft < _uint128(rhs);
}
inline bool operator<(const _uint128 &lft, short rhs) {
  return lft < _int128(rhs);
}
inline bool operator<(const _uint128 &lft, unsigned short rhs) {
  return lft < _uint128(rhs);
}


// operator<= for built in integral types as second argument
inline bool operator<=(const _int128 &lft, __int64 rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _int128 &lft, unsigned __int64 rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _int128 &lft, long rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _int128 &lft, unsigned long rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _int128 &lft, int rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _int128 &lft, unsigned int rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _int128 &lft, short rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _int128 &lft, unsigned short rhs) {
  return lft <= _uint128(rhs);
}

inline bool operator<=(const _uint128 &lft, __int64 rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _uint128 &lft, unsigned __int64 rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _uint128 &lft, long rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _uint128 &lft, unsigned long rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _uint128 &lft, int rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _uint128 &lft, unsigned int rhs) {
  return lft <= _uint128(rhs);
}
inline bool operator<=(const _uint128 &lft, short rhs) {
  return lft <= _int128(rhs);
}
inline bool operator<=(const _uint128 &lft, unsigned short rhs) {
  return lft <= _uint128(rhs);
}

// Assign operators where second argument is built in integral type
// operator+= for built in integral types as second argument
inline _int128  &operator+=(_int128  &lft, __int64 rhs) {
  return lft += (_int128)rhs;
}
inline _int128  &operator+=(_int128  &lft, unsigned __int64 rhs) {
  return lft += (_uint128)rhs;
}
inline _int128  &operator+=(_int128  &lft, long rhs) {
  return lft += (_int128)rhs;
}
inline _int128  &operator+=(_int128  &lft, unsigned long rhs) {
  return lft += (_uint128)rhs;
}
inline _int128  &operator+=(_int128  &lft, int rhs) {
  return lft += (_int128)rhs;
}
inline _int128  &operator+=(_int128  &lft, unsigned int rhs) {
  return lft += (_uint128)rhs;
}
inline _int128  &operator+=(_int128  &lft, short rhs) {
  return lft += (_int128)rhs;
}
inline _int128  &operator+=(_int128  &lft, unsigned short rhs) {
  return lft += (_uint128)rhs;
}

inline _uint128 &operator+=(_uint128 &lft, __int64 rhs) {
  return lft += (_int128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, unsigned __int64 rhs) {
  return lft += (_uint128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, long rhs) {
  return lft += (_int128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, unsigned long rhs) {
  return lft += (_uint128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, int rhs) {
  return lft += (_int128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, unsigned int rhs) {
  return lft += (_uint128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, short rhs) {
  return lft += (_int128)rhs;
}
inline _uint128 &operator+=(_uint128 &lft, unsigned short rhs) {
  return lft += (_uint128)rhs;
}


// operator-= for built in integral types as second argument
inline _int128  &operator-=(_int128  &lft, __int64 rhs) {
  return lft -= (_int128)rhs;
}
inline _int128  &operator-=(_int128  &lft, unsigned __int64 rhs) {
  return lft -= (_uint128)rhs;
}
inline _int128  &operator-=(_int128  &lft, long rhs) {
  return lft -= (_int128)rhs;
}
inline _int128  &operator-=(_int128  &lft, unsigned long rhs) {
  return lft -= (_uint128)rhs;
}
inline _int128  &operator-=(_int128  &lft, int rhs) {
  return lft -= (_int128)rhs;
}
inline _int128  &operator-=(_int128  &lft, unsigned int rhs) {
  return lft -= (_uint128)rhs;
}
inline _int128  &operator-=(_int128  &lft, short rhs) {
  return lft -= (_int128)rhs;
}
inline _int128  &operator-=(_int128  &lft, unsigned short rhs) {
  return lft -= (_uint128)rhs;
}

inline _uint128 &operator-=(_uint128 &lft, __int64 rhs) {
  return lft -= (_int128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, unsigned __int64 rhs) {
  return lft -= (_uint128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, long rhs) {
  return lft -= (_int128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, unsigned long rhs) {
  return lft -= (_uint128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, int rhs) {
  return lft -= (_int128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, unsigned int rhs) {
  return lft -= (_uint128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, short rhs) {
  return lft -= (_int128)rhs;
}
inline _uint128 &operator-=(_uint128 &lft, unsigned short rhs) {
  return lft -= (_uint128)rhs;
}


// operator*= for built in integral types as second argument
inline _int128  &operator*=(_int128  &lft, __int64 rhs) {
  return lft *= (_int128)rhs;
}
inline _int128  &operator*=(_int128  &lft, unsigned __int64 rhs) {
  return lft *= (_uint128)rhs;
}
inline _int128  &operator*=(_int128  &lft, long rhs) {
  return lft *= (_int128)rhs;
}
inline _int128  &operator*=(_int128  &lft, unsigned long rhs) {
  return lft *= (_uint128)rhs;
}
inline _int128  &operator*=(_int128  &lft, int rhs) {
  return lft *= (_int128)rhs;
}
inline _int128  &operator*=(_int128  &lft, unsigned int rhs) {
  return lft *= (_uint128)rhs;
}
inline _int128  &operator*=(_int128  &lft, short rhs) {
  return lft *= (_int128)rhs;
}
inline _int128  &operator*=(_int128  &lft, unsigned short rhs) {
  return lft *= (_uint128)rhs;
}

inline _uint128 &operator*=(_uint128 &lft, __int64 rhs) {
  return lft *= (_int128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, unsigned __int64 rhs) {
  return lft *= (_uint128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, long rhs) {
  return lft *= (_int128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, unsigned long rhs) {
  return lft *= (_uint128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, int rhs) {
  return lft *= (_int128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, unsigned int rhs) {
  return lft *= (_uint128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, short rhs) {
  return lft *= (_int128)rhs;
}
inline _uint128 &operator*=(_uint128 &lft, unsigned short rhs) {
  return lft *= (_uint128)rhs;
}


// operator/= for built in integral types as second argument
inline _int128  &operator/=(_int128  &lft, __int64 rhs) {
  return lft /= (_int128)rhs;
}
inline _int128  &operator/=(_int128  &lft, unsigned __int64 rhs) {
  return lft /= (_uint128)rhs;
}
inline _int128  &operator/=(_int128  &lft, long rhs) {
  return lft /= (_int128)rhs;
}
inline _int128  &operator/=(_int128  &lft, unsigned long rhs) {
  return lft /= (_uint128)rhs;
}
inline _int128  &operator/=(_int128  &lft, int rhs) {
  return lft /= (_int128)rhs;
}
inline _int128  &operator/=(_int128  &lft, unsigned int rhs) {
  return lft /= (_uint128)rhs;
}
inline _int128  &operator/=(_int128  &lft, short rhs) {
  return lft /= (_int128)rhs;
}
inline _int128  &operator/=(_int128  &lft, unsigned short rhs) {
  return lft /= (_uint128)rhs;
}

inline _uint128 &operator/=(_uint128 &lft, __int64 rhs) {
  return lft /= (_int128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, unsigned __int64 rhs) {
  return lft /= (_uint128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, long rhs) {
  return lft /= (_int128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, unsigned long rhs) {
  return lft /= (_uint128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, int rhs) {
  return lft /= (_int128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, unsigned int rhs) {
  return lft /= (_uint128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, short rhs) {
  return lft /= (_int128)rhs;
}
inline _uint128 &operator/=(_uint128 &lft, unsigned short rhs) {
  return lft /= (_uint128)rhs;
}


// operator%= for built in integral types as second argument
inline _int128  &operator%=(_int128  &lft, __int64 rhs) {
  return lft %= (_int128)rhs;
}
inline _int128  &operator%=(_int128  &lft, unsigned __int64 rhs) {
  return lft %= (_uint128)rhs;
}
inline _int128  &operator%=(_int128  &lft, long rhs) {
  return lft %= (_int128)rhs;
}
inline _int128  &operator%=(_int128  &lft, unsigned long rhs) {
  return lft %= (_uint128)rhs;
}
inline _int128  &operator%=(_int128  &lft, int rhs) {
  return lft %= (_int128)rhs;
}
inline _int128  &operator%=(_int128  &lft, unsigned int rhs) {
  return lft %= (_uint128)rhs;
}
inline _int128  &operator%=(_int128  &lft, short rhs) {
  return lft %= (_int128)rhs;
}
inline _int128  &operator%=(_int128  &lft, unsigned short rhs) {
  return lft %= (_uint128)rhs;
}

inline _uint128 &operator%=(_uint128 &lft, __int64 rhs) {
  return lft %= (_int128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, unsigned __int64 rhs) {
  return lft %= (_uint128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, long rhs) {
  return lft %= (_int128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, unsigned long rhs) {
  return lft %= (_uint128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, int rhs) {
  return lft %= (_int128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, unsigned int rhs) {
  return lft %= (_uint128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, short rhs) {
  return lft %= (_int128)rhs;
}
inline _uint128 &operator%=(_uint128 &lft, unsigned short rhs) {
  return lft %= (_uint128)rhs;
}


// operator&= for built in integral types as second argument
inline _int128  &operator&=(_int128  &lft, __int64 rhs) {
  return lft &= (_int128)rhs;
}
inline _int128  &operator&=(_int128  &lft, unsigned __int64 rhs) {
  return lft &= (_uint128)rhs;
}
inline _int128  &operator&=(_int128  &lft, long rhs) {
  return lft &= (_int128)rhs;
}
inline _int128  &operator&=(_int128  &lft, unsigned long rhs) {
  return lft &= (_uint128)rhs;
}
inline _int128  &operator&=(_int128  &lft, int rhs) {
  return lft &= (_int128)rhs;
}
inline _int128  &operator&=(_int128  &lft, unsigned int rhs) {
  return lft &= (_uint128)rhs;
}
inline _int128  &operator&=(_int128  &lft, short rhs) {
  return lft &= (_int128)rhs;
}
inline _int128  &operator&=(_int128  &lft, unsigned short rhs) {
  return lft &= (_uint128)rhs;
}

inline _uint128 &operator&=(_uint128 &lft, __int64 rhs) {
  return lft &= (_int128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, unsigned __int64 rhs) {
  return lft &= (_uint128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, long rhs) {
  return lft &= (_int128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, unsigned long rhs) {
  return lft &= (_uint128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, int rhs) {
  return lft &= (_int128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, unsigned int rhs) {
  return lft &= (_uint128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, short rhs) {
  return lft &= (_int128)rhs;
}
inline _uint128 &operator&=(_uint128 &lft, unsigned short rhs) {
  return lft &= (_uint128)rhs;
}


// operator|= for built in integral types as second argument
inline _int128  &operator|=(_int128  &lft, __int64 rhs) {
  return lft |= (_int128)rhs;
}
inline _int128  &operator|=(_int128  &lft, unsigned __int64 rhs) {
  return lft |= (_uint128)rhs;
}
inline _int128  &operator|=(_int128  &lft, long rhs) {
  return lft |= (_int128)rhs;
}
inline _int128  &operator|=(_int128  &lft, unsigned long rhs) {
  return lft |= (_uint128)rhs;
}
inline _int128  &operator|=(_int128  &lft, int rhs) {
  return lft |= (_int128)rhs;
}
inline _int128  &operator|=(_int128  &lft, unsigned int rhs) {
  return lft |= (_uint128)rhs;
}
inline _int128  &operator|=(_int128  &lft, short rhs) {
  return lft |= (_int128)rhs;
}
inline _int128  &operator|=(_int128  &lft, unsigned short rhs) {
  return lft |= (_uint128)rhs;
}

inline _uint128 &operator|=(_uint128 &lft, __int64 rhs) {
  return lft |= (_int128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, unsigned __int64 rhs) {
  return lft |= (_uint128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, long rhs) {
  return lft |= (_int128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, unsigned long rhs) {
  return lft |= (_uint128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, int rhs) {
  return lft |= (_int128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, unsigned int rhs) {
  return lft |= (_uint128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, short rhs) {
  return lft |= (_int128)rhs;
}
inline _uint128 &operator|=(_uint128 &lft, unsigned short rhs) {
  return lft |= (_uint128)rhs;
}


// operator^= for built in integral types as second argument
inline _int128  &operator^=(_int128  &lft, __int64 rhs) {
  return lft ^= (_int128)rhs;
}
inline _int128  &operator^=(_int128  &lft, unsigned __int64 rhs) {
  return lft ^= (_uint128)rhs;
}
inline _int128  &operator^=(_int128  &lft, long rhs) {
  return lft ^= (_int128)rhs;
}
inline _int128  &operator^=(_int128  &lft, unsigned long rhs) {
  return lft ^= (_uint128)rhs;
}
inline _int128  &operator^=(_int128  &lft, int rhs) {
  return lft ^= (_int128)rhs;
}
inline _int128  &operator^=(_int128  &lft, unsigned int rhs) {
  return lft ^= (_uint128)rhs;
}
inline _int128  &operator^=(_int128  &lft, short rhs) {
  return lft ^= (_int128)rhs;
}
inline _int128  &operator^=(_int128  &lft, unsigned short rhs) {
  return lft ^= (_uint128)rhs;
}

inline _uint128 &operator^=(_uint128 &lft, __int64 rhs) {
  return lft ^= (_int128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, unsigned __int64 rhs) {
  return lft ^= (_uint128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, long rhs) {
  return lft ^= (_int128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, unsigned long rhs) {
  return lft ^= (_uint128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, int rhs) {
  return lft ^= (_int128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, unsigned int rhs) {
  return lft ^= (_uint128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, short rhs) {
  return lft ^= (_int128)rhs;
}
inline _uint128 &operator^=(_uint128 &lft, unsigned short rhs) {
  return lft ^= (_uint128)rhs;
}

_int128   _strtoi128( const char    *str, char    **end, int radix);
_uint128  _strtoui128(const char    *str, char    **end, int radix);
_int128   _wcstoi128( const wchar_t *str, wchar_t **end, int radix);
_uint128  _wcstoui128(const wchar_t *str, wchar_t **end, int radix);

char     *_i128toa(   _int128   value, char    *str , int radix);
char     *_ui128toa(  _uint128  value, char    *str , int radix);
wchar_t  *_i128tow(   _int128   value, wchar_t *str , int radix);
wchar_t  *_ui128tow(  _uint128  value, wchar_t *str , int radix);

//String toString(const _int128  &n , int precision = 0, int width = 0, int flags = 0);
//String toString(const _uint128 &n , int precision = 0, int width = 0, int flags = 0);

#ifdef _UNICODE
#define _tcstoi128  _wcstoi128
#define _tcstoui128 _wcstoui128
#define _i128tot    _i128tow
#define _ui128tot   _ui128tow
#else
#define _tcstoi128  _strtoi128
#define _tcstoui128 _strtoui128
#define _i128tot    _i128toa
#define _ui128tot   _ui128toa
#endif // _UNICODE

inline char radixLetter(unsigned int c) {
  return (c < 10) ? ('0' + c) : ('a' + (c-10));
}

inline bool iswodigit(wchar_t ch) {
  return ('0' <= ch) && (ch < '8');
}

extern const _int128  _I128_MIN, _I128_MAX;
extern const _uint128 _UI128_MAX;

 // use _standardRandomGenerator if rnd == NULL
//inline _uint128 randInt128(Random *rnd = NULL) {
//  if (rnd == NULL) rnd = _standardRandomGenerator;
//  return _uint128(rnd->nextInt64(), rnd->nextInt64());
//}

//inline _uint128 randInt128(const _uint128 &n, Random *rnd = NULL) {
//  return randInt128(rnd) % n;
//}
//
//inline _int128 randInt128(const _int128 &from, const _int128 &to, Random *rnd = NULL) {
//  return randInt128(to-from+1, rnd) + from;
//}
//
//inline unsigned long int128Hash(const _int128 &n) {
//  return uint64Hash(LO64(n) ^ HI64(n));
//}
//
//inline unsigned long uint128Hash(const _uint128 &n) {
//  return uint64Hash(LO64(n) ^ HI64(n));
//}

inline int int128HashCmp(const _int128 &n1, const _int128 &n2) {
  return int128cmp(&n1, &n2);
}

inline int uint128HashCmp(const _uint128 &n1, const _uint128 &n2) {
  return uint128cmp(&n1, &n2);
}

//std::istream  &operator>>(std::istream  &s,       _int128  &n);
//std::ostream  &operator<<(std::ostream  &s, const _int128  &n);
//std::istream  &operator>>(std::istream  &s,       _uint128 &n);
//std::ostream  &operator<<(std::ostream  &s, const _uint128 &n);
//
//std::wistream &operator>>(std::wistream &s,       _int128  &n);
//std::wostream &operator<<(std::wostream &s, const _int128  &n);
//std::wistream &operator>>(std::wistream &s,       _uint128 &n);
//std::wostream &operator<<(std::wostream &s, const _uint128 &n);

//StrStream &operator<<(StrStream &stream   , const _int128  &n);
//StrStream &operator<<(StrStream &stream   , const _uint128 &n);