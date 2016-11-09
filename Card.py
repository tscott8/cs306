import random


class Card(object):
    suit_names = ["club", "Diamond", "Spade", "Heart"]
    rank_names = [None, "Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]

    def __init__(self, suit=int(random.random()), value=int(random.random())):
        self.suit = suit % 4
        self.rank = value % 13 + 1

    def __str__(self):
        return '%s of %s' % (Card.rank_names[self.rank], Card.suit_names[self.suit])

    def __repr__(self):
        return self.__str__()

    def __gt__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 > t2

    def __lt__(self, other):
        t1 = self.suit, self.rank
        t2 = other.suit, other.rank
        return t1 < t2


class Deck(object):
    def __init__(self):
        self.cards = []
        for suit in range(4):
            for rank in range(1, 14):
                card = Card(suit, rank)
                self.cards.append(card)

    def get_cards(self):
        return self.cards

    def shuffle(self):
        random.shuffle(self.cards)

    def reverse(self):
        reversed(self.cards)
