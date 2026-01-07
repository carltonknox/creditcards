from credit_card import CreditCard

citi_custom_cash = CreditCard(
    name="Citi Custom Cash",
    custom_categories={"groceries", "dining", "gas", "drugstore", "home improv", "live entertainment", "streaming", "transit"},
    custom_rates=[0.05],
    monthly_caps={"custom": 500},
    base_rate=0.01
)
citi_double_cash = CreditCard(
    name="Citi Double Cash",
    base_rate=0.02
)
chase_freedom_flex = CreditCard(
    name="Chase Freedom Flex",
    flat_rates={
        "dining": 0.03,
        "drugstore": 0.03,
        "travelportal": 0.05
        },
    rotating_categories={"dining": (0.05,0.25),
                         "groceries": (0.05,0.25)},
    monthly_caps={"rotating": 500},
    base_rate=0.01
)
discover_it = CreditCard(
    name="Discover IT",
    rotating_categories={"dining": (0.05,0.25),
                         "groceries": (0.05,0.25)},
    monthly_caps={"rotating": 500},
    base_rate=0.01
)
amex_bce = CreditCard(
    name="AMEX Blue Cash Everyday",
    flat_rates={
        "groceries": 0.03,
        "gas": 0.03,
        "online retail": 0.03,
        "amextravel": 0.02
    },
    monthly_caps={
        "groceries": 500,
        "gas": 500,
        "online retail": 500
    },
    base_rate=0.01
)
amex_bcp = CreditCard(
    name="AMEX Blue Cash Preferred",
    flat_rates={
        "groceries": 0.06,
        "gas": 0.03,
        "streaming": 0.06,
        "amextravel": 0.02
    },
    monthly_caps={
        "groceries": 500,
        "gas": 500,
        "streaming": 500
    },
    fee=95/12,
    base_rate=0.01
)
cap_one_savor = CreditCard(
    name="Capital One Savor",
    flat_rates={
        "dining": 0.03,
        "groceries": 0.03,
        "entertainment": 0.03,
        "streaming": 0.03,
        "caponetravel": 0.05,
        "caponeentertainment": 0.08},
    base_rate=0.01
)

citi_custom_cash2 = CreditCard(
    name="Citi Custom Cash2",
    custom_categories={"groceries", "dining", "gas", "drugstore", "home improv", "live entertainment", "streaming", "transit"},
    custom_rates=[0.05],
    monthly_caps={"custom": 500},
    base_rate=0.01
)
citi_custom_cash3 = CreditCard(
    name="Citi Custom Cash3",
    custom_categories={"groceries", "dining", "gas", "drugstore", "home improv", "live entertainment", "streaming", "transit"},
    custom_rates=[0.05],
    monthly_caps={"custom": 500},
    base_rate=0.01
)
chase_sapphire_reserve = CreditCard(
    name="Chase Sapphire Reserve",
    flat_rates={
        "travelportal": 0.08,         # 8× points → 8% travel portal spend 
        "travel": 0.04,              # 4× points → 4% on direct airline/hotel
        "hotel": 0.04,              # 4× points → 4% on direct airline/hotel
        "dining": 0.03,              # 3× points on dining 
    },
    cpp=1.50,
    base_rate=0.01,                 # 1% on everything else 
    fee=(795 - (300+120/4+120+5*12+120 )) / 12  # $795 fee offset by travel, dining, StubHub, Apple, Peloton, Lyft credits
)
chase_sapphire_preferred = CreditCard(
    name="Chase Sapphire Preferred",
    flat_rates={
        "travelportal": 0.05,         # 5× points → 5% equivalent when redeemed for travel
        "travel": 0.02,              # 2× points → 2% on general travel
        "dining": 0.03,              # 3× points → 3% on dining
        "online grocery": 0.03,      # 3× points on grocery online
        "ride share": 0.05,
        "streaming": 0.03            # 3× points on select streaming services
    },
    cpp=1.25,
    base_rate=0.01,                 # 1% on everything else
    fee=(95- (50))/12                       # $95 annual fee
)
amex_gold = CreditCard(
    name="Amex Gold",
    flat_rates={
        "dining": 0.04,            # 4% on dining worldwide
        "groceries": 0.04,   # 4% on US supermarkets, capped
        "travel": 0.03,           # 3% on flights booked directly or via Amex Travel
        "travelportal":0.03
    },
    monthly_caps={
        "groceries": 25000/12  # $25k/year cap for supermarkets
    },
    # cpp=0.6,                     # 0.6 cpp ~ worst case statement credit
    cpp=1.0,                     # 1.0 cpp ~ normal amex travel portal
    # cpp=1.5,                     # 1.5 cpp ~ OPTIMIZED travel transfer points
    base_rate=0.01,               # 1% elsewhere
    fee=(325 - (120+120))/12            
)
fidelity_visa = CreditCard(
    name="Fidelity Rewards Visa",
    base_rate=0.02
)
discover_current = CreditCard(
    name="Discover IT",
    flat_rates={
        "groceries": 0.05
    },
    monthly_caps={
        "groceries": 500
    },
    base_rate=0.01
)
chase_current = CreditCard(
    name="Chase Freedom Flex",
    flat_rates={
        "dining": 0.05,
        "drugstore": 0.03,
        "travelportal": 0.05
        },
    monthly_caps={
        "dining": 500
    },
    base_rate=0.01
)