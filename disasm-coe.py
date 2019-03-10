# -*- coding: utf-8 -*-
import capstone as cs

'''
#### `.coe` File Format Example

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

> Note:  
> - The leading two lines are required!
> - One instruction word per line only!
> - Instruction words must be found in the first column!
> - Instruction words are in __BIG ENDIAN__!
'''

######## Configurations - CHANGE ME !!! ########

# path to `.coe` file to be disassemblied
filename = './ram_init_os.coe'


######## Helper Functions ########

def chr_to_num(in_: str):
    if len(in_) != 1:
        raise ValueError('{}: in_ = \'{}\''.format('chr_to_num', in_))
    if in_ in '1234567890':
        return ord(in_) - ord('0')
    if in_ in 'abcdef':
        return ord(in_) - ord('a') + 10
    if in_ in 'ABCDEF':
        return ord(in_) - ord('A') + 10
    raise ValueError()

def str_to_byte(in_: str):
    if len(in_) != 2:
        raise ValueError('{}: in_ = \'{}\''.format('str_to_byte', in_))
    return chr_to_num(in_[0]) * 16 + chr_to_num(in_[1])


def word_to_intlist(in_: str):
    if len(in_) != 8:
        raise ValueError('{}: in_ = \'{}\''.format('word_to_intlist', in_))
    bytelist = []
    for plc in range(0, 8, 2):
        bytelist.append(str_to_byte(in_[plc:plc+2]))
    return bytelist


######### Main #########

bytelist = []   # list of int
with open(filename, 'r') as coefile:
    # skip file property lines
    coefile.readline()
    coefile.readline()
    for lineno, line in enumerate(coefile):
        if line.strip() == ';':
            break
        try:
            bytelist.extend(word_to_intlist(line.split(' ')[0]))
        except ValueError as e:
            print('Caught ValueError: {}'.format(e))
            break
    print('')

md = cs.Cs(cs.CS_ARCH_MIPS, cs.CS_MODE_MIPS32 + cs.CS_MODE_BIG_ENDIAN)
md.mnemonic_setup(cs.mips.MIPS_INS_AUI, 'lui')
code = bytes(bytelist)

print('Address     Word       Instruction')
print('=======     ====       ===========')
print('')

__guess_seg_end = False     # static variable of `likely_segment_end()`
def likely_segment_end(mne: str):
    '''
    It is naiively believed that on a platform with delay slot, unconditional
    branching / jumping followed by an empty delay slot, i.e. `nop`, is likely
    indicating a `goto` / `return` statement in disassembly.

    Inserting an empty line in the output is definitely good for your eyes.
    '''
    global __guess_seg_end
    if (mne[0] in 'j') or (mne in ['b', 'sdbbp', 'eret']):
        __guess_seg_end = True
    elif __guess_seg_end and mne == 'nop':
        __guess_seg_end = False
        return True
    return False

for instr in md.disasm(code, 0xbfc00000):
    print('0x{:8x}: {:8s}   {:<7s}{:s}'.format(
        instr.address, instr.bytes.hex(), instr.mnemonic, instr.op_str
    ))
    if likely_segment_end(instr.mnemonic):
        print('')
