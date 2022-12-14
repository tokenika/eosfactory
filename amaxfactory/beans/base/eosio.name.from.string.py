

def char_to_symbol( char ):
  c = ord(char)
  if( c >= ord('a') and c <= ord('z') ):
     return ( c - ord('a') ) + 6;
  if( c >= ord('1') and c <= ord('5') ):
     return (c - ord('1')) + 1;
  return 0;


def string_to_uint64_t( s ):
  n = 0;
  l = min(12, len(s))
  for i in range( 0, min(12, len(s)) ):
     # NOTE: char_to_symbol() returns char type, and without this explicit
     # expansion to uint64 type, the compilation fails at the point of usage
     # of string_to_name(), where the usage requires constant (compile time) expression.
     n |= (char_to_symbol(s[i]) & 0x1f) << (64 - 5 * (i + 1));
  # The for-loop encoded up to 60 high bits into uint64 'name' variable,
  # if (strlen(str) > 12) then encode str[12] into the low (remaining)
  # 4 bits of 'name'
  if (len(s) > 12):
     n |= char_to_symbol(s[12]) & 0x0F;
  return n;

## test
string_to_uint64_t("a")
string_to_uint64_t("amax")
#hex(6138663577826885632)
#0x5530ea0000000000
m=string_to_uint64_t("merchantx")

print("merchantxpro")
l=string_to_uint64_t("merchantxpro")<<64 | 0
u=string_to_uint64_t("merchantxpro")<<64 | (2**64-1)
print(l)
print(u)
    
print("hotpottester")
l=string_to_uint64_t("hotpottester")<<64 | 0
u=string_to_uint64_t("hotpottester")<<64 | (2**64-1)
print(l)
print(u)
print("123451234512")
l=string_to_uint64_t("123451234512")
u=string_to_uint64_t("test14")<<64 | (2**64-1)
print(l)
print(u)

print("amax2dxi1413 << 64")
l=string_to_uint64_t("amax2dxi1413") << 64
u=string_to_uint64_t("amax2dxi1413") <<64 | (2**64-1)
print(l)
print(u)
import os
re = os.popen(f"amcli -u http://exp1.nchain.me:8889  get table aplink.farm aplink.farm allots  --index 2 --key-type i128 -L {l} -U {u}   -l 1000").read()
print(re)


print("planid:11")
l2=11<<64 | 0
u2=11<<64 | (2**64-1)
print(l2)
print(u2)

print("user1")
l3=string_to_uint64_t("user1")
u3=string_to_uint64_t("user1")
print(l3)
print(u3)

print(float(1)/1000)
print("123451234555")
print(string_to_uint64_t("123451234555"))

#cleos get table eosio.token eosio accounts
#cleos get table eosio.token 6138663577826885632 accounts

#cleos get table eosio.token merchant1 accounts
#cleos get table eosio.token 10569533373498785792 accounts
