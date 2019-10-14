# *-* coding: utf-8 *-*
class TreeNode:
    def __init__(self, name, fre, parent):
        self.name = name
        self.frequent = fre
        self.nodeLink = None
        self.parent = parent
        self.children = {}

    def addFre(self, fre):
        self.frequent += fre

    def show(self, deep=1):
        print('  ' * deep, self.name, ' ', self.frequent)
        for child in self.children.values():
            child.show(deep + 1)
