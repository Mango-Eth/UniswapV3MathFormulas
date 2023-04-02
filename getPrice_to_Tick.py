import math

# Turns regular price into tick. 5000 => 85176
def price_to_tick(price):
    return math.floor(math.log(price, 1.0001))

print(price_to_tick(5300))

# Turns tick into price. 85176 => 5000 ( rounded, resolution loss. )
def tick_to_price(tick):
    return round(1.0001 ** tick)

print(tick_to_price(85176))