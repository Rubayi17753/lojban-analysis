def substring_positions(st, subst, mode=0, out='list', delim=' '):

    positions = list()

    if isinstance(st, str):
        if mode == 0:
                for x in subst:
                    current_pos = -1
                    for i, y in enumerate(st):
                        if i not in positions:
                            if x == y:
                                current_pos = i
                                break
                    positions.append(current_pos)
                
                del x
                del y
                del current_pos
                
                positions = (str(pos + 1) if pos != -1 else '_' for pos in positions)

        elif mode == 1:
                positions = ('/'.join(str(i + 1) for i in range(len(st)) if st[i] == s) for s in subst)

    if out == 'tuple':
        return positions
    elif out == 'list':
        return list(positions)
    elif out == 'string':
        return delim.join(positions)    