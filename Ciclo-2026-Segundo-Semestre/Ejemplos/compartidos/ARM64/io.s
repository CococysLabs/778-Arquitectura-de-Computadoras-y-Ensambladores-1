// Auxiliares Linux AArch64. Preservan x19-x29 y SP.
// write_all: x0=fd, x1=buffer, x2=bytes; devuelve x0=0 o errno negativo.
// Modifica x0-x3, x8. read_retry conserva x1/x2 y modifica x0/x3/x8.

.text
write_all:
    mov x3, x0
.Lwrite_next:
    cbz x2, .Lwrite_ok
    mov x0, x3
    mov x8, #64
    svc #0
    cmp x0, #-4
    b.eq .Lwrite_next
    cmp x0, #0
    b.lt .Lwrite_return
    b.eq .Lwrite_zero
    add x1, x1, x0
    sub x2, x2, x0
    b .Lwrite_next
.Lwrite_zero:
    mov x0, #-5
.Lwrite_return:
    ret
.Lwrite_ok:
    mov x0, #0
    ret

read_retry:
    mov x3, x0
.Lread_again:
    mov x0, x3
    mov x8, #63
    svc #0
    cmp x0, #-4
    b.eq .Lread_again
    ret

// read_line: x0=buffer, x1=capacidad; devuelve x0=longitud (sin LF/CR final),
// -1 si falla read o -2 si excede capacidad. x1=1 si encontró EOF, 0 si no.
// Consume la línea completa aun si no cabe. No añade NUL. Modifica x0-x3/x8.
read_line:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    stp x19, x20, [sp, #-16]!
    stp x21, x22, [sp, #-16]!
    sub sp, sp, #16
    mov x19, x0
    mov x20, x1
    mov x21, #0
    mov x22, #0
.Lline_next:
    mov x0, #0
    mov x1, sp
    mov x2, #1
    bl read_retry
    cmp x0, #0
    b.lt .Lline_io_error
    b.eq .Lline_eof
    ldrb w2, [sp]
    cmp w2, #10
    b.eq .Lline_newline
    cmp x21, x20
    b.hs .Lline_overflow
    strb w2, [x19, x21]
    add x21, x21, #1
    b .Lline_next
.Lline_overflow:
    mov x22, #1
    b .Lline_next
.Lline_eof:
    mov x1, #1
    b .Lline_finish
.Lline_newline:
    mov x1, #0
.Lline_finish:
    cbnz x22, .Lline_too_long
    cbz x21, .Lline_length
    sub x0, x21, #1
    ldrb w2, [x19, x0]
    cmp w2, #13
    csel x21, x0, x21, eq
.Lline_length:
    mov x0, x21
    b .Lline_return
.Lline_too_long:
    mov x0, #-2
    b .Lline_return
.Lline_io_error:
    mov x0, #-1
    mov x1, #0
.Lline_return:
    add sp, sp, #16
    ldp x21, x22, [sp], #16
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret

// Error irrecuperable: informa por stderr y termina con código 1.
io_error:
    mov x0, #2
    ldr x1, =io_error_text
    mov x2, io_error_len
    bl write_all
    mov x0, #1
    mov x8, #93
    svc #0

.section .rodata
io_error_text:
    .ascii "Error de entrada/salida. Revise rutas, permisos y descriptores.\n"
    io_error_len = . - io_error_text
.text
