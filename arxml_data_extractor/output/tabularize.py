def tabularize(data: list) -> list:
    rows = __flatten(data)
    return rows


def __flatten(data):
    if isinstance(data, dict):
        rows = []
        for value in data.values():
            res = __flatten(value)
            if isinstance(res, list):
                if isinstance(res[0], list):
                    rows = __concatenate(rows, res)
                else:
                    rows.extend(res)
            else:
                rows.append(res)
        return rows
    elif isinstance(data, list):
        rows = []
        for value in data:
            res = __flatten(value)
            if isinstance(res, list) and type(res[0]) is list:
                rows.extend(res)
            else:
                rows.append(res)
        return rows
    else:
        return data


# len(left) == len(right)
# left  = [[a, b], [c, d]]
# right = [[w, x], [y, z]]
# res   = [[a, b, w, x],
#          [c, d, y, z]]
#
# len(left) > len(right)
# left  = [[a, b], [c, d], [e, f]]
# right = [[w, x], [y, z]]
# res   = [[a, b, w, x],
#          [a, b, y, z],
#          [c, d, w, x],
#          [c, d, y, z],
#          [e, f, w, x],
#          [e, f, y, z]]
#
# len(left) < len(right)
# left  = [[a, b], [c, d]]
# right = [[u, v], [w, x], [y, z]]
# res   = [[a, b, u, v],
#          [a, b, w, x],
#          [a, b, y, z],
#          [c, d, u, v],
#          [c, d, w, x],
#          [c, d, y, z]]
def __concatenate(left: list, right: list) -> list:
    if not left:
        return right

    if type(left[0]) is not list:
        return [left + r for r in right]

    if len(left) == len(right):
        return [l + right[i] for i, l in enumerate(left)]

    return [l + r for l in left for r in right]
