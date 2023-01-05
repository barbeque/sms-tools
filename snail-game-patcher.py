# Patches a 1.3 BIOS ROM to jump directly to snail game
# Must re-checksum after this

import os, sys

if len(sys.argv) < 2:
	print("usage:", sys.argv[0], "<BIOS ROM file>")
	sys.exit(1)

rom = []
with open(sys.argv[1], 'rb') as f:
	rom = bytearray(f.read())

# now replace some bytes
target = 0x0114
search = [ 0xcd, 0x00, 0xc7 ] # CALL $c700 (cartridge checker)
replace = [ 0xc3, 0x90, 0x0b ] # JP $0b90

assert(len(search) == len(replace))

for i in range(len(search)):
	if rom[target + i] != search[i]:
		print("Expected to see", hex(search[i]), "at", hex(target+i), "but found", hex(rom[target+i]), "instead.")
		sys.exit(2)
	else:
		rom[target + i] = replace[i]

with open('patched.sms', 'wb') as f:
	f.write(rom)
