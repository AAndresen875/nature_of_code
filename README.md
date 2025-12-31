# nature_of_code
study notes for the nature of code

The book can be found here https://natureofcode.com/
Their github: https://github.com/nature-of-code/noc-book-2?tab=readme-ov-file
Another github with python examples: https://github.com/Oenarion/Ecosystem/tree/main

# Environment management and GUI notes:
I have notes on various "animation" or visualization packages in the "animation toolkit" related to choosing a specific package for the simulation visualization. Certain options are dead ends and I did not continue with the example, but I do have content breif examples of different packages. 

I am working on a windows machine using windows subsystem for linux. I am doing environment management with conda, and the installation packages required can be found in the requirements.txt file.

I am using the ubuntu distribution and I needed to install WSLg [docs](https://github.com/microsoft/wslg). I followed the installation instructions under "Install instructions (Existing WSL install)" and I just installed Gedit and X11 apps. For vispy, I also needed to install OpenGL dependencies which I did with: `sudo apt install -y mesa-utils libgl1-mesa-glx libglu1-mesa`. I will be using EGL backend which is designed for headless/server environments and should work with WSLg.

# Code review checklist:
1. Is there additional cleaning up that needs to be done?
2. are the classes defined logically in the cardonality to each other and file location?
3. Are you using doc strings on all classes and methods?

Wishlist (to add):
1. test coverage
2. linting
3. CI/CD pipeline