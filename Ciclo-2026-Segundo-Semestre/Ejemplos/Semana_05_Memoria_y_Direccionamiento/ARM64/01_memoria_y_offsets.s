.data
.balign 8
arreglo: .quad 10, 20, 30, 40
byte_con_signo: .byte 0xfb

.text
.global _start
_start:
    ldr x9, =arreglo       // Pseudoinstrucción: obtener la dirección, no su contenido.
    ldr x10, [x9]
    ldr x11, [x9, #8]
    mov x12, #25
    str x12, [x9, #8]
    mov x13, #2
    ldr x14, [x9, x13, lsl #3]  // Índice 2, elementos de ocho bytes.

    ldr x15, =byte_con_signo
    ldrb w16, [x15]
    ldrsb x17, [x15]

resultados:
    mov x0, #0
    mov x8, #93
    svc #0
