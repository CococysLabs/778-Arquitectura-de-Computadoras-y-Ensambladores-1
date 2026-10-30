.text
.global _start
_start:
    mov x9, #0xaa
    mov x10, #0x0f
    and x11, x9, x10
    orr x12, x9, x10
    eor x13, x9, x10
    bic x14, x9, x10
    lsl x15, x9, #1        // Registro de 64 bits: no se limita a un byte.
    lsr x16, x9, #1
    mov x17, #-8
    asr x18, x17, #1

resultados:
    mov x0, #0
    mov x8, #93
    svc #0
