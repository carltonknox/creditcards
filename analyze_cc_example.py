from credit_card import CreditCard
from cards import *
from analysis import analyze_credit_cards
    
#Analysis
monthly_spending = {
    "etc": 100,
    "dining": 100,
    "groceries": 100,
    "drugstore": 100,
    "gas": 100,
    "streaming": 100,
    "travel": 100,
    "travelportal": 100,
    "car rental": 100,
    "entertainment": 100,
    "online retail": 100,
    "public transit": 100,
    "ride share": 100
}
all_cards = [
    citi_custom_cash,
    cap_one_savor,
    chase_freedom_flex,
    discover_it,
    amex_bce,
    amex_bcp,
    chase_sapphire_reserve
]
analyze_credit_cards(all_cards,monthly_spending)
