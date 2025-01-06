from MetaTrader5 import (order_send, TRADE_ACTION_DEAL, ORDER_TIME_GTC, ORDER_FILLING_IOC, TRADE_ACTION_SLTP,
                         TRADE_RETCODE_DONE)
from .config import DEVIATION, MAGIC

__all__ = ["execute_request", "create_trade_request", "adjust_trade_request", "adjust_stops_request",
           "adjust_stop_loss_request", "adjust_take_profit_request"]


def execute_request(request):
    """Execute a trading request and check the result.

    Args:
        request (dict): The trading request to be executed.

    Returns:
        result: The result of the order send operation.

    Raises:
        ValueError: If the request is invalid.
        RuntimeError: If the order send operation fails.
    """

    result = order_send(request)

    if result is None or result.retcode != TRADE_RETCODE_DONE:
        retcode = result.retcode if result is not None else "None"
        raise RuntimeError(f"{__file__}: {execute_request.__name__}"
                           "Failed to open trade / adjust stops. "
                           "Check that you have algotrading enabled, and that the markets are open.\n"
                           f"retcode= : {retcode}")

    return result


def create_trade_request(direction, symbol, volume, price, comment):
    """Create a trade request dictionary with the specified parameters."""
    request = {
        'action': TRADE_ACTION_DEAL,
        'type_time': ORDER_TIME_GTC,
        'type_filling': ORDER_FILLING_IOC,
        'type': direction,
        'symbol': symbol,
        'volume': volume,
        'price': price,
        'comment': comment,
        'deviation': DEVIATION,
        'magic': MAGIC
    }

    return request


def adjust_trade_request(ticket):
    """Create a request dictionary to adjust the stops of an existing trade."""
    request = {
        'action': TRADE_ACTION_SLTP,
        'position': ticket,
    }

    return request


def adjust_take_profit_request(ticket, take_profit):
    """Adjust the take profit for a given trade ticket."""
    request = adjust_trade_request(ticket)
    request['tp'] = take_profit

    return request


def adjust_stop_loss_request(ticket, stop_loss):
    """Adjust the stop loss for a given trade ticket."""
    request = adjust_trade_request(ticket)
    request['sl'] = stop_loss

    return request


def adjust_stops_request(ticket, take_profit, stop_loss):
    """Adjust the take profit and stop loss for a given trade ticket."""
    request = adjust_trade_request(ticket)
    request['tp'] = take_profit
    request['sl'] = stop_loss

    return request
