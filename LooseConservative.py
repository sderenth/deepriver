from pypokerengine.players import BasePokerPlayer
from pypokerengine.api.game import setup_config, start_poker
import random
from pypokerengine.utils.card_utils import gen_cards, estimate_hole_card_win_rate
import pandas as pd
from sqlalchemy import create_engine

class LooseConservative(BasePokerPlayer):

    def declare_action(self, valid_actions, hole_card, round_state):
        community_card = round_state['community_card']
        win_rate = estimate_hole_card_win_rate(
                nb_simulation=1000,
                nb_player=self.nb_player,
                hole_card=gen_cards(hole_card),
                community_card=gen_cards(community_card)
                )
        ex_win_rate = 1 / self.nb_player
        if (win_rate / ex_win_rate >= 1.8) and (valid_actions[2]['amount']['max'] != -1):
            action = valid_actions[2]  # fetch raise action info
            bet = int(action['amount']['min']*1.25)
        elif win_rate / ex_win_rate > 1.0:
            action = valid_actions[1]  # fetch FOLD action info
            bet = int(action['amount'])
        else:
            action = valid_actions[1]  # fetch Call action info
            bet = action['amount']
        #print("Loose Conservative: ", hole_card, "; Prob: ", win_rate)
        return action['action'], bet

    def receive_game_start_message(self, game_info):
        self.nb_player = game_info['player_num']

    def receive_round_start_message(self, round_count, hole_card, seats):
        pass

    def receive_street_start_message(self, street, round_state):
        pass

    def receive_game_update_message(self, action, round_state):
        pass

    def receive_round_result_message(self, winners, hand_info, round_state):
        pass

def setup_ai():
    return LooseConservative()