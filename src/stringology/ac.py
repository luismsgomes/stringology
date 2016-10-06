
class AhoCorasick:
    '''
    Aho-Corasick implementation

    For an accurate algorithm description see:
    Dan Gusfield, "Algorithms on Strings, Trees, and Sequences: Computer
    Science and Computational Biology", Cambridge University Press, 1997, p 58

    >>> lookup = AhoCorasick(['AB', 'ABC', 'BC', 'C'])
    >>> list(lookup('ABCD'))
    [('AB', 0), ('ABC', 0), ('BC', 1), ('C', 2)]
    '''

    class Node:
        # fail = failure link; out = output link
        __slots__ = 'fail', 'out', 'pattern', 'edges'

        def __init__(self):
            self.fail = None
            self.out = None
            self.pattern = None
            self.edges = {}

    def __call__(self, text):
        node = self.root
        for position, symbol in enumerate(text, start=1):
            while symbol not in node.edges and node is not self.root:
                node = node.fail
            if symbol in node.edges:
                node = node.edges[symbol]
                if node.pattern is not None:
                    yield node.pattern, position - len(node.pattern)
                other = node.out
                while other is not None:
                    yield other.pattern, position - len(other.pattern)
                    other = other.out

    def __init__(self, patterns):
        # create nodes and edges
        self.root = self.Node()
        for pattern in patterns:
            node = self.root
            for symbol in pattern:
                if symbol not in node.edges:
                    node.edges[symbol] = self.Node()
                node = node.edges[symbol]
            node.pattern = pattern
        # create the failure and output links
        self.root.fail = self.root
        for node in self.root.edges.values():
            node.fail = self.root
        # breadth-first traversal of the tree (excluding the root)
        to_visit = list(self.root.edges.values())
        for parent in to_visit:
            for symbol, node in parent.edges.items():
                to_visit.append(node)
                w = parent.fail
                while symbol not in w.edges and w is not self.root:
                    w = w.fail
                if symbol in w.edges:
                    node.fail = w.edges[symbol]
                else:
                    node.fail = self.root
                if node.fail.pattern is not None:
                    node.out = node.fail
                else:
                    node.out = node.fail.out


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
