class Node:
 
    def __init__(self, data):
 
        self.data = data
 
        self.left = None
 
        self.right = None
 
class BinaryTree:
 
    def __init__(self):
 
        self.root = None
 
         
 
    def add_node(self, data):
 
        new_node = Node(data)
 
        # If root is None, assign the new node to the root
 
        if self.root is None:
 
            self.root = new_node
 
        else:
 
            focus_node = self.root
 
            parent = None
 
            while True:
 
                parent = focus_node
 
                 
 
                # If data is less than focus_node, assign focus_node to the left child
 
                if data < focus_node.data:
 
                    focus_node = focus_node.left
 
                    # If there's no left child, assign the new node to the left child
 
                    if focus_node is None:
 
                        parent.left = new_node
 
                        return
 
                else:
 
                    focus_node = focus_node.right
 
                    # If there's no right child, assign the new node to the right child
 
                    if focus_node is None:
 
                        parent.right = new_node
 
                        return
 
    def pre_order_traversal(self, focus_node):
 
        if focus_node is not None:
 
            print(focus_node.data, end=" ")
 
            self.pre_order_traversal(focus_node.left)
 
            self.pre_order_traversal(focus_node.right)
 
# Example usage
 
tree = BinaryTree()
 
tree.add_node(50)
 
tree.add_node(25)
 
tree.add_node(75)
 
tree.add_node(12)
 
tree.add_node(37)
 
tree.add_node(43)
 
tree.add_node(30)
 
tree.pre_order_traversal(tree.root)

# Time Complexity: O(h), h is height of tree.
# Auxiliary Space: O(h), h is height of tree.