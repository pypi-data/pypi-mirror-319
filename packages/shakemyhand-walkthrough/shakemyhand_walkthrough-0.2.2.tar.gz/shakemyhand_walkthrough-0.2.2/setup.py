from setuptools import setup, find_packages

setup(
    name="shakemyhand-walkthrough",
    version="0.2.2",
    description="Interactive Python walkthrough for the 'Shake My Hand' 2025 Iris CTF challenge",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Admiral SYN-ACKbar",
    author_email="admiral@admiralsyn-ackbar.com",
    url="https://github.com/admiralsyn-ackbar/shakemyhand-walkthrough",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        "scapy>=2.5.0"
    ],
    entry_points={
        "console_scripts": [
            "shakemyhand-walkthrough=shakemyhand_walkthrough.shakemyhand_walkthrough:main"
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.7',
)
