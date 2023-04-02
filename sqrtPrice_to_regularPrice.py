import math

#5602799062589022220467625569229 target price

#print(math.floor(math.sqrt(5000) * 2**96)) #5602277097478614198912276234240

def rounding(p):
    val = (p / 2**96)**2
    return round(val)

#print(rounding(5607496748582694414465769584139))
#print(rounding(5602223755577321903022134995699))

def not_rounding(p):
    val = (p / 2**96)**2
    return val

print(not_rounding(5604464981235387621667342876360))

