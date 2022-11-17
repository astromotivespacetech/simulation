def normalize(val, min, max):

    if val - min == 0:
        return 0
    else:
        normalized = (val - min) / (max - min)
        return normalized


def constrain(val, min, max):

    if val > max:
        val = max
    elif val < min:
        val = min

    return val
