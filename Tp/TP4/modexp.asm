.use bignum

modexp:
  ;; r1 = r2 ^ r3 mod r4
  ;; r  = b  ^ e

  ;; backup arguments and ra
  sub r30 r30 #1                ; decr sp
  mov !r30 r31                  ; push ra

  ;; init r5 (res)
  mov r5 r1                     ; r5 points on res (r1)
  mov r20 r5                    ; r20 is res
  mov r21 #1                    ; r21 is 1 (initial len(res))
  cal bignum_init               ; res = 0
  mov !r5,#-1 #1                ; res = 1

  ;; init r6 (base)
  mov r6 #500000                ; base is stored at @500000
  mov r20 r6                    ; r20 is base
  mov r21 r2                    ; r21 is b
  cal bignum_copy               ; base = b

  ;; init r7 (exp)
  mov r7 #510000                ; exp is stored at @510000
  mov r20 r7                    ; r20 is exp
  mov r21 r3                    ; r21 is e
  cal bignum_copy               ; exp = e

  ;; init r8 (tmp)
  mov r8 #520000                ; tmp is stored at @520000
  mov r20 r8                    ; r20 is tmp
  mov r21 #1                    ; r21 is 1 (initial len(tmp))
  cal bignum_init               ; tmp = 0

_modexp_loop:
  mov r20 r7
  cal bignum_zero
  beq _modexp_end !r7 #0

  and r9 #1 !r7,#-1
  beq _modexp_loop_sqr r9 #0
  
_modexp_loop_mul:
  mov r20 r8
  mov r21 r5
  cal bignum_copy

  mov r20 r5
  mov r21 r8
  mov r22 r6
  mov r24 r4
  cal bignum_mul

_modexp_loop_sqr:
  mov r20 r8
  mov r21 r6
  cal bignum_copy

  mov r20 r6
  mov r21 r8
  mov r22 r8
  mov r24 r4
  cal bignum_mul

_modexp_loop_shift:
  mov r20 r7
  mov r21 #1
  cal bignum_rshift

  jmp _modexp_loop              ; loop

_modexp_end:
  ;; restore ra
  mov r31 !r30                  ; pop ra
  add r30 r30 #1                ; incr sp
  ret
