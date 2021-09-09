from otree.api import Currency as c, currency_range
from ._builtin import Page, WaitPage
from .models import Constants
import json

class Decision(Page):
    form_model = 'player'
    form_fields = ['income', 'volatility', 'drawdown']

    def before_next_page(self):
        self.player.generate_data()



class Trade(Page):
    pass


page_sequence = [
    Decision,
    Trade
]
