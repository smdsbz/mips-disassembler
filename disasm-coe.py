# -*- coding: utf-8 -*-
import capstone as cs


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

filename = './ram_init_os.coe'
bytelist = []   # list of int
with open(filename, 'r') as coefile:
    # skip file property lines
    coefile.readline()
    coefile.readline()
    # parse __FORMATTED__ vector
    for lineno, line in enumerate(coefile):
        # print('processing line No.{}'.format(lineno), end='\r')
        try:
            bytelist.extend(word_to_intlist(line.split(' ')[0]))
        except ValueError as e:
            # print('Caught ValueError: ', end='')
            # print(e)
            break
    print('')

md = cs.Cs(cs.CS_ARCH_MIPS, cs.CS_MODE_MIPS32 + cs.CS_MODE_BIG_ENDIAN)
md.mnemonic_setup(cs.mips.MIPS_INS_AUI, 'lui')
code = bytes(bytelist)
print('Address     Word       Instruction')
print('=======     ====       ===========')

for instr in md.disasm(code, 0xbfc00000):
    print('0x{:8x}: {:8s}   {:<7s}{:s}'.format(
        instr.address, instr.bytes.hex(), instr.mnemonic, instr.op_str
    ))
