import os
import glob
import imageio.v2 as imageio
from wand.image import Image
import PySimpleGUI as sg
from moviepy.editor import ImageSequenceClip

# Function to create an MP4 movie from images.
def create_mp4(input_folder, output_path, fps):
    # Get a sorted list of image paths.
    image_paths = sorted(
        [
            os.path.join(input_folder, file)
            for file in os.listdir(input_folder)
            if file.lower().endswith((".png", ".jpg", ".jpeg"))
        ]
    )
    # Read in images.
    images = [imageio.imread(path) for path in image_paths]
    if images:
        # Create and write video file.
        clip = ImageSequenceClip(images, fps=fps)
        clip.write_videofile(output_path, codec="mpeg4")


# Function to create a GIF from images.
def create_gif(input_folder, output_path, duration, loop):
    # Ensure output path ends with .gif.
    if not output_path.lower().endswith(".gif"):
        output_path += ".gif"
    # Get a sorted list of image paths.
    image_paths = sorted(
        [
            os.path.join(input_folder, file)
            for file in os.listdir(input_folder)
            if file.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".exr"))
        ]
    )
    # Read in images.
    images = [imageio.imread(path) for path in image_paths]
    if images:
        # Create and write GIF file.
        imageio.mimsave(output_path, images, duration=duration, loop=loop)


# Function to process images with various effects.
def process_images(
    input_folder,
    output_folder,
    dither,
    num_colors,
    pixelate,
    pixelate_factor,
    resize,
    width,
    height,
    rotate,
    angle,
    blur,
    radius,
    mirror,
):
    processing_done = False
    for img_path in glob.glob(os.path.join(input_folder, "*")):
        if img_path.lower().endswith((".png", ".jpg", ".jpeg", ".tiff", ".exr")):
            # Apply requested image processing operations.
            with Image(filename=img_path) as img:
                if dither:
                    img.quantize(number_colors=int(num_colors), dither="riemersma")
                    processing_done = True
                if pixelate:
                    img.resize(
                        int(img.width // pixelate_factor),
                        int(img.height // pixelate_factor),
                    )
                    img.resize(
                        img.width * pixelate_factor, img.height * pixelate_factor
                    )
                    processing_done = True
                if resize:
                    img.resize(width, height)
                    processing_done = True
                if rotate:
                    img.rotate(angle)
                    processing_done = True
                if blur:
                    img.gaussian_blur(radius=radius)
                    processing_done = True
                if mirror:
                    img.flop()
                    processing_done = True
                img.save(
                    filename=os.path.join(output_folder, os.path.basename(img_path))
                )
    return processing_done


# Set up PySimpleGUI.
sg.theme("DarkBlue")

# Define the layout of the GUI.
layout = [
    [
        sg.Text(
            "Process Images bakes input folder images to output folder with selected effects"
        )
    ],
    [
        sg.Text("Input Folder", size=(15, 1)),
        sg.InputText(key="-IN-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Text("Output Folder", size=(15, 1)),
        sg.InputText(key="-OUT-"),
        sg.FolderBrowse(),
    ],
    [
        sg.Checkbox("Dither", key="-DITHER-"),
        sg.InputText(key="-NUM_COLORS-", default_text="256"),
    ],
    [
        sg.Checkbox("Pixelate", key="-PIXELATE-"),
        sg.InputText(key="-PIXELATE_FACTOR-", default_text="1"),
    ],
    [
        sg.Checkbox("Resize", key="-RESIZE-"),
        sg.InputText(key="-WIDTH-", default_text="512"),
        sg.InputText(key="-HEIGHT-", default_text="512"),
    ],
    [
        sg.Checkbox("Rotate", key="-ROTATE-"),
        sg.InputText(key="-ANGLE-", default_text="90"),
    ],
    [sg.Checkbox("Blur", key="-BLUR-"), sg.InputText(key="-RADIUS-", default_text="0")],
    [sg.Checkbox("Mirror", key="-MIRROR-", default=False)],
    [
        sg.Text("MP4 output path"),
        sg.InputText(key="-MP4-"),
        sg.FileSaveAs(file_types=(("MP4 Files", "*.mp4"),)),
    ],
    [sg.Text("MP4 FPS"), sg.InputText(key="-FPS-", default_text="24")],
    [
        sg.Text("GIF output path"),
        sg.InputText(key="-GIF-"),
        sg.FileSaveAs(file_types=(("GIF Files", "*.gif"),)),
    ],
    [sg.Text("GIF delay time in ms"), sg.InputText(key="-DURATION-", default_text="5")],
    [sg.Text("GIF loop count"), sg.InputText(key="-LOOP-", default_text="0")],
    [
        sg.Button("Process Images"),
        sg.Button("Create MP4"),
        sg.Button("Create GIF"),
        sg.Button("Exit"),
    ],
]

# Define icon path.
icon_path = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "data_set_icon_246682.ico"
)
# Create the GUI window.
window = sg.Window("ImageChef", layout, background_color="", icon=icon_path)

# Main event loop.
while True:
    event, values = window.read()
    if event in (None, "Exit"):
        break
    elif event == "Process Images":
        try:
            pixelate_factor = int(values["-PIXELATE_FACTOR-"])
            width = int(values["-WIDTH-"])
            height = int(values["-HEIGHT-"])
            angle = float(values["-ANGLE-"])
            radius = float(values["-RADIUS-"])
            if not values["-IN-"] or not os.path.isdir(values["-IN-"]):
                raise ValueError("Invalid or non-existent input folder")
            if not values["-OUT-"]:
                sg.popup(
                    "No output folder specified, processed images will be saved in the input folder."
                )
        except ValueError as e:
            sg.popup(f"Invalid input: {e}")
            continue

        processing_done = process_images(
            values["-IN-"],
            values["-OUT-"],
            values["-DITHER-"],
            values["-NUM_COLORS-"],
            values["-PIXELATE-"],
            pixelate_factor,
            values["-RESIZE-"],
            width,
            height,
            values["-ROTATE-"],
            angle,
            values["-BLUR-"],
            radius,
            values["-MIRROR-"],
        )
        if processing_done:
            sg.popup("Processing Done")
        else:
            sg.popup("No Processing Done")

    elif event == "Create MP4":
        try:
            fps = int(values["-FPS-"])
            if not values["-IN-"] or not os.path.isdir(values["-IN-"]):
                raise ValueError("Invalid or non-existent input folder")
            if not values["-MP4-"]:
                raise ValueError("Output path for MP4 is empty")
            create_mp4(values["-IN-"], values["-MP4-"], fps)
        except ValueError as e:
            sg.popup(f"Invalid input for MP4 creation: {e}")

    elif event == "Create GIF":
        try:
            duration = float(values["-DURATION-"])
            loop = int(values["-LOOP-"])
            if not values["-OUT-"] or not os.path.isdir(values["-OUT-"]):
                raise ValueError("Invalid or non-existent output folder")
            if not values["-GIF-"]:
                raise ValueError("Output path for GIF is empty")
            create_gif(values["-OUT-"], values["-GIF-"], duration, loop)
        except ValueError as e:
            sg.popup(f"Invalid input for GIF creation: {e}")

window.close()
