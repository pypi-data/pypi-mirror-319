from setuptools import setup, find_packages
from setuptools.command.install import install

class CustomInstallCommand(install):
    def run(self):
        # Standard installation
        super().run()
        
        # Show a thank you message after installing the dependencies
        self.show_thank_you_message()

    def show_thank_you_message(self):
        print("\n\n==================== EryonAI Installation Complete ====================")
        print("Thank you for installing EryonAI! 🎉")
        print("We hope you enjoy using this advanced language model for your interactive tasks.")
        print("If you have any questions, feel free to reach out to us at eryon.ai.company@gmail.com.")
        print("=======================================================================\n")

setup(
    name="eryonai",
    version="0.5.0",
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
