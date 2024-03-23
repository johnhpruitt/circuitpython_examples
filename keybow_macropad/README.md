# Keybow2040 Macropad

## What is this project for?
This project is forked from [NevynUK's macropad for the Keybow2040](https://github.com/NevynUK/Keybow2040). I found this project when I was looking for a different way to organize macropads, other than the delivered examples.  

The default examples are great, but they put a lot of logic in the while() loop for keybow.update() and I wanted to set some colors or custom release code. When I put those in the big while() loop, it   really messed with timing and the board flashed a few times before it crashed.

NevynUK's project put almost all that logic on key releases instead of during the while loop, and that solved my problem.

## What other projects did it depend on?
1. [Assembly instructions from Pimoroni](https://learn.pimoroni.com/article/assembling-keybow-2040)
2. [PMK](https://github.com/pimoroni/pmk-circuitpython): Pimoroni provides a library to interface with two of their Raspberry Pi 2040 based kaypads.
3. [Pimoroni CircuitPython tutorial](https://learn.pimoroni.com/article/circuitpython-and-keybow-2040): This will show you how do get the right version of circuitpython flashed to the Keybow2040 and download the Adafruit HID libraries.

## Why do this at all?
 My other macropad had a failed controller. Rather then drop in another Pro Micro and flash it with QMK, I bought a [Keybow2040 by Pimoroni](https://shop.pimoroni.com/products/keybow-2040) to learn more about circuitpython. I have an extra [Adafruit KB2040](https://www.adafruit.com/product/5302) now, if I want to revive that older board.
