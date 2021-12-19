#-------------------------------------------------------------------------------------#
#   Importing necessary packages and libraries.
import math
import pprint
import time
import random
import sys,time,random
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

weapons_slots = {

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
# loot drops in enemy fights. There are four levels of rarity and the more rare items
# have a lower chance of dropping. Drops utilize a random number generation between
# 1 and 1,000.

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
# weapon drop in enemy fights. There are 10 weapons and the more rare weapons have a 
# lower chance of dropping. Drops utilize a random number generation between 1 and 1,000
# which is a separate RNG from the rarity and prefix.

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
#   This block of code is designed to assign the ultimate weapons that are assigned to
# each boss. Each boss will have a very small percentage chance to drop their unique
# ultimate weapon. This dictionary is where that drop rate is set.

boss_drops = {
    "Midnight Wolf": 
        {
            "Name": "Ultimate Frenzied Bow",
            "Drop Rate": 20
        }
}

def store():

    bought = ""
    loot_amount = 10
    money_count = 4000
    item_list = []
    time.sleep(0.5)
    
    for i in range(0, loot_amount):
        A = loot(1)
        item_list.append(A)
        
    print_slow("Welcome to the local store!")
    time.sleep(0.5)
    print('...')
    
    while bought != 'exit': 
    
        time.sleep(1)
        print_slow("Would you like to buy or sell?")
        print("")
        buy_or_sell = input()
    
        if buy_or_sell == 'buy':
            
            time.sleep(.5)
            item_1 = list(item_list[0])
            item_2 = list(item_list[1])
            item_3 = list(item_list[2])
            item_4 = list(item_list[3])
            item_5 = list(item_list[4])
            item_6 = list(item_list[5])
            item_7 = list(item_list[6])
            item_8 = list(item_list[7])
            item_9 = list(item_list[8])
            item_10 = list(item_list[9])
            
            cost_1 = round(((item_1[0]**cost_calc[item_1[1]])**cost_calc[item_1[2]])*cost_calc[item_1[3]],0)
            cost_2 = round(((item_2[0]**cost_calc[item_2[1]])**cost_calc[item_2[2]])*cost_calc[item_2[3]],0)
            cost_3 = round(((item_3[0]**cost_calc[item_3[1]])**cost_calc[item_3[2]])*cost_calc[item_3[3]],0)
            cost_4 = round(((item_4[0]**cost_calc[item_4[1]])**cost_calc[item_4[2]])*cost_calc[item_4[3]],0)
            cost_5 = round(((item_5[0]**cost_calc[item_5[1]])**cost_calc[item_5[2]])*cost_calc[item_5[3]],0)
            cost_6 = round(((item_6[0]**cost_calc[item_6[1]])**cost_calc[item_6[2]])*cost_calc[item_6[3]],0)
            cost_7 = round(((item_7[0]**cost_calc[item_7[1]])**cost_calc[item_7[2]])*cost_calc[item_7[3]],0)
            cost_8 = round(((item_8[0]**cost_calc[item_8[1]])**cost_calc[item_8[2]])*cost_calc[item_8[3]],0)
            cost_9 = round(((item_9[0]**cost_calc[item_9[1]])**cost_calc[item_9[2]])*cost_calc[item_9[3]],0)
            cost_10 = round(((item_10[0]**cost_calc[item_10[1]])**cost_calc[item_10[2]])*cost_calc[item_10[3]],0)

            print('#1:', 'level',item_1[0], item_1[1], item_1[2], item_1[3], "--", '${:,.0f}'.format(cost_1))
            print('#2:', 'level',item_2[0], item_2[1], item_2[2], item_2[3], "--", '${:,.0f}'.format(cost_2))
            print('#3:', 'level',item_3[0], item_3[1], item_3[2], item_3[3], "--", '${:,.0f}'.format(cost_3))
            print('#4:', 'level',item_4[0], item_4[1], item_4[2], item_4[3], "--", '${:,.0f}'.format(cost_4))
            print('#5:', 'level',item_5[0], item_5[1], item_5[2], item_5[3], "--", '${:,.0f}'.format(cost_5))
            print('#6:', 'level',item_6[0], item_6[1], item_6[2], item_6[3], "--", '${:,.0f}'.format(cost_6))
            print('#7:', 'level',item_7[0], item_7[1], item_7[2], item_7[3], "--", '${:,.0f}'.format(cost_7))
            print('#8:', 'level',item_8[0], item_8[1], item_8[2], item_8[3], "--", '${:,.0f}'.format(cost_8))
            print('#9:', 'level',item_9[0], item_9[1], item_9[2], item_9[3], "--", '${:,.0f}'.format(cost_9))
            print('#10:', 'level',item_10[0], item_10[1], item_10[2], item_10[3], "--", '${:,.0f}'.format(cost_10))
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
        
            if bought == '1':
            
                if money_count >= cost_1:
                
                    print_slow("That will be ")
                    print('${:,.0f}'.format(cost_1), end='')
                    print_slow(" are you sure you want to buy? Y or N:")
                    print("")
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_1
                            outcome = element_roll(money_count)
                            item_1.append(outcome)   
                            backpack_storage.append(item_1)

                            print_slow('Would you like to return to the menu? Y or N:')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print_slow("Sorry, you don\'t have enough space in your backpack")
                            break
                        
                    elif decision == 'N':
                    
                        print_slow("Ok, no worries! What else would you like to buy?")
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_1:
                
                    print_slow("You dont have enough money to buy this item")
                    time.sleep(.25)
                    print_slow("What else would you like to buy?")
                    
                else:
                
                    print('ERROR')

            elif bought == '2':
            
                if money_count >= cost_2:
                
                    print('That will be', '${:,.0f}'.format(cost_2), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_2
                            outcome = element_roll(money_count)
                            item_2.append(outcome)   
                            backpack_storage.append(item_2)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_2:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')

            elif bought == '3':
            
                if money_count >= cost_3:
                
                    print('That will be', '${:,.0f}'.format(cost_3), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_3
                            outcome = element_roll(money_count)
                            item_3.append(outcome)   
                            backpack_storage.append(item_3)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_3:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')

            elif bought == '4':
            
                if money_count >= cost_4:
                
                    print('That will be', '${:,.0f}'.format(cost_4), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_4
                            outcome = element_roll(money_count)
                            item_4.append(outcome)   
                            backpack_storage.append(item_4)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_4:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')
                    
            elif bought == '5':
            
                if money_count >= cost_5:
                
                    print('That will be', '${:,.0f}'.format(cost_5), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_5
                            outcome = element_roll(money_count)
                            item_5.append(outcome)   
                            backpack_storage.append(item_5)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_5:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')
                    
            elif bought == '6':
            
                if money_count >= cost_6:
                
                    print('That will be', '${:,.0f}'.format(cost_6), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_6
                            outcome = element_roll(money_count)
                            item_6.append(outcome)   
                            backpack_storage.append(item_6)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_6:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')

            elif bought == '7':
            
                if money_count >= cost_7:
                
                    print('That will be', '${:,.0f}'.format(cost_7), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_7
                            outcome = element_roll(money_count)
                            item_7.append(outcome)   
                            backpack_storage.append(item_7)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_7:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')
                    
            elif bought == '8':
            
                if money_count >= cost_8:
                
                    print('That will be', '${:,.0f}'.format(cost_8), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_8
                            outcome = element_roll(money_count)
                            item_8.append(outcome)   
                            backpack_storage.append(item_8)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_8:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')                    

            elif bought == '9':
            
                if money_count >= cost_9:
                
                    print('That will be', '${:,.0f}'.format(cost_9), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_9
                            outcome = element_roll(money_count)
                            item_9.append(outcome)   
                            backpack_storage.append(item_9)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_9:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')

            elif bought == '10':
            
                if money_count >= cost_10:
                
                    print('That will be', '${:,.0f}'.format(cost_10), 'are you sure you want to buy? Y or N:')
                    decision = input()
                    
                    if decision == 'Y':
                    
                        if len(backpack_storage) <= 20:
                    
                            money_count = money_count - cost_10
                            outcome = element_roll(money_count)
                            item_10.append(outcome)   
                            backpack_storage.append(item_10)

                            print('Would you like to buy or sell anything else? Y or N')
                            user_input = input()
            
                            if user_input == 'Y':
                                continue
                            elif user_input == 'N':
                                break
                        
                        else:
                        
                            print('Sorry, you don\'t have enough space in your backpack')
                            break
                        
                    elif decision == 'N':
                    
                        print('Ok, no worries! What else would you like to buy?')
                        
                    else:
                    
                        print('ERROR')
                            
                elif money_count < cost_10:
                
                    print('You dont have enough money to buy this item')
                    time.sleep(.25)
                    print('What else would you like to buy?')
                    
                else:
                
                    print('ERROR')        
        
        elif buy_or_sell == 'sell':
        
            print_slow("Ok let\'s take a look at your inventory!")
            print("")
            time.sleep(1)
            
            for i in range(0,len(backpack_storage)):
            
                print(i+1,end='')
                print(':', 'level', backpack_storage[i][0], backpack_storage[i][1], backpack_storage[i][2], backpack_storage[i][3], backpack_storage[i][4])
            
            
    return


def print_slow(str):

    for letter in str:
        sys.stdout.write(letter)
        sys.stdout.flush()
        time.sleep(0.07)



def element_roll(money_count):
    
    rand_roll = random.randrange(1,100)
    
    if rand_roll >= 70:
        
        print_slow("your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Water")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ")
        print('${:,.0f}'.format(money_count))
        outcome = 'Water'
   
    elif rand_roll >= 40 and rand_roll < 70:
    
        print_slow("your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Earth")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ")
        print('${:,.0f}'.format(money_count))
        outcome = 'Earth'
       
    elif rand_roll >= 10 and rand_roll < 40:
    
        print_slow("your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Lightning")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ") 
        print('${:,.0f}'.format(money_count))
        outcome = 'Lightning'
     
    elif rand_roll >= 3 and rand_roll < 10:
    
        print_slow("your weapon\'s element is...")
        time.sleep(0.75)
        print("")
        print_slow("Ice")
        time.sleep(0.75)
        print("")
        print_slow("Remaining money balance: ") 
        print('${:,.0f}'.format(money_count))
        outcome = 'Ice'

    elif rand_roll < 3:

        print_slow("your weapon\'s element is...")
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
    

def boss_battle_1():

    player_level = 1
    player_hp = 100
    boss_hp = 4
    count = 0

    print('Boss Fight - Midnight Wolf!')
    
    while boss_hp > 0 and player_hp > 0:
        
        opp_hit = 5 
        print('wolf attacks with a bite')
        player_hp = player_hp - opp_hit
        time.sleep(1.5)
        
        print('What kind of attack would you like to use?')
        print("""
        1. Compact Attack
        2. Heavy Attack
        3. Special Attack
        """)
        
        user_input = input()
    
        if user_input == "1":
    
            hit = (weapons_list['weapon_1']['damage']) * (weapons_list['weapon_1']['level_dmg_multiplier']) 
            boss_hp = boss_hp - hit
            time.sleep(1)
            print(boss_hp)            
            print(player_hp)
            
        elif user_input == 2:
        
            time.sleep(1)
            
        elif user_input == 3:
        
            time.sleep(1)
            
        else:
        
            print('ERROR')
    
    boss_drop_check = random.randrange(1,1000)
    loot_amount = random.randrange(4,8)
    
    if boss_drop_check > boss_drops['Midnight Wolf']['Drop Rate']:
        print(boss_drops['Midnight Wolf']['Name'])
    
    loot_drop = loot(loot_amount)
    return loot_drop
    
    
def loot(loot_amount):
    
    loot_lvl = []
    loot_rare = []
    loot_pref = []
    loot_weap = []
    
    for i in range(0, loot_amount):
        
        count = 0
        
        loot_level = random.randrange(1,1000)
        loot_rarity = random.randrange(1,1000)
        loot_type = random.randrange(1,1000)
        loot_prefix = random.randrange(1,1000)
        
        
        if loot_level >= loot_levels['equal_to_player']:
            loot_lvl.append(player_level)
        elif loot_level >= loot_levels['player_level_plus_1']:
            loot_lvl.append(player_level + 1)
        elif loot_level >= loot_levels['player_level_plus_2']:
            loot_lvl.append(player_level + 2)
        elif loot_level >= loot_levels['player_level_plus_3']:
            loot_lvl.append(player_level + 3)
        else:
            print('ERROR rarity')
        
    
        if loot_prefix >= loot_prefixes['yielding']:
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
            
                
        if loot_type >= loot_weapons['short_sword']:
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
        
        
        if loot_rarity >= loot_table_rarity['Common']:
            loot_rare.append('Common')
        elif loot_rarity >= loot_table_rarity['Rare'] and loot_rarity < loot_table_rarity['Common']: 
            loot_rare.append('Rare')
        elif loot_rarity >= loot_table_rarity['Exotic'] and loot_rarity < loot_table_rarity['Rare']:
            loot_rare.append('Exotic')
        elif loot_rarity >= loot_table_rarity['Legendary']and loot_rarity < loot_table_rarity['Exotic']:
            loot_rare.append('Legendary')
        else:
            print('ERROR rarity')
            
        return(loot_lvl[i], loot_rare[i], loot_pref[i], loot_weap[i])
       
        
  
def main():

    store()
    print(weapons_list)
    
    boss_battle_1()
      
main()
            
                        