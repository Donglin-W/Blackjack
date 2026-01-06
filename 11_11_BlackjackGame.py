# -*- coding: utf-8 -*-
"""
Created on Tue Nov 11 16:28:55 2025

@author: phili
"""

import random
import time
import os

def create_deck():
    suits = ['♠', '♥', '♦', '♣']
    ranks = {'A','2','3','4','5','6','7','8','9','10','J','K',}
    deck = []
    for suit in suits:
        for rank in ranks:
            deck.append((suit, rank))
    return deck

def shuffle_deck(deck):
    random.shuffle(deck)
    return deck

def deal_card(deck):
    if len(deck) > 0:
        return deck.pop()
    return None

def card_to_string(card):
    suit, rank = card
    return f"{rank}{suit}"

def get_card_value(card):
    suit, rank = card
    if rank in ['J','Q','K']:
        return 10
    elif rank == 'A':
        return 11
    else:
        return int(rank)

def create_hand():
    return {'cards':[],'value':0,'aces':0}

def add_card_to_hand(hand,card):
    hand['cards'].append(card)
    hand['value'] += get_card_value(card)
    suit, rank = card
    if rank== 'A' :
        hand['aces'] += 1
        
def adjust_for_ace(hand):
    while hand['value']>21 and hand['aces']>0:
        hand['value'] -= 10
        hand['aces'] -=1
        
def get_hand_value(hand):
    adjust_for_ace(hand)
    return hand['value']

def hand_to_string(hand):
    cards_str = ",".join([card_to_string(card) for card in hand['cards']])
    value = get_hand_value(hand)
    return (f"{cards_str}(Worth: {value})")
card = deal_card(shuffle_deck(create_deck()))
    
def show_hands(player_hand, dealer_hand, hide_dealer=False):
    print("\n" + "-" *50)
    print(f"Your cards: {hand_to_string(player_hand)}")
    time.sleep(2)
    if hide_dealer:
        first_card = dealer_hand['cards'][0]
        print(f"Dealer's hand: {card_to_string(first_card)}, [?]")
        time.sleep(2)
    else:
        print(f"Dealer's hand: {hand_to_string(dealer_hand)}")
    print("-"*50)
    time.sleep (2)
    
def show_final_result(player_hand, dealer_hand):
    player_value = get_hand_value(player_hand)
    dealer_value = get_hand_value(dealer_hand)
    print("\n" + "-"*50)
    print("Results are:")
    print(f"Your points: {player_value}")
    print(f"Dealer's points: {player_value}")
    print("-"*50)
    if player_value>dealer_value:
        print("\nCongrtulations! You won!")
    elif player_value<dealer_value: 
        print ("\nYou lost...")
    else:
        print ("Tie!")
        return None
    
def initial_deal(deck, player_hand, dealer_hand):
    print ("\nPassing cards...")
    time.sleep(2)
    add_card_to_hand(player_hand, deal_card(deck))
    add_card_to_hand(player_hand, deal_card(deck))
    add_card_to_hand(dealer_hand, deal_card(deck))
    add_card_to_hand(dealer_hand, deal_card(deck))
    
def player_turn(deck, player_hand, dealer_hand):
    while True:
        choice = input("\nDo you want to hit(H) or stand(s)?  ").upper()
        if choice == "H":
            new_card = deal_card(deck)
            print("\nYou chose to hit, drawing a card...")
            time.sleep(2)
            print(f"\nYou got {card_to_string(new_card)}")
            time.sleep(1)
            add_card_to_hand(player_hand, new_card)
            print(f"Your hand: {hand_to_string(player_hand)}")
            time.sleep(0.5)
            if get_hand_value(player_hand)>21:
                print("\nHand busted! You lost!")
                return False
        elif choice == "S":
            print("\nYou chose to stand")
            return True
        else:
            print("\nInvalid letter, please enter H or S")
            
def dealer_turn(deck, dealer_hand):
    print("\nDealer's turn")
    time.sleep(2)
    while get_hand_value(dealer_hand)<17:
        new_card = deal_card(deck)
        print("Dealer takes a card")
        time.sleep(2)
        print(f"He got {card_to_string(new_card)}")
        time.sleep(1)
        add_card_to_hand(dealer_hand, new_card)
        print(f"Dealer's cards: {hand_to_string(dealer_hand)}")
        time.sleep (2)
    if get_hand_value(dealer_hand)>21:
        print("\nDealer's hand busted! You won!")
        return False
    return True
    
def play_game(player_name, player_data):
    #print("Welcome to Blackjack :)")
    time.sleep(1)
    check_bankruptcy(player_data)
    bet = get_bet_amount(player_data)
    print(f"\nThere are ${bet} on the line for this round!")
    time.sleep(1)
    deck = create_deck()
    shuffle_deck(deck)
    player_hand = create_hand()
    dealer_hand = create_hand()
    initial_deal(deck, player_hand, dealer_hand)
    show_hands(player_hand, dealer_hand, hide_dealer=True)
    if get_hand_value(player_hand) ==21:
        print("\nCongratulations! You got a Blackjack!")
        show_hands(player_hand, dealer_hand, hide_dealer=False)
        update_game_result(player_data, bet, True)
        return
    player_continue = player_turn(deck, player_hand, dealer_hand)
    if not player_continue:
        update_game_result(player_data, bet, False)
        return
    show_hands(player_hand, dealer_hand, hide_dealer=False)
    dealer_continue = dealer_turn(deck, dealer_hand)
    if not dealer_continue:
            update_game_result(player_data, bet, True)
            return
    result = show_final_result(player_hand, dealer_hand)
    update_game_result(player_data, bet, result)
    
def load_player_data(filename="players.txt"):
    script_dir = os.path.dirname(os.path.abspath(__file__))
    filepath = os.path.join(script_dir, filename)
    players = {}
    if not os.path.exists(filepath):
        return players
    try:
        with open(filepath, "r", encoding = "utf-8") as file:
            for line in file:
                line = line.strip()
                if line:
                    parts = line.split(",")
                    if len(parts) ==5:
                        name = parts[0]
                        money = int(parts[1])
                        total = int(parts[2])
                        wins = int(parts[3])
                        win_rate = parts[4]
                        players[name]  = {
                            'money' : money,
                            'total' : total,
                            'wins' : wins,
                            'win rate' : win_rate
                        }
    except Exception as e:
         print (f"An error occured when attempted to get info: {e}")
    return players
                
def save_player_data(players, filename="players.txt"):
    try:
        with open(filename, "w", encoding="utf-8") as file:
            for name, data in players.items():
                if data['total'] >0:
                    win_rate = (data['wins'] / data['total']) *100
                    win_rate_str = f"{win_rate:.1f}%"
                else:
                   win_rate_str = "0.0%"
                line = f"{name}, {data['money']}, {data['total']}, {data['wins']}, {win_rate_str}\n"
                file.write(line)
    except Exception as e:
        print(f"An error ocured when attempted to get info: {e}")
        
def get_or_create_player(players):
    name = input("Enter your name: ").strip()
    if name in players: 
        print(f"\n Welcome back, {name}!")
        time.sleep(1)
        print(f"Your account balance: ${players[name]['money']}")
        time.sleep(1)
        print(f"Games played: {players[name]['total']}")
        time.sleep(1)
        print(f"Wins: {players[name]['wins']}")
        time.sleep(1)
        print(f"Win percentage: {players[name]['win_rate']}")
        time.sleep(1)
    else:
        time.sleep(1)
        print(f"\nWelcome to the game {name}!")
        time.sleep(1)
        print("We opened a bank account for you with $100")
        time.sleep(1)
        players[name] = {
            'money' : 100, 
            'total': 0,
            'wins' : 0,
            'win_rate': '0.0%'
            }
    return name, players[name]
    
def check_bankruptcy(player_data):
    if player_data['money'] <=0:
        print("\n"+"="* 50)
        time.sleep(1)
        print("You lost all your money, the charity donated $10 to you")
        time.sleep(1)
        print("=" * 50)
        player_data['money'] = 10
    
def get_bet_amount(player_data):
    while True:
        print(f"\nYou currently have: ${player_data['money']}")
        try: 
            bet = int(input(f"Enter the amount you're wiling to bet (At least $10, at most ${player_data['money']}):"))
            if bet<10:
                print ("You have to bet at least $10")
            elif bet > player_data['money']:
                print(f"You can't bet more than the ${player_data['money']} you have")
            else:
                return bet
        except ValueError:
            print("Enter a valid number")
                
def update_game_result (player_data, bet, is_win):
   player_data['total'] += 1
   if is_win == True:
       player_data['wins'] += 1
       player_data['money'] += bet
       print(f"\n[+] You won ${bet}! You currently have: ${player_data['money']}")
   elif is_win == False:
       player_data['money'] -= bet
       print(f"\n[-] You lost ${bet}! You currently have: ${player_data['money']}")
   else:
       print(f"\nTie! You currently have: ${player_data['money']}")
   if player_data['total'] > 0:
       win_rate = (player_data['wins'] / player_data['total']) * 100
       player_data['win_rate'] = f"{win_rate:.1f}%"

def main():
    time.sleep(1)
    print("Welcome to Blackjack :)")
    time.sleep(1)
    players = load_player_data()
    player_name, player_data = get_or_create_player(players)
    print ("\n" + "-"*50)
    time.sleep(1)
    while True:
        play_game(player_name, player_data)
        save_player_data(players)
        print("\nPlayer data saved")
        time.sleep(1)
        players = load_player_data()
        print(f"players =>{players}")
        player_data = players[player_name]
        print ("\n" + "-"*50)
        time.sleep(1)
        play_again = input("Want to play another round? [Y/N]: ").upper()
        if play_again == "N":    
            time.sleep(1)
            print("\nBye bye!")
            return
        else:                    
            print("Invalid letter, please enter Y or N")
            
if __name__ == "__main__":
    main()