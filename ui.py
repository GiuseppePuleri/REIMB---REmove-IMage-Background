# ui.py
from PyQt5.QtCore import Qt, QUrl, pyqtSignal, QObject
from PyQt5.QtGui import QIcon, QDesktopServices, QPixmap
from PyQt5.QtWidgets import QFrame, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QFileDialog, QMessageBox
from qfluentwidgets import FluentWindow, SubtitleLabel, FluentIcon as FIF, NavigationItemPosition, setFont
import threading
from functions import process_images

#
#
#

class Widget(QFrame):
    def __init__(self, text: str, parent=None):
        super().__init__(parent=parent)
        # Initializes the base class QFrame. The parent widget is passed to QFrame as an argument (default is None).
        
        self.label = SubtitleLabel(text, self)
        # A custom label widget (likely a subclass of QLabel) is created and assigned to 'self.label'. The label's text is set to the value of 'text' passed to the constructor. 'self' is passed as the parent, meaning the label will be contained within the 'Widget' instance.

        self.hBoxLayout = QHBoxLayout(self)
        # Creates a horizontal layout (QHBoxLayout) to manage the placement of widgets inside this 'Widget' instance. The layout is set as the layout of the 'Widget' object (this). It will automatically manage the arrangement of child widgets.

        setFont(self.label, 24)
        # The 'setFont' function (likely a custom function or imported utility) is called on 'self.label' to set the font size to 24. This adjusts the appearance of the label text to be larger.

        self.label.setAlignment(Qt.AlignCenter)
        # This ensures that the text within the label will be centered horizontally and vertically.

        self.hBoxLayout.addWidget(self.label, 1, Qt.AlignCenter)
        # Adds the label to the layout. The '1' specifies the stretch factor, meaning the widget will stretch to take available space in the layout. Qt.AlignCenter ensures the label remains centered in the layout.

        self.setObjectName(text.replace(' ', '-'))
        # Sets the object name of the widget to be the 'text' string with spaces replaced by dashes ('-'). This could be useful for identification, styling, or for referencing the widget programmatically in other parts of the code.


class HomeWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("homeWidget")  # Sets the object name of the widget to "homeWidget"
        self.running = False  # Initializes a flag to track whether some process is running
        self.zip_file_path = ""  # Placeholder for the path to a ZIP file (initially empty)
        self.output_dir = ""  # Placeholder for the output directory (initially empty)
        self.initUI()  # Calls the method to initialize the user interface

    def initUI(self):
        self.layout = QVBoxLayout(self)  # Creates a vertical layout to hold widgets inside the home widget

        # Title section with background image
        self.titleWidget = QFrame(self)  # Creates a QFrame for the title section
        self.titleWidget.setObjectName("titleWidget")  # Sets the object name for the title widget
        self.titleWidgetLayout = QVBoxLayout(self.titleWidget)  # Creates a vertical layout for the title widget
        self.titleWidgetLayout.setContentsMargins(40, 20, 40, 20)  # Adds padding around the content

        # Title label
        self.titleLabel = SubtitleLabel("Hello!", self.titleWidget)  # Creates a custom subtitle label with the text "Hello!"
        setFont(self.titleLabel, 40)  # Sets the font size for the title label to 40

        # Create a QFont object to set the text to bold
        font = self.titleLabel.font()
        font.setBold(True)  # Makes the font bold
        self.titleLabel.setFont(font)

        self.titleLabel.setAlignment(Qt.AlignCenter)  # Centers the text within the label
        self.titleWidgetLayout.addWidget(self.titleLabel, alignment=Qt.AlignLeft)  # Adds the title label to the layout, aligned to the left

        # Paragraph label
        self.paragraphLabel = QLabel(
            "This is one software of Light Open Free Integrated Software (LOFIS): a collection of software that I developed for work or personal needs."
            "I decided, believing in the idea of ​open-source, to release the code of all my projects. "
            "You can find other tools online!",
            self.titleWidget
        )

        setFont(self.paragraphLabel, 18)  # Increases the font size for the paragraph
        self.paragraphLabel.setWordWrap(True)  # Enables word wrapping for the paragraph text
        self.paragraphLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Aligns the paragraph text to the top-left corner
        self.paragraphLabel.setStyleSheet("color: white;")  # Sets the text color to white
        self.paragraphLabel.setMaximumWidth(self.width() * 6)  # Limits the width to 60% of the widget's width
        self.titleWidgetLayout.addWidget(self.paragraphLabel, alignment=Qt.AlignLeft)  # Adds the paragraph to the layout

        # Sets a fixed width for the paragraph
        paragraph_width = int(self.width() * 10)  # 60% of the widget's width
        self.paragraphLabel.setFixedWidth(paragraph_width)

        # Add title widget to main layout
        self.layout.addWidget(self.titleWidget)  # Adds the title section to the main vertical layout

        # Apply background image with fade effect
        self.setStyleSheet(
            """
            #titleWidget {
                background-image: url(images/wallpaper.jpg);
                background-repeat: no-repeat;  
                background-position: center;
                border-radius: 10px;
            }

            #homeWidget {
                background-color: #59666D;
                padding: 30%;
            }

            #SubtitleLabel {
                font-weight:bold;
            }
            """
        )

        # Controls layout (upper section)
        self.controlsLayout = QHBoxLayout()  # Creates a horizontal layout for controls (presumably buttons, etc.)
        self.controlsLayout.setContentsMargins(10, 10, 10, 10)  # Adds padding around the controls section

class RemoveBGWidget(QFrame):
    update_status = pyqtSignal(str)  # Signal to update status

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("removeBGWidget")  # Assign a unique name to the widget
        self.update_status.connect(self.update_status_label)
        self.running = False
        self.zip_file_path = ""
        self.output_dir = ""
        self.initUI()

    def initUI(self):
        self.layout = QVBoxLayout(self)

        # Title section with background image
        self.titleWidget = QFrame(self)
        self.titleWidget.setObjectName("titleWidget")
        self.titleWidgetLayout = QVBoxLayout(self.titleWidget)
        self.titleWidgetLayout.setContentsMargins(40, 20, 40, 20)  # Optimized margins

        # Title label
        self.titleLabel = SubtitleLabel("REIMB - Remove image backgrounds", self.titleWidget)
        setFont(self.titleLabel, 40)
        self.titleLabel.setAlignment(Qt.AlignCenter)
        self.titleWidgetLayout.addWidget(self.titleLabel, alignment=Qt.AlignLeft)

        # Create a QFont object to set the bold font style
        font = self.titleLabel.font()
        font.setBold(True)  # Enable bold font
        self.titleLabel.setFont(font)

        # Paragraph label
        self.paragraphLabel = QLabel(
            "Choose the .zip file and output directory. The process will begin after pressing 'START'. "
            "You can also check the status from the middle part.",
            self.titleWidget
        )
        setFont(self.paragraphLabel, 18)  # Increased font size
        self.paragraphLabel.setWordWrap(True)  # Enable text wrapping
        self.paragraphLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align to top-left
        self.paragraphLabel.setStyleSheet("color: white;")  # Set text color to white
        self.paragraphLabel.setMaximumWidth(self.width() * 6)  # Take 60% of the window width
        self.titleWidgetLayout.addWidget(self.paragraphLabel, alignment=Qt.AlignLeft)

        # Set a fixed width for the paragraph
        paragraph_width = int(self.width() * 10)  # 60% of the window width
        self.paragraphLabel.setFixedWidth(paragraph_width)

        # Add title widget to main layout
        self.layout.addWidget(self.titleWidget)

        # Apply background image with fade effect
        self.setStyleSheet(
            """
            #titleWidget {
                background-image: url(images/wallpaper-two.png);
                background-repeat: no-repeat;
                background-position: top;
                border-radius: 10px;
            }

            #removeBG {
                background-color: #2b211b;
            }
            """
        )

        # Controls layout (upper section)
        self.controlsLayout = QHBoxLayout()
        self.controlsLayout.setContentsMargins(10, 10, 10, 10)

        self.zipButton = QPushButton("Select ZIP File", self)
        self.zipButton.setFixedHeight(40)
        self.zipButton.clicked.connect(self.select_zip)
        self.controlsLayout.addWidget(self.zipButton)

        self.zipButton.setStyleSheet("""
            QPushButton {
                background-color: #456270;  /* Background color */
                color: white;  /* Text color */
                border-radius: 5px;  /* Rounded corners */
                border: 1px solid #456270;  /* Border color */
            }
            QPushButton:hover {
                background-color: #244C58;  /* Hover color */
            }
            QPushButton:pressed {
                background-color: #244C58;  /* Pressed button color */
            }
        """)

        self.outputDirButton = QPushButton("Select Output Directory", self)
        self.outputDirButton.setFixedHeight(40)
        self.outputDirButton.clicked.connect(self.select_output_dir)
        self.controlsLayout.addWidget(self.outputDirButton)

        self.outputDirButton.setStyleSheet("""
            QPushButton {
                background-color: #456270;  /* Background color */
                color: white;  /* Text color */
                border-radius: 5px;  /* Rounded corners */
                border: 1px solid #456270;  /* Border color */
            }
            QPushButton:hover {
                background-color: #244C58;  /* Hover color */
            }
            QPushButton:pressed {
                background-color: #244C58;  /* Pressed button color */
            }
        """)
        self.layout.addLayout(self.controlsLayout)

        # Status and start/stop buttons (lower section)
        self.bottomLayout = QVBoxLayout()
        self.bottomLayout.setContentsMargins(10, 10, 10, 10)

        self.statusLabel = SubtitleLabel("Status: Waiting", self)
        setFont(self.statusLabel, 16)
        self.statusLabel.setAlignment(Qt.AlignCenter)
        self.bottomLayout.addWidget(self.statusLabel, alignment=Qt.AlignCenter)

        self.startStopButton = QPushButton("START PROCESS", self)
        self.startStopButton.setFixedHeight(40)
        self.startStopButton.clicked.connect(self.start_stop_process)
        self.bottomLayout.addWidget(self.startStopButton, alignment=Qt.AlignCenter)

        self.startStopButton.setStyleSheet("""
            QPushButton {
                background-color: #ba7d5f;  /* Background color */
                color: white;  /* Text color */
                border-radius: 5px;  /* Rounded corners */
                border: 1px solid #ba7d5f;  /* Border color */
            }
            QPushButton:hover {
                background-color: #cb8f6b;  /* Hover color */
            }
            QPushButton:pressed {
                background-color: #46555F;  /* Pressed button color */
            }
        """)
        # Set a fixed width for the button
        start_width = int(self.width() * 10)
        self.startStopButton.setFixedWidth(start_width)

        self.layout.addLayout(self.bottomLayout)
        
    def update_status_label(self, message):
        self.statusLabel.setText(message)

    def start_stop_process(self):
        if not self.zip_file_path or not self.output_dir:
            QMessageBox.warning(self, "Warning", "Select both ZIP file and output directory first.")
            return

        if self.running:
            self.running = False
            self.startStopButton.setText("Start")
            self.statusLabel.setText("Process stopped.")
        else:
            self.running = True
            self.startStopButton.setText("Stop")
            self.statusLabel.setText("Processing...")
            threading.Thread(target=self._start_processing).start()

    def _start_processing(self):
        """Calls the process_images function from functions.py."""
        process_images(
            zip_file_path=self.zip_file_path,
            output_dir=self.output_dir,
            update_status_callback=self.update_status.emit,  # Passes the callback for status updates
            running_flag=lambda: self.running  # Passes the dynamic running flag
        )
        
    def select_zip(self):
        """Opens a dialog to select a ZIP file."""
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Sets the read-only option
        file_path, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "", "ZIP Files (*.zip);;All Files (*)", options=options)
        
        if file_path:
            self.zip_file_path = file_path
            self.update_status.emit(f"Selected ZIP File: {self.zip_file_path}")

    def select_output_dir(self):
        """Opens a dialog to select the output directory."""
        options = QFileDialog.Options()
        dir_path = QFileDialog.getExistingDirectory(self, "Select Output Directory", options=options)
        
        if dir_path:
            self.output_dir = dir_path
            self.update_status.emit(f"Selected Output Directory: {self.output_dir}")

class OtherWidget(QFrame):

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("OtherWidget")  # Set a unique object name for the widget
        self.running = False  # A flag to check if the process is running
        self.zip_file_path = ""  # To store the path of the selected ZIP file
        self.output_dir = ""  # To store the output directory path
        self.initUI()  # Initialize the user interface

    def initUI(self):
        self.layout = QVBoxLayout(self)  # Main layout for the widget

        # Title section with background image
        self.titleWidget = QFrame(self)  # Create a frame for the title section
        self.titleWidget.setObjectName("titleWidget")  # Set a unique object name
        self.titleWidgetLayout = QVBoxLayout(self.titleWidget)  # Layout inside the title frame
        self.titleWidgetLayout.setContentsMargins(40, 20, 40, 20)  # Optimized margins for the title section

        # Title label for the widget
        self.titleLabel = SubtitleLabel("You can Use Other Online Tools", self.titleWidget)
        setFont(self.titleLabel, 40)  # Set font size to 40 for the title label
        self.titleLabel.setAlignment(Qt.AlignCenter)  # Center align the title label
        self.titleWidgetLayout.addWidget(self.titleLabel, alignment=Qt.AlignLeft)  # Add title to layout

        # Paragraph label with a description of the online tools
        self.paragraphLabel = QLabel(
            "Find other tools online! There are other free tools available that you might be interested in. You can find them on the website lofis.puleri.it.",
            self.titleWidget
        )
        setFont(self.paragraphLabel, 18)  # Set font size for the paragraph
        self.paragraphLabel.setWordWrap(True)  # Enable text wrapping
        self.paragraphLabel.setAlignment(Qt.AlignLeft | Qt.AlignTop)  # Align text to the top left
        self.paragraphLabel.setStyleSheet("color: white;")  # Set the text color to white
        self.paragraphLabel.setMaximumWidth(self.width() * 6)  # Set the paragraph's maximum width
        self.titleWidgetLayout.addWidget(self.paragraphLabel, alignment=Qt.AlignLeft)  # Add paragraph to layout

        # Set a fixed width for the paragraph
        paragraph_width = int(self.width() * 10)  # Calculate 60% of the widget's width
        self.paragraphLabel.setFixedWidth(paragraph_width)

        # Add title widget to the main layout
        self.layout.addWidget(self.titleWidget)

        # Apply styles including background image for the title widget
        self.setStyleSheet(
            """
            #titleWidget {
                background-image: url(images/wallpaper-two.png);
                background-repeat: no-repeat;
                background-position: top;
                border-radius: 10px;
            }

            #removeBG {
                background-color: #2b211b;
            }
            """
        )

        # Online link buttons (lower section)
        self.bottomLayout = QVBoxLayout()  # Layout for the bottom section
        self.bottomLayout.setContentsMargins(10, 10, 10, 10)  # Set margins for the bottom section

        # Button to open online tools
        self.linkButton = QPushButton("Use other Tools Online", self)
        self.linkButton.setFixedHeight(40)  # Set a fixed height for the button
        self.linkButton.clicked.connect(lambda: QDesktopServices.openUrl(QUrl("https://lofis.puleri.it/index.php")))  # Open the website on click

        self.bottomLayout.addWidget(self.linkButton, alignment=Qt.AlignCenter)  # Add the link button to layout

        # Styling for the link button
        self.linkButton.setStyleSheet("""
            QPushButton {
                background-color: #ba7d5f;  /* Background color */
                color: white;  /* Text color */
                border-radius: 5px;  /* Rounded corners */
                border: 1px solid #ba7d5f;  /* Border color */
            }
            QPushButton:hover {
                background-color: #cb8f6b;  /* Color when hovered */
            }
            QPushButton:pressed {
                background-color: #46555F;  /* Color when pressed */
            }
        """)
        # Set a fixed width for the link button
        start_width = int(self.width() * 10) 
        self.linkButton.setFixedWidth(start_width)

        # Add the bottom layout (which contains the button) to the main layout
        self.layout.addLayout(self.bottomLayout)

    # Method to select a ZIP file for image processing
    def select_zip(self):
        options = QFileDialog.Options()
        options |= QFileDialog.ReadOnly  # Set to read-only mode
        file_path, _ = QFileDialog.getOpenFileName(self, "Select ZIP File", "", "ZIP files (*.zip)", options=options)
        if file_path:
            self.zip_file_path = file_path  # Store the path of the selected ZIP file
            self.statusLabel.setText(f"ZIP selected: {self.zip_file_path}")  # Update status label
        else:
            QMessageBox.warning(self, "Warning", "No ZIP file selected.")  # Show warning if no file is selected

    # Method to select the output directory where processed images will be saved
    def select_output_dir(self):
        directory = QFileDialog.getExistingDirectory(self, "Select Output Directory")  # Open directory selection dialog
        if directory:
            self.output_dir = directory  # Store the selected output directory
            self.statusLabel.setText(f"Output directory: {self.output_dir}")  # Update status label
        else:
            QMessageBox.warning(self, "Warning", "No output directory selected.")  # Show warning if no directory is selected

    # Method to start or stop the image processing
    def start_stop_process(self):
        if not self.zip_file_path or not self.output_dir:
            QMessageBox.warning(self, "Warning", "Select both ZIP file and output directory first.")  # Show warning if either file or directory is missing
            return

        # Toggle the processing state
        if self.running:
            self.running = False  # Stop processing
            self.startStopButton.setText("Start")  # Change button text to "Start"
            self.statusLabel.setText("Process stopped.")  # Update the status
        else:
            self.running = True  # Start processing
            self.startStopButton.setText("Stop")  # Change button text to "Stop"
            self.statusLabel.setText("Processing...")  # Update the status
            threading.Thread(target=self.process_images).start()  # Start a new thread for image processing

    # Method to process images from the selected ZIP file
    def process_images(self):
        try:
            output_folder = self.create_output_folder()  # Create the output folder for processed images

            # Extract the ZIP file contents to the temp_images folder
            with zipfile.ZipFile(self.zip_file_path, 'r') as zip_ref:
                zip_ref.extractall('temp_images')

            images = [f for f in os.listdir('temp_images') if f.lower().endswith(('.png', '.jpg', '.jpeg'))]  # Get all image files

            # Process each image in the extracted folder
            for image_name in images:
                if not self.running:  # If the process was stopped, break the loop
                    break
                self.process_single_image(image_name, output_folder)  # Process each image

            self.statusLabel.setText("Process completed." if self.running else "Process stopped.")  # Update status
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")  # Show error message if something goes wrong
        finally:
            self.running = False  # Reset the running flag
            self.startStopButton.setText("Start")  # Change button text back to "Start"
            self.cleanup_temp_folder()  # Clean up the temporary folder

    # Method to create the output folder for processed images
    def create_output_folder(self):
        zip_name = os.path.splitext(os.path.basename(self.zip_file_path))[0]  # Get the name of the ZIP file without extension
        output_folder = os.path.join(self.output_dir, zip_name)  # Create a folder with the same name as the ZIP file
        os.makedirs(output_folder, exist_ok=True)  # Create the folder if it doesn't exist
        return output_folder

    # Method to process a single image (background removal)
    def process_single_image(self, image_name, output_folder):
        try:
            image_path = os.path.join('temp_images', image_name)  # Path of the current image
            with open(image_path, 'rb') as image_file:
                img_data = image_file.read()  # Read the image data

            output_image_data = remove(img_data)  # Call the background removal function (assumed to be defined elsewhere)
            output_image = Image.open(io.BytesIO(output_image_data))  # Open the processed image

            # Define the output image path
            output_image_path = os.path.join(output_folder, f"no_bg_{os.path.splitext(image_name)[0]}")

            # Save the processed image (consider transparency for PNG images)
            if output_image.mode in ('RGBA', 'LA') or ('transparency' in output_image.info):
                output_image.save(f"{output_image_path}.png", "PNG")  # Save as PNG if transparency exists
            else:
                output_image.convert("RGB").save(f"{output_image_path}.jpg", "JPEG")  # Save as JPEG otherwise

        except Exception as e:
            print(f"Error processing {image_name}: {e}")  # Print error message if processing fails for a single image

    # Method to clean up temporary folder after processing
    def cleanup_temp_folder(self):
        try:
            for file in os.listdir('temp_images'):
                os.remove(os.path.join('temp_images', file))  # Remove each file from the folder
            os.rmdir('temp_images')  # Remove the folder itself
        except Exception:
            pass  # Ignore any errors during cleanup

class LicenseWidget(QFrame):
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.setObjectName("LicenseWidget")  # Set a unique object name for the widget
        self.initUI()  # Initialize the user interface of the widget

    def initUI(self):
        self.layout = QVBoxLayout(self)  # Create a vertical layout for the widget

        # Create a label to display the license text
        self.paragraphLabel = QLabel(
            """
            Copyright (C) 2025 Giuseppe Puleri

            Questo programma è software libero: puoi redistribuirlo e/o modificarlo secondo i termini della GNU General Public License come pubblicata dalla Free Software Foundation, versione 3 della licenza, o (a tua scelta) qualsiasi versione successiva.

            Questo programma è distribuito nella speranza che sia utile, ma SENZA ALCUNA GARANZIA; senza nemmeno la garanzia implicita di COMMERCIABILITÀ o IDONEITÀ PER UNO SCOPO PARTICOLARE. Consulta la GNU General Public License per maggiori dettagli.

            Dovresti aver ricevuto una copia della GNU General Public License insieme a questo programma. In caso contrario, consulta <https://www.gnu.org/licenses/>.

            ---

            ### Termini della Licenza (estratto)

            **0. Definizioni.**
            Questa licenza si applica a qualsiasi programma o altro lavoro contenente una dichiarazione da parte del detentore del copyright che consente la distribuzione sotto i termini della presente Licenza. "Il Programma" si riferisce a qualsiasi programma o lavoro del genere, e un "lavoro basato sul Programma" indica il Programma o qualsiasi lavoro derivato secondo la legge sul copyright.

            **1. Libertà di utilizzo.**
            Hai il permesso di usare, studiare, condividere e modificare questo software, a condizione che ogni copia che distribuisci contenga gli stessi termini della GPL.

            **2. Distribuzione delle modifiche.**
            Se modifichi una copia del Programma o crei un lavoro basato su di esso, devi fornire il codice sorgente completo con qualsiasi distribuzione.

            **3. Compatibilità e versioni.**
            Puoi scegliere di applicare i termini di una versione più recente della Licenza pubblicata dalla Free Software Foundation.

            ---

            Per il testo completo della licenza, visita <https://www.gnu.org/licenses/gpl-3.0.html>.
            """,
            self  # Set this QLabel as part of the current widget (self)
        )

        setFont(self.paragraphLabel, 12)  # Set font size for the license text (12 pixels)
        self.paragraphLabel.setWordWrap(True)  # Enable text wrapping in the label so long lines break to the next line
        self.paragraphLabel.setAlignment(Qt.AlignCenter | Qt.AlignCenter)  # Center the text inside the label
        self.paragraphLabel.setStyleSheet("color: white;")  # Set the text color to white for better visibility

        # Add the paragraph label to the main layout of the widget
        self.layout.addWidget(self.paragraphLabel, alignment=Qt.AlignCenter)

        # Set a fixed width for the paragraph label based on the widget's width (10% of the widget width)
        paragraph_width = int(self.width() * 10)
        self.paragraphLabel.setFixedWidth(paragraph_width)  # Apply the fixed width to the label


class Window(FluentWindow):

    def __init__(self):
        super().__init__()  # Initialize the base FluentWindow class

        self.currentWidget = None  # Inizializza senza widget

        # Create sub interfaces (different screens or sections within the main window)
        self.homeInterface = HomeWidget(self)  # Home page widget
        self.remove_bgInterface = RemoveBGWidget(self)  # Image background removal page widget
        self.convert_to_webpInterface = OtherWidget(self)  # Convert images to WEBP format widget
        
        self.chatInterface = Widget('Write me an email: pulerigiuseppe@virgilio.it', self)  # Contact me section
        self.licenseInterface = LicenseWidget(self)  # License section widget

        self.initNavigation()  # Initialize the navigation bar
        self.initWindow()  # Initialize window-specific properties (e.g., title, icon)

    def loadWidget(self, widgetClass):
        if not self.currentWidget or not isinstance(self.currentWidget, widgetClass):
            if self.currentWidget:
                self.currentWidget.deleteLater()
            self.currentWidget = widgetClass(self)
            self.setCentralWidget(self.currentWidget)

    def initNavigation(self):
        # Add sub interfaces (screens) to the navigation menu with their respective icons and names
        self.addSubInterface(self.homeInterface, FIF.HOME, 'Home')  # Home button in navigation
        self.addSubInterface(self.remove_bgInterface, FIF.ZOOM, 'Remove Background')  # Background removal button
        self.addSubInterface(self.convert_to_webpInterface, FIF.TILES, 'Convert Image To WEBP Format')  # Convert to WEBP button

        self.navigationInterface.addSeparator()  # Add a separator in the navigation bar

        # Add 'Contact Me' and 'License' buttons at the bottom of the navigation menu
        self.addSubInterface(self.chatInterface, FIF.CHAT, 'Contact Me', NavigationItemPosition.BOTTOM)  # Chat/contact me button
        self.addSubInterface(self.licenseInterface, FIF.DOCUMENT, 'License', NavigationItemPosition.BOTTOM)  # License button

    def initWindow(self):
        # Set the application window's icon and title
        self.setWindowIcon(QIcon('images/logo.webp'))  # Set window icon to a WEBP image (logo)
        self.setWindowTitle('LOFIS - REIMB Software')  # Set the window's title to 'LOFIS - REIMB Software'
