import os

class DelegateTreeDisplay:
    def __init__(self, delegate, root_path):
        self.delegate = delegate
        self.root_path = root_path

    def show(self, node=None, indent=0):
        """Recursive display using delegate"""
        if node is None:
            node = self.root_path
        print("  " * indent + f"📁 {os.path.basename(node)}")
        for child in self.delegate.get_children(node):
            self.show(child, indent + 1)

# =====================================
# 3️⃣ Parameterized Adapters Approach
# =====================================
class TreeDisplay:
    def __init__(self, get_children_func, render_node_func):
        self.get_children = get_children_func
        self.render_node = render_node_func

    def show(self, node, indent=0):
        """Recursive display of directories"""
        print("  " * indent + self.render_node(node))
        for child in self.get_children(node):
            self.show(child, indent + 1)

# Dynamically get the parent directory of the script's folder
current_file_path = os.path.abspath(__file__)  # Absolute path of the script
script_directory = os.path.dirname(current_file_path)  # Folder of the script
directory_path = os.path.dirname(script_directory)  # Parent folder


# 🔹 Using Delegate Adapter
print("\n🔹 Using Delegate Objects Approach")
delegate_adapter = DelegateTreeDisplay(DirectoryDelegate(), directory_path)
delegate_adapter.show()

