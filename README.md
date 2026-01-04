# Photo-Batch-Downscaler
A simple, fast, and user-friendly GUI application for batch resizing high-resolution photos, built in Python.
Designed for photographers, creatives, and anyone who needs to prepare images for the web without sacrificing quality.

## ✨ Features

- 🖱 **Drag & Drop support** for easy image import  
- 📐 **Batch resize by maximum width** (default: 2048 px)  
- 🖨 **Custom DPI control** (default: 100 DPI)  
- 🎚 **Adjustable JPEG quality** (default: 80%)  
- 🗂 **Choose custom output folder**  
- 🧠 **Preserves EXIF metadata** when available  
- ⚡ **High-quality LANCZOS resampling**  
- 📊 **Progress bar and status updates**  
- 🧵 **Background processing** (UI stays responsive)

**Supported formats**
- JPG / JPEG  
- PNG  
- TIFF  
- BMP  
- WEBP  

---

## 🖼 Use case

This tool is ideal if you:
- Want to upload photos to websites, portfolios, or social media
- Need consistent export settings across many images
- Prefer a lightweight desktop tool over heavy photo editors
- Want Lightroom-like export defaults without opening Lightroom

---

## 🛠 Requirements

- Python **3.9+**
- Operating Systems:
  - macOS
  - Windows
  - Linux (with Tk support)

---
## 📦 Installation

Clone the repository:

```bash
git clone https://github.com/yourusername/photo-batch-downscaler.git
cd photo-batch-downscaler
```

Install dependencies:
```bash
pip install pillow tkinterdnd2
```

## ▶️ Usage

Run the application:

```bash
python photo_downscaler.py
```

## Workflow

1. Drag & drop images into the window **or** click **Add Images**
2. Adjust export settings (width, DPI, quality)
3. Choose an output folder
4. Click **Process Images**
5. Done ✅

Processed images are saved using the original filenames.

---

## ⚙ Default Export Settings

| Setting     | Default  |
|------------|----------|
| Max width  | 2048 px  |
| Resolution | 100 DPI  |
| Quality    | 80%      |
| Resampling | LANCZOS  |

These defaults are chosen to match common **Lightroom web export presets**.

---

## 🧠 Technical Notes

- EXIF data is preserved when possible
- Images smaller than the max width are **not upscaled**
- Processing runs in a background thread to keep the UI responsive
- Uses **Pillow** for image handling and **tkinterdnd2** for drag & drop

---

## 🚀 Possible Extensions

Ideas if you want to extend the tool:

- Rename files on export
- Convert all images to JPEG / WebP
- Height-based resizing
- Preset profiles (Instagram, Web, Portfolio)
- CLI version for automation

---

## 📄 License

MIT License – feel free to use, modify, and share.

---

## 🙌 Contributions

Pull requests and suggestions are very welcome.  
If you use this tool in your workflow, a ⭐ on GitHub is always appreciated.



