# From the formula: sqrt(P(i)) = 1.0001^i/2 we can find the tick (i) via:
# i = log(sqrt(1.0001), sqrt(P(i))).   Remember that: Log(base, value).
# Also remember that here P is the "price" which in v3 is calculated as:
# sqrt(P) = sqrt(y/x) Therefore: Its the ratio of x in terms of y.
# Later on, for liquidity calculations we need 3 ticks, which we get from 3 different Prices(points).
# Pc = Price current Pl = Price lower Pu = Price upper. From the Pu - Pc - Pl curve that is created.
# We later address Pl and Pu as B and A.
# Where trades going towards A represent a diminishing price. (More Eth, less Usdc).
# While trades going towards B represent a growing price. (Less Eth, more Usdc), which makes Eth more valuable also Price, cuz Price is in terms of Eth(x).
#

import math

def price_to_tick(p):
    return math.floor(math.log(p, 1.0001))

price_to_tick(5000)      #85176
#Calculates the exact tick for the price(5000).
# This formula might differ, depending on the state of Price.
# In v3 Price is sqrtPriceX96, therefore it will be sqrt(5000) = 70.71 and not 50000.
# In that case, we need to: use this formula:

def price_to_tick_sqrtPrice(p):
    return math.floor(math.log(p, math.sqrt(1.0001)))
    # Makes sense, in the other you calculate X in base Z. 
    # If you only have the root of X all of a sudden you need to apply sqrt(Z). Duh..

print(price_to_tick_sqrtPrice(70.71))   #85175


q96 = 2**96

#Q64.96 is a fixed point number, has 64 bits for the left side of the decimal point and 96 bits for the right side.
#Its base is 2^96. Therefore, converting a number into Q64.96 is as simple as multiplying it by its base.

def price_to_sqrtp(p):
    return int(math.sqrt(p) * q96)
    #Again turns non square-rooted numbers into Q64.96
    #If we are dealing with the v3 variables, you need to remove the math.sqrt() and only multiply p by 2^96.
print(price_to_sqrtp(5000))    #5602277097478614198912276234240

#Finally to calculate the liquidity of our ranges, we need to calculate 2 liquidities.
#If we remember our curve B - Pc - A. Where B represents the point where we have (Eth = 0 : Usdc = Infinity) and A represents (Eth = Inifinty : Usdc = 0).
# We can derive that each side of these curves only need 1 type of reserves. What i mean is that:
# From Pc - B, only price incremeanting trades occur, therefore it only needs ETH as liquidity and no USDC. (The more eth is bought, the higher the price, also less eth = high price.).
# From Pc - B, only price lowering trades occur, therefore we only need USDC, on that curve.
# For uniform liquidity repartition, we need to calculate both sides and then use the smallest one for simplicity.
# Using the bigger one would make the contract a bit more complex, mainly because the bigger one includes the small one.

# IMPORTANT: The formulas for both curves:

# B - Pc curve: (We use Pb as B, and Pa as A, Pc stays as price current)
# L = delta(x)( (sqrt(Pb)sqrt(Pc)) / sqrt(Pb) - sqrt(Pc))

# Pc - A curve: (L stands for liquidity)
# L = delta(y) / (sqrt(Pc) - sqrt(Pa))


sqrtp_low = price_to_sqrtp(4545)    #5341294542274603406682713227264
sqrtp_cur = price_to_sqrtp(5000)    #5602277097478614198912276234240
sqrtp_upp = price_to_sqrtp(5500)    #5875717789736564987741329162240




def liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return (amount * (pa * pb) / q96) / (pb - pa)

def liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount * q96 / (pb - pa)

eth = 10**18
amount_eth = 1 * eth
amount_usdc = 5000 * eth
# we use these valeus as our deltas

liq0 = liquidity0(amount_eth, sqrtp_cur, sqrtp_upp)     #1.5194373080147697e+21
liq1 = liquidity1(amount_usdc, sqrtp_cur, sqrtp_low)    #1.5178823437515099e+21
liq = int(min(liq0, liq1))

# we get the lower number of both values with line 80.
print(liq, "liquidty")  #1517882343751509868544

# Finally some calculations to make sure, correct amounts are deposited.
# These functions just round up, the by the user selected values. A periphery contract does the calculation, this isnt very user friendly if ud ont know math.

def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * q96 * (pb - pa) / pa / pb)


def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * (pb - pa) / q96)

amount0 = calc_amount0(liq, sqrtp_upp, sqrtp_cur)
amount1 = calc_amount1(liq, sqrtp_low, sqrtp_cur)
(amount0, amount1)
 #(998976618347425408, 5000000000000000000000) (eth, usdc)


