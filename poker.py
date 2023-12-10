"""
Code reference: https://github.com/Sondar4/poker-sim/blob/master/poker.py
Additional comments have been added to the code to demonstrate our understanding of how it works
Comments are based off the following reference: https://www.wikihow.com/Sample/Poker-Hands-Cheat-Sheet
"""
from random import shuffle #shuffles a list
from pdb import set_trace

"""
card_dict = {('Clubs', '2'): 0, ('Clubs', '3'): 1, ('Clubs', '4'): 2, ('Clubs', '5'): 3, ('Clubs', '6'): 4, 
             ('Clubs', '7'): 5, ('Clubs', '8'): 6, ('Clubs', '9'): 7, ('Clubs', '10'): 8, ('Clubs', 'Jack'): 9, 
             ('Clubs', 'Queen'): 10, ('Clubs', 'King'): 11, ('Clubs', 'Ace'): 12, ('Diamonds', '2'): 13, ('Diamonds', '3'): 14, 
             ('Diamonds', '4'): 15, ('Diamonds', '5'): 16, ('Diamonds', '6'): 17, ('Diamonds', '7'): 18, ('Diamonds', '8'): 19,
             ('Diamonds', '9'): 20, ('Diamonds', '10'): 21, ('Diamonds', 'Jack'): 22, ('Diamonds', 'Queen'): 23, ('Diamonds', 'King'): 24,
             ('Diamonds', 'Ace'): 25, ('Hearts', '2'): 26, ('Hearts', '3'): 27, ('Hearts', '4'): 28, ('Hearts', '5'): 29, ('Hearts', '6'): 30,
             ('Hearts', '7'): 31, ('Hearts', '8'): 32, ('Hearts', '9'): 33, ('Hearts', '10'): 34, ('Hearts', 'Jack'): 35, ('Hearts', 'Queen'): 36,
             ('Hearts', 'King'): 37, ('Hearts', 'Ace'): 38, ('Spades', '2'): 39, ('Spades', '3'): 40, ('Spades', '4'): 41, ('Spades', '5'): 42,
             ('Spades', '6'): 43, ('Spades', '7'): 44, ('Spades', '8'): 45, ('Spades', '9'): 46, ('Spades', '10'): 47, ('Spades', 'Jack'): 48,
             ('Spades', 'Queen'): 49, ('Spades', 'King'): 50, ('Spades', 'Ace'): 51}
"""

card_dict = {(0, 2): 0, (0, 3): 1, (0, 4): 2, (0, 5): 3, (0, 6): 4, (0, 7): 5, 
             (0, 8): 6, (0, 9): 7, (0, 10): 8, (0, 11): 9, (0, 12): 10, (0, 13): 11,
             (0, 14): 12, (1, 2): 13, (1, 3): 14, (1, 4): 15, (1, 5): 16, (1, 6): 17,
             (1, 7): 18, (1, 8): 19, (1, 9): 20, (1, 10): 21, (1, 11): 22, (1, 12): 23, (1, 13): 24,
             (1, 14): 25, (2, 2): 26, (2, 3): 27, (2, 4): 28, (2, 5): 29, (2, 6): 30, (2, 7): 31, (2, 8): 32,
             (2, 9): 33, (2, 10): 34, (2, 11): 35, (2, 12): 36, (2, 13): 37, (2, 14): 38, (3, 2): 39, (3, 3): 40,
             (3, 4): 41, (3, 5): 42, (3, 6): 43, (3, 7): 44, (3, 8): 45, (3, 9): 46, (3, 10): 47, (3, 11): 48,
             (3, 12): 49, (3, 13): 50, (3, 14): 51}

suits = [0,1,2,3]
ranks = [2,3,4,5,6,7,8,9,10,11,12,13,14]


def card_to_int(suit, rank):
    """
    Converts a card into an integer to store in the observation space
    :param suit: suit of a card (0->3, refer to Card class)
    :param rank: rank of a card (2->14, refer to Card class)
    :return: integer representing the unique card
    """
    rank_modified = rank - 2
    return 13 * suit + rank_modified


def int_to_card(card_int):
    """
    Converts an integer into a card to store in the observation space
    integer representing the unique card
    :param card_int: integer representing a specific card
    :return: suit of a card (0->3, refer to Card class) and rank of a card (2->14, refer to Card class)
    """
    rank_modified = card_int % 13
    rank = rank_modified + 2
    suit = (card_int - rank_modified)/13
    return suit, rank


class Card:
    """Represents a card of a standard poker deck.
    The rank is an integer from 2 to 14. It starts at 2 to be more intuitive.
    The suit is an integer from 0 to 3 as follows:
        0 -> Clubs
        1 -> Hearts
        2 -> Spades
        3 -> Diamonds
    """
    suit_names = ['Clubs', 'Diamonds', 'Hearts', 'Spades']
    rank_names = [None, None, '2', '3', '4', '5', '6', '7',
                  '8', '9', '10', 'Jack', 'Queen', 'King', 'Ace']
    
    
    

    def __init__(self, suit=0, rank=2):
        """
        Initializes a card based on a given suit and rank
        :param suit: suit of card (defaults to 0 for 'Clubs')
        :param rank: rank of card (defaults to 2)
        """
        if type(rank) != int or type(suit) != int:
            print('Card attributes must be int type')
            raise TypeError
        else:
            self.suit = suit
            self.rank = rank

    """
    def __init__(self, card_int):
        
        Initializes a card based on a given unique card int
        :param suit: suit of card (defaults to 0 for 'Clubs')
        :param rank: rank of card (defaults to 2)
        
    """
    def __str__(self):
        """
        Returns the name of the card in a universally understood format
        E.g. "2 of Clubs"
        """
        return '%s of %s' % (Card.rank_names[self.rank],
                             Card.suit_names[self.suit])

    def print_tuple(self):
        """
        Returns the card as a tuple
        :return: tuple (suit, rank)
        """
        return (self.suit, self.rank)
        #return card_dict[(self.suit, self.rank)]

    def __lt__(self, other):
        """
        Checks if the rank of the current card is less than that of another specified card
        :param other: other card
        :return: boolean whether current card is less than other card
        """
        return self.rank < other.rank


class Deck:
    """Represents a poker Deck.
    A list of cards can be given to generate the Deck.

    The Deck is a list of Cards.
    """

    def __init__(self, used_cards=[]):
        """
        Initializes a deck of cards (aka draw pile)
        :param used_cards: cards not initially in the deck (defaults to no cards)
        """
        used_pairs = [(card.suit, card.rank) for card in used_cards]
        self.cards = [Card(x, y + 2) for x in range(4) for y in range(13) if (x, y) not in used_pairs]

    def __str__(self):
        """
        Prints out all the cards in the deck as a string
        :return: string containing all the cards in the deck
        """
        res = []
        for card in self.cards:
            res.append(str(card))
        return '\n'.join(res)

    def print_list_tuple(self):
        """
        Returns the cards in the deck as a list of tuples, where each tuple has suit followed by rank
        :return: list of tuples
        """
        list_tuple = []
        for card in self.cards:
            list_tuple.insert(1, card.print_tuple())
        return list_tuple

    def print_tuple_tuple(self):
        """
        Returns the cards in the deck as a tuple of tuples, where each tuple has suit followed by rank
        :return: tuple of tuples
        """
        # tuples are immutable, so we need to know how many tuples will be in each
        num_cards = len(self.cards)
        if num_cards == 2: # if hand of agent or villain
           tuple_tuple = (self.cards[0].print_tuple, self.cards[1].print_tuple)
         #   tuple_tuple = (card_dict[self.cards[0].print_tuple()], card_dict[self.cards[1].print_tuple()])
        else: # if table
            #print(card_dict[self.cards[0].print_tuple()])
           """
            tuple_tuple = (card_dict[self.cards[0].print_tuple()], 
                           card_dict[self.cards[1].print_tuple()],
                           card_dict[self.cards[2].print_tuple()],
                           card_dict[self.cards[3].print_tuple()],
                           card_dict[self.cards[4].print_tuple()])
            
            """
           tuple_tuple = (self.cards[0].print_tuple, 
                           self.cards[1].print_tuple,
                           self.cards[2].print_tuple,
                           self.cards[3].print_tuple,
                           self.cards[4].print_tuple)
          
            
        return tuple_tuple
    
    def print_tuple_tuple_tuple(self):
        """
        Returns the cards in the deck as a tuple of tuples, where each tuple has suit followed by rank
        :return: tuple of tuples
        """
        # tuples are immutable, so we need to know how many tuples will be in each
        num_cards = len(self.cards)
        if num_cards == 2: # if hand of agent or villain
         #  tuple_tuple = (self.cards[0].print_tuple(), self.cards[1].print_tuple())
            tuple_tuple = (card_dict[self.cards[0].print_tuple()], card_dict[self.cards[1].print_tuple()])
        else: # if table
            #print(card_dict[self.cards[0].print_tuple()])
           
            tuple_tuple = (card_dict[self.cards[0].print_tuple()], 
                           card_dict[self.cards[1].print_tuple()],
                           card_dict[self.cards[2].print_tuple()],
                           card_dict[self.cards[3].print_tuple()],
                           card_dict[self.cards[4].print_tuple()])
            
            
          
            
        return tuple_tuple

    def shuffle(self):
        """
        Shuffles all the cards in the deck
        """
        shuffle(self.cards)

    def pop_card(self):
        """
        Pops/takes a card from the deck
        :return: popped card
        """
        return self.cards.pop()

    def add_card(self, card):
        """
        Adds a card to the deck
        :param card: added card to the deck
        """
        self.cards.append(card)

    def move_cards(self, hand, num):
        """
        Moves specified number of cards from the top of the deck into a hand or table
        :param hand: player or table that takes the cards from the deck
        :param num: number of cards taken from the deck
        """
        for i in range(num):
            hand.add_card(self.pop_card())


class Hand(Deck):
    """Represents a hand of playing cards.

    This can be of a player or of the table
    """

    def __init__(self, label=''):
        """
        Initializes a hand's name (player or table)
        :param label: player or table (defaults to empty string)
        """
        self.cards = []
        self.label = label

    def all_cards(self, table):
        """Returns a sorted tuple of the cards of the hand and the table.

        The tuple is sorted by rank and if ranks are equal by suit.
        """
        return tuple(sorted(self.cards + table.cards, key=lambda card: (card.rank, card.suit)))

    def best_hand(self, table):
        """Returns a tuple with the best hand that can be built with the cards
        in the hand and the table.
        [The best hands are in order from greatest to least value]

        output: int, str, tuple
        [score of hand, name of hand, and the highest card of hand]
        """
        cards = self.all_cards(table) # combines cards from player's hand with the table's cards as a sorted tuple

        test = is_straight_flush(cards) # checks for a straight flush
        if test[0]:
            return 8, 'straight flush', test[1]

        test = is_four(cards) # checks for a four of a kind
        if test[0]:
            return 7, 'four of a kind', test[1]

        test = is_full_house(cards) # checks for a full house
        if test[0]:
            return 6, 'full house', test[1]

        test = is_flush(cards) # checks for a flush
        if test[0]:
            return 5, 'flush', test[1]

        test = is_straight(cards) # checks for a straight
        if test[0]:
            return 4, 'straight', test[1]

        test = is_three(cards) # checks for a three of a kind
        if test[0]:
            return 3, 'three of a kind', test[1]

        test = is_two_pair(cards) # checks for a two pair
        if test[0]:
            return 2, 'two pair', test[1]

        test = is_pair(cards) # checks for a pair
        if test[0]:
            return 1, 'pair', test[1]

        return 0, 'highest card', is_highest_card(cards)[1] # if no hand better than a Pair, defaults to a high card


def is_straight_flush(cards):
    """Returns a boolean and a tuple with the cards that make the straight flush.

    straight flush: contains five cards in sequence, all of the same suit.
    """
    straight_flush = False
    counter = 0
    for i in range(len(cards) - 1):
        if cards[i].rank + 1 == cards[i + 1].rank and cards[i].suit == cards[i + 1].suit:
            counter += 1
        else:
            counter = 0
        if counter > 3: # checks for at least four comparisons for at least five sequential cards
            straight_flush = True
            j = i + 1
    if straight_flush:
        return True, tuple((cards[j - i] for i in range(5)))  # Returns the highest card first
    return False, 0


def is_four(cards):
    """Returns a boolean and a tuple with the cards that make the four of a kind.

    four of a kind: contains four cards of one rank and an unmatched card of another rank
    """
    four = False
    ranks = tuple((card.rank for card in cards))
    counter = 0
    for i in range(len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            counter += 1
        else:
            counter = 0
        if counter > 2: # checks for at least three comparisons for at least four sequential cards
            four = True
            j = i + 1
    if four:
        four1 = tuple((cards[j - i] for i in range(4)))
        unused_cards = [card for card in cards if card not in four1]
        return True, four1 + (unused_cards[-1],)
    return False, 0


def is_full_house(cards):
    """Returns a boolean and a tuple with the cards that make the full house.

    full house: contains three matching cards of one rank and two matching cards of another rank
    """
    pair = False
    three = False
    ranks = tuple((card.rank for card in cards))
    i = 0
    while i < (len(cards) - 1):
        if ranks[i] == ranks[i + 1]:
            if i < (len(cards) - 2):
                if ranks[i + 1] == ranks[i + 2]: # three matching cards in one rank
                    three = True
                    j = i + 2
                    i += 2
            else: # two matching cards of another rank
                pair = True
                k = i + 1
                i += 1
        i += 1
    if pair and three:
        pair1 = tuple((cards[k - i] for i in range(2)))
        three1 = tuple((cards[j - i] for i in range(3)))
        return True, pair1 + three1
    return False, 0


def is_flush(cards):
    """Returns a boolean and a tuple with the cards that make the flush.

    flush: contains five cards of the same suit, not in rank or sequence
    """
    flush = False
    suits_counter = [0, 0, 0, 0]  # 0: Clubs, 1: Hearts, 2: Spades, 3: Diamonds
    for card in cards:
        suits_counter[card.suit] += 1
    for i in range(4):
        if suits_counter[i] > 4:
            flush = True
            flush_suit = i
    # If there's a flush let's get the best hand
    if flush == True:
        suit_ordered_cards = tuple(sorted(cards, key=lambda card: (card.suit, card.rank)))
        for i in range(len(cards)):
            if suit_ordered_cards[-i - 1].suit == flush_suit:
                return True, tuple((suit_ordered_cards[-i - 1 - j] for j in range(5)))
    return False, 0


def is_straight(cards):
    """Returns a boolean and a tuple with the cards that make the straight.

    straight: contains five cards of sequential rank but in more than one suit
    """
    straight = False
    counter = 0
    for i in range(len(cards) - 1):
        if cards[i].rank + 1 == cards[i + 1].rank:
            counter += 1
        else:
            counter = 0
        if counter > 3: # four comparisons to compare five sequential cards
            straight = True
            j = i + 1
    if straight:
        return True, tuple((cards[j - i] for i in range(5)))
    return False, 0


def is_three(cards):
    """Returns a boolean and a tuple with the cards that make the three of a kind.

    three of a kind: three cards of three same rank, plus two unmatched cards
    """
    three = False
    ranks = tuple((card.rank for card in cards))
    counter = 0
    for i in range(len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            counter += 1
        else:
            counter = 0
        if counter > 1:
            three = True
            j = i + 1
    if three:
        three1 = tuple((cards[j - i] for i in range(3)))
        unused_cards = [card for card in cards if card not in three1]
        return True, three1 + (unused_cards[-1], unused_cards[-2])
    return False, 0


def is_two_pair(cards):
    """Returns a boolean and a tuple with the cards that make the two pairs.

    two pairs: two cards of the same rank, plus two cards of another rank (that match each other,
    but not the same pair), plus one unmatched card
    """
    pair_counter = 0
    ranks = tuple((card.rank for card in cards))
    j = list()
    i = 0
    while i < (len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            pair_counter += 1
            j.append(i + 1)
            i += 1
        i += 1
    if pair_counter > 1:
        pair1 = tuple((cards[j[-1] - i] for i in range(2)))
        pair2 = tuple((cards[j[-2] - i] for i in range(2)))
        unused_cards = [card for card in cards if card not in pair1 + pair2]
        return True, pair1 + pair2 + (unused_cards[-1],)
    return False, 0


def is_pair(cards):
    """Returns a boolean and a tuple with the cards that make the pair.

    pair: two cards of the same rank, plus three other unmatched cards
    """
    pair = False
    ranks = tuple((card.rank for card in cards))
    i = 0
    while i < (len(ranks) - 1):
        if ranks[i] == ranks[i + 1]:
            pair = True
            j = i + 1
            i += 1
        i += 1
    if pair:
        pair1 = tuple((cards[j - i] for i in range(2)))
        unused_cards = [card for card in cards if card not in pair1]
        return True, pair1 + (unused_cards[-1], unused_cards[-2], unused_cards[-3])
    return False, 0


def is_highest_card(cards):
    """Returns the hand with the highest cards.

    high card: no two cards have the same rank, the five cards are not in sequence, and the five cards are not
    all the same suit
    """
    return True, tuple((cards[-i - 1] for i in range(5)))


def rate(result, name, cards):
    """Gives a score to a 5 cards hand. The score is a vector of 6 dimensions.
    The input of the function must be the output of the best_hand method.

    The function should be called something like this: score = rate(*player.best_hand(table))

    Jennifer: All the cards will be considered to determine a winner and prevent a tie from happening.
    However, since we just need to find out the highest card value of whatever hand is being played and we don't mind
    ties for our implementation, we only care about the value of the highest card type, aka cards[0]
    """
    score = [result, 0, 0, 0, 0, 0]
    # The other 5 dimensions depend on the kind of hand.
    # Straight flush
    if score[0] == 8:
        score[1] = cards[0].rank
    # Four of a kind
    elif score[0] == 7:
        score[1] = cards[0].rank
        score[2] = cards[-1].rank
    # Full house
    elif score[0] == 6:
        score[1] = cards[-1].rank
        score[2] = cards[0].rank
    # Flush
    elif score[0] == 5:
        for i in range(5):
            score[i + 1] = cards[i].rank
    # Straight
    elif score[0] == 4:
        score[1] = cards[0].rank
    # Three of a kind
    elif score[0] == 3:
        score[1] = cards[0].rank
        score[2] = cards[-2].rank
        score[3] = cards[-1].rank
    # Two pair
    elif score[0] == 2:
        score[1] = max(cards[0].rank, cards[2].rank)
        score[2] = min(cards[0].rank, cards[2].rank)
        score[3] = cards[-1].rank
    # Pair
    elif score[0] == 1:
        score[1] = cards[0].rank
        for i in range(3):
            score[i + 2] = cards[i + 2].rank
    # Highest card
    else:
        for i in range(5):
            score[i + 1] = cards[i].rank

    return tuple(score)


if __name__ == '__main__': # not quite sure what this does
    set_trace()

