import math
class CreditCard:
    def __init__(self, name, flat_rates=None, rotating_categories=None, custom_categories=None, custom_rates=None, monthly_caps=None,fee=None, cpp=None, base_rate=0.01):
        """
        - name: str - name of the card
        - flat_rates: dict - category -> reward rate (e.g., {"groceries": 0.05})
        - rotating_categories: dict - category -> ( reward rate, yearly chance% ) (e.g., {"dining": (0.05,0.25), "groceries": (0.05,0.25)})
        - custom_categories: set - category (e.g. {"groceries", "dining", "gas"})
        - custom_rates: list - reward rates (e.g. [0.05] or [0.03, 0.02, 0.01] in case of ranked custom rates)
        - monthly_caps: dict - category -> cap amount (e.g., {"groceries": 500}). "custom" and "rotating" are special keywords
        - fee: float - monthly fee. ((Annual fee - annual credits)/12)
        - cpp: float - cents per point. default: 1.0. 
        - base_rate: float - base reward if no category matches
        """
        self.name = name
        self.flat_rates = flat_rates or {}
        self.rotating_categories = rotating_categories or {}
        self.custom_categories = set(custom_categories or [])
        self.custom_rates = custom_rates or []
        self.monthly_caps = monthly_caps or {}
        self.fee=fee or 0
        self.cpp=cpp or 1.0
        self.base_rate = base_rate
        self.use = {}
        self.time=0
        self.custom_i=0

    def reset(self):
        self.use={}
        self.time = 0
        self.custom_i=0
    
    #probably should return the reward amount, actual used amount in case of cap, and % chance of occurance so the main script can do the appropriate probability calculations
    def calc_rot(self, amount, category):
        if category in self.rotating_categories:
            
            rate,chance =self.rotating_categories[category]
            
            cap = self.monthly_caps.get("rotating",math.inf)
            
            if ("rot_"+category) not in self.use:
                self.use[("rot_"+category)] = 0
            used=self.use[("rot_"+category)]
            
            available = max(cap - used, 0)
            
            usable=min(amount,available)
            reward=usable*rate*self.cpp
           
            return reward, usable, chance
        else:
            return 0, 0, 0
    def use_rot(self,amount,category):
        #same as above, but actually increment self.use by return value
        reward, usable, chance = self.calc_rot(amount,category)
        self.use[("rot_"+category)] = self.use.get(("rot_"+category), 0) + usable
        return reward, usable, chance
    
    def calc_custom(self, amount, category):
        if category in self.custom_categories:
            if self.custom_i >= len(self.custom_rates):
                return 0,0
            rate =self.custom_rates[self.custom_i]
            
            cap = self.monthly_caps.get("custom",math.inf)
            
            if (category) not in self.use:
                self.use[(category)] = 0
            used=self.use[(category)]
            
            available = max(cap - used, 0)
            
            usable=min(amount,available)
            reward=usable*rate*self.cpp
           
            return reward, usable
        else:
            return 0, 0
    def use_custom(self,amount,category):
        #same as above, but actually increment self.use by return value
        reward, usable = self.calc_custom(amount,category)
        self.use[category] = self.use.get(category, 0) + usable
        # self.custom_i+=1
        return reward, usable
        
    def calc_flat(self,amount,category):
        if category in self.flat_rates:
            rate =self.flat_rates[category]
            
            cap = self.monthly_caps.get(category,math.inf)
            
            if (category) not in self.use:
                self.use[(category)] = 0
            used=self.use[(category)]
            
            available = max(cap - used, 0)
            
            usable=min(amount,available)
            reward=usable*rate*self.cpp
           
            return reward, usable
        else:
            reward=amount*self.base_rate
            return reward, amount
    def use_flat(self,amount,category):
        #same as above, but actually increment self.use by return value
        reward, usable = self.calc_flat(amount,category)
        self.use[category] = self.use.get(category, 0) + usable
        # self.custom_i+=1
        return reward, usable