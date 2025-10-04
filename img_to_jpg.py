import os
from PIL import Image


def convert_to_jpg(input_folder, output_folder):
    # Create output folder if it doesn't exist
    os.makedirs(output_folder, exist_ok=True)

    # Supported input formats
    valid_extensions = (".jpg", ".jpeg", ".png", ".jfif")

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(valid_extensions):
            input_path = os.path.join(input_folder, filename)
            base_name, _ = os.path.splitext(filename)
            output_filename = base_name + ".jpg"
            output_path = os.path.join(output_folder, output_filename)
            if os.path.exists(output_path):
                print(f"File already exists, skipping: {output_path}")
                continue

            try:
                with Image.open(input_path) as img:
                    rgb_img = img.convert("RGB")
                    rgb_img.save(output_path, "JPEG")
            except Exception as e:
                print(f"Error processing {filename}: {e}")


# Set input and output directories
input_directory = "./imgs"
output_directory = "./converted_imgs"

convert_to_jpg(input_directory, output_directory)
