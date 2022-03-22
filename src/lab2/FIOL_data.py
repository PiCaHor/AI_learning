class Message:
    def __init__(self, left_node='', relation='', right_node=''):
        self.left_node = left_node
        self.relation = relation
        self.right_node = right_node

    def printf(self):
        print("This is a test: The relation is " + self.relation + "(" + self.left_node + "," + self.right_node + ")")

    def left(self):
        return self.left_node

    def right(self):
        return self.right_node

    def relat(self):
        return self.relation


class Logic:
    def __init__(self, relation='', mod=0):
        self.relation = relation
        self.mod = mod

    def get_relate(self):
        return self.relation

    def get_mod(self):
        return self.mod
