.text
.global _start
_start:
    mov x9, #-1
    mov w9, #42             // Escribir W9 pone a cero los 32 bits altos de X9.

    movz x10, #0xdef0
    movk x10, #0x9abc, lsl #16
    movk x10, #0x5678, lsl #32
    movk x10, #0x1234, lsl #48
    mov x11, xzr

resultados:
    mov x0, #0
    mov x8, #93
    svc #0
