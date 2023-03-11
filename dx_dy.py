
# The bellow formula should get you the amounts needed for the remainind dx or dy needed for a specific range.
# Requirements:
# Delta X               (Exmpl. 1 ETH)      (dx)
# Price_current         (Exmpl. 1500)       (y/x Ratio of y for 1 x)
# Price_a               (Exmpl. 1300)       (lower price range -> liquidity from Pc - Pa is in USDC(y), because ETH isnt needed.)
# Price_b               (Exmpl. 1700)       (upper price range -> liquidty is made out of pure ETH(x))
# Pb - Pc - Pa makes a graph around the current price. So the formulas are derived from both sides of the graph, separated by the current price.

import math

def return_dy(
        deltaX,
        Pc,
        Pa,
        Pb
): 
    return (deltaX/((1/math.sqrt(Pc)) - (1/math.sqrt(Pb)))) * (math.sqrt(Pc) - math.sqrt(Pa))

result = return_dy(1, 1563.07, 1000.3, 1800.9)
print(result)


def return_dx(
        deltaY,
        Pc,
        Pa,
        Pb
):
    return (deltaY/(math.sqrt(Pc) - math.sqrt(Pa))) * ((1/math.sqrt(Pc)) - (1/math.sqrt(Pb)))

resultX = return_dx(4000, 1570.56, 1000.3, 1800.9)
print(resultX)

#works
# to verify use: https://app.uniswap.org/#/add/ETH/0xA0b86991c6218b36c1d19D4a2e9Eb0cE3606eB48/3000?maxPrice=1800.870000&minPrice=1000.3