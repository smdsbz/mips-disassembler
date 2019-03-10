# mips-disassembler
Bakup port for a simple MIPS disassembler script built upon `capstone`. Takes `.coe` files in, spits human readable out.

## Sample Output

```asm

Address     Word       Instruction
=======     ====       ===========

0xbfc00000: 3c069fc0   lui    $a2, 0x9fc0
0xbfc00004: 24c60014   addiu  $a2, $a2, 0x14
0xbfc00008: 00c00008   jr     $a2
0xbfc0000c: 40804800   mtc0   $zero, $t1, 0
0xbfc00010: 00000000   nop    

0xbfc00014: 40116000   mfc0   $s1, $t4, 0
0xbfc00018: 7e3104c0   ext    $s1, $s1, 0x13, 1
0xbfc0001c: 12200002   beqz   $s1, 0xbfc00028
0xbfc00020: 00000000   nop    
0xbfc00024: 7000003f   sdbbp  
0xbfc00028: 3c069fc0   lui    $a2, 0x9fc0
0xbfc0002c: 24c60288   addiu  $a2, $a2, 0x288
0xbfc00030: 00c0f809   jalr   $a2
0xbfc00034: 00000000   nop    

0xbfc00038: 3c069fc0   lui    $a2, 0x9fc0
0xbfc0003c: 24c60308   addiu  $a2, $a2, 0x308
0xbfc00040: 00000000   nop    
0xbfc00044: 3c069fc0   lui    $a2, 0x9fc0
0xbfc00048: 24c600a4   addiu  $a2, $a2, 0xa4
0xbfc0004c: 00c0f809   jalr   $a2
0xbfc00050: 00000000   nop    

```

## Input File Example

```text
memory_initialization_radix=16;
memory_initialization_vector=
3C10BFC0 00000000 00000000 00000000
36100000 00000000 00000000 00000000
BE090010 00000000 00000000 00000000
8E110000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
00000000 00000000 00000000 00000000
;
```

For explicit restrictions, see heading of the script `disasm-coe.py`.  
