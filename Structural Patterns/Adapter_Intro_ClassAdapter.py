# Existing class with an incompatible interface
class TextView:
    def get_extent(self):
        return "Text dimensions calculated"

# Expected interface in the drawing editor
class Shape:
    def bounding_box(self):
        raise NotImplementedError

# Adapter: Inherits from both Shape and TextView
class TextShape(Shape, TextView):  # Inheriting both classes
    def bounding_box(self):
        return self.get_extent()  # Calls TextView's method

# Usage
text_shape = TextShape()
print(text_shape.bounding_box())  # Output: "Text dimensions calculated"
