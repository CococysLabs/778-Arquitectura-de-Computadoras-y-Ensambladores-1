.include "io.s"
.data
msg: .ascii "Hello, World!\n"
    msg_len = . - msg

.text
.global _start

_start:
    // write(1, dirección, longitud)
    ldr x1, =msg            // dirección del mensaje
    mov x2, msg_len         // longitud del mensaje
    mov x0, #1              // stdout
    bl write_all
    cmp x0, #0
    b.lt io_error

    // exit(0)
    mov x0, #0              // código de salida
    mov x8, #93             // syscall de salida
    svc #0                  // ejecutar syscall

// print("Hello, World!\n")
