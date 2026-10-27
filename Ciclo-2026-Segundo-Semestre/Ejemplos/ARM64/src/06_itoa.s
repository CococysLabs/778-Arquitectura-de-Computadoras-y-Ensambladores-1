// x0=entero con signo, x1=fin exclusivo del buffer, x2=inicio del buffer.
// Devuelve x0=0, x1=inicio del texto, x2=longitud; x0=-1 si no hay espacio.
// No añade NUL. Si falla, puede haber escrito parte del texto dentro del buffer.
// Modifica x0-x7; preserva x19-x29 y SP.
.text
itoa:
    mov x7, x2
    mov x2, #0
    mov x3, #10
    lsr x4, x0, #63
    cbz x4, .Litoa_digit
    // La magnitud de INT64_MIN cabe como entero sin signo.
    neg x0, x0
.Litoa_digit:
    cmp x1, x7
    b.ls .Litoa_error
    udiv x5, x0, x3
    msub x6, x5, x3, x0
    add w6, w6, #'0'
    strb w6, [x1, #-1]!
    add x2, x2, #1
    mov x0, x5
    cbnz x0, .Litoa_digit
    cbz x4, .Litoa_ok
    cmp x1, x7
    b.ls .Litoa_error
    mov w5, #'-'
    strb w5, [x1, #-1]!
    add x2, x2, #1
.Litoa_ok:
    mov x0, #0
    ret
.Litoa_error:
    mov x0, #-1
    ret
