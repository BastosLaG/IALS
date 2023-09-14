print_str: ;; arg in r20
    mov r10 #0
_ps_loop:
    beq _ps_end_loop !r20,r10 #0
    prc !r20,r10
    add r10 r10 #1
    jmp _ps_loop
_ps_end_loop: ;;
    prc #10
    ret
main:
    mov r1 #10
    mov r2 #11
    mov r3 #12
    
    prn r1
    prn r2
    prn r3
    prc #10
    mov r29 r1
    mov r1 r3
    mov r2 r2
    mov r3 r29

    prn r1
    prn r2
    prn r3
    prc #10

    add r4 r1 r2 
    mul r5 r1 r2
    sub r6 r1 r2
    div r7 r1 r2
    
    prn r4
    prc #10
    prn r5
    prc #10
    prn r6
    prc #10
    prn r7
    prc #10

    add r30 r30 #-1
    mov !r30 r31

    mov @300 #83
    mov @301 #97
    mov @302 #108
    mov @303 #117
    mov @304 #116
    mov @305 #0

    mov r20 #300

    cal print_str
    
    mov r31 !r30
    add r30 r30 #1

    ret
    