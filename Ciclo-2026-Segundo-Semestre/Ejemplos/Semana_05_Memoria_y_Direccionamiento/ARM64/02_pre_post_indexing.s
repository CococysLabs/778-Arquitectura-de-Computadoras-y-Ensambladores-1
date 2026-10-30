.data
.balign 8
arreglo: .quad 10, 20, 30, 40

.text
.global _start
_start:
    ldr x9, =arreglo
    mov x12, x9

    ldr x10, [x9, #8]!     // Primero avanza ocho bytes, después lee 20.
    mov x15, x9
    ldr x11, [x9], #8      // Primero lee 20, después avanza ocho bytes.
    mov x16, x9

    mov x13, #99
    str x13, [x9], #8
    mov x17, x9
    ldr x18, [x12, #16]
    mov x14, #77
    str x14, [x9, #-8]!

resultados:
    mov x0, #0
    mov x8, #93
    svc #0
