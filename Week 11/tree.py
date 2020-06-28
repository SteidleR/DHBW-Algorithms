class Node:
    """Element of a tree
    Args:
        name (all): name of the Node
        parent (class:Node): parent node to attach to
    """
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        if parent:
            self.parent = parent
            parent.add_child(self)
    
    def add_child(self, child):
        """add a new child to the current node

        Args:
            child (class:Node): child node
        """
        self.children.append(child)

    def getChildValues(self):
        v = []
        for c in self.children:
            v.append(c.name)
        return v

    def printNode(self, level=0):
        """Converts the Node with subelements to printable string

        Args:
            level (int): level of opperation, for root node: 0

        Returns:
            str: string of current node with subelements
            all: name of node
        """
        screen = str(self.name) + "\n"
        if self.children:
            for c in self.children:
                screen += "   "*level + "|---" + str(c.printNode(level+1)) + "\n"
            return screen
        else:
            return self.name

def printTree(root):
    """Prints the complete Tree of given root

    Args:
        root (class:Node): root Node of tree
    """
    screen = root.printNode()
    print(screen)
