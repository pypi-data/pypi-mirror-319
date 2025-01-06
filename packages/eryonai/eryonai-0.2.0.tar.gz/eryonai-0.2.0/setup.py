from setuptools import setup, find_packages
from setuptools.command.install import install
import os
import subprocess
import sys

class CustomInstallCommand(install):
    def run(self):
        # Verifică dacă se poate interacționa cu utilizatorul
        if sys.stdin.isatty():
            self.show_ascii_art()
            self.ask_play_game()
        else:
            print("Automated installation detected. Skipping interactive setup.")
        
        # Continuă cu instalarea standard
        super().run()

    def show_ascii_art(self):
        ascii_art = """
        .@@@@@@@@@@@@@@@@@=     
        +@@@@@@@@@@@@       @@@@@@@       @@@@@     :@@@@@@@@@@@@@@@@@@@@@+   
        +@@@@@@@@@@@@       .@@@@@@@-      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
        +@@@@+          -@@@: -@@@@@@@@%     =@@@@     %@@@@@-      #@@@  +@@@@%        @@@@@@@@@      @@@@@     +@@@@@@@@@@@@@@@@@@@@@@   
        """
        print(ascii_art)

    def ask_play_game(self):
        # Întreabă utilizatorul dacă vrea să joace un joc
        play_game = input("While you wait, would you like to play a quick game? (Y/N): ").strip().lower()

        if play_game == 'y':
            print("Awesome! Let's start the game!")
            self.run_game()
        else:
            print("No problem! Installation will continue.")
        
    def run_game(self):
        # Verifică dacă fișierul game.py există și îl rulează
        game_script = "game.py"  # Înlocuiește cu calea ta reală a jocului

        if os.path.exists(game_script):
            print(f"Opening {game_script}... Let's have some fun!")
            subprocess.run(["python", game_script])
        else:
            print(f"Error: It seems we can't find {game_script}. Please make sure the script is in the installation folder.")
            
setup(
    name="eryonai",
    version="0.2.0",
    packages=find_packages(),
    install_requires=[
        'requests',
        'torch',
        'transformers',
    ],
    description="Eryon AI is an advanced language model designed for interactive tasks.",
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
