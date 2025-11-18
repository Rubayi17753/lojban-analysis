def substring_positions(st, subst, mode='list', delimiter=' '):
    
    positions = ('/'.join(str(i + 1) for i in range(len(st)) if st[i] == s) for s in subst)

    if mode == 'tuple':
        return positions
    elif mode == 'list':
        return list(positions)
    elif mode == 'string':
        return delimiter.join(positions)