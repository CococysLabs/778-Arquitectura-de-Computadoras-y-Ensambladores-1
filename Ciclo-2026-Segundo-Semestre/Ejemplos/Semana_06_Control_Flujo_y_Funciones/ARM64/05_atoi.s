// Convierte dígitos decimales sin signo dentro de [x0, x1).
// Devuelve x0=valor, x1=primer byte no consumido, x2=0 si es válido o -1.
// Admite 0..INT64_MAX; no consume el separador. Rechaza vacío y desbordamiento.
// Modifica x0-x7; preserva x19-x29 y SP.
.text
atoi:
    mov x3, x0
    mov x4, #0
    mov x5, #0
    ldr x6, =922337203685477580
.Latoi_next:
    cmp x3, x1
    b.hs .Latoi_done
    ldrb w7, [x3]
    sub w7, w7, #'0'
    cmp w7, #9
    b.hi .Latoi_done
    cmp x4, x6
    b.hi .Latoi_error
    b.ne .Latoi_accumulate
    cmp w7, #7
    b.hi .Latoi_error
.Latoi_accumulate:
    mov x0, #10
    madd x4, x4, x0, x7
    add x3, x3, #1
    mov x5, #1
    b .Latoi_next
.Latoi_done:
    cbz x5, .Latoi_error
    mov x0, x4
    mov x1, x3
    mov x2, #0
    ret
.Latoi_error:
    mov x0, #0
    mov x1, x3
    mov x2, #-1
    ret
