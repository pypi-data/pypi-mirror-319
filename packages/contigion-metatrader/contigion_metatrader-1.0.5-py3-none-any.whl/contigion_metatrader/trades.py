from MetaTrader5 import positions_get, order_calc_profit
from .actions import close_trade


def close_profits():
    """Close all profitable positions."""
    for position in positions_get():
        ticket = position.ticket
        trade = positions_get(ticket=ticket)[-1]

        if trade.profit > 0:
            close_trade(ticket)


def close_losses():
    """Close all losing positions."""
    for position in positions_get():
        ticket = position.ticket
        trade = positions_get(ticket=ticket)[-1]

        if trade.profit < 0:
            close_trade(ticket)


def close_all_trades():
    """Close all open trades."""
    for position in positions_get():
        close_trade(position.ticket)


def close_last_trade():
    """Close the most recent trade."""
    positions = positions_get()

    if positions:
        close_trade(positions[-1].ticket)


def get_open_trades():
    """Retrieve all open trades.

    Returns:
        list: A list of open positions.
    """
    return positions_get()


def get_open_trade(ticket):
    """Retrieve a specific open trade by ticket.

    Args:
        ticket (int): The trade ticket number.

    Returns:
        object: The position object if found; otherwise, None.
    """
    positions = positions_get(ticket=ticket)
    return positions[-1] if positions else None


def trades_in_profit():
    """Count the number of profitable trades."""
    positions = positions_get()
    profitable_trades = sum(position.profit > 0 for position in positions if position.profit is not None)

    return f"{profitable_trades} / {len(positions) if positions else 0}"


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
