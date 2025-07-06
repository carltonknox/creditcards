from credit_card import CreditCard
#Analysis
def analyze_credit_cards(all_cards,monthly_spending):
    money_spent= {cat:0 for cat in monthly_spending.keys()}
    total_time = {cat:0 for cat in monthly_spending.keys()}
    total_rewards={cat:{"cards":[],"portions":[]} for cat in monthly_spending.keys()}
    #Begin with rotating categories
    rotcats={}
    for category,amount in monthly_spending.items():
        # print(category,amount)
        for card in all_cards:
            reward,used,chance=card.calc_rot(amount,category)
            if(reward):
                if category not in rotcats:
                    rotcats[category]=[]
                rotcats[category].append((card.name,reward,used,chance))
    # print("Rotating Categories:", rotcats)
    rotcats_merged={}
    for cat,cards in rotcats.items():
        card_names=[]
        reward=cards[0][1]
        used=cards[0][2]
        
        inv_prob=1
        ratios=[]
        for card in cards:
            assert(card[1]==reward)
            assert(card[2]==used)
            inv_prob*=(1-card[3])
            card_names.append(card[0])
            ratios.append(card[3])
        merged_prob=1-inv_prob
        rotcats_merged[cat]=((card_names,reward,used,merged_prob,ratios))
        total_time[cat]+=merged_prob
        total_rewards[cat]["cards"]=card_names.copy()
        total_rewards[cat]["portions"].append({"reward":reward, "portion":used, "time":merged_prob,"ratios":ratios,"cards":card_names})
        
        
    # print("Merged Rotating Categories:", rotcats_merged)
    #Then assign custom cards
    for card in all_cards:
        while(card.custom_i < len(card.custom_rates)):
            # print("Found custom card",card.name)
            best_cat="None"
            best_reward=0
            
            custom_list=[]
            
            for category,amount in monthly_spending.items():
                already_used=money_spent.get(category,0)
                reward, used = card.calc_custom(amount-already_used,category)
                # if reward > best_reward:
                #     best_reward=reward
                #     best_cat=category
                if reward>0:
                    custom_list.append((category,reward))
            
            custom_list=sorted(custom_list, key=lambda x: x[1], reverse=True)
            # print(custom_list)
                
            i=0
            while(card.time<1 and i < len(custom_list)):
                best_cat,best_reward= custom_list[i]
                already_used=money_spent.get(best_cat,0)
                
                best_time=1
                if best_cat in rotcats_merged and total_time[best_cat] <1.0:
                    best_time=min(1-total_time[best_cat],1-card.time)
                    
                
                
                reward, used = card.use_custom(monthly_spending[best_cat]-already_used,best_cat)
                money_spent[best_cat]=already_used+used
                card.time+=best_time
                # print(card.name,best_cat,best_reward,used,best_time)
                
                if total_time[best_cat]<1 and len(total_rewards[best_cat]["portions"])>0:
                    #continue portion from rotating category
                    prev_portion=total_rewards[best_cat]["portions"][-1]
                    prev_portion_amount=prev_portion["portion"]
                    assert(used==prev_portion_amount)
                total_rewards[best_cat]["portions"].append({"reward":best_reward, "portion":used, "time":best_time,"ratios":[best_time],"cards":[card.name]})
                total_rewards[best_cat]["cards"].append(card.name)
                total_time[best_cat]+=best_time
                
                
                
                i+=1
            card.custom_i+=1
            
    # print(total_time)
    # print(money_spent)
    # print(monthly_spending)
    # for key,val in total_rewards.items():
    #     print(key,val)
            
    #Then calculate the rest
    while any([(total_time[cat]<1 or money_spent[cat]<monthly_spending[cat]) and monthly_spending[cat]>0 for cat in monthly_spending.keys()]):
        for cat in monthly_spending.keys():
            if total_time[cat]<1 and len(total_rewards[cat]["portions"])>0:
                #Need to fill out previous portion of money
                prev_portion=total_rewards[cat]["portions"][-1]
                prev_portion_amount=prev_portion["portion"]
                prev_portion_remaining_time=1-total_time[cat]
                
                
                best_reward=0
                best_used=0
                best_card=None
                for card in all_cards:
                    reward, used = card.calc_flat(prev_portion_amount,cat)
                    assert(used==prev_portion_amount)
                    if reward>best_reward:
                        best_reward=reward
                        best_used=used
                        best_card=card
                assert(best_card is not None)
                best_card.use_flat(best_used,cat)
                    
                    
                total_rewards[cat]["portions"].append({"reward":best_reward, "portion":best_used, "time":prev_portion_remaining_time,"ratios":[prev_portion_remaining_time],"cards":[best_card.name]})
                total_rewards[cat]["cards"].append(best_card.name)
                total_time[cat]=1.0
                
            #should be filled out now
            if money_spent[cat] < monthly_spending[cat]:
                #Need to fill out rest of money with flat rate
                best_reward=0
                best_used=0
                best_card=None
                for card in all_cards:
                    reward, used = card.calc_flat(monthly_spending[cat]-money_spent[cat],cat)
                    if reward>best_reward:
                        best_reward=reward
                        best_used=used
                        best_card=card
                assert(best_card is not None)
                best_card.use_flat(best_used,cat)
                total_rewards[cat]["portions"].append({"reward":best_reward, "portion":best_used, "time":1.0,"ratios":[1.0],"cards":[best_card.name]})
                total_rewards[cat]["cards"].append(best_card.name)
                
                money_spent[cat]+=best_used
                total_time[cat]=1.0

    print("_________________________")            
    for key,val in total_rewards.items():
        print(key,val)
        

        
    print(f"{'Category':<20}{'Monthly Spend':>20}{'Cash Back $':>15}{'Cash Back %':>15}{' ' * 4}{'cards':<50}")

    total_spending=0
    total_cashback=0
    card_contribution = {card.name:0 for card in all_cards}
    card_contribution_percat= {cat:{} for cat in monthly_spending.keys()}
    card_fees = {card.name:-card.fee for card in all_cards}
    


    for cat in total_rewards.keys():
        total_reward = sum(p["reward"] * p["time"] for p in total_rewards[cat]["portions"])
        total_reward=0
        for p in total_rewards[cat]["portions"]:
            portion_reward=p["reward"] * p["time"]
            total_reward+=portion_reward
            totalratio=sum(p["ratios"])
            for i in range(len(p["ratios"])):
                card=p["cards"][i]
                partial_card_contrib=p["ratios"][i]*portion_reward/totalratio
                card_contribution[card]+=partial_card_contrib
                card_contribution_percat[cat][card]=partial_card_contrib + card_contribution_percat[cat].get(card,0)
        cash_back = (total_reward / monthly_spending[cat]) * 100 if monthly_spending[cat] != 0 else 0
        # cards=",".join((total_rewards[cat]["cards"]))
        cards = ",".join([f"{card}({card_contribution_percat[cat].get(card, 0) / total_reward:.0%})" for card in total_rewards[cat]["cards"]
    ])
        # print(cards)
        # print(f"{cat:<20}${monthly_spending[cat]:>14.2f}${total_reward:>14.2f}{cash_back_pct:>14.2f}%")
        print(f"{cat:<20}{f'${monthly_spending[cat]:,.2f}':>20}{f'${total_reward:,.2f}':>15}{cash_back:>14.2f}%{' ' * 4}{cards:<50}")
        total_spending+=monthly_spending[cat]
        total_cashback+=total_reward
    annual_fees=sum(c.fee for c in all_cards)
    total_cashback -= annual_fees
    if annual_fees>0:
        print(f"{'annual fees':<20}{'':>20}{f'-${annual_fees:,.2f}':>15}{'':>15}")
        
    cash_back=(total_cashback/total_spending)*100 if total_spending!=0 else 0
    print(f"{'total':<20}{f'${total_spending:,.2f}':>20}{f'${total_cashback:,.2f}':>15}{cash_back:>14.2f}%")

    print("PER CARD CONTRIBUTION:"+'-'*50)
    print(f"{'CARD':<30}{'contributed':>20}{'monthly fees':>20}")
    for card, reward in card_contribution.items():
        print(f"{card:<30}{f'${reward:,.2f}':>20}{f'{card_fees[card]:,.2f}':>20}")
        