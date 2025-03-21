# Existing class with an incompatible interface
class TextView:
    def get_extent(self):
        return "Text dimensions calculated"

# Expected interface in the drawing editor
class Shape:
    def bounding_box(self):
        raise NotImplementedError

# Adapter: Uses composition (has a reference to TextView)
class TextShape(Shape):
    def __init__(self, text_view: TextView):
        self.text_view = text_view  # Composition: using TextView inside

    def bounding_box(self):
        return self.text_view.get_extent()  # Calls TextView's method

# Usage
text_view = TextView()
text_shape = TextShape(text_view)

print(text_shape.bounding_box())  # Output: "Text dimensions calculated"
