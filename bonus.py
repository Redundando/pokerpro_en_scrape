
def get_proper_bonus(operator="") -> str:
    bonuses = {
        "888poker": "$88 No Deposit Bonus",
        "betkings": "$100 Free Tickets & Cash",
        "clubgg": "Access to Private Clubs",
        "coral poker": "Free $30 Tickets",
        "partypoker": "$30 Free Tickets",
        "ggpoker": "$100 Free Tickets",
        "pokerbros": "Biggest Selection of Clubs",
        "pokerking": "100% up to $2,000",
        "pokio pokerpro clubs": "Exclusive VIP Deals",
        "pppoker": "VIP Rakeback",
        "wptglobal": "100% up to $1,200",
        "guts poker": "€1,000 Welcome Bonus",
        "natural8": "200% up to $1,000",
        "betfair": "€200 Welcome Bonus",
        "bwin": "Up to 40% Cashback",
        "infinity poker": "Personal VIP Deals",
        "suprema poker app": "Personal VIP Deals",
        "peoples poker": "PokerPro VIP Program",
        "partypoker spain": "€40 Free Play Bonus",
        "highstakes": "100% up to $2,000",
        "redstar poker": "200% up to €2,000",
        "2bet4win": "100% up to $600",
        "upoker": "PokerPro VIP Deal",
        "partypoker france": "€40 Free Play Bonus",
        "bet365": "€365 Welcome Bonus",
        "titanpoker": "70% VIP Cashback",
        "betsafe": "100% up to €2,000",
        "betsson poker": "100% up to €2,000",
    }
    op = operator.lower().strip()
    if op in bonuses.keys():
        return bonuses[op]
    return "Exclusive VIP Deals"
