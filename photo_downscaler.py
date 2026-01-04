"""
Photo Batch Downscaler - A simple GUI tool for batch resizing high-resolution photos
Author: Your Name
License: MIT
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinterdnd2 import DND_FILES, TkinterDnD
from PIL import Image, ExifTags
import os
from pathlib import Path
import threading


class PhotoDownscalerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Photo Batch Downscaler")
        self.root.geometry("900x700")
        self.root.resizable(True, True)
        
        # Default settings
        self.max_width = tk.IntVar(value=2048)
        self.dpi = tk.IntVar(value=100)
        self.quality = tk.IntVar(value=80)
        self.output_folder = tk.StringVar(value="")
        
        # File list
        self.image_files = []
        
        self.create_widgets()
        
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights for responsiveness
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(2, weight=1)
        
        # Title
        title_label = ttk.Label(main_frame, text="Photo Batch Downscaler", 
                                font=("Segoe UI", 16, "bold"))
        title_label.grid(row=0, column=0, pady=(0, 10), sticky=tk.W)
        
        # Settings Frame
        settings_frame = ttk.LabelFrame(main_frame, text="Export Settings", padding="10")
        settings_frame.grid(row=1, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        settings_frame.columnconfigure(1, weight=1)
        
        # Max Width
        ttk.Label(settings_frame, text="Max Width (px):").grid(row=0, column=0, sticky=tk.W, pady=5)
        width_spinbox = ttk.Spinbox(settings_frame, from_=100, to=10000, 
                                     textvariable=self.max_width, width=15)
        width_spinbox.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        # DPI
        ttk.Label(settings_frame, text="Resolution (DPI):").grid(row=0, column=2, sticky=tk.W, pady=5, padx=(20, 0))
        dpi_spinbox = ttk.Spinbox(settings_frame, from_=72, to=300, 
                                   textvariable=self.dpi, width=15)
        dpi_spinbox.grid(row=0, column=3, sticky=tk.W, padx=5)
        
        # Quality
        ttk.Label(settings_frame, text="Quality (%):").grid(row=1, column=0, sticky=tk.W, pady=5)
        quality_scale = ttk.Scale(settings_frame, from_=1, to=100, 
                                  variable=self.quality, orient=tk.HORIZONTAL)
        quality_scale.grid(row=1, column=1, sticky=(tk.W, tk.E), padx=5)
        quality_label = ttk.Label(settings_frame, textvariable=self.quality)
        quality_label.grid(row=1, column=2, sticky=tk.W, padx=(20, 0))
        
        # Output Folder
        ttk.Label(settings_frame, text="Output Folder:").grid(row=2, column=0, sticky=tk.W, pady=5)
        output_entry = ttk.Entry(settings_frame, textvariable=self.output_folder)
        output_entry.grid(row=2, column=1, columnspan=2, sticky=(tk.W, tk.E), padx=5)
        browse_btn = ttk.Button(settings_frame, text="Browse...", command=self.browse_output_folder)
        browse_btn.grid(row=2, column=3, padx=5)
        
        # File List Frame
        files_frame = ttk.LabelFrame(main_frame, text="Images to Process (Drag & Drop)", padding="10")
        files_frame.grid(row=2, column=0, sticky=(tk.W, tk.E, tk.N, tk.S), pady=(0, 10))
        files_frame.columnconfigure(0, weight=1)
        files_frame.rowconfigure(0, weight=1)
        
        # Listbox with scrollbar
        scrollbar = ttk.Scrollbar(files_frame, orient=tk.VERTICAL)
        self.file_listbox = tk.Listbox(files_frame, yscrollcommand=scrollbar.set, 
                                       selectmode=tk.EXTENDED, height=15)
        scrollbar.config(command=self.file_listbox.yview)
        
        self.file_listbox.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))
        
        # Enable drag and drop
        self.file_listbox.drop_target_register(DND_FILES)
        self.file_listbox.dnd_bind('<<Drop>>', self.on_drop)
        
        # Buttons Frame
        buttons_frame = ttk.Frame(files_frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=(10, 0))
        
        add_btn = ttk.Button(buttons_frame, text="Add Images...", command=self.add_images)
        add_btn.grid(row=0, column=0, padx=5)
        
        remove_btn = ttk.Button(buttons_frame, text="Remove Selected", command=self.remove_selected)
        remove_btn.grid(row=0, column=1, padx=5)
        
        clear_btn = ttk.Button(buttons_frame, text="Clear All", command=self.clear_all)
        clear_btn.grid(row=0, column=2, padx=5)
        
        # Progress Frame
        progress_frame = ttk.Frame(main_frame)
        progress_frame.grid(row=3, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        progress_frame.columnconfigure(0, weight=1)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Progressbar(progress_frame, variable=self.progress_var, 
                                           maximum=100, mode='determinate')
        self.progress_bar.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=5)
        
        self.status_label = ttk.Label(progress_frame, text="Ready", foreground="gray")
        self.status_label.grid(row=1, column=0, sticky=tk.W)
        
        # Process Button
        self.process_btn = ttk.Button(main_frame, text="Process Images", 
                                      command=self.process_images, style="Accent.TButton")
        self.process_btn.grid(row=4, column=0, pady=5)
        
    def browse_output_folder(self):
        folder = filedialog.askdirectory(title="Select Output Folder")
        if folder:
            self.output_folder.set(folder)
    
    def on_drop(self, event):
        files = self.root.tk.splitlist(event.data)
        for file_path in files:
            if self.is_valid_image(file_path):
                if file_path not in self.image_files:
                    self.image_files.append(file_path)
                    self.file_listbox.insert(tk.END, os.path.basename(file_path))
    
    def add_images(self):
        files = filedialog.askopenfilenames(
            title="Select Images",
            filetypes=[
                ("Image files", "*.jpg *.jpeg *.png *.bmp *.tiff *.webp"),
                ("All files", "*.*")
            ]
        )
        for file_path in files:
            if file_path not in self.image_files:
                self.image_files.append(file_path)
                self.file_listbox.insert(tk.END, os.path.basename(file_path))
    
    def remove_selected(self):
        selected = self.file_listbox.curselection()
        for index in reversed(selected):
            self.file_listbox.delete(index)
            self.image_files.pop(index)
    
    def clear_all(self):
        self.file_listbox.delete(0, tk.END)
        self.image_files.clear()
    
    def is_valid_image(self, file_path):
        valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff', '.webp'}
        return Path(file_path).suffix.lower() in valid_extensions
    
    def process_images(self):
        if not self.image_files:
            messagebox.showwarning("No Images", "Please add images to process.")
            return
        
        output_folder = self.output_folder.get()
        if not output_folder:
            messagebox.showwarning("No Output Folder", 
                                 "Please select an output folder.")
            return
        
        # Create output folder if it doesn't exist
        os.makedirs(output_folder, exist_ok=True)
        
        # Disable button during processing
        self.process_btn.config(state='disabled')
        
        # Run processing in a separate thread
        thread = threading.Thread(target=self.process_thread, daemon=True)
        thread.start()
    
    def process_thread(self):
        total = len(self.image_files)
        max_width = self.max_width.get()
        dpi = self.dpi.get()
        quality = self.quality.get()
        output_folder = self.output_folder.get()
        
        success_count = 0
        error_count = 0
        
        for idx, file_path in enumerate(self.image_files):
            try:
                # Update status
                self.root.after(0, self.update_status, 
                              f"Processing {idx + 1}/{total}: {os.path.basename(file_path)}")
                
                # Process image
                self.resize_image(file_path, output_folder, max_width, dpi, quality)
                success_count += 1
                
                # Update progress
                progress = ((idx + 1) / total) * 100
                self.root.after(0, self.progress_var.set, progress)
                
            except Exception as e:
                error_count += 1
                print(f"Error processing {file_path}: {str(e)}")
        
        # Completion
        self.root.after(0, self.processing_complete, success_count, error_count)
    
    def resize_image(self, input_path, output_folder, max_width, dpi, quality):
        # Open image
        img = Image.open(input_path)
        
        # Preserve EXIF data
        exif_data = None
        if hasattr(img, '_getexif') and img._getexif() is not None:
            exif_data = img.info.get('exif')
        
        # Calculate new dimensions
        width, height = img.size
        if width > max_width:
            ratio = max_width / width
            new_width = max_width
            new_height = int(height * ratio)
        else:
            new_width, new_height = width, height
        
        # Resize image with high-quality resampling
        resized_img = img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        # Prepare output path
        file_name = os.path.basename(input_path)
        output_path = os.path.join(output_folder, file_name)
        
        # Save with settings
        save_kwargs = {
            'quality': quality,
            'dpi': (dpi, dpi),
        }
        
        # Add EXIF data if available
        if exif_data:
            save_kwargs['exif'] = exif_data
        
        # Determine format
        img_format = img.format if img.format else 'JPEG'
        
        resized_img.save(output_path, format=img_format, **save_kwargs)
    
    def update_status(self, message):
        self.status_label.config(text=message)
    
    def processing_complete(self, success_count, error_count):
        self.progress_var.set(100)
        self.status_label.config(text=f"Complete! Processed: {success_count}, Errors: {error_count}")
        self.process_btn.config(state='normal')
        
        messagebox.showinfo("Processing Complete", 
                          f"Successfully processed {success_count} images.\nErrors: {error_count}")


def main():
    root = TkinterDnD.Tk()
    app = PhotoDownscalerApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
