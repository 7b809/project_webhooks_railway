def parse_option_symbol(symbol: str):
    """
    Extract strike and option type (CE/PE)
    Example:
        NIFTY26FEB25350CE
    Returns:
        strike (str), option_type (str)
    """

    if not symbol:
        return None, None

    if symbol.endswith("CE"):
        option_type = "CE"
    elif symbol.endswith("PE"):
        option_type = "PE"
    else:
        return None, None

    # Extract strike (numbers before CE/PE)
    # Works for 5-digit strikes like 25350
    strike = symbol[-7:-2]

    return strike, option_type
