from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess

class CustomInstallCommand(install):
    def run(self):
        ascii_art = """
                                                                                                                                      
                                                                                                                                      
                                                                                                              .@@@@@@@@@@@@@@@@@=     
   +@@@@@@@@@@@@                                                                    @@@@@@@       @@@@@     :@@@@@@@@@@@@@@@@@@@@@+   
   +@@@@@@@@@@@@                                                                   .@@@@@@@-      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@+          -@@@: -@@@@@@@@%     =@@@@     %@@@@@-      #@@@  +@@@@%        @@@@@@@@@      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@+          *@@@@@@@@@*:@@@@+    @@@@+  *@@@@@@@@@@@    @@@@@@@@@@@@@.     =@@@@ @@@@#     @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@@@@@@@@    *@@@@@@=:-  +@@@@   @@@@@  #@@@@@  =@@@@@   @@@@@@-.*@@@@@     @@@@- =@@@@     @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@@@@@@@@    *@@@@#       @@@@@  @@@@   @@@@@    +@@@@#  @@@@@    @@@@@    #@@@@   @@@@@    @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@+          *@@@@-        @@@@-@@@@+   @@@@@    -@@@@@  @@@@@    @@@@@   :@@@@@@@@@@@@@-   @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@+          *@@@@-        :@@@@@@@@    @@@@@.   @@@@@=  @@@@@    @@@@@   @@@@@@@@@@@@@@@   @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@@@@@@@@@=  *@@@@-         #@@@@@@:    :@@@@@@@@@@@@@   @@@@@    @@@@@  -@@@@=     #@@@@-  @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
   +@@@@@@@@@@@@+  *@@@@-          @@@@@#       @@@@@@@@@@.    @@@@@    @@@@@  @@@@@       @@@@@  @@@@@      @@@@@@@@@@@@@@@@@@@@@.   
                                   @@@@@           =**+.                                                      -@@@@@@@@@@@@@@@@@:     
                               .@@@@@@@                                                                                               
                               %@@@@@%                                                                                                
                                                                                                                                      
                                                                                                                                                                                                                                    
                                                                                                                                                                                                                                                                                                                                                                                                                                             
"""

# Print the ASCII art
        print(ascii_art)


        # Custom text displayed during installation
        print("\n\n==================== EryonAI Installation ====================")
        print("EryonAI is being installed. This process shouldn't take too long.")
        print("=================================================================\n")
        
        # Ask user if they want to play a game
        play_game = input("While you wait, would you like to play a quick game? (Y/N): ").strip().lower()

        if play_game == 'y':
            print("Awesome! I'll open a game for you to enjoy while the installation completes.")
            self.run_game()
        else:
            print("No problem! Feel free to relax while EryonAI gets set up.")
        
        # Continue with the regular installation
        super().run()

    def run_game(self):
        # Path to the game script
        game_script = "game.py"  # Replace with your Python game script

        # Check if the game script exists and run it
        if os.path.exists(game_script):
            print(f"Opening {game_script}... Let's have some fun!")
            subprocess.run(["python", game_script])
        else:
            print(f"Error: It seems we can't find {game_script}. Please make sure the script is in the installation folder.")

setup(
    name="eryonai",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'torch',
        'transformers',
    ],
    description="Eryon AI is an advanced language model designed for interactive tasks, integrating natural language processing with features like Wikipedia search and memory management. It enhances real-time responses by leveraging information from Wikipedia and recalling previously stored memories for more personalized interactions.",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author="EryonAI",
    author_email="eryon.ai.company@gmail.com",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
)
