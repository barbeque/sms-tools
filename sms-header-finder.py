import sys

if len(sys.argv) < 2:
	print('need an argument')
	sys.exit(1)

junk = []
with open(sys.argv[1], 'rb') as f:
	junk = f.read()

POSSIBLE_OFFSETS = [0x1ff0, 0x3ff0, 0x7ff0]
found_it = False
for offset in POSSIBLE_OFFSETS:
	sliced = junk[offset : offset + 8]
	assert(len(sliced) == 8)
	if junk[offset:offset + 8] == b'TMR SEGA':
		print('Found TMR SEGA header at', hex(offset))
		found_it = True
		break

if not found_it:
	print('Could not find a TMR SEGA header. Might be a Japanese ROM.')
