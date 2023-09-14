.include modexp.asm

main:
  sub r30 r30 #1
  mov !r30 r31
  mov r1 #30000
  mov r2 #10000
  mov r3 #20000
  mov r4 #40000
  mov r20 r2
  mov r21 #5
  prc #109
  prc #32
  prc #61
  prc #32
  cal bignum_init
  mov !r20,#-1 #147
  mov !r20,#-2 #238
  mov !r20,#-3 #255
  mov !r20,#-4 #192
  mov !r20,#-5 #66
  cal bignum_print
  mov r20 r3
  mov r21 #4
  cal bignum_init
  mov !r20,#-1 #193
  mov !r20,#-2 #108
  mov !r20,#-3 #21
  mov !r20,#-4 #61
  mov r20 r4
  mov r21 #5
  prc #78
  prc #32
  prc #61
  prc #32
  cal bignum_init
  mov !r20,#-1 #31
  mov !r20,#-2 #120
  mov !r20,#-3 #154
  mov !r20,#-4 #201
  mov !r20,#-5 #2
  cal bignum_print
  prc #115
  prc #32
  prc #61
  prc #32
  mov r20 r1
  mov r21 r2
  mov r22 r3
  mov r24 r4
  cal modexp
  mov r20 r1
  cal bignum_print
  mov r31 !r30
  add r30 r30 #1
  ret
