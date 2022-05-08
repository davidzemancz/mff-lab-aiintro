def can_take(a, b):
    """
        Return True if a player can take a when b was played before
        Note that can_take(a, b) == can_take(b, a)
    """
    return a % b == 0 if a >= b else b % a == 0

cache = {}
stones_length = 0

def player(stones, last):
    """
        Return one move of the current player
        stones: A list of remaining numbers which have not been taken.
        last: A number taken in the last move.
        The function is expected to return one number which can be taken to win if the position is winning, and False if the position is loosing.

        TODO: Implement this function.
    """
    global stones_length, cache

    if len(stones) >= stones_length:
        stones_length = len(stones)
        cache = {}
    
    #if len(cache) % 10000 == 0:
    #    print(len(cache))

    params_hash = hash(tuple(stones)) + (hash(last) * 100)

    c = cache.get(params_hash)
    if c is not None:
        return c

    ret = False

    if len(stones) > 0:
        possible_stones = [s for s in stones if can_take(s, last)]
        winning = []
        for stone in possible_stones:
            
            player2Winning = None

            new_stones = stones.copy()
            new_stones.remove(stone)
            player2Winning = player(new_stones, stone) 
            
            if not player2Winning:
                ret = stone
                break

    cache[params_hash] = ret
    return ret