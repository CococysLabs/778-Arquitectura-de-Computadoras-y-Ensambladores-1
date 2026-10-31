.text
.global _start
_start:
    mov x9, #20
    mov x10, #6
    add x11, x9, x10
    sub x12, x9, x10
    mul x13, x9, x10
    sdiv x14, x9, x10
    udiv x15, x9, x10

    movz w16, #0xffff
    movk w16, #0x7fff, lsl #16
    mov w17, #1
    adds w18, w16, w17      // INT32_MAX + 1: N=1, Z=0, C=0, V=1.

resultados:
    mov x0, #0
    mov x8, #93
    svc #0
