import random

COLORS = ['Red', 'Green', 'Blue', 'Yellow']
VALUES = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'Skip', 'Reverse', '+2']

def create_deck():
    deck = []
    for color in COLORS:
        for value in VALUES:
            deck.append(f"{color} {value}")
            if value != '0':
                deck.append(f"{color} {value}")
    random.shuffle(deck)
    return deck

class UnoGame:
    def __init__(self):
        self.players = []
        self.deck = create_deck()
        self.hands = {}
        self.turn = 0
        self.started = False
        self.top_card = None
        self.direction = 1  # 1 = clockwise, -1 = counterclockwise

    def add_player(self, player_id):
        if len(self.players) < 4 and player_id not in self.players:
            self.players.append(player_id)
            self.hands[player_id] = [self.deck.pop() for _ in range(7)]
            return True
        return False

    def start_game(self):
        if len(self.players) >= 2:
            self.started = True
            self.top_card = self.deck.pop()
            return True
        return False

    def get_hand(self, player_id):
        return self.hands.get(player_id, [])

    def current_player(self):
        return self.players[self.turn % len(self.players)]

    def play_card(self, player_id, card):
        if player_id != self.current_player():
            return "❌ Not your turn."
        if card not in self.hands[player_id]:
            return "❌ You don't have that card."
        top_color, top_value = self.top_card.split()
        card_color, card_value = card.split()
        if card_color == top_color or card_value == top_value:
            self.top_card = card
            self.hands[player_id].remove(card)
            if self.is_winner(player_id):
                return f"🎉 {player_id} wins the game!"
            self.turn = (self.turn + self.direction) % len(self.players)
            return f"✅ Card played. Top card is now: {self.top_card}"
        else:
            return "❌ Invalid move."

    def draw_card(self, player_id):
        if player_id != self.current_player():
            return "❌ Not your turn."
        if not self.deck:
            self.deck = create_deck()
        card = self.deck.pop()
        self.hands[player_id].append(card)
        self.turn = (self.turn + self.direction) % len(self.players)
        return f"You drew: {card}"

    def is_winner(self, player_id):
        return len(self.hands[player_id]) == 0
