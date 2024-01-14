async def numtotext(number):
    number = int(number)
    abbreviations = [
        (1e12, 'T'),
        (1e9, 'B'),
        (1e6, 'M'),
        (1e3, 'K')
    ]
    for factor, suffix in abbreviations:
        if number >= factor:
            abbreviated = number / factor
            return f"{abbreviated:.2f}{suffix}"
    return str(number)
async def txttonum(value):
    multipliers = {'k': 1000, 'm': 1000000, 'b': 1000000000, 't': 1000000000000}
    if 'e' in value.lower():
        number_parts = value.lower().split('e')
        base = float(number_parts[0])
        exponent = int(number_parts[1])

        if exponent < 0:
            return int(base / (10 ** abs(exponent)))
        elif exponent > 0:
            return int(base * (10 ** exponent))
        else:
            return int(base)

    suffix = value[-1].lower()
    if suffix in multipliers:
        number = float(value[:-1]) * multipliers[suffix]
        return int(number)

    return int(value)
