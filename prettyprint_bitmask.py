import struct


def pretty_print32(x, long=False):
    """
    Accepts a 32-bit integer and returns a string showing the values
    of each bit in the number. Useful for comparing error status to
    bitmask tables in TRDI PD0 documentation.

    Accepts an optional boolean argument long for specifying long output or
    wide output. The default behavior is wide output (long=False.)
    """
    esw = x + 2 ** 32 if x < 0 else x
    s = ""
    if long:
        prefix = [
            "LSW 00: ", "LSW 01: ", "LSW 02: ", "LSW 03: ",
            "LSW 04: ", "LSW 05: ", "LSW 06: ", "LSW 07: ",
            "LSW 08: ", "LSW 09: ", "LSW 10: ", "LSW 11: ",
            "LSW 12: ", "LSW 13: ", "LSW 14: ", "LSW 15: ",
            "MSW 00: ", "MSW 01: ", "MSW 02: ", "MSW 03: ",
            "MSW 04: ", "MSW 05: ", "MSW 06: ", "MSW 07: ",
            "MSW 08: ", "MSW 09: ", "MSW 10: ", "MSW 11: ",
            "MSW 12: ", "MSW 13: ", "MSW 14: ", "MSW 15: ",
        ]
        mask = 0b1
        for i in range(0,32):
            c = '1' if esw & (mask << i) else '0'
            s += prefix[i] + c + '\n'
    else:
        seps = [
            "Low 16 BITS\nLSB\nBITS 07 06 05 04 03 02 01 00\n      ",
            "\nMSB\nBITS 15 14 13 12 11 10 09 08\n      ",
            "\nHigh 16 BITS\nLSB\nBITS 07 06 05 04 03 02 01 00\n      ",
            "\nMSB\nBITS 15 14 13 12 11 10 09 08\n      ",
        ]
        esb = struct.pack('<I', esw)
        for sep, byte in zip(seps, esb):
            s += sep
            for c in f'{byte:08b}':
                s += f'{c:3s}'
    return s


def pretty_print16(x, long=False):
    """
    Accepts a 16-bit integer and returns a string showing the values
    of each bit in the number. Useful for comparing BIT result to
    bitmask tables in TRDI PD0 documentation.

    Accepts an optional boolean argument long for specifying long output or
    wide output. The default behavior is wide output (long=False.)
    """
    esw = x + 2 ** 16 if x < 0 else x
    s = ""
    if long:
        prefix = [
            "LSB 00: ", "LSB 01: ", "LSB 02: ", "LSB 03: ",
            "LSB 04: ", "LSB 05: ", "LSB 06: ", "LSB 07: ",
            "MSB 00: ", "MSB 01: ", "MSB 02: ", "MSB 03: ",
            "MSB 04: ", "MSB 05: ", "MSB 06: ", "MSB 07: ",

        ]

        mask = 0b1
        s += ""
        for i in range(0,16):
            c = '1' if esw & (mask << i) else '0'
            s += prefix[i] + c + '\n'
    else:
        seps = [
            "LSB 07 06 05 04 03 02 01 00\n     ",
            "\nMSB 07 06 05 04 03 02 01 00\n     ",
        ]
        esb = struct.pack('<H', esw)
        for sep, byte in zip(seps, esb):
            s += sep
            for c in f'{byte:08b}':
                s += f'{c:3s}'
    return s