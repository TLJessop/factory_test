import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import json
import csv
import os
import threading
import time
from data_generator import generate_data

class DataGeneratorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("User Data Generator")
        self.root.geometry("800x600")
        self.root.minsize(700, 500)
        
        # Set application icon if available
        try:
            self.root.iconbitmap("app_icon.ico")
        except:
            pass  # Icon not found, use default
        
        # Initialize variables
        self.fields = []  # List to store field definitions
        self.is_generating = False
        self.setup_ui()
        
    def setup_ui(self):
        """Create and arrange all UI elements"""
        # Create main frame with padding
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Create top section for field management
        self.create_field_section(main_frame)
        
        # Create middle section for generation settings
        self.create_settings_section(main_frame)
        
        # Create bottom section for action buttons
        self.create_action_section(main_frame)
        
        # Create status bar
        self.status_var = tk.StringVar(value="Ready")
        status_bar = ttk.Label(self.root, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        status_bar.pack(side=tk.BOTTOM, fill=tk.X)
        
        # Apply some styling
        style = ttk.Style()
        style.configure("Generate.TButton", font=("Helvetica", 12, "bold"))
        
    def create_field_section(self, parent):
        """Create the field management section"""
        # Create labeled frame for fields
        field_frame = ttk.LabelFrame(parent, text="Field Configuration", padding="10")
        field_frame.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # Split into two columns
        left_frame = ttk.Frame(field_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        right_frame = ttk.Frame(field_frame)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=(10, 0))
        
        # Field list with scrollbar
        list_frame = ttk.Frame(left_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)
        
        self.field_list = tk.Listbox(list_frame, height=10)
        self.field_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.field_list.bind('<<ListboxSelect>>', self.on_field_select)
        
        scrollbar = ttk.Scrollbar(list_frame, orient=tk.VERTICAL, command=self.field_list.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.field_list.config(yscrollcommand=scrollbar.set)
        
        # Field input controls
        input_frame = ttk.Frame(right_frame)
        input_frame.pack(fill=tk.X, pady=5)
        
        # Field name input
        ttk.Label(input_frame, text="Field Name:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.field_name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.field_name_var).grid(row=0, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        # Field type selection
        ttk.Label(input_frame, text="Field Type:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.field_type_var = tk.StringVar()
        
        # List of supported field types
        field_types = [
            "Full Name", "First Name", "Last Name", "Email", "Phone Number",
            "Address", "City", "Country", "Postal Code", "Date of Birth",
            "Username", "Password", "Text", "Number", "Boolean", "UUID",
            "Job Title", "Company", "Credit Card", "URL"
        ]
        
        field_type_combo = ttk.Combobox(input_frame, textvariable=self.field_type_var, values=field_types)
        field_type_combo.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5, pady=5)
        field_type_combo.current(0)  # Set default selection
        
        # Field action buttons
        button_frame = ttk.Frame(right_frame)
        button_frame.pack(fill=tk.X, pady=10)
        
        ttk.Button(button_frame, text="Add Field", command=self.add_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Update Field", command=self.update_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Remove Field", command=self.remove_field).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear All", command=self.clear_fields).pack(side=tk.LEFT, padx=5)
        
    def create_settings_section(self, parent):
        """Create the generation settings section"""
        settings_frame = ttk.LabelFrame(parent, text="Generation Settings", padding="10")
        settings_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Number of records
        ttk.Label(settings_frame, text="Number of Records:").grid(row=0, column=0, sticky=tk.W, padx=5, pady=5)
        self.num_records_var = tk.StringVar(value="10")
        ttk.Entry(settings_frame, textvariable=self.num_records_var, width=10).grid(row=0, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Export format
        ttk.Label(settings_frame, text="Export Format:").grid(row=1, column=0, sticky=tk.W, padx=5, pady=5)
        self.export_format_var = tk.StringVar(value="JSON")
        ttk.Combobox(settings_frame, textvariable=self.export_format_var, values=["JSON", "CSV"], width=10).grid(row=1, column=1, sticky=tk.W, padx=5, pady=5)
        
        # Output file
        ttk.Label(settings_frame, text="Output File:").grid(row=2, column=0, sticky=tk.W, padx=5, pady=5)
        file_frame = ttk.Frame(settings_frame)
        file_frame.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5, pady=5)
        
        self.output_file_var = tk.StringVar()
        ttk.Entry(file_frame, textvariable=self.output_file_var).pack(side=tk.LEFT, fill=tk.X, expand=True)
        ttk.Button(file_frame, text="Browse...", command=self.browse_output_file).pack(side=tk.RIGHT, padx=(5, 0))
        
    def create_action_section(self, parent):
        """Create the action buttons section"""
        action_frame = ttk.Frame(parent, padding="10")
        action_frame.pack(fill=tk.X, padx=5, pady=5)
        
        # Progress bar
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(action_frame, variable=self.progress_var, maximum=100)
        self.progress_bar.pack(fill=tk.X, pady=(0, 10))
        
        # Generate button
        generate_btn = ttk.Button(
            action_frame, 
            text="Generate Data", 
            command=self.generate_data,
            style="Generate.TButton"
        )
        generate_btn.pack(pady=5)
        
    def add_field(self):
        """Add a new field to the list"""
        field_name = self.field_name_var.get().strip()
        field_type = self.field_type_var.get()
        
        if not field_name:
            messagebox.showerror("Error", "Field name cannot be empty")
            return
        
        # Check for duplicate field names
        for field in self.fields:
            if field["name"] == field_name:
                messagebox.showerror("Error", f"Field '{field_name}' already exists")
                return
        
        # Add the field
        self.fields.append({"name": field_name, "type": field_type})
        self.update_field_list()
        self.field_name_var.set("")  # Clear the field name entry
        self.status_var.set(f"Added field: {field_name} ({field_type})")
        
    def update_field(self):
        """Update the selected field"""
        selected = self.field_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No field selected")
            return
        
        index = selected[0]
        old_field = self.fields[index]
        
        new_field_name = self.field_name_var.get().strip()
        new_field_type = self.field_type_var.get()
        
        if not new_field_name:
            messagebox.showerror("Error", "Field name cannot be empty")
            return
        
        # Check for duplicate field names (excluding the current field)
        for i, field in enumerate(self.fields):
            if i != index and field["name"] == new_field_name:
                messagebox.showerror("Error", f"Field '{new_field_name}' already exists")
                return
        
        # Update the field
        self.fields[index] = {"name": new_field_name, "type": new_field_type}
        self.update_field_list()
        self.status_var.set(f"Updated field: {new_field_name} ({new_field_type})")
        
    def remove_field(self):
        """Remove the selected field"""
        selected = self.field_list.curselection()
        if not selected:
            messagebox.showerror("Error", "No field selected")
            return
        
        index = selected[0]
        field = self.fields[index]
        
        # Remove the field
        del self.fields[index]
        self.update_field_list()
        self.field_name_var.set("")  # Clear the field name entry
        self.status_var.set(f"Removed field: {field['name']}")
        
    def clear_fields(self):
        """Clear all fields"""
        if not self.fields:
            return
            
        if messagebox.askyesno("Confirm", "Are you sure you want to clear all fields?"):
            self.fields = []
            self.update_field_list()
            self.field_name_var.set("")  # Clear the field name entry
            self.status_var.set("All fields cleared")
        
    def on_field_select(self, event):
        """Handle field selection from the list"""
        selected = self.field_list.curselection()
        if not selected:
            return
        
        index = selected[0]
        field = self.fields[index]
        
        self.field_name_var.set(field["name"])
        self.field_type_var.set(field["type"])
        
    def update_field_list(self):
        """Update the field list display"""
        self.field_list.delete(0, tk.END)
        for field in self.fields:
            self.field_list.insert(tk.END, f"{field['name']} ({field['type']})")
        
    def browse_output_file(self):
        """Open file dialog to select output file"""
        format_ext = ".json" if self.export_format_var.get().lower() == "json" else ".csv"
        
        filename = filedialog.asksaveasfilename(
            defaultextension=format_ext,
            filetypes=[
                ("JSON files", "*.json"),
                ("CSV files", "*.csv"),
                ("All files", "*.*")
            ]
        )
        
        if filename:
            self.output_file_var.set(filename)
            
    def generate_data(self):
        """Generate the data based on current settings"""
        if self.is_generating:
            messagebox.showinfo("Info", "Data generation is already in progress")
            return
            
        # Validate inputs
        if not self.fields:
            messagebox.showerror("Error", "No fields defined")
            return
            
        try:
            num_records = int(self.num_records_var.get())
            if num_records <= 0:
                messagebox.showerror("Error", "Number of records must be positive")
                return
        except ValueError:
            messagebox.showerror("Error", "Invalid number of records")
            return
            
        export_format = self.export_format_var.get()
        output_file = self.output_file_var.get()
        
        if not output_file:
            messagebox.showerror("Error", "Output file not specified")
            return
            
        # Check if output file extension matches the selected format
        expected_ext = ".json" if export_format.lower() == "json" else ".csv"
        if not output_file.lower().endswith(expected_ext):
            output_file += expected_ext
            self.output_file_var.set(output_file)
            
        # Start generation in a separate thread
        self.is_generating = True
        threading.Thread(target=self._generate_data_thread, args=(
            self.fields, num_records, export_format, output_file
        )).start()
        
    def _generate_data_thread(self, fields, num_records, export_format, output_file):
        """Background thread for data generation"""
        try:
            self.status_var.set("Generating data...")
            self.progress_var.set(0)
            
            # Update progress periodically
            def update_progress():
                for i in range(1, 101):
                    if not self.is_generating:
                        break
                    self.progress_var.set(i)
                    time.sleep(0.01 * min(num_records / 100, 1))  # Scale with record count
                    
            progress_thread = threading.Thread(target=update_progress)
            progress_thread.daemon = True
            progress_thread.start()
            
            # Generate the data
            records = generate_data(fields, num_records)
            
            # Export the data
            if export_format.lower() == "json":
                self._export_json(records, output_file)
            else:
                self._export_csv(records, output_file)
                
            # Ensure progress bar reaches 100%
            self.progress_var.set(100)
            
            # Show success message
            self.root.after(0, lambda: messagebox.showinfo(
                "Success", 
                f"Generated {num_records} records and saved to:\n{output_file}"
            ))
            self.status_var.set(f"Generated {num_records} records successfully")
            
        except Exception as e:
            self.root.after(0, lambda: messagebox.showerror("Error", f"Failed to generate data: {str(e)}"))
            self.status_var.set("Error generating data")
            
        finally:
            self.is_generating = False
            
    def _export_json(self, records, output_file):
        """Export records to JSON format"""
        with open(output_file, 'w', encoding='utf-8') as f:
            json.dump(records, f, indent=2, ensure_ascii=False, default=str)
            
    def _export_csv(self, records, output_file):
        """Export records to CSV format"""
        if not records:
            return
            
        # Get all unique field names across all records
        fieldnames = set()
        for record in records:
            fieldnames.update(record.keys())
        fieldnames = sorted(list(fieldnames))
        
        with open(output_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(records)
            
    def show_about_dialog(self):
        """Show information about the application"""
        messagebox.showinfo(
            "About User Data Generator",
            "User Data Generator v1.0\n\n"
            "A tool for generating sample user data for testing and debugging.\n\n"
            "Features:\n"
            "- Generate customizable user data\n"
            "- Export to JSON or CSV formats\n"
            "- Define your own field structure\n\n"
            "© 2025 User Data Generator Team"
        )
