#!/usr/bin/env python3
"""
MTL Generator GUI

A simple graphical interface for generating Word documents from JSON data.
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from mtl_generator import MTLGenerator


class MTLGeneratorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("MTL Document Generator")
        self.root.geometry("600x400")
        
        # Variables
        self.json_file_var = tk.StringVar(value="mtl1_data.json")
        self.template_file_var = tk.StringVar(value="MTL1_MasterTemplate_Placeholders.docx")
        self.output_file_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # JSON File Selection
        ttk.Label(main_frame, text="JSON Data File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.json_file_var, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_json_file).grid(row=0, column=2, padx=5, pady=5)
        
        # Template File Selection
        ttk.Label(main_frame, text="Template File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.template_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_template_file).grid(row=1, column=2, padx=5, pady=5)
        
        # Output File Selection
        ttk.Label(main_frame, text="Output File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(row=2, column=2, padx=5, pady=5)
        
        # Options frame
        options_frame = ttk.LabelFrame(main_frame, text="Options", padding="5")
        options_frame.grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)
        
        self.use_template_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Use template (if available)", variable=self.use_template_var).grid(row=0, column=0, sticky=tk.W)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="Generate Document", command=self.generate_document).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Preview JSON", command=self.preview_json).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Exit", command=self.root.quit).grid(row=0, column=2, padx=5)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=5)
        
        self.output_text = tk.Text(text_frame, height=10, width=70, wrap=tk.WORD)
        scrollbar = ttk.Scrollbar(text_frame, orient=tk.VERTICAL, command=self.output_text.yview)
        self.output_text.configure(yscrollcommand=scrollbar.set)
        
        self.output_text.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")
        
        text_frame.columnconfigure(0, weight=1)
        text_frame.rowconfigure(0, weight=1)
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(6, weight=1)
        
    def browse_json_file(self):
        filename = filedialog.askopenfilename(
            title="Select JSON Data File",
            filetypes=[("JSON files", "*.json"), ("All files", "*.*")]
        )
        if filename:
            self.json_file_var.set(filename)
            
    def browse_template_file(self):
        filename = filedialog.askopenfilename(
            title="Select Word Template File",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        if filename:
            self.template_file_var.set(filename)
            
    def browse_output_file(self):
        filename = filedialog.asksaveasfilename(
            title="Save Document As",
            defaultextension=".docx",
            filetypes=[("Word documents", "*.docx"), ("All files", "*.*")]
        )
        if filename:
            self.output_file_var.set(filename)
    
    def log_message(self, message):
        """Add message to output text area."""
        self.output_text.insert(tk.END, message + "\n")
        self.output_text.see(tk.END)
        self.root.update()
    
    def generate_document(self):
        """Generate the Word document."""
        json_file = self.json_file_var.get()
        template_file = self.template_file_var.get() if self.use_template_var.get() else None
        output_file = self.output_file_var.get()
        
        # Clear output
        self.output_text.delete(1.0, tk.END)
        
        # Validate inputs
        if not json_file or not os.path.exists(json_file):
            self.log_message("❌ Error: JSON file not found or not specified")
            return
            
        if template_file and not os.path.exists(template_file):
            self.log_message(f"⚠️  Warning: Template file not found: {template_file}")
            self.log_message("Will create basic document instead")
            template_file = None
        
        try:
            self.log_message("Starting document generation...")
            self.log_message(f"📄 JSON file: {json_file}")
            
            if template_file:
                self.log_message(f"📋 Template: {template_file}")
            else:
                self.log_message("📋 Template: Creating basic document")
            
            # Generate document
            generator = MTLGenerator(json_file)
            result_file = generator.generate_document(template_path=template_file, output_path=output_file)
            
            self.log_message(f"✅ Document generated successfully!")
            self.log_message(f"📁 Output: {result_file}")
            
            messagebox.showinfo("Success", f"Document generated successfully!\n\nSaved as: {result_file}")
            
        except Exception as e:
            error_msg = f"❌ Error generating document: {str(e)}"
            self.log_message(error_msg)
            messagebox.showerror("Error", str(e))
    
    def preview_json(self):
        """Preview the JSON data."""
        json_file = self.json_file_var.get()
        
        if not json_file or not os.path.exists(json_file):
            messagebox.showerror("Error", "JSON file not found or not specified")
            return
        
        try:
            generator = MTLGenerator(json_file)
            data = generator.data
            
            preview_window = tk.Toplevel(self.root)
            preview_window.title("JSON Data Preview")
            preview_window.geometry("500x400")
            
            text_widget = tk.Text(preview_window, wrap=tk.WORD)
            scrollbar = ttk.Scrollbar(preview_window, orient=tk.VERTICAL, command=text_widget.yview)
            text_widget.configure(yscrollcommand=scrollbar.set)
            
            text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
            scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
            
            # Format JSON data for display
            import json
            formatted_json = json.dumps(data, indent=2)
            text_widget.insert(tk.END, formatted_json)
            text_widget.config(state=tk.DISABLED)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error reading JSON file: {str(e)}")


def main():
    root = tk.Tk()
    app = MTLGeneratorGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
