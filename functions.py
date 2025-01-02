# functions.py
import os
import zipfile
from PIL import Image
import io
from rembg import remove

# Function to create an output folder based on the ZIP file name
def create_output_folder(zip_file_path, output_dir):
    zip_name = os.path.splitext(os.path.basename(zip_file_path))[0]  # Extracts the file name without extension
    output_folder = os.path.join(output_dir, zip_name)  # Creates a folder path using the output directory and the zip file name
    os.makedirs(output_folder, exist_ok=True)  # Creates the folder if it doesn't exist
    return output_folder  # Returns the path to the created folder

# Main function to process images from a ZIP file
def process_images(zip_file_path, output_dir, update_status_callback, running_flag):
    try:
        # Step 1: Create the output folder
        output_folder = create_output_folder(zip_file_path, output_dir)

        # Step 2: Extract images from the ZIP file into a temporary folder
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            zip_ref.extractall('temp_images')  # Extract all files to 'temp_images' directory

        # Step 3: Get a list of images in the extracted folder
        images = [f for f in os.listdir('temp_images') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]

        # Step 4: Process each image
        for image_name in images:
            if not running_flag():  # Checks if the process has been stopped
                update_status_callback("Process stopped.")  # Updates the status to 'stopped'
                break  # Exits the loop if the process is stopped
            update_status_callback(f"Processing {image_name}...")  # Updates status for each image being processed
            process_single_image(image_name, output_folder)  # Processes the individual image

        # Final status update
        update_status_callback("Process completed." if running_flag() else "Process stopped.")
    except Exception as e:
        update_status_callback(f"An error occurred: {e}")  # If an error occurs, update the status with the error message
    finally:
        cleanup_temp_folder()  # Cleans up the temporary extracted folder

# Function to process a single image (removes background and saves the processed image)
def process_single_image(image_name, output_folder):
    try:
        image_path = os.path.join('temp_images', image_name)  # Full path to the image file in the temp folder
        with open(image_path, 'rb') as image_file:
            img_data = image_file.read()  # Read the image data

        output_image_data = remove(img_data)  # Remove the background from the image using rembg
        output_image = Image.open(io.BytesIO(output_image_data))  # Open the processed image data as an image

        # Set the output path for the processed image
        output_image_path = os.path.join(output_folder, f"no_bg_{os.path.splitext(image_name)[0]}")

        # Check if the image has transparency (RGBA) and save accordingly
        if output_image.mode in ('RGBA', 'LA') or ('transparency' in output_image.info):
            output_image.save(f"{output_image_path}.png", "PNG")  # Save as PNG if transparency is present
        else:
            output_image.convert("RGB").save(f"{output_image_path}.jpg", "JPEG")  # Save as JPG if no transparency

    except Exception as e:
        print(f"Error processing {image_name}: {e}")  # Print any errors encountered while processing the image

# Cleanup function to remove the temporary folder after processing is complete
def cleanup_temp_folder():
    try:
        for file in os.listdir('temp_images'):  # Iterate through files in the temp folder
            os.remove(os.path.join('temp_images', file))  # Remove each file
        os.rmdir('temp_images')  # Remove the empty temp folder
    except Exception:
        pass  # If any error occurs during cleanup, simply pass (ignore the error)
