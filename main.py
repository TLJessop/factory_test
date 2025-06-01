#!/usr/bin/env python3
"""
User Data Generator - Main Entry Point

This module serves as the entry point for the User Data Generator application.
It initializes the GUI and handles dependency checking and error handling.
"""

import tkinter as tk
import sys
import importlib.util
import traceback
from tkinter import messagebox

# Define required dependencies
REQUIRED_PACKAGES = ['faker']

def check_dependencies():
    """
    Check if all required packages are installed.
    
    Returns:
        bool: True if all dependencies are met, False otherwise
    """
    missing_packages = []
    
    for package in REQUIRED_PACKAGES:
        if importlib.util.find_spec(package) is None:
            missing_packages.append(package)
    
    if missing_packages:
        error_message = (
            "Missing required packages:\n"
            f"{', '.join(missing_packages)}\n\n"
            "Please install them using pip:\n"
            f"pip install {' '.join(missing_packages)}"
        )
        messagebox.showerror("Dependency Error", error_message)
        return False
    
    return True

def main():
    """
    Main function to initialize and run the application.
    
    Returns:
        int: Exit code (0 for success, non-zero for errors)
    """
    # Check dependencies before importing application modules
    if not check_dependencies():
        return 1
    
    try:
        # Import the GUI module (only import after dependency check)
        from gui import DataGeneratorApp
        
        # Create and configure the root window
        root = tk.Tk()
        root.title("User Data Generator")
        
        # Apply a theme if available
        try:
            from ttkthemes import ThemedTk
            root = ThemedTk(theme="arc")  # Use a modern theme if available
        except ImportError:
            # ttkthemes is optional, continue with default theme
            pass
        
        # Create the application instance
        app = DataGeneratorApp(root)
        
        # Set up menu bar
        menu_bar = tk.Menu(root)
        
        # File menu
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Exit", command=root.quit)
        menu_bar.add_cascade(label="File", menu=file_menu)
        
        # Help menu
        help_menu = tk.Menu(menu_bar, tearoff=0)
        help_menu.add_command(label="About", command=app.show_about_dialog)
        menu_bar.add_cascade(label="Help", menu=help_menu)
        
        root.config(menu=menu_bar)
        
        # Start the application main loop
        root.mainloop()
        
        return 0
        
    except Exception as e:
        # Handle unexpected errors
        error_message = (
            f"An unexpected error occurred:\n{str(e)}\n\n"
            "Please report this issue with the following details:\n"
            f"{traceback.format_exc()}"
        )
        messagebox.showerror("Application Error", error_message)
        print(error_message, file=sys.stderr)
        return 1

if __name__ == "__main__":
    # Run the main function when the script is executed directly
    sys.exit(main())
