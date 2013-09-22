# Run this when booting the Raspberry Pi in order to turn
# on and configure the display

from lib.gpio import blink
from time import sleep

menu = 11
up = 10
right = 9

d = 0.2

# turn on the display and wait for it to come on
blink(menu, d)
sleep(3)

# turn on the menu
blink(menu, d)
sleep(1)

# move down to the second row
for i in range(7):
  blink(up, d)
  sleep(0.25)

# move to the right
blink(right, d)
