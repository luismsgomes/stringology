

def align(s1, s2, gap=' '):
    '''aligns two strings

    >>> print(*align('pharmacy', 'farmácia', gap='_'), sep='\\n')
    pharmac_y
    _farmácia

    >>> print(*align('advantage', 'vantagem', gap='_'), sep='\\n')
    advantage_
    __vantagem

    '''
    # first we compute the dynamic programming table
    m, n = len(s1), len(s2)
    table = []  # the table is extended lazily, one row at a time
    row = list(range(n+1))  # the first row is 0, 1, 2, ..., n
    table.append(list(row))  # copy row and insert into table
    for i in range(m):
        p = i
        row[0] = i+1
        for j in range(n):
            t = 0 if s1[i] == s2[j] else 1
            p, row[j+1] = row[j+1], min(p+t, row[j]+1, row[j+1]+1)
        table.append(list(row))  # copy row and insert into table
    # now we trace the best alignment path from cell [m][n] to cell [0],[0]
    s1_, s2_ = '', ''

    i, j = m, n
    while i != 0 and j != 0:
        _, i, j, s1_, s2_ = min(
            (table[i-1][j-1], i-1, j-1, s1[i-1]+s1_, s2[j-1]+s2_),
            (table[i-1][j], i-1, j, s1[i-1]+s1_, gap+s2_),
            (table[i][j-1], i, j-1, gap+s1_, s2[j-1]+s2_)
        )
    if i != 0:
        s1_ = s1[:i]+s1_
        s2_ = gap*i+s2_
    if j != 0:
        s1_ = gap*j+s1_
        s2_ = s2[:j]+s2_
    return s1_, s2_


def mismatches(s1, s2, context=0):
    '''extract mismatched segments from aligned strings

    >>> list(mismatches(*align('pharmacy', 'farmácia'), context=1))
    [('pha', ' fa'), ('mac', 'mác'), ('c y', 'cia')]

    >>> list(mismatches(*align('constitution', 'constituição'), context=1))
    [('ution', 'uição')]

    >>> list(mismatches(*align('idea', 'ideia'), context=1))
    [('e a', 'eia')]

    >>> list(mismatches(*align('instructed', 'instruído'), context=1))
    [('ucted', 'u ído')]

    >>> list(mismatches(*align('concluded', 'concluído'), context=1))
    [('uded', 'uído')]
    '''
    n = len(s1)
    assert(len(s2) == n)
    lct, rct = context, context if isinstance(context, int) else context
    i = None
    for j in range(n):
        if s1[j] == s2[j]:
            if i is not None:
                # report mismatch segment [i:j] with lct chars of left context
                # and rct chars of right context
                p, q = max(0, i-lct), min(j+rct, n)
                yield s1[p:q], s2[p:q]
                i = None
        elif i is None:
                i = j
    if i is not None:
        p = max(i-lct, 0)
        yield s1[p:], s2[p:]
