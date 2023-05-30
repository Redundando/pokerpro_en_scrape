def get_proper_logo(operator="") -> str:
    logos = {
        "888poker": "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b9/888poker-logo.png/600px-888poker-logo.png",
        "betkings": "https://pbs.twimg.com/profile_images/1612368086367100929/wZ_PvIUq_400x400.jpg",
        "clubgg": "https://www.primedope.com/wp-content/uploads/ClubGG-Logo.webp",
        "coral poker": "https://nodepositbonuscasino.com/wp-content/uploads/2022/11/coral-casino.png",
        "partypoker": "https://www.vgnpoker.com/wp-content/uploads/sites/8/2018/09/partypoker-icon.png",
        "ggpoker": "https://cdn.asp.events/CLIENT_CL_Gamin_A45C4908_5056_B725_6B2249A7AD85625A/sites/iGB-Live-2022/media/libraries/exhibitors/06570262-dc44-11ec-910306e21988b83f-logo.png",
        "pokerbros": "https://www.primedope.com/wp-content/uploads/PokerBros-Logo.webp",
        "pokerking": "https://www.primedope.com/wp-content/uploads/PokerKing-Logo.webp",
        "pokio pokerpro clubs": "https://www.primedope.com/wp-content/uploads/pokio-logo.webp",
        "pppoker": "https://www.primedope.com/wp-content/uploads/pppoker-logo.webp",
        "wptglobal": "https://www.primedope.com/wp-content/uploads/WPT-Global-Logo.webp",
        "guts poker": "https://www.primedope.com/wp-content/uploads/Logo-Guts-Poker.webp",
        "natural8": "https://www.primedope.com/wp-content/uploads/Natural8-Logo-1.webp",
        "betfair": "https://www.primedope.com/wp-content/uploads/Betfair-Poker-Logo.webp",
        "bwin": "https://www.primedope.com/wp-content/uploads/Bwin-Logo.webp",
        "infinity poker": "https://www.primedope.com/wp-content/uploads/Infinity-Poker-Logo.webp",
        "suprema poker app": "https://www.primedope.com/wp-content/uploads/Suprema-Poker-Logo.webp",
        "peoples poker": "https://www.primedope.com/wp-content/uploads/peoples-poker-logo.webp",
        "partypoker spain": "https://www.primedope.com/wp-content/uploads/PartyPoker-Spain-Logo.webp",
        "highstakes": "https://www.primedope.com/wp-content/uploads/Highstakes-Logo-1.webp",
        "redstar poker": "https://www.primedope.com/wp-content/uploads/Redstar-Poker-Logo.webp",
        "2bet4win": "https://www.primedope.com/wp-content/uploads/2bet4win-Logo.webp",
        "upoker": "https://www.primedope.com/wp-content/uploads/uPoker-Logo.webp",
        "partypoker france": "https://www.primedope.com/wp-content/uploads/PartyPoker-France-Logo.webp",
        "bet365": "https://www.primedope.com/wp-content/uploads/Bet365-Logo.webp",
        "titanpoker": "https://www.primedope.com/wp-content/uploads/TitanPoker-Logo.webp",
        "betsafe": "https://www.primedope.com/wp-content/uploads/Betsafe-Logo.webp",
        "betsson poker": "https://www.primedope.com/wp-content/uploads/betsson-logo-2.webp",
    }
    op = operator.lower().strip()
    #print(f"###\n {operator} - {op} \n ###")
    if op in logos.keys():
        #print(f"###\n {logos[op]} - {op} \n ###")
        return logos[op]
    return ""
