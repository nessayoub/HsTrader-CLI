from hstrader import HsTrader
from hstrader.models import Event, Tick, Order, CrtOrder, OrderType, SideType, Status, Position
import click

CLIENT_ID = "24100180_8073259861"
SECRET = "dd2c318e96ed8cbdf66479bac04529d9e29b4a3da9d8deb634ec686358009100"

client = HsTrader(CLIENT_ID, SECRET)

def validate_symbol(ctx, param, value):
    try: 
        client.get_symbol(value)
    except:
        raise click.BadParameter("Invalid Symbol")
    return value.upper()

def validate_operation(ctx, param, value):
    if value not in ["buy_limit", "sell_limit", "buy_market"]:
        raise click.BadParameter("Invalid operation type")
    return value

def validate_volume(ctx, param, value):
    if value <= 0:
        raise click.BadParameter("Volume must be a positive integer")
    return value

def validate_price(ctx, param, value):
    if value <= 0:
        raise click.BadParameter("Price must be a positive number")
    return value

@click.command()
@click.option(
    "--symbol", type=str, callback=validate_symbol,
    prompt="Enter symbol", default="", show_default=False
)
@click.option(
    "--operation", type=click.Choice(["buy_limit", "sell_limit", "buy_market"]), callback=validate_operation,
    prompt="Enter operation ", default="", show_default=False
)
@click.option(
    "--volume", type=float, callback=validate_volume,
    prompt="Enter volume", default="", show_default=False
)
def trade(symbol, operation, volume):
    """Place a trade"""
    symbol = client.get_symbol(symbol)
    if operation != 'buy_market':
        price = click.prompt("Enter price", type=float)
    else:
        price = symbol.last_ask
    if operation == 'buy_market':
        order_type = OrderType.MARKET_ORDER
        side = SideType.BUY
    elif operation == 'buy_limit':
        order_type = OrderType.BUY_LIMIT
        side = SideType.BUY
    else:
        order_type = OrderType.SELL_LIMIT
        side = SideType.SELL
    
    new_order = CrtOrder(symbol, volume, side, order_type, order_price=price)
    client.create_order(new_order)
    print(f"Order Placed: {symbol}, {order_type}, volume = {volume}, price = {price}")

if __name__ == "__main__":
    trade()










