Program 3

WARNING: THERE ARE NOISES IN THIS PROGRAM. PLEASE ADJUST YOUR VOLUME ACCORDINGLY. (The Volume has been set to a safe level, but if you are wearing headphones, you may be surprised)

Overview: This program was meant to create a firework using pyOpenGL.

Use: Create a Firework object and then call its render method within the infinite loop

Options:

Firework(nump, type, startTime, endTime, startPOS, length, level, split, color)

nump: Number of particles to include in the firework
type: Either "normal", which creates a firework that just shoots straight up, or "spin", which creates a firework that spins as it goes up
startTime: simulation time to launch the firework
endTime: simulation time to stop rendering the firework
startPOS: coordinates of where to launch the firework from
length: length of the tail for each particle
level: level of recursion.  Should be set to 0 as a default
split: True makes the firework split when it stops rendering, False keeps it normal
color: color of the firework.  If no color is inserted, a random assortment of colors is generated for each particle.

Features:
The program features the ability to create fireworks with a multitude of different options.  It also includes sounds for the fireworks ascent, explosion, and the assumed audience. The audience's reaction
is not the same to each firework each time but, is instead, randomly selected from 3 sound bytes, and are played randomly for each particle that the firework releases.  I also added in ambient noises, so there is
never a moment were the display is completely silent.