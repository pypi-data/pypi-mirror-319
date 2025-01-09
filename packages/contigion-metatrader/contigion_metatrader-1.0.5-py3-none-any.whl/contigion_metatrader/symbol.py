from MetaTrader5 import symbol_info


def get_point(symbol):
    """
    Retrieves the point value for a given symbol.

    This function attempts to fetch information about the specified symbol
    and extracts its point value. If the symbol information cannot be
    retrieved or an error occurs, an exception is raised.

    Args:
        symbol (str): The trading symbol.

    Returns:
        float: The point value for the symbol.

    Raises:
        RuntimeError: If the symbol information is None.
        Exception: If an error occurs during the retrieval process.
    """

    try:
        info = symbol_info(symbol)

        if info is None:
            raise RuntimeError(f"{__file__}: {get_point.__name__}"
                               f"Failed to retrieve information for symbol: {symbol}")

        return info.point

    except Exception:
        raise Exception(f"{__file__}: {get_point.__name__}"
                        "Error retrieving the point value")


def get_spread(symbol):
    """Get the spread for a given trading symbol using MetaTrader 5.

    Args:
        symbol (str): The trading symbol (e.g., 'USDJPY').

    Returns:
        float: The spread value.
    """

    info = symbol_info(symbol)

    return info.spread
