# REIMB - REmove-IMage-Background

This application processes images contained in ZIP files, removes their backgrounds, and saves the results. It features a graphical user interface (GUI) built with PyQt5, utilizing the Fluent Design System for a modern and user-friendly experience.

In addition to the Python version, an executable file (`.exe`) is also available, allowing users to run the application on Windows without needing to install Python or any dependencies.
## Features

- **ZIP File Processing**: Extracts and processes images from ZIP archives.  
- **Background Removal**: Automatically removes the background from images.  
- **Batch Processing**: Handles multiple images in a single workflow.  
- **GUI**: Intuitive and modern interface using PyQt5 and QFluentWidgets.  
- **Error Handling**: Provides feedback and logs issues encountered during processing.  

---

## File Structure

### `functions.py`

Core logic for processing images:

- `create_output_folder(zip_file_path, output_dir)`: Creates an output directory for storing processed images.
- `process_images(zip_file_path, output_dir, update_status_callback, running_flag)`: Orchestrates the entire image processing workflow.
- `process_single_image(image_name, output_folder)`: Processes a single image by removing its background.
- `cleanup_temp_folder()`: Cleans up temporary files after processing.

### `main.py`

Entry point of the application:

- Initializes the PyQt5 application.
- Sets up the Fluent Design theme (dark mode).
- Launches the main application window (`Window` from `ui.py`).

### `ui.py`

Defines the GUI layout and behavior:

- `FluentWindow`: Main application window.
- Navigation and interactive elements (buttons, labels, etc.).
- Connects GUI elements with backend functions like `process_images`.

---

## Requirements

### Python
- Version: 3.8+

### Libraries
- `PyQt5`
- `qfluentwidgets`
- `rembg`
- `Pillow`

### System
- Compatible with Windows, macOS, and Linux.

---

## Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd <repository_name>

## Usage

1. Launch the application by running `main.py`.
2. Use the GUI to select a ZIP file containing images.
3. Specify an output directory for processed images.
4. Click the **Start** button to begin processing.
5. View progress and results through the GUI.

---

## Technical Details

### Background Removal

- Utilizes the `rembg` library to process images using AI for background removal.  
- Supports various image formats such as `.png`, `.jpg`, and `.jpeg`.

### Threading

- The `process_images` function supports threading to keep the GUI responsive during intensive operations.

### Temporary Files

- Extracted images are temporarily stored in a directory (`temp_images`) and cleaned up automatically after processing.
