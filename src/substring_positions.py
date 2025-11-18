def substring_positions(st, subst, mode='list'):

    for s in subst:
        positions = (''.join(i for i in range(len(st)) if st[i] == s) for s in subst)

    if mode == 'tuple':
        return positions
    elif mode == 'list':
        return list(positions)
    elif mode == 'string':
        return '/'.join(positions)