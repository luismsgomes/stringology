
def all_ngrams(seq, minn=1, maxn=None):
    ngrams = []
    if maxn is None:
        maxn = len(seq)
    for n in range(minn, maxn + 1):
        for start in range(0, len(seq) - n + 1):
            ngrams.append(seq[start:start + n])
    return ngrams
