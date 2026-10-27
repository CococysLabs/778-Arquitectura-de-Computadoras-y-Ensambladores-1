// Reservar el vector en la pila del llamador mantiene válido su contenido.
.include "io.s"
.include "08_read_numbers.s"
.include "06_itoa.s"

.section .rodata
sum_text: .ascii "Suma: "
    sum_text_len = . - sum_text
sub_text: .ascii "Resta: "
    sub_text_len = . - sub_text
newline: .ascii "\n"
number_error:
    .ascii "Error: entrada inválida, capacidad excedida o desbordamiento.\n"
    number_error_len = . - number_error
.bss
number: .skip 32
.text
.global _start
_start:
    // 2048 enteros de 8 bytes; SP conserva alineación de 16 bytes.
    sub sp, sp, #4, lsl #12
    mov x0, sp
    mov x1, #2048
    bl read_numbers
    cmp x0, #0
    b.lt invalid_numbers
    mov x25, x0
    mov x24, sp
    mov x27, #0
.Lsum_next:
    cbz x25, .Lsum_done
    ldr x10, [x24], #8
    adds x27, x27, x10
    b.vs invalid_numbers
    sub x25, x25, #1
    b .Lsum_next
.Lsum_done:
    add sp, sp, #4, lsl #12
    neg x28, x27

    ldr x1, =sum_text
    mov x2, sum_text_len
    bl print
    mov x0, x27
    bl print_number
    bl print_newline

    ldr x1, =sub_text
    mov x2, sub_text_len
    bl print
    mov x0, x28
    bl print_number
    bl print_newline

    mov x0, #0
    mov x8, #93
    svc #0

print_number:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    ldr x2, =number
    add x1, x2, #32
    bl itoa
    cbnz x0, invalid_numbers
    bl print
    ldp x29, x30, [sp], #16
    ret

print_newline:
    ldr x1, =newline
    mov x2, #1
print:
    mov x0, #1
    // Conservar el enlace durante la llamada a write_all.
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    bl write_all
    cmp x0, #0
    b.lt io_error
    ldp x29, x30, [sp], #16
    ret

invalid_numbers:
    mov x0, #2
    ldr x1, =number_error
    mov x2, number_error_len
    bl write_all
    mov x0, #2
    mov x8, #93
    svc #0
