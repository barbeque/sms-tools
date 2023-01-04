import sys

if len(sys.argv) < 2:
	print('need an argument')
	sys.exit(1)

junk = []
with open(sys.argv[1], 'rb') as f:
	junk = f.read()
print('ROM length', len(junk))

POSSIBLE_OFFSETS = [0x1ff0, 0x3ff0, 0x7ff0]
found_it = False
# now search the entire rom for it
for i in range(0, len(junk) - 8):
	chunk = junk[i : i + 8]
	if chunk == b'TMR SEGA':
		print('Found TMR SEGA header at', hex(i))
		if i not in POSSIBLE_OFFSETS:
			print('This is an unexpected location')
		found_it = True
		break

if not found_it:
	print('TMR SEGA header could not be found. Maybe a Japanese ROM?')
