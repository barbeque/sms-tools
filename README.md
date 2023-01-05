# SMS Tools

## The Tools
 * `sms-header-finder.py`: Checks a ROM image to see if its "TMR SEGA" header is at a valid location. It doesn't currently compute the checksum.
 * `sms-header-injector.py`: Injects a valid header into an 8kB ROM image, including the checksum.
 * `snail-game-patcher.py`: Patches a v1.3 SMS BIOS so that it can be booted as a cartridge, and loads the built-in _Snail Maze_ game immediately.

## How to make a _Snail Maze_ cartridge?
By hacking up the v1.3 SMS BIOS, you too can get a dedicated _Snail Maze_ ROM.

Here's how you do it:
 1. Find an 8-kilobyte v1.3 SMS BIOS ROM whose MD5 matches `840481177270d5642a14ca71ee72844c`
 2. Use the `snail-game-patcher.py` script on it to patch out the check for "cartridge inserted" on that SMS BIOS ROM. It will now jump right into _Snail Maze_.
 3. Use the `sms-header-injector.py` script on the result of step 2 (which should be called something like `patched.sms`.) This will add the header information that makes the export SMS BIOS think it is a cartridge.
 4. You should now have a ROM image called `header.sms` with the MD5 of `20da321e16a2f50590820b6b50c5d633`.
 5. Run that image, and after the second Sega logo (the music and animation is just too good) your export SMS should jump right into _Snail Maze_. Enjoy it, or not.

Here's what happens:
 1. When the SMS is turned on, its internal BIOS looks for a cartridge to run. It looks in a few different places for this, such as $1ff0, which is where we put our modified header in the v1.3 image.
 2. Finding the "TMR SEGA" header at $1ff0, it then goes on to do a bunch of other checks (checksum, region, etc)
 3. Once it's happy with that, it boots the cartridge.
 4. The cartridge, however, is a copy of the v1.3 SMS BIOS that we've modified.
 5. Rather than check for a cartridge _again_, this "inner BIOS" just jumps right to _Snail Maze_.

## Special Thanks To
 * [Masible Prod](https://github.com/masible/smssum)'s SMSSum, which was used to sanity-check my checksum generation (it was off by one.)
 * [segmtfault from SMSPower](https://www.smspower.org/forums/15317-BIOS13FullyCommentedDisassembly) and their excellent commented disassembly of the v1.3 SMS BIOS, which sped things up greatly.
 * Nicole from [Nicole Express](https://nicole.express/), who pointed me to the aforementioned disassembly and saved me at least an evening of debugger poking
