// Lee datos/lecturas.csv: columna de enteros 0..INT64_MAX, LF/CRLF,
// líneas vacías y '$' opcional al final. Máximo 4096 bytes.
// x0=vector del llamador, x1=capacidad en enteros de 8 bytes.
// Devuelve x0=cantidad o -1 (abrir), -2 (leer/cerrar), -3 (tamaño),
// -4 (formato/desbordamiento), -5 (capacidad). El vector puede quedar parcial.
// Preserva x19-x29 y SP; modifica x0-x8. El llamador reserva su propia pila.
.include "05_atoi.s"

.section .rodata
numbers_filename:
    .asciz "datos/lecturas.csv"
.bss
numbers_buffer:
    .skip 4097
.text
read_numbers:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    stp x19, x20, [sp, #-16]!
    stp x21, x22, [sp, #-16]!
    stp x23, x24, [sp, #-16]!
    stp x25, x26, [sp, #-16]!
    mov x19, x0
    mov x20, x1
    mov x0, #-100
    ldr x1, =numbers_filename
    mov x2, #0
    mov x3, #0
    mov x8, #56
    svc #0
    cmp x0, #0
    b.lt .Lnumbers_open_error
    mov x21, x0
    mov x22, #0
.Lnumbers_read:
    mov x0, x21
    ldr x1, =numbers_buffer
    add x1, x1, x22
    mov x2, #4097
    sub x2, x2, x22
    bl read_retry
    cmp x0, #0
    b.lt .Lnumbers_read_error
    b.eq .Lnumbers_close
    add x22, x22, x0
    cmp x22, #4096
    b.hi .Lnumbers_size_error
    b .Lnumbers_read
.Lnumbers_close:
    mov x0, x21
    mov x8, #57
    svc #0
    cmp x0, #0
    b.lt .Lnumbers_closed_error
    ldr x23, =numbers_buffer
    add x24, x23, x22
    mov x25, #0
.Lnumbers_next:
    cmp x23, x24
    b.hs .Lnumbers_ok
    ldrb w26, [x23]
    cmp w26, #10
    b.eq .Lnumbers_skip
    cmp w26, #13
    b.eq .Lnumbers_skip
    cmp w26, #'$'
    b.eq .Lnumbers_sentinel
    mov x0, x23
    mov x1, x24
    bl atoi
    cbnz x2, .Lnumbers_format_error
    mov x23, x1
    cmp x23, x24
    b.hs .Lnumbers_save
    ldrb w26, [x23]
    cmp w26, #10
    b.eq .Lnumbers_save
    cmp w26, #13
    b.eq .Lnumbers_save
    cmp w26, #'$'
    b.ne .Lnumbers_format_error
.Lnumbers_save:
    cmp x25, x20
    b.hs .Lnumbers_capacity_error
    str x0, [x19, x25, lsl #3]
    add x25, x25, #1
    b .Lnumbers_next
.Lnumbers_skip:
    add x23, x23, #1
    b .Lnumbers_next
.Lnumbers_sentinel:
    add x23, x23, #1
.Lnumbers_trailing:
    cmp x23, x24
    b.hs .Lnumbers_ok
    ldrb w26, [x23], #1
    cmp w26, #10
    b.eq .Lnumbers_trailing
    cmp w26, #13
    b.eq .Lnumbers_trailing
    b .Lnumbers_format_error
.Lnumbers_ok:
    mov x0, x25
    b .Lnumbers_return
.Lnumbers_open_error:
    mov x0, #-1
    b .Lnumbers_return
.Lnumbers_read_error:
    mov x26, #-2
    b .Lnumbers_close_error
.Lnumbers_size_error:
    mov x26, #-3
.Lnumbers_close_error:
    mov x0, x21
    mov x8, #57
    svc #0
    mov x0, x26
    b .Lnumbers_return
.Lnumbers_closed_error:
    mov x0, #-2
    b .Lnumbers_return
.Lnumbers_format_error:
    mov x0, #-4
    b .Lnumbers_return
.Lnumbers_capacity_error:
    mov x0, #-5
.Lnumbers_return:
    ldp x25, x26, [sp], #16
    ldp x23, x24, [sp], #16
    ldp x21, x22, [sp], #16
    ldp x19, x20, [sp], #16
    ldp x29, x30, [sp], #16
    ret
