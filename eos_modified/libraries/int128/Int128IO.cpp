#include <comdef.h>
#include <atlconv.h>

#include "include/int128/Int128.h"


using namespace std;

#define BASICSTRING basic_string<Ctype, char_traits<Ctype>, allocator<Ctype> >

template<class Ctype> class StringTemplate : public BASICSTRING {
public:
  StringTemplate() {
  }
  StringTemplate(const char    *str) {
    if(sizeof(Ctype) == sizeof(char)) {
      __super::operator=((const Ctype*)str);
    } else {
      USES_CONVERSION;
      __super::operator=((const Ctype*)A2W(str));
    }
  }
  StringTemplate(const wchar_t *str) {
    if(sizeof(Ctype) == sizeof(wchar_t)) {
      __super::operator=((const Ctype*)str);
    } else {
      USES_CONVERSION;
      __super::operator=((const Ctype*)W2A(str));
    }
  }

  StringTemplate &operator+=(const StringTemplate &str) {
    __super::operator+=(str.c_str());
    return *this;
  }
  StringTemplate &operator+=(char    ch) {
    __super::operator+=((Ctype)ch);
    return *this;
  }
  StringTemplate &operator+=(wchar_t ch) {
    __super::operator+=((Ctype)ch);
    return *this;
  }
};

template<class Ctype> StringTemplate<Ctype> operator+(const StringTemplate<Ctype> &s1
  , const StringTemplate<Ctype> &s2) 
{
  return StringTemplate<Ctype>((BASICSTRING)s1 + (BASICSTRING)s2);
}

#define MAXTMPSIZE 1000
template<class Ctype> StringTemplate<Ctype> getFillerString(streamsize l, Ctype ch = ' ') {
  StringTemplate<Ctype> result;
  if(l <= MAXTMPSIZE) {
    Ctype tmp[MAXTMPSIZE+1], *cp = tmp + l;
    for(*cp = 0; cp-- > tmp;) *cp = ch;
    result = tmp;
  } else {
    Ctype *tmp = new Ctype[(int)l + 1], *cp = tmp + l;
    for(*cp = 0; cp-- > tmp;) *cp = ch;
    result = tmp;
    delete[] tmp;
  }
  return result;
}

template<class Ctype> class Int128Stream 
  : public StringTemplate<Ctype>, public StreamParameters 
{
private:
  Int128Stream &addResult(const StringTemplate<Ctype> &prefix, const char *buf);
public:
  Int128Stream(ostream &out) : StreamParameters(out) {
  }
  Int128Stream(wostream &out) : StreamParameters(out) {
  }

  Int128Stream &operator<<(const _int128  &n);
  Int128Stream &operator<<(const _uint128 &n);
};

template<class Ctype> Int128Stream<Ctype> &Int128Stream<Ctype>::addResult(const StringTemplate<Ctype> &prefix, const char *buf) {
  const streamsize wantedWidth = getWidth();
  const streamsize resultWidth = strlen(buf) + prefix.length();
  StringTemplate<Ctype> result;
  if(wantedWidth > resultWidth) {
    const streamsize fillerLength = wantedWidth - resultWidth;
    switch(getFlags() & ios::adjustfield) {
    case ios::left:
      result =  prefix;
      result += buf;
      result += getFillerString<Ctype>(fillerLength);
      break;
    case ios::right:
      result =  getFillerString<Ctype>(fillerLength);
      result += prefix;
      result += buf;
      break;
    case ios::internal:
      result = prefix;
      result += getFillerString<Ctype>(fillerLength);
      result += buf;
      break;
    default: // do as ios::left
      result =  prefix;
      result += buf;
      result += getFillerString<Ctype>(fillerLength);
      break;
    }
  } else {
    result =  prefix;
    result += buf;
  }
  *this += result;
  return *this;
}

template<class Ctype> Int128Stream<Ctype> &Int128Stream<Ctype>::operator<<(const _int128 &n) {
  StringTemplate<Ctype> prefix;
  char                  buf[200];
  const int             flags = getFlags();
  switch(flags & ios::basefield) {
  case ios::dec:
    { const bool negative = (n < 0);
      const _uint128 v = negative ? -n : n;
      _ui128toa(v, buf, 10);
      if(negative) {
        prefix = "-";
      } else if(flags & ios::showpos) {
        prefix = "+";
      }
      break;
    }
  case ios::hex:
    { const _uint128 v = n;
      if((flags & ios::showbase) && v) prefix = (flags & ios::uppercase) ? "0X" : "0x";
      _ui128toa(v, buf, 16);
      if(flags & ios::uppercase) {
        for(char *cp = buf; *cp; cp++) {
          if(iswlower(*cp)) *cp = _toupper(*cp);
        }
      }
    }
    break;
  case ios::oct:
    { const _uint128 v = n;
      if((flags & ios::showbase) && v) prefix = "0";
      _ui128toa(v, buf, 8);
      break;
    }
  }
  return addResult(prefix, buf);
}

template<class Ctype> Int128Stream<Ctype> &Int128Stream<Ctype>::operator<<(const _uint128 &n) {
  StringTemplate<Ctype> prefix;
  char                  buf[200];
  const int             flags = getFlags();
  switch(flags & ios::basefield) {
  case ios::dec:
    _ui128toa(n, buf, 10);
    break;
  case ios::hex:
    { if((flags & ios::showbase) && n) prefix = (flags & ios::uppercase) ? "0X" : "0x";
      _ui128toa(n, buf, 16);
      if(flags & ios::uppercase) {
        for(char *cp = buf; *cp; cp++) {
          if(iswlower(*cp)) *cp = _toupper(*cp);
        }
      }
    }
    break;
  case ios::oct:
    if((flags & ios::showbase) && n) prefix = "0";
    _ui128toa(n, buf, 8);
    break;
  }
  return addResult(prefix, buf);
}

template<class IStreamType, class Ctype> void fetchChar(IStreamType &in, Ctype &ch) {
  in >> ch;
}
template<class IStreamType, class Ctype> void  peekChar(IStreamType &in, Ctype &ch) {
  ch = in.peek();
  if(ch == EOF) {
    fetchChar(in,ch);
  }
}
template<class IStreamType, class Ctype> void appendCharGetNext(IStreamType &in, Ctype &ch, StringTemplate<wchar_t> &buf) {
  fetchChar(in,ch);
  buf += ch;
  peekChar(in,ch);
}
template<class IStreamType, class Ctype> void  skipChar(IStreamType &in, Ctype &ch) {
  fetchChar(in,ch);
  peekChar(in,ch);
}
template<class IStreamType, class Ctype> void  eatWhite(IStreamType &in, Ctype &ch) {
  peekChar(in,ch);
  while(iswspace(ch)) {
    skipChar(in,ch);
  }
}
template<class IStreamType, class Ctype> void  eatFiller(IStreamType &in, Ctype &ch) {
  const Ctype fc = in.fill();
  if(ch == fc) {
    if(in.flags() & ios::skipws) {
      in.setf(0,ios::skipws);
      do {
        skipChar(in,ch);
      } while(ch == fc);
      in.setf(1,ios::skipws);
    } else {
      do {
        skipChar(in,ch);
      } while(ch == fc);
    }
  }
}

//#define fetchChar(in, ch)         { in >> ch; addToFetched(ch);                           }
//#define peekChar( in, ch)         { ch = in.peek(); if(ch == EOF) fetchChar(in,ch)        }
//#define appendCharGetNext(in, ch) { fetchChar(in,ch); buf += ch; peekChar(in,ch);         }
//#define skipChar( in, ch)         { fetchChar(in,ch); peekChar(in,ch);                    }
//#define eatWhite( in, ch)         { peekChar(in,ch); while(iswspace(ch)) skipChar(in,ch); }
//#define eatFiller(in, ch)         { const Ctype fc = in.fill(); while(ch == fc) skipChar(in,ch); }

template <class IStreamType, class Ctype> IStreamType &operator>>(IStreamType &in, _int128 &n) {
  if(in.ipfx(0)) {
    StringTemplate<wchar_t> buf;
    Ctype                   ch;
    bool                    gotDigits = false;
    const int               flags = in.flags();
    if(flags & ios::skipws) {
      eatWhite(in, ch);
    } else {
      peekChar(in, ch);
    }
    _int128 result;
    switch(flags & ios::basefield) {
    case ios::dec:
      if((ch == '+') || (ch =='-')) appendCharGetNext(in, ch, buf);
      while(iswdigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoi128(buf.c_str(), NULL, 10);
      }
      break;
    case ios::hex:
      if(ch == '0') {
        skipChar(in, ch);
        if((ch == 'x') || (ch == 'X')) {
          skipChar(in, ch);
        } else {
          buf += '0';
          gotDigits = true;
        }
      }
      if((flags & ios::adjustfield) == ios::internal) {
        eatFiller(in, ch);
      }
      while(iswxdigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoi128(buf.c_str(), NULL, 16);
      }
      break;
    case ios::oct:
      if(ch == '0') {
        skipChar(in, ch);
        if(!iswodigit(ch)) {
          buf += '0';
          gotDigits = true;
        }
      }
      if((flags & ios::adjustfield) == ios::internal) {
        eatFiller(in, ch);
      }
      while(iswodigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoi128(buf.c_str(), NULL, 8);
      }
      break;
    }
    if(!gotDigits || (errno == ERANGE)) {
      in.setstate(ios::failbit);
    } else {
      n = result;
    }
    in.isfx();
  }
  return in;
}

template <class IStreamType, class Ctype> IStreamType &operator>>(IStreamType &in, _uint128 &n) {
  if(in.ipfx(0)) {
    StringTemplate<wchar_t> buf;
    Ctype                   ch;
    bool                    gotDigits = false;
    const int               flags = in.flags();
    if(flags & ios::skipws) {
      eatWhite(in, ch);
    } else {
      peekChar(in, ch);
    }

    _uint128 result;
    switch(flags & ios::basefield) {
    case ios::dec:
      if(ch == '+') appendCharGetNext(in, ch, buf);
      while(iswdigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoui128(buf.c_str(), NULL, 10);
      }
      break;
    case ios::hex:
      if(ch == '0') {
        skipChar(in, ch);
        if((ch == 'x') || (ch == 'X')) {
          skipChar(in, ch);
        } else {
          buf += '0';
          gotDigits = true;
        }
      }
      if((flags & ios::adjustfield) == ios::internal) {
        eatFiller(in, ch);
      }
      while(iswxdigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoui128(buf.c_str(), NULL, 16);
      }
      break;
    case ios::oct:
      if(ch == '0') {
        skipChar(in, ch);
        if(!iswodigit(ch)) {
          buf += '0';
          gotDigits = true;
        }
      }
      if((flags & ios::adjustfield) == ios::internal) {
        eatFiller(in, ch);
      }
      while(iswodigit(ch)) {
        appendCharGetNext(in, ch, buf);
        gotDigits = true;
      }
      if(gotDigits) {
        errno = 0;
        result = _wcstoui128(buf.c_str(), NULL, 8);
      }
      break;
    }
    if(!gotDigits || (errno == ERANGE)) {
      in.setstate(ios::failbit);
    } else {
      n = result;
    }
    in.isfx();
  }
  return in;
}

template <class OStreamType, class Ctype> OStreamType &operator<<(OStreamType &out, const _int128 &n) {
  if(out.opfx()) {
    Int128Stream<Ctype> buf(out);
    buf << n;
    out << buf.c_str();
    if(out.flags() & ios::unitbuf) {
      out.flush();
    }
    out.osfx();
  }
  return out;
}

template <class OStreamType, class Ctype> OStreamType &operator<<(OStreamType &out, const _uint128 &n) {
  if(out.opfx()) {
    Int128Stream<Ctype> buf(out);
    buf << n;
    out << buf.c_str();
    if(out.flags() & ios::unitbuf) {
      out.flush();
    }
    out.osfx();
  }
  return out;
}

istream  &operator>>(istream &s, _int128 &n) {
  return ::operator>> <istream, char>(s, n);
}

ostream  &operator<<(ostream &s, const _int128 &n) {
  return ::operator<< <ostream, char>(s, n);
}

wistream &operator>>(wistream &s, _int128 &n) {
  return ::operator>> <wistream, wchar_t>(s, n);
}

wostream &operator<<(wostream &s, const _int128 &n) {
  return ::operator<< <wostream, wchar_t>(s, n);
}


istream  &operator>>(istream &s, _uint128 &n) {
  return ::operator>> <istream, char>(s, n);
}

ostream  &operator<<(ostream &s, const _uint128 &n) {
  return ::operator<< <ostream, char>(s, n);
}

wistream &operator>>(wistream &s, _uint128 &n) {
  return ::operator>> <wistream, wchar_t>(s, n);
}

wostream &operator<<(wostream &s, const _uint128 &n) {
  return ::operator<< <wostream, wchar_t>(s, n);
}