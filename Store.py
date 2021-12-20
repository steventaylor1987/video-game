#-------------------------------------------------------------------------------------#
#   Importing necessary packages and libraries.
import math
import pprint
import time
import random
import sys

#-------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------#
#   Setting global variables for use in other classes and functions
player_level = 2
player_hp = 100

#-------------------------------------------------------------------------------------#

#-------------------------------------------------------------------------------------#
#   This block of code is designed to maintain and manage backpack inventory. The 
# purpose here is to store just the name, level, and prefix of the weapon. The 
# statistics for damage, weakness, etc... will be stored in another dictionary or array.

backpack_storage = []


#-------------------------------------------------------------------------------------#
#   This block of code called "weapons_slots" is designed to create the data
# structure for the players 'in-use' weapons. The player can only hold 2 weapons 
# at a time, but can utilize the backpack to store additional items and weapons.
# Each weapon will have a type, damage, and level damage multiplier,
# but only certain weapons will have the special effects. Additionally, loot
# dropped by enemies will contain a rarity level and extra aspects.

weapon_slots = {

        "weapon_1":
            {
                "weapon_type": [],
                "level": [],
                "rarity": [],
                "damage": [],
                "level_dmg_multiplier": [],
                "special": 
                    {
                        "special_type": [],
                        "strength": [],
                        "weakness": [],
                        "damage_multiplier": [],
                        "weakness_multiplier": []
                    }
            },
            
        "weapon_2":
            {
                "weapon_type": [],
                "level": [],
                "rarity": [],
                "damage": [],
                "level_dmg_multiplier": [],
                "special": 
                    {
                        "special_type": [],
                        "strength": [],
                        "weakness": [],
                        "damage_multiplier": [],
                        "weakness_multiplier": []
                    }
            }
}


#-------------------------------------------------------------------------------------#


#-------------------------------------------------------------------------------------#
#   This block of code is designed to store the base values for all weapons. This will 
# only include data and descriptions that can be used elsewhere such as when the player
# enters into a battle, or places a weapon into their active use (i.e. "weapons_list")

### UNFINISHED -- Still need to finish this dictionary for battles

weapons_stats = {

    "short_sword": 
        {
            "damage": 8,
            "level_dmg_multiplier": 1.04,
            "special":
                {
                    1:
                        {
                            "fire": 
                                {
                                    "strength": "ice",
                                    "weakness": "water",
                                    "damage_multiplier": 1.10,
                                    "weakness_multiplier": 0.92
                                }
                        },
                 
                    
                    2:
                        {
                            "ice": 
                                {
                                    "strength": "earth",
                                    "weakness": "fire",
                                    "damage_multiplier": 1.08,
                                    "weakness_multiplier": 0.90
                                }
                        },
                    
                    
                    3:
                        {
                            "lightning": 
                                {
                                    "strength": "water",
                                    "weakness": "earth",
                                    "damage_multiplier": 1.09,
                                    "weakness_multiplier": 0.95
                                }
                        },

                    4:
                        {
                            "water": 
                                {
                                    "strength": "fire",
                                    "weakness": "lightning",
                                    "damage_multiplier": 1.12,
                                    "weakness_multiplier": 0.94
                                }
                        },

                    5:
                        {
                            "earth": 
                                {
                                    "strength": "lightning",
                                    "weakness": "ice",
                                    "damage_multiplier": 1.07,
                                    "weakness_multiplier": 0.91
                                }
                        },
                }
        }
}

#-------------------------------------------------------------------------------------#
#   This block of code is designed to set the rarity levels and probabilities for
# loot drops in enemy fights and store inventory. There are four levels of rarity and 
# the more rare items have a lower chance of dropping. Drops utilize a random number 
# generation between 1 and 1,000.

loot_table_rarity = {
    "Common": 400,
    "Rare": 120,
    "Exotic": 25,
    "Legendary": 1
}


#-------------------------------------------------------------------------------------#
#   This block of code is designed to be a key value pair dictionary used in the auto-
# generation of loot for both fights and stores. The values for rarities and prefixes
# are used as scaling tools combined with the player's level. the values for the 
# weapons themselves are the base costs before scalars. 
# ie: level 50. Legendary Swift Hunter Bow would be cost valued at ((50^1.12)^1.10)*300

cost_calc = {
    "Common": 1,          
    "Rare": 1.04,         
    "Exotic": 1.08,       
    "Legendary": 1.12,    
    "Yielding": 1,        
    "Strong": 1.05,       
    "Swift": 1.10,        
    "Necromantic": 1.12,  
    "Blighted": 1.14,     
    "Burgeoning": 1.16,
    "Short Sword": 500,
    "Hunter Bow": 300,
    "Warrior Bow": 700,
    "Elven Bow": 1200,
    "Arrow": 10,
    "Refined Arrow": 20,
    "Long Sword": 800,
    "Regal Sword": 1200,
    "Small Ax": 400,
    "Dwarven Ax": 1000,
    "Mage Staff": 500,
    "Wizards Staff": 2000
}

#-------------------------------------------------------------------------------------#
#   This block of code is designed to set the weapons drops and probabilities for each
# weapon drop in enemy fights and store inventory. There are 10 weapons and the more 
# rare weapons have a lower chance of dropping. Drops utilize a random number generation 
# between 1 and 1,000 which is a separate RNG from the rarity and prefix.

loot_weapons = {
    "short_sword": 850,
    "hunter_bow": 700,
    "warrior_bow": 650,
    "elven_bow": 625,
    "long_sword": 400,
    "regal_sword": 300,
    "small_ax": 150,
    "dwarven_ax": 100,
    "mage_staff": 20,
    "wizards_staff": 1  
}


#-------------------------------------------------------------------------------------#
#   This block of code is designed to set the weapon prefix options for loot drops and
# store inventory. The RNG parts of the loot drop will randomly assign levels, 
# prefixes, weapons, and rarity based on the weights details in these dictionaries.

loot_prefixes = {
    "yielding": 750,
    "strong": 500,
    "swift": 200,
    "necromantic": 100,
    "blighted": 50,
    "burgeoning": 1
}


#-------------------------------------------------------------------------------------#
#   This block of code is designed to set the loot level options for loot drops.
# The RNG parts of the loot drop will randomly assign levels, prefixes, weapons, and
# rarity based on the weights details in these dictionaries.

loot_levels = {
    "equal_to_player": 500,
    "player_level_plus_1": 200,
    "player_level_plus_2": 50,
    "player_level_plus_3": 1
}


#-------------------------------------------------------------------------------------#
#   This block of code is designed to assign the 'Ultimate' weapons that are assigned to
# each boss. Each boss will have a very small percentage chance to drop their unique
# Ultimate weapon. This dictionary is where that drop rate is set.

boss_drops = {

    "Razor Wolf": 
        {
            "Name": "Ultimate Frenzied Bow",
            "Description": "Fires between 2-4 arrows for every attack",
            "Drop Rate": 20
        }
}

def store():

    bought = ""           ### Establishing bought as a variable ahead of the while loop
    buy_or_sell = ""      ### Establishing buy_or_sell as a variable ahead of the while loop
    loot_amount = 10      ### Allows for easy adjustment for store inventory. Can be any number up to 10.
    money_count = 4000    ### User's funds. TO_DO: Still need to determine how this operates (global varible? Function to track funds?)
    item_list = []        
    time.sleep(0.5)
    
    for i in range(0, loot_amount): ### This for loop calls on the loot() function to randomly generate the loot for the store inventory
        A = loot(1)
        item_list.append(A)
        
    print_slow("Welcome to the local store!")
    time.sleep(0.5)
    print('...')
    loot_amount = None
    
    while bought != "exit" or buy_or_sell != "3":  # While loop is established for when the user is in the store. 
    
        time.sleep(1)
        print_slow("What would you like to do?")
        print("")
        time.sleep(0.75)
        print("1. Buy")
        time.sleep(0.5)
        print("2. Sell")
        time.sleep(0.5)
        print("3. Exit")
        print("")
        buy_or_sell = input()
    
        if buy_or_sell == '1':
            
            ###     The following code is designed to auto calculate the cost of the 10 weapons in the store based on
            ### their attributes such as level, prefix, weapon type, etc... Because the store loot is RNG, the cost
            ### must be generated by calculation instead of a static value. 
            
            time.sleep(.5)
            item_1 = item_list[0][0]  ### Items 1 through 10 are the items this store can/will sell.
            item_2 = item_list[1][0]
            item_3 = item_list[2][0]
            item_4 = item_list[3][0]
            item_5 = item_list[4][0]
            item_6 = item_list[5][0]
            item_7 = item_list[6][0]
            item_8 = item_list[7][0]
            item_9 = item_list[8][0]
            item_10 = item_list[9][0]
            
            cost_1 = round(((item_1[0]**cost_calc[item_1[1]])**cost_calc[item_1[2]])*cost_calc[item_1[3]],0)  ### Cost calculations. 
            cost_2 = round(((item_2[0]**cost_calc[item_2[1]])**cost_calc[item_2[2]])*cost_calc[item_2[3]],0)  ### Rarer item cost more.
            cost_3 = round(((item_3[0]**cost_calc[item_3[1]])**cost_calc[item_3[2]])*cost_calc[item_3[3]],0)
            cost_4 = round(((item_4[0]**cost_calc[item_4[1]])**cost_calc[item_4[2]])*cost_calc[item_4[3]],0)
            cost_5 = round(((item_5[0]**cost_calc[item_5[1]])**cost_calc[item_5[2]])*cost_calc[item_5[3]],0)
            cost_6 = round(((item_6[0]**cost_calc[item_6[1]])**cost_calc[item_6[2]])*cost_calc[item_6[3]],0)
            cost_7 = round(((item_7[0]**cost_calc[item_7[1]])**cost_calc[item_7[2]])*cost_calc[item_7[3]],0)
            cost_8 = round(((item_8[0]**cost_calc[item_8[1]])**cost_calc[item_8[2]])*cost_calc[item_8[3]],0)
            cost_9 = round(((item_9[0]**cost_calc[item_9[1]])**cost_calc[item_9[2]])*cost_calc[item_9[3]],0)
            cost_10 = round(((item_10[0]**cost_calc[item_10[1]])**cost_calc[item_10[2]])*cost_calc[item_10[3]],0)
            
            print("")
            print_slow("---------- MENU ----------")
            print("")
            time.sleep(0.5)
            print('#1:', 'level',item_1[0], item_1[1], item_1[2], item_1[3], "--", '${:,.0f}'.format(cost_1))  ### Printing store inventory
            print('#2:', 'level',item_2[0], item_2[1], item_2[2], item_2[3], "--", '${:,.0f}'.format(cost_2))  ### Printing store inventory
            print('#3:', 'level',item_3[0], item_3[1], item_3[2], item_3[3], "--", '${:,.0f}'.format(cost_3))  ### Printing store inventory
            print('#4:', 'level',item_4[0], item_4[1], item_4[2], item_4[3], "--", '${:,.0f}'.format(cost_4))  ### Printing store inventory
            print('#5:', 'level',item_5[0], item_5[1], item_5[2], item_5[3], "--", '${:,.0f}'.format(cost_5))  ### Printing store inventory
            print('#6:', 'level',item_6[0], item_6[1], item_6[2], item_6[3], "--", '${:,.0f}'.format(cost_6))  ### Printing store inventory
            print('#7:', 'level',item_7[0], item_7[1], item_7[2], item_7[3], "--", '${:,.0f}'.format(cost_7))  ### Printing store inventory
            print('#8:', 'level',item_8[0], item_8[1], item_8[2], item_8[3], "--", '${:,.0f}'.format(cost_8))  ### Printing store inventory
            print('#9:', 'level',item_9[0], item_9[1], item_9[2], item_9[3], "--", '${:,.0f}'.format(cost_9))  ### Printing store inventory
            print('#10:', 'level',item_10[0], item_10[1], item_10[2], item_10[3], "--", '${:,.0f}'.format(cost_10))  ### Printing store inventory
            print("")
            time.sleep(0.5)
            print_slow("Current money balance: ")
            print('${:,.0f}'.format(money_count))
            print("")
            time.sleep(0.5)
            print_slow("Type exit to leave")
            time.sleep(0.5)
            print("")
            print_slow("What item would you like to buy? (Enter number i.e 3)")
            print("")
            bought = input()
        
            ### The following set of 'if' statements is designed to account for the user's interaction at the store
            ### The checks in place are as follows:
            ### ----- 1: Check to see if user chose to buy, sell, or exit.
            ### ----- 2: Check to see if user has enough money to purchase desired weapon.
            ### ----- 3: Check to confirm if user really wants to buy desired weapon.
            ### ----- 4: Check to see if user has enough space in their backpack to store weapon.
            ### ----- 5: Check to see if user wants to return to the main menu.
        
            if bought == '1':  ### User chose 'buy' this item number
            
                if money_count >= cost_1: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_1), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_1     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_1.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_1)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_1:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '2':  ### User chose 'buy' this item number
            
                if money_count >= cost_2: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_2), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_2     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_2.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_2)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_2:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')
            
            
            elif bought == '3':  ### User chose 'buy' this item number
            
                if money_count >= cost_3: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_3), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_3     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_3.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_3)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_3:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')            

            elif bought == '4':  ### User chose 'buy' this item number
            
                if money_count >= cost_4: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_4), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_4     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_4.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_4)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries! What else would you like to buy?")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_4:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '5':  ### User chose 'buy' this item number
            
                if money_count >= cost_5: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_5), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_5     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_5.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_5)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_5:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '6':  ### User chose 'buy' this item number
            
                if money_count >= cost_6: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_6), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_6     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_6.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_6)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_6:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '7':  ### User chose 'buy' this item number
            
                if money_count >= cost_7: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_7), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_7     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_7.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_7)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_7:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '8':  ### User chose 'buy' this item number
            
                if money_count >= cost_8: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_8), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_8     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_8.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_8)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_8:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '9':  ### User chose 'buy' this item number
            
                if money_count >= cost_9: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_9), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_9     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)    ### RNG for elemental aspect of weapon.
                            item_9.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_9)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_9:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')

            elif bought == '10':  ### User chose 'buy' this item number
            
                if money_count >= cost_10: ### Does user have enough money?
                
                    print_slow("That will be ") ### Print slow is a slow printing function to make the user experience better
                    print('${:,.0f}'.format(cost_10), end='')
                    print_slow(" are you sure you want to buy it?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to buy?
                    
                        if len(backpack_storage) <= 5: ### Does user have enough backpack space?
                    
                            money_count = money_count - cost_10     ### Money adjustment after purchase is confirmed.
                            outcome = element_roll(money_count)     ### RNG for elemental aspect of weapon.
                            item_10.append(outcome)                 ### Update weapon with RNG element choice.
                            backpack_storage.append(item_10)        ### Update user's backpack with purchased weapon.

                            print_slow("Would you like to return to the main menu?")
                            print("")
                            print_slow("1. Yes")
                            print("")
                            print_slow("2. No")
                            print("")
                            user_input = input()
            
                            if user_input == '1':
                                continue
                            elif user_input == '2':
                                print_slow("Ok, have a great day!") ### Breaks indicate that user leaves the store.
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack") ### Inform user they don't have backpack space
                            print("")
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_10:
                
                    print_slow("You dont have enough money to buy this item")  ### Inform user of insufficient funds. 
                    time.sleep(.25)
                    print("")
                    
                else:
                
                    print('ERROR')
        
        elif buy_or_sell == '2':  ### User has chosen to sell.
        
            print_slow("Ok let\'s take a look at your inventory!")
            print("")
            time.sleep(1)
            sell_choice = ""
            
            if len(backpack_storage) > 0:  ### Check to see if they have anything in their backpack inventory. 
            
                for i in range(0,len(backpack_storage)):
                
                    print(i+1,end='')
                    print(':', 'level', backpack_storage[i][0], backpack_storage[i][1], backpack_storage[i][2], backpack_storage[i][3], "-- ", end='')
                    time.sleep(0.75)
                    cost_item = 0.95*round(((backpack_storage[i][0]**cost_calc[backpack_storage[i][1]])**cost_calc[backpack_storage[i][2]])*cost_calc[backpack_storage[i][3]],0)
                    print('${:,.0f}'.format(cost_item))
                    
                time.sleep(0.75)
                print_slow("Enter the number of the item you would like sell. (Type \'exit\' to leave)")
                print("")
                time.sleep(0.75)
                sell_choice = input()
                
                if sell_choice == "1":
                    
                    sell_1 = 0.95*round(((backpack_storage[0][0]**cost_calc[backpack_storage[0][1]])**cost_calc[backpack_storage[0][2]])*cost_calc[backpack_storage[0][3]],0)
                    print_slow("I can pay ") 
                    print('${:,.0f}'.format(sell_1), end='')
                    print_slow(" for that weapon")
                    print("")
                    print_slow("Would you still like to sell it to me?")
                    print("")
                    print_slow("1. Yes")
                    print("")
                    print_slow("2. No")
                    print("")
                    decision = input()
                    
                    if decision == '1': ### Does user really want to sell?
                    
                        print_slow("Thank you! You have sold: ")
                        print("Level", backpack_storage[0][0], backpack_storage[0][1], backpack_storage[0][2], backpack_storage[0][3], backpack_storage[0][4])
                        time.sleep(0.75)
                        print("")
                        money_count = money_count + (0.95*round(((backpack_storage[0][0]**cost_calc[backpack_storage[0][1]])**cost_calc[backpack_storage[0][2]])*cost_calc[backpack_storage[0][3]],0))
                        print("You now have ", '${:,.0f}'.format(money_count))
                        backpack_storage.pop(0)
                        
                    elif decision == '2': ### User chose not to buy intended item.
                    
                        print_slow("Ok, no worries!")
                        print("")

                    else:
                    
                        print("ERROR")
                    
                elif sell_choice == "2":
            
                    if len(backpack_storage) <= 1:
                    
                        print_slow("Invalid selection. No item exists at that spot") ### User tried to sell something that wasn't there.
                        print("")
                        
                    else:
                        
                        ### - Determining what the store can pay for this given item (A percentage of face value usually)
                        
                        sell_2 = 0.95*round(((backpack_storage[1][0]**cost_calc[backpack_storage[1][1]])**cost_calc[backpack_storage[1][2]])*cost_calc[backpack_storage[1][3]],0)
                        print_slow("I can pay ") 
                        print('${:,.0f}'.format(sell_2), end='')
                        print_slow(" for that weapon")
                        print("")
                        print_slow("Would you still like to sell it to me?")
                        print("")
                        print_slow("1. Yes")
                        print("")
                        print_slow("2. No")
                        print("")
                        decision = input()
                        
                        if decision == '1': ### Does user really want to sell?
                        
                            print_slow("Thank you! You have sold: ")
                            print("Level", backpack_storage[1][0], backpack_storage[1][1], backpack_storage[1][2], backpack_storage[1][3], backpack_storage[1][4])
                            time.sleep(0.75)
                            print("")
                            money_count = money_count + (0.95*round(((backpack_storage[1][0]**cost_calc[backpack_storage[1][1]])**cost_calc[backpack_storage[1][2]])*cost_calc[backpack_storage[1][3]],0))
                            print("You now have ", '${:,.0f}'.format(money_count))
                            backpack_storage.pop(1)   ### Remove that item from the user's backpack after selling it.
                            
                        elif decision == '2': ### User chose not to buy intended item.
                        
                            print_slow("Ok, no worries!") ### User had second thoughts about selling that item.
                            print("")

                        else:   ### Should never be encountered
                        
                            print("ERROR")
                
                elif sell_choice == "3":
            
                    if len(backpack_storage) <= 2:
                    
                        print_slow("Invalid selection. No item exists at that spot") ### User tried to sell something that wasn't there.
                        print("")
                        
                    else:
                        
                        ### - Determining what the store can pay for this given item (A percentage of face value usually)
                        
                        sell_3 = 0.95*round(((backpack_storage[2][0]**cost_calc[backpack_storage[2][1]])**cost_calc[backpack_storage[2][2]])*cost_calc[backpack_storage[2][3]],0)
                        print_slow("I can pay ") 
                        print('${:,.0f}'.format(sell_3), end='')
                        print_slow(" for that weapon")
                        print("")
                        print_slow("Would you still like to sell it to me?")
                        print("")
                        print_slow("1. Yes")
                        print("")
                        print_slow("2. No")
                        print("")
                        decision = input()
                        
                        if decision == '1': ### Does user really want to sell?
                        
                            print_slow("Thank you! You have sold: ")
                            print("Level", backpack_storage[2][0], backpack_storage[2][1], backpack_storage[2][2], backpack_storage[2][3], backpack_storage[2][4])
                            time.sleep(0.75)
                            print("")
                            money_count = money_count + (0.95*round(((backpack_storage[2][0]**cost_calc[backpack_storage[2][1]])**cost_calc[backpack_storage[2][2]])*cost_calc[backpack_storage[2][3]],0))
                            print("You now have ", '${:,.0f}'.format(money_count))
                            backpack_storage.pop(2)   ### Remove that item from the user's backpack after selling it.
                            
                        elif decision == '2': ### User chose not to buy intended item.
                        
                            print_slow("Ok, no worries!") ### User had second thoughts about selling that item.
                            print("")

                        else:   ### Should never be encountered
                        
                            print("ERROR")

                elif sell_choice == "4":
            
                    if len(backpack_storage) <= 3:
                    
                        print_slow("Invalid selection. No item exists at that spot") ### User tried to sell something that wasn't there.
                        print("")
                        
                    else:
                        
                        ### - Determining what the store can pay for this given item (A percentage of face value usually)
                        
                        sell_4 = 0.95*round(((backpack_storage[3][0]**cost_calc[backpack_storage[3][1]])**cost_calc[backpack_storage[3][2]])*cost_calc[backpack_storage[3][3]],0)
                        print_slow("I can pay ") 
                        print('${:,.0f}'.format(sell_4), end='')
                        print_slow(" for that weapon")
                        print("")
                        print_slow("Would you still like to sell it to me?")
                        print("")
                        print_slow("1. Yes")
                        print("")
                        print_slow("2. No")
                        print("")
                        decision = input()
                        
                        if decision == '1': ### Does user really want to sell?
                        
                            print_slow("Thank you! You have sold: ")
                            print("Level", backpack_storage[3][0], backpack_storage[3][1], backpack_storage[3][2], backpack_storage[3][3], backpack_storage[3][4])
                            time.sleep(0.75)
                            print("")
                            money_count = money_count + (0.95*round(((backpack_storage[3][0]**cost_calc[backpack_storage[3][1]])**cost_calc[backpack_storage[3][2]])*cost_calc[backpack_storage[3][3]],0))
                            print("You now have ", '${:,.0f}'.format(money_count))
                            backpack_storage.pop(3)   ### Remove that item from the user's backpack after selling it.
                            
                        elif decision == '2': ### User chose not to buy intended item.
                        
                            print_slow("Ok, no worries!") ### User had second thoughts about selling that item.
                            print("")

                        else:   ### Should never be encountered
                        
                            print("ERROR")
                elif sell_choice == "5":
            
                    if len(backpack_storage) <= 4:
                    
                        print_slow("Invalid selection. No item exists at that spot") ### User tried to sell something that wasn't there.
                        print("")
                        
                    else:
                        
                        ### - Determining what the store can pay for this given item (A percentage of face value usually)
                        
                        sell_5 = 0.95*round(((backpack_storage[4][0]**cost_calc[backpack_storage[4][1]])**cost_calc[backpack_storage[4][2]])*cost_calc[backpack_storage[4][3]],0)
                        print_slow("I can pay ") 
                        print('${:,.0f}'.format(sell_5), end='')
                        print_slow(" for that weapon")
                        print("")
                        print_slow("Would you still like to sell it to me?")
                        print("")
                        print_slow("1. Yes")
                        print("")
                        print_slow("2. No")
                        print("")
                        decision = input()
                        
                        if decision == '1': ### Does user really want to sell?
                        
                            print_slow("Thank you! You have sold: ")
                            print("Level", backpack_storage[4][0], backpack_storage[4][1], backpack_storage[4][2], backpack_storage[4][3], backpack_storage[4][4])
                            time.sleep(0.75)
                            print("")
                            money_count = money_count + (0.95*round(((backpack_storage[4][0]**cost_calc[backpack_storage[4][1]])**cost_calc[backpack_storage[4][2]])*cost_calc[backpack_storage[4][3]],0))
                            print("You now have ", '${:,.0f}'.format(money_count))
                            backpack_storage.pop(4)   ### Remove that item from the user's backpack after selling it.
                            
                        elif decision == '2': ### User chose not to buy intended item.
                        
                            print_slow("Ok, no worries!") ### User had second thoughts about selling that item.
                            print("")

                        else:   ### Should never be encountered
                        
                            print("ERROR")

                else:
                
                    print_slow("Invalid selection")
                    print("")
                
            else:
            
                print_slow("Sorry, it looks like you have no weapons to sell!") ### This is displayed when the user tries to sell when they have nothing to sell. 
                print("")
                continue
            
        elif buy_or_sell == "3":
            
            print_slow("Ok, have a great day!") ### User chose to exit the store. 
            break
            
        else:
        
            print("ERROR")  ### Should never be encountered, but will help with debugging if needed. 
            
    return

### END OF store() FUNCITON ----------------------------------------------------------------###


### ------------------------------------------------------------------------------- ###
### This function is designed to slowly print things that the user is interacting with
### In the cases of a battle, or a store interaction, it is a more pleasant experience
### to see the words slowly appear instead of abruptly.

def print_slow(str):

    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.06)
        
### END OF print_slow() FUNCITON ----------------------------------------------------------------###


### ------------------------------------------------------------------------------- ###
### This function is designed to randomly generate an elemental component to weapons,
### armor, etc... These elemental properties will have special strengths and weaknesses
### in battle, and players can build loadouts for special bosses, etc...

def element_roll(money_count):
    
    rand_roll = random.randrange(1,100) ### Randomly generating a number to determine element.
    
    if rand_roll >= 70: ### If RNG is between 70-100, element = Water
        
        print_slow("Your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Water")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ")
        print('${:,.0f}'.format(money_count))
        outcome = 'Water'
   
    elif rand_roll >= 40 and rand_roll < 70:  ### If RNG is between 40-70, element = Earth
    
        print_slow("Your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Earth")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ")
        print('${:,.0f}'.format(money_count))
        outcome = 'Earth'
       
    elif rand_roll >= 10 and rand_roll < 40:  ### If RNG is between 10-40, element = Lightning
    
        print_slow("Your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Lightning")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ") 
        print('${:,.0f}'.format(money_count))
        outcome = 'Lightning'
     
    elif rand_roll >= 3 and rand_roll < 10:  ### If RNG is between 3-10, element = Ice
    
        print_slow("Your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Ice")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ") 
        print('${:,.0f}'.format(money_count))
        outcome = 'Ice'

    elif rand_roll < 3:  ### If RNG is less than 3, element = Fire. Fire has special properties among elements.

        print_slow("Your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Fire")
        time.sleep(0.75)
        print("")
        print_slow("How rare!!!")
        time.sleep(0.5)
        print("")
        print_slow("Remaining money balance: ") 
        print('${:,.0f}'.format(money_count))
        outcome = 'Fire'
    
    return outcome

### END OF element_roll() FUNCITON ----------------------------------------------------------------###


### ------------------------------------------------------------------------------- ###
### This function is designed to randomly generate a list of loot for both store 
### inventory as well as for battles and RNG loot drops from enemies and bosses. This
### function uses the lists and dictionaries for levels, prefixes, weapon types, etc...
### The parameter (loot_amount) is to determine how much RNG loot should be generated
### on each call of this function. 

def loot(loot_amount):
    
    loot_lvl = []   ### - Level list established
    loot_rare = []  ### - Rarity list established
    loot_pref = []  ### - Prefix list established
    loot_weap = []  ### - Weapon Type list established
    loot_det = []   ### - Resulting Loot list established
    
    for i in range(0, loot_amount):
        
        count = 0
        
        loot_level = random.randrange(1,1000)   ### - Randomly generating numbers to reference in specific dictionaries. 
        loot_rarity = random.randrange(1,1000)
        loot_type = random.randrange(1,1000)
        loot_prefix = random.randrange(1,1000)
        
        
        if loot_level >= loot_levels['equal_to_player']:       ### Checking RNG value to determine loot levels. 
            loot_lvl.append(player_level)
        elif loot_level >= loot_levels['player_level_plus_1']:
            loot_lvl.append(player_level + 1)
        elif loot_level >= loot_levels['player_level_plus_2']:
            loot_lvl.append(player_level + 2)
        elif loot_level >= loot_levels['player_level_plus_3']:
            loot_lvl.append(player_level + 3)
        else:
            print('ERROR rarity')
        
    
        if loot_prefix >= loot_prefixes['yielding']:           ### Checking RNG value to determine prefix for weapon.
            loot_pref.append('Yielding')
        elif loot_prefix >= loot_prefixes['strong'] and loot_prefix < loot_prefixes['yielding']: 
            loot_pref.append('Strong')
        elif loot_prefix >= loot_prefixes['swift'] and loot_prefix < loot_prefixes['strong']:
            loot_pref.append('Swift')
        elif loot_prefix >= loot_prefixes['necromantic']and loot_prefix < loot_prefixes['swift']:
            loot_pref.append('Necromantic')
        elif loot_prefix >= loot_prefixes['blighted']and loot_prefix < loot_prefixes['necromantic']:
            loot_pref.append('Blighted')
        elif loot_prefix >= loot_prefixes['burgeoning']and loot_prefix < loot_prefixes['blighted']:
            loot_pref.append('Burgeoning')
        else:
            print('ERROR rarity')
            
                
        if loot_type >= loot_weapons['short_sword']:           ### Checking RNG value to determine weapon type. 
            loot_weap.append('Short Sword')
        elif loot_type >= loot_weapons['hunter_bow'] and loot_type < loot_weapons['short_sword']: 
            loot_weap.append('Hunter Bow')
        elif loot_type >= loot_weapons['warrior_bow'] and loot_type < loot_weapons['hunter_bow']:
            loot_weap.append('Warrior Bow')
        elif loot_type >= loot_weapons['elven_bow'] and loot_type < loot_weapons['warrior_bow']:
            loot_weap.append('Elven Bow')
        elif loot_type >= loot_weapons['long_sword'] and loot_type < loot_weapons['elven_bow']:
            loot_weap.append('Long Sword')
        elif loot_type >= loot_weapons['regal_sword'] and loot_type < loot_weapons['long_sword']:
            loot_weap.append('Regal Sword')
        elif loot_type >= loot_weapons['small_ax'] and loot_type < loot_weapons['regal_sword']:
            loot_weap.append('Small Ax')
        elif loot_type >= loot_weapons['dwarven_ax']and loot_type < loot_weapons['small_ax']:
            loot_weap.append('Dwarven Ax')
        elif loot_type >= loot_weapons['mage_staff'] and loot_type < loot_weapons['dwarven_ax']:
            loot_weap.append('Mage Staff')
        elif loot_type >= loot_weapons['wizards_staff'] and loot_type < loot_weapons['mage_staff']:
            loot_weap.append('Wizards Staff')
        else: 
            print("ERROR weapons")
        
        
        if loot_rarity >= loot_table_rarity['Common']:          ### Checking RNG value to determine weapong rarity. 
            loot_rare.append('Common')
        elif loot_rarity >= loot_table_rarity['Rare'] and loot_rarity < loot_table_rarity['Common']: 
            loot_rare.append('Rare')
        elif loot_rarity >= loot_table_rarity['Exotic'] and loot_rarity < loot_table_rarity['Rare']:
            loot_rare.append('Exotic')
        elif loot_rarity >= loot_table_rarity['Legendary']and loot_rarity < loot_table_rarity['Exotic']:
            loot_rare.append('Legendary')
        else:
            print('ERROR rarity')
            
        loot_det.append([loot_lvl[i], loot_rare[i], loot_pref[i], loot_weap[i]])  # Appending loot list to return function call.
        
    return(loot_det)

### END OF loot() FUNCITON ----------------------------------------------------------------###             
  

def main():

    store()  
      
main()     
