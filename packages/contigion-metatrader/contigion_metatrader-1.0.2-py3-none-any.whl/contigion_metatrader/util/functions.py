from MetaTrader5 import order_calc_profit, symbol_info

__all__ = ["calculate_profit", "get_point", "get_spread"]


def calculate_profit(trade_type, symbol, volume, open_price, close_price):
    """Calculate the profit for a trade.

    Args:
        trade_type (int): The type of trade (buy/sell).
        symbol (str): The trading symbol.
        volume (float): The volume of the trade.
        open_price (float): The opening price of the trade.
        close_price (float): The closing price of the trade.

    Returns:
        float: The calculated profit.
    """
    return order_calc_profit(trade_type, symbol, volume, open_price, close_price)


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
            raise RuntimeError(f"Failed to retrieve information for symbol: {symbol}")

        return info.point

    except Exception:
        raise Exception("Error retrieving the point value")


def get_spread(symbol):
    """Get the spread for a given trading symbol using MetaTrader 5.

    Args:
        symbol (str): The trading symbol (e.g., 'USDJPY').

    Returns:
        float: The spread value.
    """

    info = symbol_info(symbol)

    return info.spread
