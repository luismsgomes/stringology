

def ed(s1, s2):
    '''edit distance

    >>> ed('', ''), ed('a', 'a'), ed('','a'), ed('a', ''), ed('a!a', 'a.a')
    (0, 0, 1, 1, 1)

    This implementation takes only O(min(|s1|,|s2|)) space.
    '''
    m, n = len(s1), len(s2)
    if m < n:
        m, n = n, m         # ensure n <= m, to use O(min(n,m)) space
        s1, s2 = s2, s1
    d = list(range(n+1))
    for i in range(m):
        p = i
        d[0] = i+1
        for j in range(n):
            t = 0 if s1[i] == s2[j] else 1
            p, d[j+1] = d[j+1], min(p+t, d[j]+1, d[j+1]+1)
    return d[n]


def ned(s1, s2):
    return ed(s1, s2) / max(1, len(s1), len(s2))


def edsim(s1, s2):
    return 1.0 - ned(s1, s2)
