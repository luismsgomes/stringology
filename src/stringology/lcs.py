

def llcs(s1, s2):
    '''length of the longest common sequence

    This implementation takes O(len(s1) * len(s2)) time and
    O(min(len(s1), len(s2))) space.

    Use only with short strings.

    >>> llcs('a.b.cd','!a!b!c!!!d!')
    4
    '''
    m, n = len(s1), len(s2)
    if m < n:  # ensure n <= m, to use O(min(n,m)) space
        m, n = n, m
        s1, s2 = s2, s1
    l = [0] * (n+1)
    for i in range(m):
        p = 0
        for j in range(n):
            t = 1 if s1[i] == s2[j] else 0
            p, l[j+1] = l[j+1], max(p+t, l[j], l[j+1])
    return l[n]


def lcsr(s1, s2):
    '''longest common sequence ratio

    >>> lcsr('ab', 'abcd')
    0.5
    '''
    if s1 == s2:
        return 1.0
    return llcs(s1, s2) / max(1, len(s1), len(s2))


def lcp(s1, s2):
    '''longest common prefix

    >>> lcp('abcdx', 'abcdy'), lcp('', 'a'), lcp('x', 'yz')
    (4, 0, 0)
    '''
    i = 0
    for i, (c1, c2) in enumerate(zip(s1, s2)):
        if c1 != c2:
            return i
    return min(len(s1), len(s2))
