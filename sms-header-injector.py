# Builds a valid ROM based on one that doesn't have a ROM
# works for 8k ROMs only for now

import sys, os

if len(sys.argv) < 2:
	print('Usage:', sys.argv[0], '<ROM file>')
	sys.exit(1)

rom = []
with open(sys.argv[1], 'rb') as f:
	rom = bytearray(f.read())

assert(len(rom) >= 8192)

# generate the mutant version of the ROM using hard coded bullshit
def overwrite(rom, start_address, new_bytes):
	assert(start_address + len(new_bytes) <= len(rom))
	for i in range(len(new_bytes)):
		rom[start_address + i] = new_bytes[i]
	return rom

# produce the two-byte little endian checksum of the ROM
# that the SMS BIOS will want to see
def calculate_checksum(rom):
	checksum = 0
	for i in range(0x0000, 0x1fef):
		checksum += rom[i]
	# hack it into a 2 byte location idk?
	# little endian, remember
	return [ (checksum & 0x00ff) - 1, ((checksum & 0xff00) >> 8) + 1 ]

checksum = calculate_checksum(rom)

# https://www.smspower.org/Development/ROMHeader
old_len = len(rom)
# TMR SEGA header
overwrite(rom, 0x1ff0, b'TMR SEGA')
assert(len(rom) == old_len)
# reserved space
overwrite(rom, 0x1ff8, [ 0, 0 ])
assert(len(rom) == old_len)
# Checksum:
overwrite(rom, 0x1ffa, checksum)
# product code
overwrite(rom, 0x1ffc, [ 0, 0 ])
# high 4 bits of product code + version nibble
overwrite(rom, 0x1ffe, [ 0 ])
# SMS region code (high 4 bits) + rom size (low 4 bits)
region_code = 0x04 # SMS Export
rom_size = 0x0a # 8KB (unused by retail games)
overwrite(rom, 0x1fff, [ (region_code << 4) | rom_size])

with open('header.sms', 'wb') as f:
	f.write(rom)
