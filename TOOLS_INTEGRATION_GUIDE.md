# Tools Integration Guide

This guide shows how to integrate all the tool modules into your main.py PyQt6 application.

## Available Tool Modules

1. **tools_brush.py** - Various brush types (Basic, Airbrush, Watercolor, Pencil, Marker, Chalk, Oil, Smudge, Blur, Sharpen)
2. **tools_selection.py** - Selection tools (Rectangular, Elliptical, Freehand, Polygonal, Magic Wand)
3. **tools_shapes.py** - Shape tools (Rectangle, Ellipse, Line, Polygon, Star, Arrow)
4. **tools_perspective.py** - Perspective tools for POV images (Circular, Spherical, Cylindrical, Isometric)
5. **tools_special_brushes.py** - Special brushes (Pattern, Stamp, Noise) and Custom Brush Creator
6. **tools_transform.py** - Transform tools (Move, Rotate, Scale, Flip, Skew, Perspective Transform)
7. **tools_fill.py** - Fill and Eraser tools (Bucket Fill, Basic Eraser, Background Eraser, Magic Eraser, Smudge Eraser)
8. **tools_text.py** - Text tools (Basic Text, Rich Text, Text on Path)
9. **tools_filters.py** - Image filters (Blur, Sharpen, Emboss, Edge Detect, Noise, Brightness/Contrast, Hue/Saturation, Invert, Grayscale)
10. **tools_color.py** - Color tools (Color Picker, Gradient, Color Balance, Color Replace, Selective Color)
11. **tools_utility.py** - Utility tools (Crop, Resize, Canvas Size, Rotate Canvas, Flip Canvas, Histogram, Info)

## Basic Integration Example

```python
# In your main.py, add these imports:

from tools_brush import BasicBrush, AirbrushTool, WatercolorBrush, PencilTool, MarkerTool
from tools_selection import RectangularSelection, EllipticalSelection, FreehandSelection, MagicWandSelection
from tools_shapes import RectangleTool, EllipseTool, LineTool, StarTool
from tools_perspective import CircularPerspective, SphericalPerspective, CylindricalPerspective, PerspectiveManager
from tools_special_brushes import CustomBrush, BrushLibrary, PatternBrush, StampBrush
from tools_transform import MoveTool, RotateTool, ScaleTool, FlipTool
from tools_fill import FillTool, BasicEraser, MagicEraser
from tools_text import TextTool, RichTextTool
from tools_filters import BlurFilter, SharpenFilter, BrightnessContrastFilter
from tools_color import ColorPickerTool, GradientTool, MultiStopGradient
from tools_utility import CropTool, ResizeTool, CanvasSizeTool

# In your Canvas class, add tool management:

class Canvas(QWidget):
    def __init__(self):
        super().__init__()
        # ... existing code ...
        
        # Initialize tools
        self.current_tool = None
        self.tool_type = "brush"  # brush, selection, shape, etc.
        
        # Brush tools
        self.basic_brush = BasicBrush()
        self.airbrush = AirbrushTool()
        self.watercolor = WatercolorBrush()
        self.current_brush = self.basic_brush
        
        # Selection tools
        self.rect_selection = RectangularSelection()
        self.ellipse_selection = EllipticalSelection()
        self.freehand_selection = FreehandSelection()
        self.magic_wand = MagicWandSelection()
        self.current_selection = None
        
        # Shape tools
        self.rectangle_tool = RectangleTool()
        self.ellipse_tool = EllipseTool()
        self.line_tool = LineTool()
        self.current_shape = None
        
        # Perspective tools
        self.perspective_manager = PerspectiveManager()
        
        # Custom brushes
        self.brush_library = BrushLibrary()
        self.custom_brush = CustomBrush()
        
        # Other tools
        self.fill_tool = FillTool()
        self.eraser = BasicEraser()
        self.text_tool = TextTool()
        self.color_picker = ColorPickerTool()
        self.crop_tool = CropTool()
        
    def set_tool(self, tool_name):
        """Switch between tools"""
        self.tool_type = tool_name
        
    def mousePressEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton:
            world_pos = self.screen_to_world(e.position())
            
            if self.tool_type == "brush":
                self.drawing = True
                self.last_pos = world_pos
                self.path = QPainterPath()
                self.path.moveTo(world_pos)
                
            elif self.tool_type == "selection":
                if self.current_selection:
                    self.current_selection.start_selection(world_pos)
                    
            elif self.tool_type == "fill":
                self.fill_tool.fill_at_point(self.layers.current.pixmap, world_pos)
                self.update()
                
            elif self.tool_type == "color_picker":
                color = self.color_picker.pick_color(self.layers.current.pixmap, world_pos)
                self.brush_color = color
                
            # ... handle other tools ...
            
    def mouseMoveEvent(self, e):
        if self.drawing and self.tool_type == "brush":
            cur = self.screen_to_world(e.position())
            self.path.quadTo(self.last_pos, (self.last_pos + cur) / 2)
            
            painter = QPainter(self.layers.current.pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            self.current_brush.draw_stroke(painter, self.path)
            painter.end()
            
            self.last_pos = cur
            self.update()
            
        # ... handle other tools ...
        
    def mouseReleaseEvent(self, e):
        if e.button() == Qt.MouseButton.LeftButton and self.drawing:
            self.drawing = False
            # Create undo command
            cmd = DrawCommand(self.layers.current, self.path, self.current_brush.create_pen())
            self.undo_stack.push(cmd)
```

## Advanced Features

### Custom Brush Creation

```python
# Create a custom brush
custom_brush = CustomBrush()
custom_brush.name = "My Custom Brush"
custom_brush.size = 30
custom_brush.hardness = 0.7
custom_brush.spacing = 0.3
custom_brush.scatter = 0.2
custom_brush.color_dynamics = True
custom_brush.size_dynamics = True

# Create brush tip shape
custom_brush.create_brush_tip("round")  # or "square", "flat", "texture"

# Save brush
custom_brush.save_brush("my_brush.json")

# Load brush
loaded_brush = CustomBrush()
loaded_brush.load_brush("my_brush.json")

# Add to library
brush_library = BrushLibrary()
brush_library.add_brush("My Brush", custom_brush)
```

### Perspective Tools for POV Images

```python
# Set up circular perspective for fisheye POV
perspective_manager = PerspectiveManager()
perspective_manager.set_perspective("circular")
circular = perspective_manager.perspectives["circular"]
circular.center = QPointF(4000, 4000)  # Canvas center
circular.radius = 2000
circular.strength = 1.0

# Transform points when drawing
world_pos = perspective_manager.transform_point(screen_pos)

# Draw perspective grid
perspective_manager.draw_grid(painter, canvas_bounds)
```

### Using Filters

```python
# Apply blur filter
blur = BlurFilter()
blur.radius = 10
blur.intensity = 1.0
blurred_pixmap = blur.apply(layer.pixmap)

# Apply brightness/contrast
brightness = BrightnessContrastFilter()
brightness.brightness = 20
brightness.contrast = 15
adjusted_pixmap = brightness.apply(layer.pixmap)
```

### Gradient Tool

```python
# Create linear gradient
gradient = GradientTool()
gradient.start_point = QPointF(0, 0)
gradient.end_point = QPointF(100, 100)
gradient.start_color = QColor("#ff0000")
gradient.end_color = QColor("#0000ff")
gradient.gradient_type = "linear"

# Fill selection with gradient
painter = QPainter(layer.pixmap)
gradient.fill_area(painter, selection_path)
painter.end()
```

## Tool Palette UI Integration

Add tool buttons to your toolbar:

```python
# In RemVi.__init__:
tb = self.addToolBar("Tools")

# Brush tools
tb.addAction("Brush", lambda: self.canvas.set_tool("brush"))
tb.addAction("Airbrush", lambda: self.canvas.set_tool("airbrush"))
tb.addAction("Watercolor", lambda: self.canvas.set_tool("watercolor"))
tb.addAction("Pencil", lambda: self.canvas.set_tool("pencil"))

# Selection tools
tb.addAction("Rect Select", lambda: self.canvas.set_tool("rect_selection"))
tb.addAction("Ellipse Select", lambda: self.canvas.set_tool("ellipse_selection"))
tb.addAction("Freehand Select", lambda: self.canvas.set_tool("freehand_selection"))
tb.addAction("Magic Wand", lambda: self.canvas.set_tool("magic_wand"))

# Shape tools
tb.addAction("Rectangle", lambda: self.canvas.set_tool("rectangle"))
tb.addAction("Ellipse", lambda: self.canvas.set_tool("ellipse"))
tb.addAction("Line", lambda: self.canvas.set_tool("line"))
tb.addAction("Star", lambda: self.canvas.set_tool("star"))

# Other tools
tb.addAction("Fill", lambda: self.canvas.set_tool("fill"))
tb.addAction("Eraser", lambda: self.canvas.set_tool("eraser"))
tb.addAction("Text", lambda: self.canvas.set_tool("text"))
tb.addAction("Color Picker", lambda: self.canvas.set_tool("color_picker"))
tb.addAction("Crop", lambda: self.canvas.set_tool("crop"))

# Perspective tools
perspective_menu = tb.addMenu("Perspective")
perspective_menu.addAction("None", lambda: self.canvas.perspective_manager.set_perspective("none"))
perspective_menu.addAction("Circular", lambda: self.canvas.perspective_manager.set_perspective("circular"))
perspective_menu.addAction("Spherical", lambda: self.canvas.perspective_manager.set_perspective("spherical"))
perspective_menu.addAction("Cylindrical", lambda: self.canvas.perspective_manager.set_perspective("cylindrical"))
```

## Notes

- All tools are designed to work with QPixmap and QPainter
- Most tools support undo/redo through your existing DrawCommand system
- Custom brushes can be saved/loaded as JSON files
- Perspective tools transform coordinates before drawing
- Filters work on QPixmap/QImage objects
- All tools are modular and can be used independently

