# RemVi — Next Level Professional Image Editor

A high-performance, modern image editor built with PyQt6, optimized for low-end laptops while delivering a professional-grade UI/UX experience.

## Features

### Tools
- **Brush Tool** - Customizable brush with size and opacity controls
- **Eraser Tool** - Remove parts of your artwork
- **Eyedropper Tool** - Pick colors directly from the canvas
- **Pan Tool** - Navigate large canvases easily

### Color Management
- **Color Picker** - RGB sliders with live preview
- **Color Swatches** - Quick access to common colors
- **Advanced Color Dialog** - Full-featured color selection

### 📑 Layer System
- **Multiple Layers** - Work with unlimited layers
- **Layer Thumbnails** - Visual preview of each layer
- **Layer Properties** - Control opacity and blend modes
- **Layer Operations** - Create, delete, duplicate, and rename layers

### ⚡ Performance Optimizations
- **Dirty Region Rendering** - Only updates changed areas
- **Deferred Updates** - Throttled rendering for smooth drawing
- **Efficient Memory Usage** - Optimized for low-end hardware
- **Visible Region Culling** - Only renders what's on screen

### 🎯 Professional Features
- **Undo/Redo System** - 50-level history with memory-efficient storage
- **Multiple Blend Modes** - Normal, Multiply, Screen, Overlay, and more
- **Zoom & Pan** - Navigate large canvases with mouse wheel and middle-click
- **Export to PNG** - Save your work in high quality

## Requirements

- Python 3.8+
- PyQt6

## Installation

```bash
# Install PyQt6
pip install PyQt6

# Run the application
python main.py
```

## Usage

### Keyboard Shortcuts
- `Ctrl+N` - New file
- `Ctrl+O` - Open image
- `Ctrl+S` - Export PNG
- `Ctrl+Z` - Undo
- `Ctrl+Shift+Z` - Redo
- `Ctrl++` - Zoom in
- `Ctrl+-` - Zoom out
- `Ctrl+0` - Reset zoom
- `Ctrl+Q` - Quit

### Mouse Controls
- **Left Click** - Draw (with brush tool) or use current tool
- **Middle Click** - Pan canvas
- **Mouse Wheel** - Zoom in/out
- **Double Click Layer** - Rename layer

### Tools
- **Brush** - Draw on the canvas
- **Eraser** - Erase parts of the image
- **Eyedropper** - Pick colors from canvas
- **Pan** - Move around the canvas

## Performance Tips

The application is optimized for low-end laptops with:
- Efficient rendering that only updates changed regions
- Throttled updates during drawing (60fps cap)
- Visible region culling to avoid rendering off-screen content
- Memory-efficient undo system with region-based backups

## License

Custom image editor - feel free to modify and use as needed.
