import os
import yaml
import webbrowser
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QStatusBar, QProgressBar
from PySide6.QtGui import QColor, QAction, QIcon, QKeySequence, QShortcut
from PySide6.QtCore import Qt, QTimer
from Main_ui import Ui_FPMSoftware
from Utilities.data_handler import load_mat_file
from Utilities.display_handler import (
    display_single_raw_frame,
    display_all_raw_frames,
    display_single_raw_spectrum,
    display_all_raw_spectra,
    display_single_roi_image,
    display_all_roi_images,
)
from Utilities.message_handler import export_messages, clear_messages
from Utilities.logging_utils import log_message
from Utilities.interactive_view import ZoomableGraphicsView
from Utilities.roi_handler import select_roi_size
from Utilities.system_specs_window import SystemSpecsWindow  
from Utilities.parameter_dialog import ParameterDialog  
from WindowUI.DisplayOptionsWindow import DisplayOptionsWindow
from Utilities.status_bar_enhancement import ProfessionalStatusBar
from Utilities.about_dialog import show_about_dialog

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_FPMSoftware()
        self.ui.setupUi(self)
        self.setWindowTitle("FPM Software - Fourier Ptychographic Microscopy")
        self.setWindowIcon(QIcon("icons/FPM_icon.png"))
        
        # Apply professional theme
        self.apply_professional_theme()
        
        # Set up professional UI enhancements
        self.setup_professional_ui()
        
        doc_path = os.path.abspath("docs_package/build/html/index.html")
        self.ui.actionSoftware_Guide.triggered.connect(lambda: webbrowser.open(f"file://{doc_path}"))


        self.mat_data = None  # Initialize data storage
        self.system_specs_window = None  # Initialize system specs window
        self.recent_files = []  # Store recent files
        self.max_recent_files = 5

        # **ROI parameters (Default ROI: [X-offset, Y-offset, ROI_size, ROI_size])**
        self.roi_params = {"x_offset": 1, "y_offset": 1, "roi_size": 256}

        # **Scan for algorithm subfolders dynamically**
        self.algorithm_directory = "Algorithms"  # Directory where algorithms are stored
        self.algorithms = self.detect_algorithms()  # Automatically fetch algorithms

        # Replace default QGraphicsView with interactive view
        self.ui.display_window = ZoomableGraphicsView(self.ui.centralwidget)
        border_color = QColor(255, 255, 255)  # White border
        self.ui.display_window.setStyleSheet(f"border: 1px solid rgb({border_color.red()}, {border_color.green()}, {border_color.blue()});")
        self.ui.display_window.show()

        self.ui.gridLayout_3.addWidget(self.ui.display_window, 0, 0, 1, 1)

        # Connect buttons and menu actions to functions
        self.ui.load_butt.clicked.connect(self.load_data)
        self.ui.actionLoad_Data.triggered.connect(self.load_data)
        self.ui.actionSave_Messgaes.triggered.connect(self.export_messages)
        self.ui.actionClear_Messages.triggered.connect(self.clear_messages)
        self.ui.actionSystem_specs.triggered.connect(self.show_system_specs)
        self.ui.actionSIngle_ROI.triggered.connect(self.show_single_roi_image)
        self.ui.actionAll_ROI_images.triggered.connect(self.show_all_roi_images)
        self.ui.run_butt.clicked.connect(self.run_selected_algorithm)
        self.ui.display_butt.clicked.connect(self.show_display_options)
        
        # Connect result display actions (if they exist in the UI)
        if hasattr(self.ui, 'actionAmplitude_result'):
            self.ui.actionAmplitude_result.triggered.connect(lambda: self.display_result("amplitude"))
        if hasattr(self.ui, 'actionPhase_result'):
            self.ui.actionPhase_result.triggered.connect(lambda: self.display_result("phase"))
        if hasattr(self.ui, 'actionPupil_function'):
            self.ui.actionPupil_function.triggered.connect(lambda: self.display_result("pupil"))
        
        # Connect Help menu actions
        self.ui.actionSoftware_Guide.triggered.connect(self.show_help)
        self.ui.actionReferences.triggered.connect(self.show_about_dialog)
        
        # Add About action to Help menu
        self.ui.actionAbout = QAction("About FPM Software", self)
        self.ui.menuHelp.addAction(self.ui.actionAbout)
        self.ui.actionAbout.triggered.connect(self.show_about_dialog)


        # Connect ROI selection button
        self.ui.roi_butt.clicked.connect(lambda: select_roi_size(self))

        # Ensure algorithm menu items are checkable
        self.ui.actionGerchberg_Saxton.setCheckable(True)
        self.ui.actionEPRY.setCheckable(True)
        self.ui.actionGauss_Newton.setCheckable(True)
        self.ui.actionKramers_Kronig.setCheckable(True)
        self.ui.actionAPIC.setCheckable(True)

        # Dynamically populate the algorithm menu
        self.algorithm_actions = {}
        self.populate_algorithm_menu()
        
        # Setup keyboard shortcuts and status bar
        self.setup_keyboard_shortcuts()
        self.setup_status_bar()
        self.update_ui_state()

    def show_display_options(self):
        self.display_options_window = DisplayOptionsWindow(self)
        self.display_options_window.show()

    def setup_keyboard_shortcuts(self):
        """Setup keyboard shortcuts for common actions"""
        QShortcut(QKeySequence("Ctrl+O"), self, self.load_data)
        QShortcut(QKeySequence("Ctrl+R"), self, self.run_selected_algorithm)
        QShortcut(QKeySequence("F1"), self, self.show_help)
        QShortcut(QKeySequence("Ctrl+Q"), self, self.close)
        
    def setup_status_bar(self):
        """Setup status bar with progress indicator"""
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        self.status_bar.addPermanentWidget(self.progress_bar)
        self.status_bar.showMessage("Ready")
        
    def update_ui_state(self):
        """Update UI state based on current data and selections"""
        has_data = self.mat_data is not None
        has_algorithm = hasattr(self, 'selected_algorithm') and bool(self.selected_algorithm)
        
        # Enable/disable buttons based on state
        self.ui.run_butt.setEnabled(has_data and has_algorithm)
        self.ui.roi_butt.setEnabled(has_data)
        self.ui.display_butt.setEnabled(has_data)
        
        # Update status
        if has_data:
            frames = self.mat_data.get('imlow', np.array([])).shape[2] if 'imlow' in self.mat_data else 0
            self.status_bar.showMessage(f"Data loaded: {frames} frames")
        else:
            self.status_bar.showMessage("No data loaded")
            
    def show_help(self):
        """Show help documentation"""
        doc_path = os.path.abspath("docs_package/build/html/index.html")
        webbrowser.open(f"file://{doc_path}")

    def load_data(self):
        """Load data with improved validation and feedback"""
        try:
            self.status_bar.showMessage("Loading data...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 0)  # Indeterminate progress
            
            new_data = load_mat_file(self)
            if new_data:
                # Validate data structure
                if self.validate_mat_data(new_data):
                    self.mat_data = new_data
                    self.add_to_recent_files(getattr(self, 'current_file_path', ''))
                    self.ui.Msg_window.appendPlainText("[OK] Data loaded successfully.")
                    self.update_ui_state()
                    
                    if self.system_specs_window:
                        self.system_specs_window.load_system_specs()
                else:
                    self.ui.Msg_window.appendPlainText("[ERROR] Data validation failed.")
            else:
                self.ui.Msg_window.appendPlainText("No data loaded.")
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error loading data: {e}")
        finally:
            self.progress_bar.setVisible(False)
            self.status_bar.showMessage("Ready")
            
    def validate_mat_data(self, data):
        """Validate .mat file structure"""
        required_fields = ['imlow', 'NA_list']
        optional_fields = ['NA', 'dpix_c', 'lambda', 'mag']
        
        # Check required fields
        for field in required_fields:
            if field not in data:
                self.ui.Msg_window.appendPlainText(f"[ERROR] Required field '{field}' missing")
                return False
                
        # Validate data types and shapes
        if not hasattr(data['imlow'], 'shape') or len(data['imlow'].shape) != 3:
            self.ui.Msg_window.appendPlainText("[ERROR] 'imlow' must be a 3D array")
            return False
            
        if not hasattr(data['NA_list'], 'shape') or len(data['NA_list'].shape) != 2:
            self.ui.Msg_window.appendPlainText("[ERROR] 'NA_list' must be a 2D array")
            return False
            
        # Show data summary
        frames = data['imlow'].shape[2]
        height, width = data['imlow'].shape[:2]
        self.ui.Msg_window.appendPlainText(f"Data summary: {height}x{width} pixels, {frames} frames")
        
        return True
        
    def add_to_recent_files(self, file_path):
        """Add file to recent files list"""
        if file_path and file_path not in self.recent_files:
            self.recent_files.insert(0, file_path)
            if len(self.recent_files) > self.max_recent_files:
                self.recent_files = self.recent_files[:self.max_recent_files]

    def show_single_raw_frame(self):
        display_single_raw_frame(self)

    def show_all_raw_frames(self):
        display_all_raw_frames(self)

    def show_single_raw_spectrum(self):
        display_single_raw_spectrum(self)

    def show_all_raw_spectra(self):
        display_all_raw_spectra(self)

    def show_single_roi_image(self):
        display_single_roi_image(self)

    def show_all_roi_images(self):
        display_all_roi_images(self)

    def export_messages(self):
        export_messages(self)

    def clear_messages(self):
        clear_messages(self)

    def show_system_specs(self):
        if self.system_specs_window is None:
            self.system_specs_window = SystemSpecsWindow(self)
        if hasattr(self, "roi_params"):
            roi_text = str(self.roi_params)
            self.system_specs_window.update_roi_field(roi_text)
        self.system_specs_window.populate_algorithm_list(self.algorithms)
        self.system_specs_window.load_system_specs()
        self.system_specs_window.show()

    def detect_algorithms(self):
        if not os.path.exists(self.algorithm_directory):
            return []
        return sorted([
            folder for folder in os.listdir(self.algorithm_directory)
            if os.path.isdir(os.path.join(self.algorithm_directory, folder))
        ])

    def populate_algorithm_menu(self):
        menu_algorithms = self.ui.menuAlgorithm_specs
        menu_algorithms.clear()
        for algorithm in self.algorithms:
            shortened_name = algorithm.split(" ")[0]
            action = QAction(shortened_name, self)
            action.setCheckable(True)
            action.triggered.connect(lambda checked, alg=algorithm: self.select_algorithm(alg))
            self.algorithm_actions[algorithm] = action
            menu_algorithms.addAction(action)
        if self.algorithms:
            self.selected_algorithm = self.algorithms[0]
            self.algorithm_actions[self.selected_algorithm].setChecked(True)

    def select_algorithm(self, algorithm_name):
        self.selected_algorithm = algorithm_name
        for action in self.algorithm_actions.values():
            action.setChecked(False)
        if algorithm_name in self.algorithm_actions:
            self.algorithm_actions[algorithm_name].setChecked(True)
        self.ui.Msg_window.appendPlainText(f"[OK] Algorithm selected: {algorithm_name}")
        self.update_ui_state()
        
        if self.system_specs_window:
            self.system_specs_window.update_algorithm_selection(algorithm_name)
        config_path = os.path.join("Algorithms", algorithm_name, "config.yml")
        if os.path.exists(config_path):
            dialog = ParameterDialog(algorithm_name, parent=self)
            dialog.show()

    def load_algorithm_config(self, algorithm_name):
        config_path = os.path.join("Algorithms", algorithm_name, "config.yml")
        if not os.path.exists(config_path):
            return None
        with open(config_path, "r") as f:
            return yaml.safe_load(f)

    def run_selected_algorithm(self):
        """Run selected algorithm with improved error handling and progress feedback"""
        if not hasattr(self, 'selected_algorithm') or not self.selected_algorithm:
            self.ui.Msg_window.appendPlainText("[ERROR] No algorithm selected.")
            return
            
        if not self.mat_data:
            self.ui.Msg_window.appendPlainText("[ERROR] No data loaded.")
            return
            
        try:
            self.status_bar.showMessage(f"Running {self.selected_algorithm}...")
            self.progress_bar.setVisible(True)
            self.progress_bar.setRange(0, 100)
            self.progress_bar.setValue(0)
            
            # Disable run button during processing
            self.ui.run_butt.setEnabled(False)
            self.ui.run_butt.setText("Processing...")
            
            module_path = f"Algorithms.{self.selected_algorithm}.main_alg"
            run_module = __import__(module_path, fromlist=["run_algorithm"])
            run_algorithm = getattr(run_module, "run_algorithm")
            
            # Progress callback
            def progress_callback(progress):
                self.progress_bar.setValue(progress)
                QApplication.processEvents()
                
            # Log callback
            def log_callback(msg):
                self.ui.Msg_window.appendPlainText(f"[{self.selected_algorithm}] {msg}")
                QApplication.processEvents()
            
            Amp, Phase, Pupil = run_algorithm(
                system_params=getattr(self, 'algorithm_parameters', {}),
                roi_params=self.roi_params,
                mat_data=self.mat_data,
                log_callback=log_callback,
                progress_callback=progress_callback
            )
            
            # Store results for display
            self.reconstruction_result = {
                "amplitude": Amp.cpu().numpy() if hasattr(Amp, "cpu") else Amp,
                "phase": Phase.cpu().numpy() if hasattr(Phase, "cpu") else Phase,
                "pupil": Pupil.cpu().numpy() if hasattr(Pupil, "cpu") else Pupil,
            }
            
            self.ui.Msg_window.appendPlainText(f"[OK] {self.selected_algorithm} completed successfully.")
            self.status_bar.showMessage("Algorithm completed")
            
            # Automatically display amplitude result
            self.display_amplitude_result()
            
        except ImportError as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Algorithm module not found: {e}")
        except MemoryError:
            self.ui.Msg_window.appendPlainText("[ERROR] Insufficient memory. Try smaller ROI or reduce upsampling.")
        except ValueError as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Invalid parameters: {e}")
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Algorithm failed: {e}")
        finally:
            # Re-enable UI
            self.progress_bar.setVisible(False)
            self.ui.run_butt.setEnabled(True)
            self.ui.run_butt.setText("Run")
            self.update_ui_state()

    def display_amplitude_result(self):
        """Automatically display the amplitude reconstruction result"""
        try:
            from Utilities.display_handler import display_result_image
            display_result_image(self, "amplitude")
            self.ui.Msg_window.appendPlainText("[OK] Amplitude result displayed automatically.")
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error displaying amplitude result: {e}")
    
    def display_result(self, result_type):
        """Display a specific reconstruction result (amplitude, phase, or pupil)"""
        if not hasattr(self, 'reconstruction_result') or not self.reconstruction_result:
            self.ui.Msg_window.appendPlainText("[ERROR] No reconstruction results available. Run an algorithm first.")
            return
            
        try:
            from Utilities.display_handler import display_result_image
            display_result_image(self, result_type)
            self.ui.Msg_window.appendPlainText(f"[OK] {result_type.capitalize()} result displayed.")
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error displaying {result_type} result: {e}")

    def apply_professional_theme(self):
        """Apply the professional theme to the application"""
        try:
            # Try clean theme first (no CSS warnings)
            clean_theme_path = os.path.join(os.path.dirname(__file__), "professional_theme_clean.qss")
            if os.path.exists(clean_theme_path):
                with open(clean_theme_path, 'r', encoding='utf-8') as f:
                    style = f.read()
                self.setStyleSheet(style)
                self.ui.Msg_window.appendPlainText("[OK] Professional theme applied successfully.")
                return
            
            # Fallback to original professional theme
            theme_path = os.path.join(os.path.dirname(__file__), "professional_theme.qss")
            if os.path.exists(theme_path):
                with open(theme_path, 'r', encoding='utf-8') as f:
                    style = f.read()
                self.setStyleSheet(style)
                self.ui.Msg_window.appendPlainText("[OK] Professional theme applied (with CSS warnings).")
                return
                
            # Final fallback to existing theme
            fallback_theme = os.path.join(os.path.dirname(__file__), "fancy_dark_theme.qss")
            if os.path.exists(fallback_theme):
                with open(fallback_theme, 'r', encoding='utf-8') as f:
                    style = f.read()
                self.setStyleSheet(style)
                self.ui.Msg_window.appendPlainText("[OK] Fallback theme applied.")
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error applying theme: {e}")

    def setup_professional_ui(self):
        """Set up professional UI enhancements"""
        try:
            # Set window properties for professional appearance
            self.setMinimumSize(1200, 800)
            self.resize(1400, 900)
            
            # Center the window on screen
            self.center_window()
            
            # Replace default status bar with professional one
            self.setup_professional_status_bar()
            
            # Set up professional button styling
            self.setup_button_icons()
            
            # Enhance the message window with professional styling
            self.ui.Msg_window.setStyleSheet("""
                QPlainTextEdit#Msg_window {
                    background: #0f1419;
                    color: #00ff88;
                    border: 2px solid #2a4a3a;
                    border-radius: 6px;
                    font-family: 'Consolas', 'Monaco', 'Courier New', monospace;
                    font-size: 9pt;
                    font-weight: 500;
                    padding: 8px;
                }
            """)
            
            # Add professional welcome message
            welcome_msg = """
================================================================================
                    FPM Software - Professional Edition                      
              Fourier Ptychographic Microscopy Reconstruction                
================================================================================
  Welcome to the professional FPM reconstruction software!                   
  
  Features:                                                                   
  - Advanced reconstruction algorithms (GS, EPRY, Gauss-Newton, KK, APIC)    
  - Interactive image display with zoom and pan                              
  - Professional user interface with modern styling                          
  - Comprehensive data analysis and visualization tools                      
                                                                              
  Getting Started:                                                            
  1. Load your FPM data using the 'Load' button                              
  2. Select an algorithm from the 'Specs' menu                               
  3. Click 'Run' to start reconstruction                                     
                                                                              
  For help and documentation, use the Help menu or press F1.                 
================================================================================
            """
            self.ui.Msg_window.setPlainText(welcome_msg)
            
            self.ui.Msg_window.appendPlainText("\n[OK] Professional UI setup completed successfully.")
            
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error setting up professional UI: {e}")

    def center_window(self):
        """Center the window on the screen"""
        try:
            screen = QApplication.primaryScreen().geometry()
            size = self.geometry()
            x = (screen.width() - size.width()) // 2
            y = (screen.height() - size.height()) // 2
            self.move(x, y)
        except Exception as e:
            # If centering fails, just continue
            pass

    def setup_button_icons(self):
        """Set up professional icons for buttons"""
        try:
            # Note: In a real implementation, you would add actual icon files
            # For now, we'll use text-based indicators and enhanced styling
            
            # Enhanced button text with professional styling
            self.ui.load_butt.setText("Load Data")
            self.ui.roi_butt.setText("ROI")
            self.ui.display_butt.setText("Display")
            self.ui.run_butt.setText("Run")
            self.ui.save_butt.setText("Save")
            
            # Add tooltips for better user experience
            self.ui.load_butt.setToolTip("Load FPM data from .mat files")
            self.ui.roi_butt.setToolTip("Select Region of Interest for processing")
            self.ui.display_butt.setToolTip("Display loaded data and results")
            self.ui.run_butt.setToolTip("Run the selected reconstruction algorithm")
            self.ui.save_butt.setToolTip("Save reconstruction results")
            
        except Exception as e:
            # If icon setup fails, continue with default text
            pass

    def setup_professional_status_bar(self):
        """Set up the professional status bar"""
        try:
            # Replace the default status bar with our professional one
            self.professional_status_bar = ProfessionalStatusBar(self)
            self.setStatusBar(self.professional_status_bar)
            
            # Update the progress bar reference for compatibility
            self.progress_bar = self.professional_status_bar.progress_bar
            
            self.professional_status_bar.show_success("Professional status bar initialized")
            
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error setting up professional status bar: {e}")

    def show_about_dialog(self):
        """Show the professional about dialog"""
        try:
            show_about_dialog(self)
        except Exception as e:
            self.ui.Msg_window.appendPlainText(f"[ERROR] Error showing about dialog: {e}")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    
    # Set application properties for professional appearance
    app.setApplicationName("FPM Software")
    app.setApplicationVersion("2.0 Professional")
    app.setOrganizationName("Caltech Biophotonics Lab")
    
    # Show professional splash screen
    splash = None
    try:
        # Try the simple splash screen first (more reliable)
        from Utilities.simple_splash_screen import show_simple_splash
        splash = show_simple_splash()
    except Exception as e:
        print(f"Simple splash screen error: {e}")
        try:
            # Fallback to animated splash screen
            from Utilities.splash_screen import ProfessionalSplashScreen
            splash = ProfessionalSplashScreen()
            splash.show()
            QApplication.processEvents()
            
            # Simulate loading time
            import time
            start_time = time.time()
            while time.time() - start_time < 2.0:  # Show for 2 seconds
                QApplication.processEvents()
                time.sleep(0.01)
        except Exception as e2:
            print(f"Animated splash screen error: {e2}")
            # If both splash screens fail, continue without it
            pass
    
    # Create and show the main window
    window = MainWindow()
    window.show()
    
    # Close splash screen if it's still open
    try:
        if splash and splash.isVisible():
            splash.close()
    except Exception:
        pass
        
    sys.exit(app.exec())
