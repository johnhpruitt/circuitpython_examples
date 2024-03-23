# 1_button_light_control
One button light controller using neopixels and an Adafruit KB2040

## What is this project for?
I want to use this light for photographing Gundam, 30 Minute Missions, and other little hobby models I build to relax. 
It has a few modes that look like fire, rainbows, or police lights if you bounce it off a background or use a diffuser.

## One Button Controls
1. Short presses = select a light mode 1-6
3. Long press = stop a light mode (because if the light mode uses time.sleep() a short press wont be recognized)
4. Short + Long Press = flashlight / basic white mode. 
5. Short + Short + Long Press = programatic reset, because putting the hand wired switch down and fumbling for the reset on board is annoying.

## What other projects did it depend on?
1. [Adafruit LED Animations (CircuitPython Libraries)](https://github.com/adafruit/Adafruit_CircuitPython_LED_Animation/tree/main)

## Why do this at all? Why those hardware choices?
All of these parts were impulse purchases at MicroCenter while I was working on keyboards and other raspberry pi pico projects. 
There are definitely better form factors to fit them in a case, or pico boards that provide battery managment.

There is certainly a multi-button proper mount for 4 keyswitches available from Adafruit that connects over stemmaQT. I'm using it for another pico project.

Everything in this build was laying around so I just soldered two leads onto a single cherry style switch and made it work.
The price was right.
