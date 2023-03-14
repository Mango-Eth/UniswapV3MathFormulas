#Aver serrano, yo explico segun la cara.
import math

#In v2 if you wanted to calculate the amountOut of a reserve, you had to use the constant product formula: dy = ydx / (x + dx) or dx = xdy /(y + dy)
#In V3, things are a bit different. We use the values sqrtPriceX96 and Liquidity to calculate amountsOut. IMPORTANT: Only sqrtPrice changes its value
# on swap, Liquidity stays the same.
#Formulas:

# deltaX = delta(1/sqrt(P)) * L ==> delta(sqrt(P)) = L/deltaX    => values flip: x/l = 1/p => x = L/P => L/x = P

# deltaY = delta(sqrt(P)) * L ==>   delta(sqrt(P)) = deltaY/L

# In V3 we choose THE PRICE WE WANT OUR TRADE TO LEAD TO (i.e. it moves the current price along the curve, as we are buying eth right
# now, we are boosting the current price towards B. )
# B - PC - A. (Where B is the point where there would be only USDC tokens, A where there are only ETH tokens, and PC is the current price) *curve*
# Knowing the TARGET PRICE(Pt) the protocol will know how many tokens to take from us and return us.

# So:
# Pc = 5602277097478614198912276234240
# Liquidity = 1517882343751509868544            // from current foundry test project.
# delta(sqrt(P)) = 42/1517882343751509868544 = 2192253463713690532467206957

# The formula for the Target Price (Pt) is :

# sqrt(Pt) = sqrt(Pc) + delta(sqrt(P))      (5602277097478614198912276234240 + 2192253463713690532467206957)

#sqrt(Pt) = 5604469350942327889444743441197

def price_to_tick(p):
    return math.floor(math.log(p, 1.0001))

price_to_tick(5000)
eth = 1e18
q96 = 2**96
            
Liquidity = 1517882343751509868544
Pc = 5602277097478614198912276234240    
amountIn = 42 * eth

#We turn our amountIn into fixedPoint, then divide by liquidity as stated in the formula above:
delta_Price = (amountIn * q96) / Liquidity          #   2.1922534637136906e+27
Pt = Pc + delta_Price                               #   5.604469350942327e+30       sqrtPrice values are supposed to be this bgi.

# To transform this huge fixedPoint number into a human readable number we can:
regular_target_Price = ((Pt / q96) ** 2)    # regular_target_Price = 5003.913912782393

# Calculate the new tick:
new_tick = price_to_tick((Pt / q96) ** 2)   # 85184

#print(new_tick)

# After having found the Pt, target price, we can calculate the token amounts using these formulas:

# x = (L * (sqrt(Pb) - sqrt(Pa))) / (sqrt(Pb) * sqrt(Pa))

# y = L * (sqrt(Pb) - sqrt(Pa))

def calc_amount0(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * q96 * (pb - pa) / pa / pb)


def calc_amount1(liq, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return int(liq * (pb - pa) / q96)

amount_In = calc_amount1(Liquidity, Pt, Pc)     #41.99999999999241      dy
amount_Out = calc_amount0(Liquidity, Pt, Pc)    #0.00839671424216093    dx  claro pe care llama

#print(amount_In / eth, amount_Out / eth)

# Next some mathematical magic. To prove that our amountOut is correct, we can apply the following formula:

# deltaX = delta(1/sqrt(P)) * Liquidity

# So far we know: Liquidity, delta(sqrt(P)), deltaX. Remember that delta(sqrt(P)) != delta(1/sqrt(P)) duh -.-
# To find the value of delta(1/sqrt(P)) we can:

# delta(1/sqrt(P)) = (1/sqrt(Pt)) - (1/sqrt(Pc))

def calc_delta_1over_sqrtP(Pt, Pc):
    return ((1/Pt) - (1/Pc))            #-6.982190286589445e-35    regular number

# We now turn this regular value into fixedPoint binary.

fixedPoint_1over_sqrtP = calc_delta_1over_sqrtP(Pt, Pc) * q96

delta_X = fixedPoint_1over_sqrtP * Liquidity

print(delta_X)      # -8396714242162704.0       It has 16 digits, so in terms of ETH its 0.00839671. Also its negative because its the amount that is being removed from the pool.

