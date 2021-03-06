import heuristika from heuristika

def can_take(a, b):
    """
        Return True if a player can take a when b was played before
        Note that can_take(a, b) == can_take(b, a)
    """
    if a == 0: return False
    else: return a % b == 0 if a >= b else b % a == 0

use_cache = True
cache = {}
stones_length = 0
primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]

def player(stones, last):
    """
        Return one move of the current player
        stones: A list of remaining numbers which have not been taken.
        last: A number taken in the last move.
        The function is expected to return one number which can be taken to win 
        if the position is winning, and False if the position is loosing.

        TODO: Implement this function.
    """
    global stones_length, cache, use_cache, primes

    if use_cache:
        if len(stones) > stones_length:
            stones_length = len(stones)
            cache = {}
        
        params_hash = (hash(str(stones))*100) + (hash(last))
        ret = cache.get(params_hash)
        if ret is not None:
            return ret

    ret = False

    #for i in range(len(stones)): # ... z nejakeho duvodu je to naopak rychlejsi
    #for i in range(len(stones) - 1, -1, -1): 
    for i in heuristika(stones): 
        stone = stones[i]
        if not can_take(stone, last): continue
        
        stones[i] = 0
        player2Winning = player(stones, stone) 
        stones[i] = stone

        if not player2Winning:
            ret = stone
            #stones[i] = stone
            break

    if use_cache:
        cache[params_hash] = ret

    #print(stones, last, ret)

    return ret