# Wolfenstein-Like Renderer

I find games like *Wolfenstein 3D* to be amazing. It uses a 2D game engine to make something that looks 3D. I was inspired by *Wolfenstein 3D* to make a similar game (or at least a rendering engine) that only displays 2D graphics.  I researched how these types of games work and did my best to emulate it. I looked at various other code projects available online to better learn how this works, but all of the code in this project is entirely my own.

I was already familiar with Arcade, a 2D game engine created for Python, so I decided to use this to make my Renderer. An advantage to Arcade is its speed compared to other Python game libraries. I may eventually make a similar renderer in C++ to improve speed, but I only have plans for Python right now.

### Part One: Map and Player Character

Firstly, we need a map and a player to run around the map. This is easy enough to do using Arcade:

![top_view_no_rays](https://github.com/Melon-Catastrophe/Wolfenstein-like-Renderer/blob/master/resources/doc/top_view_no_rays.gif?raw=true)

### Part Two: Raycasting

One of the most important parts of making this style of 3D renderer is to design a Raycaster. Raycasting sends a myriad of rays out from the player to the world within the player's Field of View. The rays will stop when they hit something. The distance of each ray will tell us how tall we should make each section of wall. A visualization of these rays can be seen below.

![raycasting](https://github.com/Melon-Catastrophe/Wolfenstein-like-Renderer/blob/master/resources/doc/raycasting.gif?raw=true)

### Part Three: Object Rendering

Now we can render a wall for each ray that was calculated. For each ray, we will draw one vertical rectangle. The width of the rectangle will be determined by the number of rays divided by the width of the screen. The height of the rectangles is determined by the length of each calculated ray. The longer the ray, the shorter the drawn rectangle will be. 

By drawing these rectangles one after another, we can get a result like the one below:

​	![fpv_white](https://github.com/Melon-Catastrophe/Wolfenstein-like-Renderer/blob/master/resources/doc/fpv_white.gif?raw=true)

This looks like a good proof-of-concept, but it is pretty difficult to see depth information. We can change that by assigning a grayscale value to each wall that changes depending on its y-coordinate. This is shown below:

![fpv_grayscale](https://github.com/Melon-Catastrophe/Wolfenstein-like-Renderer/blob/master/resources/doc/fpv_grayscale.gif?raw=true)

As you can see, it is a lot easier now to see depth. You may also notice that certain walls look pretty distorted. I believe this is because no calculations are being performed to simulate a perspective plane. 

### Conclusion

Creating this type of renderer was a challenge, but it was also a lot of fun! I learned a lot about how these types of renderers work and what some of their weaknesses are. If I were to continue this project, I think I would add an actual perspective so that there would be less distortions in the final result.
