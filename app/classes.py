import uuid

class User:
    def __init__(self, name, card_number, balance=0, total_duel=0, win_duel=0, loss_duel=0, win_money=0, loss_money=0):
        self.id = str(uuid.uuid4())
        self.name = name
        self.balance = balance
        self.total_duel = total_duel
        self.win_duel = win_duel
        self.loss_duel = loss_duel
        self.win_money = win_money
        self.loss_money = loss_money
        self.cards = []
        self.cards.append(card_number)

    def add_card(self, card_number):
        return self.cards.append(card_number)

    def change_balance(self, payment):
        self.balance += int(payment)
        return self.balance

    def change_history(self, duel_win=0, duel_loss=0): #в каждом конкретном случае будет один исход, чтобы явно не указывать второй, значение
                                                            #по умолчанию указано 0
        self.total_duel += 1
        self.loss_duel += duel_loss
        self.win_duel += duel_win

    def withdrawal(self, card_number, payment):
        if card_number in self.cards and 0 < payment <= self.balance:
            self.balance -= payment
            return self.balance
        if card_number not in self.cards:
            return print('Некооректный номер карты')
        if payment > self.balance or payment <= 0:
            return print('Некорректная сумма выплаты')

class User_list:
    def __init__(self):
        self.items = []

    def add_to_user_list(self, item):
        return self.items.append(item)

    def search_user_by_id(self, id):
        for item in self.items:
            if item.id == id:
                searched_user = item
                return searched_user

    def search_by_name(self, name):
        for item in self.items:
            if item.name == name:
                searched_user = item
                return searched_user


    def search_by_id(self, id):
        for user in self.items:
            if user.id == id:
                searched_user = user
                return searched_user


    def del_user(self, id):
        user_to_del = self.search_by_id(id)
        self.items.remove(user_to_del)
        return self.items

class Pari:
    def __init__(self, title, user, bet):
        self.id = str(uuid.uuid4())
        self.name = title
        self.author_id = user.id
        self.author_name = user.name
        self.duel_rivals_name_1 = []
        self.duel_rivals_name_1.append(user.name)
        self.duel_sum_pers_1 = {user.name:bet}
        self.duel_rivals_name_2 = []
        self.duel_sum_pers_2 = {}
        if 0 < bet <= 1_000_000 and bet <= user.balance:#лимит суммы ставок
            self.duel_sum_1 = bet
        else:
            print ('Некорректная сумма ставки')
        self.duel_sum_2 = 0
        self.duel_winners = []
        self.duel_loosers = []
        self.likes = 0

    def add_rival_duel(self, User, rival_number, bet):
        if rival_number == 1:
            if 0 < bet <= 1_000_000 and bet >= User.balance:
                self.duel_sum_1 += bet
                User.change_balance(-bet)
                self.duel_sum_pers_1[User.id] = bet
                self.duel_rivals_name_1.append(User.name)
            else:
                print('Некорректная сумма ставки')
        if rival_number == 2:
            self.duel_sum_1 += bet
            User.change_balance(-bet)
            self.duel_sum_pers_2[User.id] = bet
            self.duel_rivals_name_2.append(User.name)
        else:
            print('Некорректная сумма ставки')

    def pari_result(self, winner_number, user_list):
        if winner_number == 1:
            for user_name in self.duel_rivals_name_1:
                self.duel_winners.append(user_name)
                user_w = user_list.search_by_name(user_name)
                user_w.change_history(duel_win=1)
            for user_name in self.duel_rivals_name_2:
                self.duel_loosers.append(user_name)
                user_l = user_list.search_by_name(user_name)
                user_l.change_history(duel_loss=1)
        if winner_number == 2:
            for user_name in self.duel_rivals_name_2:
                self.duel_winners.append(user_name)
                user_w = user_list.search_by_name(user_name)
                user_w.change_history(duel_win=1)
            for user_name in self.duel_rivals_name_1:
                self.duel_loosers.append(user_name)
                user_l = user_list.search_by_name(user_name)
                user_l.change_history(duel_loss=1)

    def pari_payment(self, win_number, user_list):
        pot_duel = self.duel_sum_1 + self.duel_sum_2
        if win_number == 1:
            for name in self.duel_sum_pers_1.keys():
                winner = user_list.search_by_name(name)
                pot_percent = int(self.duel_sum_pers_1.get(name))/self.duel_sum_1 * pot_duel
                winner.balance += int(pot_percent)

        if win_number == 2:
            for name in self.duel_sum_pers_2.keys():
                winner = user_list.search_by_name(name)
                pot_percent = int(self.duel_sum_pers_2.get(name))/self.duel_sum_2 * pot_duel
                winner.balance += int(pot_percent)


    def add_like(self, like):
        self.likes += like

class Pari_list:
    def __init__(self):
        self.items = []

    def add_to_pari_list(self, Pari):
        return self.items.append(Pari)

    def show(self):
        show_list = []
        for item in self.items:
            show_list.append({'id':item.id, 'name':item.name})
        return show_list

    def search_pari_by_id(self, id):
        for pari in self.items:
            if pari.id == id:
                searched_pari = pari
                return searched_pari






