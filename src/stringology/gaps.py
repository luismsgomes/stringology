"""
This module implements a solution to the gapped-keyword-set matching problem.

The gapped-keyword-set problem is the problem of finding occurrences of
(a large set of) keywords containing gaps within a text.

Solution: the solution implemented in this module employs the AhoCorasick
automaton to find fixed parts (i.e. the parts within the gaps) of keywords.

"""

from stringology.ac import AhoCorasick
from collections import defaultdict


class GappedKeywordMatcher:
    def __init__(self, patterns, toksep=' ', litsep='\t'):
        '''
        Gapped-keyword matcher.

        >>> search = GappedKeywordMatcher([
        ... [['A', 'B'], ['C']],
        ... [['A', 'B'], ['C'], ['D']],
        ... [['D', 'E']],
        ... ])
        >>> text = 'A B x y C z D E'.split()
        >>> for match in search(text):
        ...     print(match)
        ...
        ([['A', 'B'], ['C']], [0, 4])
        ([['A', 'B'], ['C'], ['D']], [0, 4, 6])
        ([['D', 'E']], [6])

        '''
        self.toksep = toksep
        self.litsep = litsep
        self.patterns = set()
        self.pattern_prefixes = set()
        literals = set()
        for pattern in patterns:
            for literal in pattern:
                assert all(
                    self.toksep not in tok and self.litsep not in tok
                    for tok in literal
                )
                literals.add(tuple(literal))
            str_literals = [self.toksep.join(literal) for literal in pattern]
            for k in range(1, len(pattern)):
                self.pattern_prefixes.add(self.litsep.join(str_literals[:k]))
            self.patterns.add(self.litsep.join(str_literals))
        self.searchliterals = AhoCorasick(literals)


    def __call__(self, sequence):
        pending = defaultdict(list) # pattern_prefix => occurrence offsets
        for (literal, start) in self.searchliterals(sequence):
            literal = self.toksep.join(literal)
            for prefix, occurrences in list(pending.items()):
                str_pattern = prefix + self.litsep + literal
                if str_pattern in self.patterns:
                    pattern = [
                        literal.split(self.toksep)
                        for literal in str_pattern.split(self.litsep)
                    ]
                    for positions in occurrences:
                        yield pattern, positions + [start]
                if str_pattern in self.pattern_prefixes:
                    pending[str_pattern].extend(
                        positions + [start] for positions in occurrences
                    )
            if literal in self.patterns:
                yield [literal.split(self.toksep)], [start]
            if literal in self.pattern_prefixes:
                pending[literal].append([start])
