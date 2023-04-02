import math

# Adding 2 eth and 10k usdc as liquidity.
# In ranges of (4800 - 5300) => (84767 - 85758)

q96 = 2**96

def price_to_sqrtp(p):
    return int(math.sqrt(p) * q96)
    #Again turns non square-rooted numbers into Q64.96
    #If we are dealing with the v3 variables, you need to remove the math.sqrt() and only multiply p by 2^96.
#print(price_to_sqrtp(5000))    #5602277097478614198912276234240

Pc = price_to_sqrtp(5000)   #5602277097478614198912276234240
Pl = price_to_sqrtp(4800)   #5489088114601192430499841179648
Pu = price_to_sqrtp(5300)   #5767897294296198798682959642624
eth = 10**18
amount_eth = 2 * eth
amount_usdc = 10000**18


def liquidity0(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return (amount * (pa * pb) / q96) / (pb - pa)

def liquidity1(amount, pa, pb):
    if pa > pb:
        pa, pb = pb, pa
    return amount * q96 / (pb - pa)

liq0 = liquidity0(amount_eth, Pc, Pu)   #4.925147256619307e+21
liq1 = liquidity1(amount_usdc, Pc, Pl)  #6.999635521070512e+71
liq = int(min(liq0, liq1))              #4925147256619306844160

print(liq0, liq1, liq)