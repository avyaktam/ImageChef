	 _ _|                                  ___|  |             _| 
	   |   __ `__ \    _` |   _` |   _ \  |      __ \    _ \  |   
	   |   |   |   |  (   |  (   |   __/  |      | | |   __/  __| 
	 ___| _|  _|  _| \__,_| \__, | \___| \____| _| |_| \___| _|   
                        |___/                                 

ImageChef is a Python tool for batch processing of images with a variety of effects. It also allows you to create MP4 videos and GIFs from a series of images. The tool is built on several Python libraries and presents a GUI for easy interaction.

Apply a variety of image effects: dithering, pixelating, resizing, rotating, blurring, and mirroring.
Create MP4 movies from a series of images.
Create GIFs from a series of images.

Installation

First, clone the repository to your local machine:

	git clone https://github.com/avyaktam/imagechef.git
	cd imagechef

Before running the script, you need to install the necessary dependencies. 
    
    pip install imageio
    pip install Wand
    pip install PySimpleGUI
    pip install moviepy

This script requires ImageMagick to be installed on your system because it uses the Wand library for image manipulation. You can download ImageMagick from their official site(https://imagemagick.org/script/download.php). Make sure to install the version of ImageMagick that corresponds with your Python version (i.e., 32-bit or 64-bit).

During the installation of ImageMagick, please ensure you check the box that says "Add application directory to your system path" for Windows, or make sure to add it manually to your PATH environment variable if you're on Linux or MacOS.

The script can be launched by either running the imagechef.py script directly with Python:

    python imagechef.py

Or by executing the provided batch file, if you're on Windows

![ImageChefGUI](https://github.com/avyaktam/ImageChef/assets/82269309/7c5fd5b4-a095-4b40-b42d-cb4c8b730d00)

