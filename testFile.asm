.section .text
    ADDI t1, t0, 20
    ADDI t2, t0, 30
    SUB t3, t1, t2
    PUTI t3
    LUI t4, 0x10000
    PUTS t4

.section .strings
    0x10000000 "Hello world\n"