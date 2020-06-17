class Node:
    def __init__(self, name, parent=None):
        self.name = name
        self.children = []
        if parent:
            self.parent = parent
            parent.add_child(self)
    
    def add_child(self, child):
        self.children.append(child)

    def printNode(self, level):
        screen = str(self.name) + "\n"
        if self.children:
            for c in self.children:
                screen += "   "*level + "|---" + str(c.printNode(level+1)) + "\n"
            return screen
        else:
            return self.name

def printTree(root):
    screen = root.printNode(0)
    print(screen)