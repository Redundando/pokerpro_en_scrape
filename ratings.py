import math


def get_proper_rating(operator="") -> str:
    ratings = {
        "888poker": 4.75,
        "betkings": 5,
        "clubgg": 4.5,
        "coral poker": 3,
        "partypoker": 5,
        "ggpoker": 4.75,
        "pokerbros": 5,
        "pokerking": 4.5,
        "pokio pokerpro clubs": 4.75,
        "pppoker": 4.75,
        "wptglobal": 5,
        "guts poker": 4.5,
        "natural8": 4.5,
        "betfair": 3,
        "bwin": 4.25,
        "infinity poker": 4.25,
        "suprema poker app": 4,
        "peoples poker": 4,
        "partypoker spain": 4,
        "highstakes": 3.5,
        "redstar poker": 4,
        "2bet4win": 4,
        "upoker": 4,
        "partypoker france": 3.75,
        "bet365": 3.75,
        "titanpoker": 3.75,
        "betsafe": 4,
        "betsson poker": 4,
    }
    op = operator.lower().strip()
    if op in ratings.keys():
        return ratings[op]
    return "4"


def get_four_ratings(rating) -> []:
    floor = math.floor(rating)
    decimal = rating - floor
    result = [floor] * 4
    if abs(decimal - 0.75) < 0.01:
        result = [floor + 1, floor + 1, floor + 1, floor]
    if abs(decimal - 0.5) < 0.01:
        result = [floor + 1, floor + 1, floor, floor]
    if abs(decimal - 0.25) < 0.01:
        result = [floor + 1, floor, floor, floor]
    if abs(decimal - 0.00) < 0.01:
        result = [floor, floor, floor, floor]
    return result
