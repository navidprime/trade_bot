trades = {
    # MACD Strategy(50,200),popcatusdt, 15m
    (0.0844,0.1041),
    (0.0783,0.1002),
    (0.0880,0.0819),
    (0.0859,0.0917),
    (0.0834,0.0709),
    (0.0753,0.0850),
    (0.0817,0.1325),
    (0.1518,0.1349),
    (0.1404,0.1354),
    (0.1394,0.1363),
    (0.1432,0.1578),
    (0.1365,0.1407),
    (0.2168,0.2040),
    (0.1906,0.1746),
    (0.1769,0.1854),
    (0.1929,0.2106),
    (0.2148,0.2119),
    (0.2125,0.2047),
    (0.2080,0.1998),
    (0.1929,0.1919),
    (0.2093,0.2286),
    (0.2943,0.3130),
    (0.3123,0.2966),
    (0.2937,0.2897),
    (0.2727,0.2636),
    (0.1707,0.1775),
    (0.1962,0.1968),
    (0.1877,0.1805),
    (0.2498,0.2384),
    (0.2276,0.2184),
    (0.2260,0.2309),
    (0.2341,0.2551),
    (0.2982,0.2855),
    (0.2982,0.3012),
    (0.2963,0.3535),
    (0.3457,0.3385),
    (0.3195,0.3162),
    (0.3722,0.3473),
    
}
initMoney = 1000
money = initMoney

wins = 0

average_win_percent = 0
average_lose_percent = 0
for trade in trades:
    diff = ((trade[1] - trade[0])/trade[0]) * 100
    if diff>0:
        wins +=1
        average_win_percent += diff
    else:
        average_lose_percent += diff
    money += money*diff/100

print("money change $ :",money-initMoney)
print(f"win rate: {wins}/{len(trades)} ({round(wins/len(trades)*100,2)}%)")
print(f"average win percent : {round(average_win_percent/wins,2)}")
print(f"average lose percent : {round(average_lose_percent/(len(trades)-wins),2)}")