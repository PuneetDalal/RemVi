# Tools and Features Summary

This document summarizes all the tools and features that have been added to RemVi, inspired by Krita and Procreate.

## 📁 Module Files Created

1. **tools_brush.py** - Brush tools
2. **tools_selection.py** - Selection tools
3. **tools_shapes.py** - Shape drawing tools
4. **tools_perspective.py** - Perspective/scale tools for POV images
5. **tools_special_brushes.py** - Special brushes and custom brush creator
6. **tools_transform.py** - Transform operations
7. **tools_fill.py** - Fill and eraser tools
8. **tools_text.py** - Text tools
9. **tools_filters.py** - Image filters and effects
10. **tools_color.py** - Color tools and adjustments
11. **tools_utility.py** - Utility tools

## 🎨 Brush Tools (tools_brush.py)

- **BasicBrush** - Standard brush with configurable hardness
- **AirbrushTool** - Soft airbrush with flow control
- **WatercolorBrush** - Watercolor effect with blending
- **PencilTool** - Hard-edged pencil
- **MarkerTool** - Semi-transparent marker
- **ChalkBrush** - Chalk with texture
- **OilBrush** - Oil paint brush
- **SmudgeTool** - Color blending tool
- **BlurTool** - Blur brush
- **SharpenTool** - Sharpen brush

## ✂️ Selection Tools (tools_selection.py)

- **RectangularSelection** - Rectangular selection
- **EllipticalSelection** - Elliptical/circular selection
- **FreehandSelection** - Freehand/lasso selection
- **PolygonalSelection** - Polygonal selection
- **MagicWandSelection** - Magic wand (color-based selection)
- **SelectionManager** - Manages selection operations (copy, cut, invert)

## 🔷 Shape Tools (tools_shapes.py)

- **RectangleTool** - Rectangle with rounded corners option
- **EllipseTool** - Ellipse/circle
- **LineTool** - Line with optional arrowheads
- **PolygonTool** - Polygon with configurable sides
- **StarTool** - Star shape with configurable points
- **ArrowTool** - Arrow shape

## 🌐 Perspective Tools (tools_perspective.py)

**For POV (Point of View) Images:**

- **CircularPerspective** - Circular/fisheye perspective
- **SphericalPerspective** - Spherical/360-degree perspective
- **CylindricalPerspective** - Cylindrical/panoramic perspective
- **IsometricPerspective** - Isometric projection
- **PerspectiveManager** - Manages perspective transformations

All perspective tools include:
- Grid visualization
- Point and path transformation
- Configurable strength/parameters

## 🖌️ Special Brushes (tools_special_brushes.py)

- **PatternBrush** - Brush that repeats a pattern
- **StampBrush** - Stamp brush with random rotation/scale
- **NoiseBrush** - Procedural noise texture brush
- **CustomBrush** - Full custom brush creator (Procreate-style)
  - Custom brush tip shapes (round, square, flat, texture)
  - Brush dynamics (size, opacity, color)
  - Scatter and rotation
  - Texture support
  - Save/load brushes as JSON
- **BrushLibrary** - Manages custom brush collection

## 🔄 Transform Tools (tools_transform.py)

- **MoveTool** - Move/translate layers
- **RotateTool** - Rotate with configurable center
- **ScaleTool** - Scale/resize with aspect ratio lock
- **FlipTool** - Horizontal/vertical flip
- **SkewTool** - Skew/distort
- **PerspectiveTransformTool** - 4-point perspective transform

## 🪣 Fill & Eraser Tools (tools_fill.py)

- **FillTool** - Bucket fill with tolerance and contiguous options
- **BasicEraser** - Eraser with configurable hardness
- **BackgroundEraser** - Erases similar colors
- **MagicEraser** - Removes all pixels of similar color
- **SmudgeEraser** - Blends/softens edges

## 📝 Text Tools (tools_text.py)

- **TextTool** - Basic text with font, color, formatting
- **RichTextTool** - HTML-based rich text
- **TextOnPathTool** - Text that follows a path

## 🎭 Filters & Effects (tools_filters.py)

- **BlurFilter** - Gaussian blur
- **SharpenFilter** - Sharpen filter
- **EmbossFilter** - Emboss effect
- **EdgeDetectFilter** - Edge detection (Sobel)
- **NoiseFilter** - Add noise
- **BrightnessContrastFilter** - Brightness/contrast adjustment
- **HueSaturationFilter** - Hue/saturation/lightness adjustment
- **InvertFilter** - Invert colors
- **GrayscaleFilter** - Convert to grayscale

## 🎨 Color Tools (tools_color.py)

- **ColorPickerTool** - Eyedropper with sample size options
- **GradientTool** - Linear, radial, and conical gradients
- **MultiStopGradient** - Gradients with multiple color stops
- **ColorBalanceTool** - Color balance adjustment (shadows/midtones/highlights)
- **ColorReplaceTool** - Replace colors with tolerance
- **SelectiveColorTool** - Selective color adjustment by color range

## 🛠️ Utility Tools (tools_utility.py)

- **CropTool** - Crop with aspect ratio options
- **ResizeTool** - Resize with interpolation options
- **CanvasSizeTool** - Adjust canvas size with anchor points
- **RotateCanvasTool** - Rotate entire canvas
- **FlipCanvasTool** - Flip entire canvas
- **HistogramTool** - Calculate image histogram
- **InfoTool** - Get image information

## 🎯 Key Features

### Custom Brush Creator (Procreate-style)
- Create custom brush tips (round, square, flat, or from image)
- Configure brush properties:
  - Size, opacity, flow, hardness
  - Spacing, scatter, rotation
  - Color dynamics, size dynamics, opacity dynamics
  - Texture support
- Save/load brushes as JSON files
- Brush library management

### Perspective Tools for POV Images
- **Circular/Fisheye** - For circular POV images
- **Spherical** - For 360-degree spherical POV
- **Cylindrical** - For panoramic POV images
- **Isometric** - For technical drawings
- All include grid visualization and coordinate transformation

### Special Brushes
- Pattern brushes with repeatable patterns
- Stamp brushes with randomization
- Noise brushes with procedural textures
- All support custom images/textures

## 📖 Usage

See `TOOLS_INTEGRATION_GUIDE.md` for detailed integration instructions.

All tools are designed to:
- Work with PyQt6 QPixmap and QPainter
- Support undo/redo (through your existing system)
- Be modular and independent
- Follow object-oriented design patterns

## 🔧 Dependencies

All tools use only:
- PyQt6 (QtWidgets, QtGui, QtCore)
- Python standard library (math, json, os)

No additional dependencies required!

