.include modexp.asm
main:
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra

  mov r0  #9000
  mov r10 #10000
  mov r11 #11000
  mov r12 #12000
  mov r13 #13000
  mov r14 #14000
  mov r15 #15000
  mov r16 #16000
  mov r17 #17000
  mov r18 #18000
  mov r19 #19000
  mov r20 r0
  mov r21 #9
  cal bignum_init
  mov !r20,#-1 #41
  mov !r20,#-2 #52
  mov !r20,#-3 #161
  mov !r20,#-4 #2
  mov !r20,#-5 #219
  mov !r20,#-6 #165
  mov !r20,#-7 #4
  mov !r20,#-8 #151
  mov !r20,#-9 #2
  mov r20 r10
  mov r21 #1
  cal bignum_init
  mov r20 r11
  mov r21 #4
  cal bignum_init
  mov !r20,#-1 #110
  mov !r20,#-2 #89
  mov !r20,#-3 #18
  mov !r20,#-4 #171
  mov r20 r12
  mov r21 #5
  cal bignum_init
  mov !r20,#-1 #159
  mov !r20,#-2 #173
  mov !r20,#-3 #135
  mov !r20,#-4 #253
  mov !r20,#-5 #1
  mov r20 r13
  mov r21 #5
  cal bignum_init
  mov !r20,#-1 #55
  mov !r20,#-2 #185
  mov !r20,#-3 #29
  mov !r20,#-4 #77
  mov !r20,#-5 #1
  mov r20 r14
  mov r21 #1
  cal bignum_init
  mov r20 r15
  mov r21 #5
  cal bignum_init
  mov !r20,#-1 #85
  mov !r20,#-2 #233
  mov !r20,#-3 #156
  mov !r20,#-4 #163
  mov !r20,#-5 #1
  mov r20 r16
  mov r21 #5
  cal bignum_init
  mov !r20,#-1 #165
  mov !r20,#-2 #182
  mov !r20,#-3 #84
  mov !r20,#-4 #18
  mov !r20,#-5 #1
  mov r20 r17
  mov r21 #4
  cal bignum_init
  mov !r20,#-1 #127
  mov !r20,#-2 #57
  mov !r20,#-3 #85
  mov !r20,#-4 #163
  mov r1 r19
  mov r2 r11
  mov r3 r16
  mov r4 r13
  cal modexp
  mov r1 r18
  mov r2 r11
  mov r3 r15
  mov r4 r12
  cal modexp
label001:
  mov r21 r18
  mov r24 r19
  cal bignum_cmp
  bne label002 r20 #1
  mov r20 r10
  mov r21 r18
  cal bignum_copy
  mov r20 r18
  mov r21 r10
  mov r22 r12
  mov r24 r0
  cal bignum_add
  jmp label001
label002:
  mov r20 r18
  mov r24 r19
  cal bignum_sub
  mov r20 r10
  mov r21 r17
  mov r22 r18
  mov r24 r12
  cal bignum_mul
  mov r20 r14
  mov r21 r10
  mov r22 r13
  mov r24 r0
  cal bignum_mul
  mov r20 r10
  mov r21 r19
  mov r22 r14
  cal bignum_add
  prc #115
  prc #32
  prc #61
  prc #32
  cal bignum_print

  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  ret
