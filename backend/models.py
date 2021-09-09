from otree.api import (
    models,
    widgets,
    BaseConstants,
    BaseSubsession,
    BaseGroup,
    BasePlayer,
    Currency as c,
    currency_range,
)
import numpy as np
import random
import json
from pprint import pprint

author = 'Your name here'

doc = """
Your app description
"""


class Constants(BaseConstants):
    name_in_url = 'backend'
    players_per_group = None
    num_rounds = 10
    trading_day_min = 3
    freq = 6
    length = int(trading_day_min * 240 / 6)
    hetto = 1
    dt = 1

    S = 76.3  # current stock price
    T = 1  # time to maturity
    lam = 1  # intensity of jump i.e. number of jumps per annum
    steps = 10  # time steps
    Npaths = 10  # number of paths to simulate
    sigma = 0.18  # annaul standard deviation , for weiner process
    m = -sigma  # meean of jump size
    r = 0.05 + sigma  # risk free rate
    v = sigma / 10  # standard deviation of jump


class Subsession(BaseSubsession):
    pass


class Group(BaseGroup):
    pass


class Player(BasePlayer):
    income = models.FloatField(min=3, max=25)
    volatility = models.FloatField(min=1, max=50)
    drawdown = models.FloatField(min=2, max=4)
    data = models.LongStringField()
    current_position = models.IntegerField(initial=1)

    def merton_jump_paths(self):
        size = (Constants.steps, Constants.Npaths)
        dt = Constants.T / Constants.steps
        poi_rv = np.multiply(np.random.poisson(Constants.lam * dt, size=size),
                             np.random.normal(self.income, self.volatility, size=size)).cumsum(axis=0)
        geo = np.cumsum(((self.income - self.volatility ** 2 / 2 - Constants.lam * (
                self.income - self.volatility ** 2 * 0.5)) * dt + \
                         Constants.sigma * np.sqrt(dt) * \
                         np.random.normal(size=size)), axis=0)

        return np.round_(np.exp(geo + poi_rv) * Constants.S, 3).tolist()

    def generate_data(self):
        data = self.merton_jump_paths()
        self.data = json.dumps(data)

    def get_data(self):
        return json.loads(self.data)
