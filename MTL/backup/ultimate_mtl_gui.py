#!/usr/bin/env python3
"""
Ultimate MTL Document Generator

This is the final, comprehensive solution that combines all the features:
- Template analysis
- Multiple placeholder formats
- GUI and command-line interfaces
- Batch processing
- Custom formatting preservation
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from custom_mtl_generator import CustomMTLGenerator
from template_processor import TemplateAnalyzer


class UltimateMTLGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Ultimate MTL Document Generator")
        self.root.geometry("700x500")
        
        # Variables
        self.json_file_var = tk.StringVar(value="mtl1_data.json")
        self.template_file_var = tk.StringVar(value="MTL1_MasterTemplate_Placeholders.docx")
        self.output_file_var = tk.StringVar()
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky="nsew")
        
        # Title
        title_label = ttk.Label(main_frame, text="Ultimate MTL Document Generator", 
                               font=('Arial', 16, 'bold'))
        title_label.grid(row=0, column=0, columnspan=3, pady=10)
        
        # JSON File Selection
        ttk.Label(main_frame, text="JSON Data File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.json_file_var, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_json_file).grid(row=1, column=2, padx=5, pady=5)
        
        # Template File Selection
        ttk.Label(main_frame, text="Template File:").grid(row=2, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.template_file_var, width=50).grid(row=2, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_template_file).grid(row=2, column=2, padx=5, pady=5)
        
        # Output File Selection
        ttk.Label(main_frame, text="Output File (optional):").grid(row=3, column=0, sticky=tk.W, pady=5)
        ttk.Entry(main_frame, textvariable=self.output_file_var, width=50).grid(row=3, column=1, padx=5, pady=5)
        ttk.Button(main_frame, text="Browse", command=self.browse_output_file).grid(row=3, column=2, padx=5, pady=5)
        
        # Buttons frame
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=4, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="Analyze Template", command=self.analyze_template).grid(row=0, column=0, padx=5)
        ttk.Button(buttons_frame, text="Generate Document", command=self.generate_document).grid(row=0, column=1, padx=5)
        ttk.Button(buttons_frame, text="Preview JSON", command=self.preview_json).grid(row=0, column=2, padx=5)
        ttk.Button(buttons_frame, text="Clear Output", command=self.clear_output).grid(row=0, column=3, padx=5)
        
        # Output text area
        ttk.Label(main_frame, text="Output:").grid(row=5, column=0, sticky=tk.W, pady=(10, 5))
        
        text_frame = ttk.Frame(main_frame)
        text_frame.grid(row=6, column=0, columnspan=3, sticky="nsew", pady=5)
        
        self.output_text = tk.Text(text_frame, height=15, width=80, wrap=tk.WORD, font=('Consolas', 9))
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
    
    def clear_output(self):
        """Clear the output text area."""
        self.output_text.delete(1.0, tk.END)
    
    def analyze_template(self):
        """Analyze the template structure."""
        template_file = self.template_file_var.get()
        
        if not template_file or not os.path.exists(template_file):
            self.log_message("❌ Template file not found or not specified")
            return
        
        self.log_message("🔍 Analyzing template...")
        
        try:
            # Redirect analyzer output to our text widget
            import io
            import sys
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            
            with redirect_stdout(output_buffer):
                analyzer = TemplateAnalyzer(template_file)
                analyzer.analyze_template()
            
            analysis_output = output_buffer.getvalue()
            self.log_message(analysis_output)
            
        except Exception as e:
            self.log_message(f"❌ Error analyzing template: {str(e)}")
    
    def generate_document(self):
        """Generate the Word document."""
        json_file = self.json_file_var.get()
        template_file = self.template_file_var.get()
        output_file = self.output_file_var.get()
        
        # Clear output
        self.clear_output()
        
        # Validate inputs
        if not json_file or not os.path.exists(json_file):
            self.log_message("❌ JSON file not found or not specified")
            return
            
        if not template_file or not os.path.exists(template_file):
            self.log_message("❌ Template file not found or not specified")
            return
        
        try:
            # Redirect generator output to our text widget
            import io
            import sys
            from contextlib import redirect_stdout
            
            output_buffer = io.StringIO()
            
            self.log_message("🚀 Starting document generation...")
            
            with redirect_stdout(output_buffer):
                generator = CustomMTLGenerator(json_file)
                result_file = generator.generate_document(
                    template_path=template_file,
                    output_path=output_file
                )
            
            generation_output = output_buffer.getvalue()
            self.log_message(generation_output)
            
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
            generator = CustomMTLGenerator(json_file)
            data = generator.data
            
            preview_window = tk.Toplevel(self.root)
            preview_window.title("JSON Data Preview")
            preview_window.geometry("600x500")
            
            text_widget = tk.Text(preview_window, wrap=tk.WORD, font=('Consolas', 10))
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
    app = UltimateMTLGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
