import os
import shutil
import glob
import stat
import platform
from setuptools import setup, find_packages

def additional_setup():
    # Get the user's home directory
    user_home = os.path.expanduser('~')

    # Set platform-specific variables
    if platform.system() == "Linux":
        crl_browser_dir = os.path.join(user_home, '.local', 'share', 'crl-browser')
        bin_dir = os.path.join(user_home, '.local', 'share', 'bin', 'crl-browser')
        bashrc_path = os.path.join(user_home, '.bashrc')
        shell_name = "bash"
    elif platform.system() == "Darwin":  # macOS
        crl_browser_dir = os.path.join(user_home, 'Library', 'Application Support', 'crl-browser')
        bin_dir = os.path.join(user_home, 'bin', 'crl-browser')
        bashrc_path = os.path.join(user_home, '.zshrc')  # Use zshrc for macOS
        shell_name = "zsh"
    elif platform.system() == "Windows":
        crl_browser_dir = os.path.join(user_home, 'AppData', 'Local', 'crl-browser')
        bin_dir = os.path.join(user_home, 'AppData', 'Local', 'bin', 'crl-browser')
        bashrc_path = os.path.join(user_home, '.bash_profile')  # For Windows WSL, for example
        shell_name = "bash"
    else:
        raise OSError("Unsupported platform")

    # Ensure the directories exist
    os.makedirs(crl_browser_dir, exist_ok=True)
    os.makedirs(bin_dir, exist_ok=True)

    # Copy the source directory
    src_dir = 'crl_browser/crl-desktop-sources-index'  # Source directory
    dst_dir = os.path.join(crl_browser_dir, 'crl-desktop-sources-index')

    if os.path.isdir(src_dir):
        # If the destination directory exists, remove it before copying
        if os.path.isdir(dst_dir):
            shutil.rmtree(dst_dir)
        shutil.copytree(src_dir, dst_dir)

    # Copy Python files to the bin directory
    python_files = glob.glob('./crl_browser/*.py')  # Find all .py files in the current directory
    for file in python_files:
        shutil.copy(file, bin_dir)

    # Set file permissions to 644
    for root, dirs, files in os.walk(crl_browser_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    for root, dirs, files in os.walk(bin_dir):
        for file in files:
            file_path = os.path.join(root, file)
            os.chmod(file_path, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)

    # Update PATH in the appropriate shell configuration file
    with open(bashrc_path, 'a') as bashrc:
        bashrc.write(f'\n# crl-browser environment\n')
        bashrc.write(f'export PATH={user_home}/.local/share/bin/crl-browser:$PATH\n')

    print(f"Setup completed successfully. Please restart your terminal for changes to take effect.")

setup(
    name="crl-advanced",
    version="2.0.0-beta.1",
    packages=find_packages(),
    install_requires=[
        'PyQt6',
        'requests',
        'psutil',
        'argparse',
        'Cython',
    ],
    entry_points={
        'console_scripts': [
            'crl-browser=crl_browser.crl_browser:main',
        ],
    },
    description="Configuration and setup for CRL Browser",
    author="Zaman",
    author_email="zipishuseyinli25@gmail.com",
    license="GPL-2.0",  # Add license type here
    long_description=open('README.md').read(),  # Read the README.md for project details
    long_description_content_type="text/markdown",
)

# Run the additional setup
if __name__ == "__main__":
    additional_setup()
