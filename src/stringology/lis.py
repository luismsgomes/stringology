from bisect import bisect


def lis(seq, indices=False):
    '''longest increasing subsequence

    >>> lis([1, 2, 5, 3, 4])
    [1, 2, 3, 4]
    '''
    if not seq:
        return []
    # prevs[i] is the index of the previous element in the longest subsequence
    # containing element i
    prevs = [None] * len(seq)
    # tails[i] is the pair (elem, index) of the lowest element of any
    # subsequence with length i + 1
    tails = [(seq[0], 0)]
    for i, elem in enumerate(seq[1:], start=1):
        if elem > tails[-1][0]:
            prevs[i] = tails[-1][1]
            tails.append((elem, i))
            continue
        # let's find a tail that we can extend
        k = bisect(tails, (elem, -1))
        if tails[k][0] > elem:
            tails[k] = (elem, i)
            if k > 0:
                prevs[i] = tails[k - 1][1]
    _, i = tails[-1]
    subseq = []
    while i is not None:
        subseq.append(i if indices else seq[i])
        i = prevs[i]
    return subseq[::-1]
