// Copiar un archivo por bloques hasta EOF.
.include "io.s"
.section .rodata
filename: .asciz "datos/lecturas.csv"
.bss
buffer: .skip 4096
.text
.global _start
_start:
    mov x0, #-100
    ldr x1, =filename
    mov x2, #0
    mov x3, #0
    mov x8, #56
    svc #0
    cmp x0, #0
    b.lt io_error
    mov x19, x0
read_loop:
    mov x0, x19
    ldr x1, =buffer
    mov x2, #4096
    bl read_retry
    cmp x0, #0
    b.lt file_error
    b.eq close_file
    mov x2, x0
    mov x0, #1
    ldr x1, =buffer
    bl write_all
    cmp x0, #0
    b.lt file_error
    b read_loop
close_file:
    mov x0, x19
    mov x8, #57
    svc #0
    cmp x0, #0
    b.lt io_error
    mov x0, #0
    mov x8, #93
    svc #0
file_error:
    mov x0, x19
    mov x8, #57
    svc #0
    b io_error
