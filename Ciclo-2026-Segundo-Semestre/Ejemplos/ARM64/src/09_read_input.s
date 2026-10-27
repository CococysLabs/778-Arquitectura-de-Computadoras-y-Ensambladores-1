// Leer bloques de hasta 64 bytes; imprimir solo los recibidos y terminar en EOF.
.include "io.s"
.section .rodata
msg_input: .ascii "Ingrese un dato: "
    msg_input_len = . - msg_input
msg_output: .ascii "Dato ingresado: "
    msg_output_len = . - msg_output
.bss
input_buffer: .skip 64
.text
.global _start
_start:
main_loop:
    mov x0, #1
    ldr x1, =msg_input
    mov x2, msg_input_len
    bl write_all
    cmp x0, #0
    b.lt io_error

    mov x0, #0
    ldr x1, =input_buffer
    mov x2, #64
    bl read_retry
    cmp x0, #0
    b.lt io_error
    b.eq input_done
    mov x19, x0

    mov x0, #1
    ldr x1, =msg_output
    mov x2, msg_output_len
    bl write_all
    cmp x0, #0
    b.lt io_error
    mov x0, #1
    ldr x1, =input_buffer
    mov x2, x19
    bl write_all
    cmp x0, #0
    b.lt io_error
    b main_loop
input_done:
    mov x0, #0
    mov x8, #93
    svc #0
