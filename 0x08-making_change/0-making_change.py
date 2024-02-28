#!/usr/bin/python3
'''Change comes from within
'''


def makeChange(coins, total):
    '''Change comes from within
    '''
    if total <= 0:
        return 0
    coins = sorted(coins, reverse=True)
    count = 0
    for coin in coins:
        if coin <= total:
            while coin <= total:
                count += 1
                total -= coin
    if total == 0:
        return count
    return -1
