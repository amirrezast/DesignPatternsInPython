import os

# =====================================
# 1️⃣ Abstract Operations Approach
# =====================================
class AbstractTreeDisplay:
    def get_children(self, node):
        """Abstract method: Should return child nodes"""
        raise NotImplementedError

    def render_node(self, node):
        """Abstract method: Should return a string representation"""
        raise NotImplementedError

    def show(self, node, indent=0):
        """Recursive method to display nodes"""
        print("  " * indent + self.render_node(node))
        for child in self.get_children(node):
            self.show(child, indent + 1)

# ✅ Concrete implementation for directories
class DirectoryTreeDisplay(AbstractTreeDisplay):
    def __init__(self, root_path):
        self.root_path = root_path

    def get_children(self, node):
        return [os.path.join(node, d) for d in os.listdir(node) if os.path.isdir(os.path.join(node, d))]

    def render_node(self, node):
        return f"📁 {os.path.basename(node)}"


# Dynamically get the parent directory of the script's folder
current_file_path = os.path.abspath(__file__)  # Absolute path of the script
script_directory = os.path.dirname(current_file_path)  # Folder of the script
directory_path = os.path.dirname(script_directory)  # Parent folder

# 🔹 Using Abstract Adapter
print("\n🔹 Using Abstract Operations Approach")
abstract_adapter = DirectoryTreeDisplay(directory_path)
abstract_adapter.show(directory_path)
