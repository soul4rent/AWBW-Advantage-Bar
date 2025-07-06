
# COs are given constants based on how important their D2D and powers are.
# first number is d2d constant, a number between 0 and 1. This represents how much units are better in general than default units.
# second number is power charge constant, a number between 0 and 1, representing how strong their power is when it's ready to be used.
# all numbers are currently arbitrary and vibes based.
CO_S4R_Formula_Constants = {
    "andy": [0, .5],
    "hachi": [0, .8],
    "jake": [.05, .3],
    "max": [.2, .3],
    "nell": [.1, .5],
    "rachel": [.05, .4],
    "sami": [.1, .6],
    "colin": [0, .7],
    "grit": [.3, .1],
    "olaf": [0, .6],
    "sasha": [0, .1], # Sasha's D2D is basically more money. She doesn't need more unit value.
    "drake": [-.1, .6], # Drake's d2d is arguably a negative with terrible copters
    "eagle": [0, .8],
    "javier": [.2, .4],
    "jess": [0, .2],
    "grimm": [-.1, .2],
    "kanbei": [.5, .2],
    "sensei": [0, .8],
    "sonja": [-.1, .2],
    "adder": [0, .2],
    "flak": [-.1, .1],
    "hawke": [.1, .7],
    "jugger": [-.1, .1],
    "kindle": [.05, .5],
    "koal": [.05, .2],
    "lash": [.2, .2],
    "sturm": [.2, .4],
    "vonbolt": [.3, .4]
}

def get_s4r_formula_result(co_name, unit_value, power_charge_current, power_charge_total, tower_count):
    percent_charge = power_charge_current / power_charge_total
    co_d2d_portion_of_score = unit_value * (1 + CO_S4R_Formula_Constants[co_name][0]) - unit_value
    charge_portion_of_score = unit_value * (1 + percent_charge * CO_S4R_Formula_Constants[co_name][1]) - unit_value
    tower_portion_of_score = unit_value * (0.1 * tower_count) # assume towers are worth ~10% of unit value
    return unit_value + co_d2d_portion_of_score + charge_portion_of_score + tower_portion_of_score