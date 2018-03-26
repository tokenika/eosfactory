; File: Int128x64.asm
; build obj - file with
; ml64 / nologo / c / Zf / Fo$(IntDir)Int128x64.obj Int128x64.asm
.CODE

; void int128sum(_int128 &dst, cnost _int128 &x, const _int128 &y);
int128sum PROC
push    rbx
mov     rax, qword ptr[rdx]
add     rax, qword ptr[r8]
mov     rbx, qword ptr[rdx + 8]
adc     rbx, qword ptr[r8 + 8]
mov     qword ptr[rcx], rax
mov     qword ptr[rcx + 8], rbx
pop     rbx
ret
int128sum ENDP

; void int128dif(_int128 &dst, const _int128 &x, const _int128 &y);
int128dif PROC
push    rbx
mov     rax, qword ptr[rdx]
sub     rax, qword ptr[r8]
mov     rbx, qword ptr[rdx + 8]
sbb     rbx, qword ptr[r8 + 8]
mov     qword ptr[rcx], rax
mov     qword ptr[rcx + 8], rbx
pop     rbx
ret
int128dif ENDP

; void int128mul(_int128 &dst, const _int128 &x, const _int128 &y);
int128mul PROC
push    rbx
mov     rax, qword ptr[rdx + 8]; rax = x.hi
mov     rbx, qword ptr[r8 + 8]; rbx = y.hi
or rbx, rax; rbx = x.hi | y.hi
mov     rbx, qword ptr[r8]; rbx = y.lo
jne     Hard; if (x.hi | y.hi) goto Hard
; simple int64 multiplication
mov     rax, qword ptr[rdx]; rax = x.lo
mul     rbx; rdx:rax = rax * rbx
mov     qword ptr[rcx], rax; dst.lo = rax
mov     qword ptr[rcx + 8], rdx; dst.hi = rdx
pop     rbx
ret
Hard : ; assume rax = x.hi, rbx = y.lo
  push    rsi
  mov     rsi, rdx; need rdx for highend of mul, so rsi = &x
  mul     rbx; rdx:rax = x.hi * y.lo
  mov     r9, rax;
mov     rax, qword ptr[rsi]; rax = x.lo
mul     qword ptr[r8 + 8]; rdx:rax = x.lo * y.hi
add     r9, rax; r9 = lo(x.hi*y.lo + x.lo*y.hi);
mov     rax, qword ptr[rsi]; rax = x.lo
mul     rbx; rdx:rax = x.lo * y.lo
add     rdx, r9
mov     qword ptr[rcx], rax
mov     qword ptr[rcx + 8], rdx
pop     rsi
pop     rbx
ret
int128mul ENDP


; void int128div(_int128 &dst, const _int128 &x, const _int128 &y);
int128div PROC
push        rdi
push        rsi
push        rbx
push        rcx
mov         r9, rdx
xor         rdi, rdi
mov         rax, qword ptr[r9 + 8]
or rax, rax
jge         L1
inc         rdi
mov         rdx, qword ptr[r9]
neg         rax
neg         rdx
sbb         rax, 0
mov         qword ptr[r9 + 8], rax
mov         qword ptr[r9], rdx
L1 :
mov         rax, qword ptr[r8 + 8]
or rax, rax
jge         L2
inc         rdi
mov         rdx, qword ptr[r8]
neg         rax
neg         rdx
sbb         rax, 0
mov         qword ptr[r8 + 8], rax
mov         qword ptr[r8], rdx
L2 :
or rax, rax
jne         L3
mov         rcx, qword ptr[r8]
mov         rax, qword ptr[r9 + 8]
xor rdx, rdx
div         rcx
mov         rbx, rax
mov         rax, qword ptr[r9]
div         rcx
mov         rdx, rbx
jmp         L4
L3 :
mov         rbx, rax
mov         rcx, qword ptr[r8]
mov         rdx, qword ptr[r9 + 8]
mov         rax, qword ptr[r9]
L5 :
  shr         rbx, 1
  rcr         rcx, 1
  shr         rdx, 1
  rcr         rax, 1
  or rbx, rbx
  jne         L5
  div         rcx
  mov         rsi, rax
  mul         qword ptr[r8 + 8]
  mov         rcx, rax
  mov         rax, qword ptr[r8]
  mul         rsi
  add         rdx, rcx
  jb          L6
  cmp         rdx, qword ptr[r9 + 8]
  ja          L6
  jb          L7
  cmp         rax, qword ptr[rdx]
  jbe         L7
  L6 :
dec         rsi
L7 :
xor         rdx, rdx
mov         rax, rsi
L4 :
dec         rdi
jne         L8
neg         rdx
neg         rax
sbb         rdx, 0
L8 :
  pop         rcx
  pop         rbx
  pop         rsi
  pop         rdi
  mov         qword ptr[rcx], rax
  mov         qword ptr[rcx + 8], rdx
  ret
  int128div ENDP

  ; void int128rem(_int128 &dst, const _int128 &x, const _int128 &y);
int128rem PROC
push        rbx
push        rdi
push        rcx
mov         r9, rdx
xor         rdi, rdi
mov         rax, qword ptr[r9 + 8]
or rax, rax
jge         L1
inc         rdi
mov         rdx, qword ptr[r9]
neg         rax
neg         rdx
sbb         rax, 0
mov         qword ptr[r9 + 8], rax
mov         qword ptr[r9], rdx
L1 :
mov         rax, qword ptr[r8 + 8]
or rax, rax
jge         L2
mov         rdx, qword ptr[r8]
neg         rax
neg         rdx
sbb         rax, 0
mov         qword ptr[r8 + 8], rax
mov         qword ptr[r8], rdx
L2 :
or rax, rax
jne         L3
mov         rcx, qword ptr[r8]
mov         rax, qword ptr[r9 + 8]
xor rdx, rdx
div         rcx
mov         rax, qword ptr[r9]
div         rcx
mov         rax, rdx
xor         rdx, rdx
dec         rdi
jns         L4
jmp         L8
L3 :
mov         rbx, rax
mov         rcx, qword ptr[r8]
mov         rdx, qword ptr[r9 + 8]
mov         rax, qword ptr[r9]
L5 :
  shr         rbx, 1
  rcr         rcx, 1
  shr         rdx, 1
  rcr         rax, 1
  or rbx, rbx
  jne         L5
  div         rcx
  mov         rcx, rax
  mul         qword ptr[r8 + 8]
  xchg        rax, rcx
  mul         qword ptr[r8]
  add         rdx, rcx
  jb          L6
  cmp         rdx, qword ptr[r9 + 8]
  ja          L6
  jb          L7
  cmp         rax, qword ptr[r9]
  jbe         L7
  L6 :
sub         rax, qword ptr[r8]
sbb         rdx, qword ptr[r8 + 8]
L7 :
  sub         rax, qword ptr[r9]
  sbb         rdx, qword ptr[r9 + 8]
  dec         rdi
  jns         L8
  L4 :
neg         rdx
neg         rax
sbb         rdx, 0
L8 :
  pop         rcx
  pop         rdi
  pop         rbx
  mov         qword ptr[rcx], rax
  mov         qword ptr[rcx + 8], rdx
  ret
  int128rem ENDP

  ; void int128neg(_int128 &dst, const _int128 &x);
int128neg PROC
mov         rax, qword ptr[rdx]
neg         rax
mov         r8, qword ptr[rdx + 8]
adc         r8, 0
neg         r8
mov         qword ptr[rcx], rax
mov         qword ptr[rcx + 8], r8
ret
int128neg ENDP

; int int128cmp(const _int128 &n1, const _int128 &n2);
int128cmp PROC
mov         rax, qword ptr[rcx + 8]; n1.hi
cmp         rax, qword ptr[rdx + 8]; n2.hi
jl          lessthan; signed compare of n1.hi and n2.hi
jg          greaterthan
mov         rax, qword ptr[rcx]; n2.lo
cmp         rax, qword ptr[rdx]; n2.lo
jb          lessthan; unsigned compare of n1.lo and n2.lo
ja          greaterthan
mov         rax, 0; they are equal
ret
greaterthan :
mov         rax, 1
ret
lessthan :
mov         rax, -1
ret
int128cmp ENDP

END

; File:UInt128x64.asm
; build obj - file with
; ml64 / nologo / c / Zf / Fo$(IntDir)UInt128x64.obj UInt128x64.asm

.CODE

; void uint128div(_uint128 &dst, const _uint128 &x, const _uint128 &y);
uint128div PROC
push        rbx
push        rsi
push        rcx
mov         r9, rdx
mov         rax, qword ptr[r8 + 8]
or rax, rax
jne         L1
mov         rcx, qword ptr[r8]
mov         rax, qword ptr[r9 + 8]
xor rdx, rdx
div         rcx
mov         rbx, rax
mov         rax, qword ptr[r9]
div         rcx
mov         rdx, rbx
jmp         L2
L1 :
mov         rcx, rax
mov         rbx, qword ptr[r8]
mov         rdx, qword ptr[r9 + 8]
mov         rax, qword ptr[r9]
L3 :
  shr         rcx, 1
  rcr         rbx, 1
  shr         rdx, 1
  rcr         rax, 1
  or rcx, rcx
  jne         L3
  div         rbx
  mov         rsi, rax
  mul         qword ptr[r8 + 8]
  mov         rcx, rax
  mov         rax, qword ptr[r8]
  mul         rsi
  add         rdx, rcx
  jb          L4
  cmp         rdx, qword ptr[r9 + 8]
  ja          L4
  jb          L5
  cmp         rax, qword ptr[r9]
  jbe         L5
  L4 :
dec         rsi
L5 :
xor         rdx, rdx
mov         rax, rsi
L2 :
pop         rcx
pop         rsi
pop         rbx
mov         qword ptr[rcx], rax
mov         qword ptr[rcx + 8], rdx
ret
uint128div ENDP

; void uint128rem(_uint128 &dst, const _uint128 &x, const _uint128 &y);
uint128rem PROC
push        rbx
push        rcx
mov         r9, rdx
mov         rax, qword ptr[r8 + 8]
or rax, rax
jne         L1
mov         rcx, qword ptr[r8]
mov         rax, qword ptr[r9 + 8]
xor rdx, rdx
div         rcx
mov         rax, qword ptr[r9]
div         rcx
mov         rax, rdx
xor         rdx, rdx
jmp         L2
L1 :
mov         rcx, rax
mov         rbx, qword ptr[r8]
mov         rdx, qword ptr[r9 + 8]
mov         rax, qword ptr[r9]
L3 :
  shr         rcx, 1
  rcr         rbx, 1
  shr         rdx, 1
  rcr         rax, 1
  or rcx, rcx
  jne         L3
  div         rbx
  mov         rcx, rax
  mul         qword ptr[r8 + 8]
  xchg        rax, rcx
  mul         qword ptr[r8]
  add         rdx, rcx
  jb          L4
  cmp         rdx, qword ptr[r9 + 8]
  ja          L4
  jb          L5
  cmp         rax, qword ptr[r9]
  jbe         L5
  L4 :
sub         rax, qword ptr[r8]
sbb         rdx, qword ptr[r8 + 8]
L5 :
  sub         rax, qword ptr[r9]
  sbb         rdx, qword ptr[r9 + 8]
  neg         rdx
  neg         rax
  sbb         rdx, 0
  L2 :
  pop         rcx
  pop         rbx
  mov         qword ptr[rcx], rax
  mov         qword ptr[rcx + 8], rdx
  ret
  uint128rem ENDP

  ; int uint128cmp(const _uint128 &n1, const _uint128 &n2);
uint128cmp PROC
mov         rax, qword ptr[rcx + 8]; n1.hi
cmp         rax, qword ptr[rdx + 8]; n2.hi
jb          lessthan; usigned compare of n1.hi and n2.hi
ja          greaterthan
mov         rax, qword ptr[rcx]; n2.lo
cmp         rax, qword ptr[rdx]; n2.lo
jb          lessthan; unsigned compare of n1.lo and n2.lo
ja          greaterthan
mov         rax, 0; they are equal
ret
greaterthan :
mov         rax, 1
ret
lessthan :
mov         rax, -1
ret
uint128cmp ENDP

END