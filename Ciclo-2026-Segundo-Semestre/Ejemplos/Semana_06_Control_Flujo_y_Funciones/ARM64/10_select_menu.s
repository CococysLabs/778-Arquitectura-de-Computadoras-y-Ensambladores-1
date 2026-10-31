// Una opción por línea: 1, 2 o 3. EOF termina sin reutilizar datos anteriores.
.include "io.s"
.section .rodata
msg_menu:
    .ascii "Seleccione una opción:\n1. Hola\n2. Mundo\n3. Salir\n"
    msg_menu_len = . - msg_menu
msg_option: .ascii "Ingrese una opción: "
    msg_option_len = . - msg_option
msg_invalid: .ascii "Opción inválida\n"
    msg_invalid_len = . - msg_invalid
msg_hello: .ascii "Hola\n"
    msg_hello_len = . - msg_hello
msg_world: .ascii "Mundo\n"
    msg_world_len = . - msg_world
msg_bye: .ascii "Adiós\n"
    msg_bye_len = . - msg_bye
.bss
input_buffer: .skip 64
.text
.global _start
_start:
menu_loop:
    ldr x1, =msg_menu
    mov x2, msg_menu_len
    bl print
    ldr x1, =msg_option
    mov x2, msg_option_len
    bl print
    ldr x0, =input_buffer
    mov x1, #64
    bl read_line
    cmp x0, #-1
    b.eq io_error
    cmp x0, #0
    b.ne .Lmenu_choice
    cbnz x1, menu_done
    b invalid_choice
.Lmenu_choice:
    cmp x0, #1
    b.ne invalid_choice
    ldr x1, =input_buffer
    ldrb w0, [x1]
    cmp w0, #'1'
    b.eq hello
    cmp w0, #'2'
    b.eq world
    cmp w0, #'3'
    b.eq goodbye
    b invalid_choice
hello:
    ldr x1, =msg_hello
    mov x2, msg_hello_len
    bl print
    b menu_loop
world:
    ldr x1, =msg_world
    mov x2, msg_world_len
    bl print
    b menu_loop
invalid_choice:
    ldr x1, =msg_invalid
    mov x2, msg_invalid_len
    bl print
    b menu_loop
goodbye:
    ldr x1, =msg_bye
    mov x2, msg_bye_len
    bl print
menu_done:
    mov x0, #0
    mov x8, #93
    svc #0
print:
    stp x29, x30, [sp, #-16]!
    mov x29, sp
    mov x0, #1
    bl write_all
    cmp x0, #0
    b.lt io_error
    ldp x29, x30, [sp], #16
    ret
