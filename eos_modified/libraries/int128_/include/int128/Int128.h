// File:Int128.h
#pragma once

#ifndef _M_X64

#error Int128 is available only in x64 arhcitecture

#else

class _int128;
class _uint128;
extern "C" {
  void int128sum(void *dst, const void *x, const void *y);
  void int128dif(void *dst, const void *x, const void *y);
  void int128mul(void *dst, const void *x, const void *y);
  void int128div(void *dst, const void *x, const void *y);
  void int128rem(void *dst, const void *x, const void *y);
  void int128neg(void *dst, const void *x);
  int  int128cmp(const void *n1, const void *n2);
  void uint128div(void *dst, const void *x, const void *y);
  void uint128rem(void *dst, const void *x, const void *y);
  int  uint128cmp(const void *n1, const void *n2);
};

class _int128 {
private:
  _int128(unsigned __int64 _lo, const unsigned __int64 _hi) : lo(_lo), hi(_hi) {
  }
public:
  unsigned __int64 lo;
  unsigned __int64 hi;

  inline _int128() {
  }
  inline _int128(unsigned __int64 n) : lo(n), hi(0) {
  }
  inline _int128(__int64 n) : lo(n), hi(n >= 0 ? 0 : -1) { // remember signextend hi if n < 0 (2-complement)
  }
  inline _int128(unsigned int n) : lo(n), hi(0) {
  }
  inline _int128(int n) : lo(n), hi(n >= 0 ? 0 : -1) {
  }
  inline _int128(unsigned short n) : lo(n), hi(0) {
  }
  inline _int128(short n) : lo(n), hi(n >= 0 ? 0 : -1) {
  }
  explicit _int128(const char *str);

  operator unsigned __int64() const {
    return lo;
  }
  operator __int64() const {
    return lo;
  }
  operator unsigned int() const {
    return (unsigned int)lo;
  }
  operator int() const {
    return (int)lo;
  }
  inline _int128 operator+(const _int128 &rhs) const {
    _int128 result;
    int128sum(&result, this, &rhs);
    return result;
  }

  inline _int128 operator-(const _int128 &rhs) const {
    _int128 result;
    int128dif(&result, this, &rhs);
    return result;
  }

  inline _int128 operator-() const {
    _int128 result;
    int128neg(&result, this);
    return result;
  }
  inline _int128 operator*(const _int128 &rhs) const {
    _int128 result;
    int128mul(&result, this, &rhs);
    return result;
  }

  inline _int128 operator/(const _int128 &rhs) const {
    _int128 result, copy(*this);
    int128div(&result, &copy, &rhs);
    return result;
  }
  inline _int128 operator%(const _int128 &rhs) const {
    _int128 result, copy(*this);
    int128rem(&result, &copy, &rhs);
    return result;
  };

  inline _int128 &operator+=(const _int128 &rhs) {
    const _int128 copy(*this);
    int128sum(this, &copy, &rhs);
    return *this;
  }
  inline _int128 &operator-=(const _int128 &rhs) {
    const _int128 copy(*this);
    int128dif(this, &copy, &rhs);
    return *this;
  }
  inline _int128 &operator*=(const _int128 &rhs) {
    const _int128 copy(*this);
    int128mul(this, &copy, &rhs);
    return *this;
  }
  inline _int128 &operator/=(const _int128 &rhs) {
    const _int128 copy(*this);
    int128div(this, &copy, &rhs);
    return *this;
  }
  inline _int128 &operator%=(const _int128 &rhs) {
    const _int128 copy(*this);
    int128rem(this, &copy, &rhs);
    return *this;
  }

  inline _int128 operator&(const _int128 &rhs) const {
    return _int128(lo&rhs.lo, hi&rhs.hi);
  }
  inline _int128 operator|(const _int128 &rhs) const {
    return _int128(lo | rhs.lo, hi | rhs.hi);
  }
  inline _int128 operator^(const _int128 &rhs) const {
    return _int128(lo^rhs.lo, hi^rhs.hi);
  }

  const char *parseDec(const char *str); // return pointer to char following the number
  const char *parseHex(const char *str); // do
  const char *parseOct(const char *str); // do
};

class _uint128 {
public:
  unsigned __int64 lo;
  unsigned __int64 hi;

  inline _uint128() {
  }
  inline _uint128(const _int128 &n) : lo(n.lo), hi(n.hi) {
  }
  inline _uint128(unsigned __int64 n) : lo(n), hi(0) {
  }
  inline _uint128(__int64 n) : lo(n), hi(n >= 0 ? 0 : -1) {
  }
  inline _uint128(unsigned int n) : lo(n), hi(0) {
  }
  inline _uint128(int n) : lo(n), hi(n >= 0 ? 0 : -1) {
  }
  inline _uint128(unsigned short n) : lo(n), hi(0) {
  }
  inline _uint128(short n) : lo(n), hi(n >= 0 ? 0 : -1) {
  }
  explicit _uint128(const char *str);

  inline operator _int128() const {
    return *(_int128*)(void*)this;
  }
  inline operator unsigned __int64() const {
    return lo;
  }
  inline operator __int64() const {
    return lo;
  }
  inline operator unsigned int() const {
    return (unsigned int)lo;
  }
  inline operator int() const {
    return (int)lo;
  }

  inline _uint128 operator+(const _uint128 &rhs) const {
    _uint128 result;
    int128sum(&result, this, &rhs);
    return result;
  }

  inline _uint128 operator-(const _uint128 &rhs) const {
    _uint128 result;
    int128dif(&result, this, &rhs);
    return result;
  }

  inline _uint128 operator*(const _uint128 &rhs) const {
    _uint128 result;
    int128mul(&result, this, &rhs);
    return result;
  }

  inline _uint128 operator/(const _uint128 &rhs) const {
    _uint128 result, copy(*this);
    uint128div(&result, &copy, &rhs);
    return result;
  }

  inline _uint128 operator%(const _uint128 &rhs) const {
    _uint128 result, copy(*this);
    uint128rem(&result, &copy, &rhs);
    return result;
  };

  inline _uint128 &operator+=(const _uint128 &rhs) {
    const _uint128 copy(*this);
    int128sum(this, &copy, &rhs);
    return *this;
  }
  inline _uint128 &operator-=(const _uint128 &rhs) {
    const _uint128 copy(*this);
    int128dif(this, &copy, &rhs);
    return *this;
  }
  inline _uint128 &operator*=(const _uint128 &rhs) {
    const _uint128 copy(*this);
    int128mul(this, &copy, &rhs);
    return *this;
  }
  inline _uint128 &operator/=(const _uint128 &rhs) {
    const _uint128 copy(*this);
    uint128div(this, &copy, &rhs);
    return *this;
  }
  inline _uint128 &operator%=(const _uint128 &rhs) {
    const _uint128 copy(*this);
    uint128rem(this, &copy, &rhs);
    return *this;
  }
  const char *parseDec(const char *str); // return pointer to char following the number
  const char *parseHex(const char *str); // do
  const char *parseOct(const char *str); // do

};

inline bool operator==(const _int128 &lft, const _int128 &rhs) {
  return (lft.lo == rhs.lo) && (lft.hi == rhs.hi);
}
inline bool operator==(const _int128 &lft, const _uint128 &rhs) {
  return (lft.lo == rhs.lo) && (lft.hi == rhs.hi);
}
inline bool operator==(const _uint128 &lft, const _int128 &rhs) {
  return (lft.lo == rhs.lo) && (lft.hi == rhs.hi);
}
inline bool operator==(const _uint128 &lft, const _uint128 &rhs) {
  return (lft.lo == rhs.lo) && (lft.hi == rhs.hi);
}
inline bool operator!=(const _int128 &lft, const _int128 &rhs) {
  return (lft.lo != rhs.lo) || (lft.hi != rhs.hi);
}
inline bool operator!=(const _int128 &lft, const _uint128 &rhs) {
  return (lft.lo != rhs.lo) || (lft.hi != rhs.hi);
}
inline bool operator!=(const _uint128 &lft, const _int128 &rhs) {
  return (lft.lo != rhs.lo) || (lft.hi != rhs.hi);
}
inline bool operator!=(const _uint128 &lft, const _uint128 &rhs) {
  return (lft.lo != rhs.lo) || (lft.hi != rhs.hi);
}

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

char    * _i128toa(_int128 value, char *str, int radix);
char    * _ui128toa(_uint128 value, char *str, int radix);
wchar_t * _i128tow(_int128 value, wchar_t *str, int radix);
wchar_t * _ui128tow(_uint128 value, wchar_t *str, int radix);

inline char radixLetter(unsigned int c) {
  return (c < 10) ? ('0' + c) : ('a' + (c - 10));
}

inline wchar_t wradixLetter(unsigned int c) {
  return (c < 10) ? ('0' + c) : ('a' + (c - 10));
}

inline bool isodigit(unsigned char ch) {
  return ('0' <= ch) && (ch < '8');
}

unsigned int convertNumberChar(char digit);

#endif // _M_X64




