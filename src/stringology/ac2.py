import collections.abc


class Node:
    # fail = failure link; out = output link
    __slots__ = 'depth', 'fail', 'out', 'value', 'edges'

    def __init__(self, depth):
        self.depth = depth
        self.fail = None
        self.out = None
        self.value = None
        self.edges = {}


def items(node, path=()):
    if node.value:
        yield path, node.value
    for symbol, child in node.edges.items():
        for item in items(child, path + (symbol,)):
            yield item


class AhoCorasick2(collections.abc.MutableMapping):
    '''
    Aho-Corasick implementation

    For an accurate algorithm description see:
    Dan Gusfield, "Algorithms on Strings, Trees, and Sequences: Computer
    Science and Computational Biology", Cambridge University Press, 1997, p 58

    >>> automaton = AhoCorasick2([('AB', 1), ('ABC', 2), ('BC', 3), ('C', 4)])
    >>> list(automaton('ABCD'))
    [((0, 2), 1), ((0, 3), 2), ((1, 3), 3), ((2, 3), 4)]
    >>> 'AB' in automaton
    True
    >>> del automaton['AB']
    >>> 'AB' in automaton
    False
    >>> sorted(automaton.values())
    [2, 3, 4]

    '''

    def __init__(self, items=None):
        self.ready = False
        self.nitems = 0
        self.root = Node(0)
        if items:
            self.update(items)

    def __call__(self, seq):
        if not self.ready:
            self.prepare()
        node = self.root
        for position, symbol in enumerate(seq, start=1):
            while symbol not in node.edges and node is not self.root:
                node = node.fail
            if symbol in node.edges:
                node = node.edges[symbol]
                if node.value is not None:
                    yield (position - node.depth, position), node.value
                out = node.out
                while out is not None:
                    yield (position - out.depth, position), out.value
                    out = out.out

    def __setitem__(self, key, value):
        if value is None:
            raise ValueError(value)
        self.ready = False
        node = self.root
        for depth, symbol in enumerate(key, start=1):
            if symbol not in node.edges:
                node.edges[symbol] = Node(depth)
            node = node.edges[symbol]
        if node.value is None:
            self.nitems += 1
        node.value = value

    def __delitem__(self, key):
        self.ready = False
        node = self.root
        path = []
        for depth, symbol in enumerate(key, start=1):
            if symbol not in node.edges:
                raise KeyError(key)
            else:
                path.append((node, symbol))
                node = node.edges[symbol]
        if node.value is None:
            raise KeyError(key)
        node.value = None
        self.nitems -= 1
        if not node.edges:
            for parent, symbol in reversed(path):
                del parent.edges[symbol]
                if parent.edges or parent.value is not None:
                    break

    def __getitem__(self, key):
        node = self.root
        for symbol in key:
            if symbol not in node.edges:
                raise KeyError(key)
            node = node.edges[symbol]
        if node.value is None:
            raise KeyError(key)
        return node.value

    def __len__(self):
        return self.nitems

    def __iter__(self):
        for key, _ in items(self.root):
            yield key

    def prepare(self):
        if self.ready:
            return  # pragma: no cover
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
                if node.fail.value is not None:
                    node.out = node.fail
                else:
                    node.out = node.fail.out
        self.ready = True

    def items(self):
        return items(self.root)

    def values(self):
        for _, value in items(self.root):
            yield value


__all__ = ["AhoCorasick2"]


if __name__ == '__main__':  # pragma: no cover
    import doctest
    doctest.testmod()
