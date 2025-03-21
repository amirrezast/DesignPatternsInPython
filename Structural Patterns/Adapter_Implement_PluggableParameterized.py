import os

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


# 🔹 Using Parameterized Adapter
print("\n🔹 Using Parameterized Adapter")
param_adapter = TreeDisplay(
    get_children_func=lambda node: [os.path.join(node, d) for d in os.listdir(node) if os.path.isdir(os.path.join(node, d))],
    render_node_func=lambda node: f"📁 {os.path.basename(node)}"
)
param_adapter.show(directory_path)
