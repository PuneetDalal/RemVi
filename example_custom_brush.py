"""
Example: Creating and Using Custom Brushes
This demonstrates how to create, customize, and use custom brushes like in Procreate
"""

from tools_special_brushes import CustomBrush, BrushLibrary
from PyQt6.QtGui import QPixmap, QColor
from PyQt6.QtCore import QPointF


# Example 1: Create a basic custom brush
def create_basic_custom_brush():
    """Create a simple custom brush"""
    brush = CustomBrush()
    brush.name = "My Custom Brush"
    brush.size = 30
    brush.opacity = 0.8
    brush.flow = 0.9
    brush.hardness = 0.7
    brush.spacing = 0.25
    brush.scatter = 0.1
    
    # Create brush tip shape
    brush.create_brush_tip("round")  # Options: "round", "square", "flat", "texture"
    
    return brush


# Example 2: Create a textured custom brush
def create_textured_brush():
    """Create a brush with texture"""
    brush = CustomBrush()
    brush.name = "Textured Brush"
    brush.size = 40
    brush.hardness = 0.3  # Soft edges
    
    # Load or create texture
    # texture = QPixmap("texture.png")
    # brush.texture = texture
    # brush.texture_scale = 1.0
    # brush.texture_opacity = 0.5
    
    # Create brush with texture shape
    brush.create_brush_tip("texture")
    
    return brush


# Example 3: Create a brush with dynamics (like Procreate)
def create_dynamic_brush():
    """Create a brush with color, size, and opacity dynamics"""
    brush = CustomBrush()
    brush.name = "Dynamic Brush"
    brush.size = 25
    
    # Enable dynamics
    brush.color_dynamics = True      # Color varies
    brush.size_dynamics = True       # Size varies
    brush.opacity_dynamics = True    # Opacity varies
    
    # Additional settings
    brush.scatter = 0.2              # Random scatter
    brush.rotation = 0                # Base rotation
    brush.spacing = 0.2              # Tighter spacing
    
    brush.create_brush_tip("round")
    
    return brush


# Example 4: Create brush from custom image
def create_brush_from_image(image_path):
    """Create brush from a custom image"""
    brush = CustomBrush()
    brush.name = "Image Brush"
    
    # Load custom brush tip image
    custom_tip = QPixmap(image_path)
    if not custom_tip.isNull():
        brush.create_brush_tip("round", custom_tip)
    
    brush.size = 50
    brush.hardness = 0.5
    
    return brush


# Example 5: Save and load brushes
def save_and_load_brush():
    """Demonstrate saving and loading brushes"""
    # Create and save brush
    brush = create_basic_custom_brush()
    brush.save_brush("my_custom_brush.json")
    
    # Load brush
    loaded_brush = CustomBrush()
    loaded_brush.load_brush("my_custom_brush.json")
    
    return loaded_brush


# Example 6: Using Brush Library
def use_brush_library():
    """Demonstrate brush library management"""
    library = BrushLibrary()
    
    # Add brushes
    brush1 = create_basic_custom_brush()
    brush2 = create_dynamic_brush()
    
    library.add_brush("Basic Brush", brush1)
    library.add_brush("Dynamic Brush", brush2)
    
    # List all brushes
    print("Available brushes:", library.list_brushes())
    
    # Get a brush
    my_brush = library.get_brush("Basic Brush")
    
    # Save entire library
    library.save_library("brush_library")
    
    # Load library
    new_library = BrushLibrary()
    new_library.load_library("brush_library")
    
    return library


# Example 7: Using custom brush for drawing
def draw_with_custom_brush(brush, painter, path, color):
    """Draw a stroke using a custom brush"""
    # Set brush color (will be applied to brush shape)
    brush.draw_stroke(painter, path, color)


# Example 8: Advanced brush configuration
def create_advanced_brush():
    """Create a highly customized brush"""
    brush = CustomBrush()
    brush.name = "Advanced Brush"
    
    # Basic properties
    brush.size = 35
    brush.opacity = 0.85
    brush.flow = 0.75
    brush.hardness = 0.6
    
    # Spacing and scatter
    brush.spacing = 0.15  # Very tight spacing for smooth strokes
    brush.scatter = 0.15  # Slight random scatter
    
    # Dynamics
    brush.color_dynamics = True
    brush.size_dynamics = True
    brush.opacity_dynamics = True
    
    # Rotation
    brush.rotation = 45  # Rotate brush 45 degrees
    
    # Texture (if you have one)
    # brush.texture = QPixmap("texture.png")
    # brush.texture_scale = 0.8
    # brush.texture_rotation = 0
    # brush.texture_opacity = 0.4
    
    # Create brush tip
    brush.create_brush_tip("round")
    
    return brush


if __name__ == "__main__":
    # Example usage
    print("Creating custom brushes...")
    
    # Create a basic brush
    basic_brush = create_basic_custom_brush()
    print(f"Created: {basic_brush.name}")
    
    # Create a dynamic brush
    dynamic_brush = create_dynamic_brush()
    print(f"Created: {dynamic_brush.name}")
    
    # Save brushes
    basic_brush.save_brush("basic_brush.json")
    dynamic_brush.save_brush("dynamic_brush.json")
    print("Brushes saved!")
    
    # Load brush
    loaded = CustomBrush()
    loaded.load_brush("basic_brush.json")
    print(f"Loaded: {loaded.name}")

