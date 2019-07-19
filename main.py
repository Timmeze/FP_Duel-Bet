import waitress
from flask import Flask, render_template, request
from db import update_user_db, update_pari_db, add_user_db, drop_user_db, add_pari_db
from classes import User, Pari, User_list, Pari_list
import os

DATABASE_URL = 'db.sqlite'

pari_list = Pari_list()
user_list = User_list()

user_1 = User('Mark','0000_0000_0000_0001')
user_2 = User('Petya', '0000_0000_0000_0002')

user_1.change_balance(100)
user_2.change_balance(200)

user_list.add_to_user_list(item=user_1)
user_list.add_to_user_list(item=user_2)


pari_1 = Pari('Пари 1', user_1, 50)
pari_list.add_to_pari_list(pari_1)
user_1.change_balance(-50)


add_user_db(DATABASE_URL, user_1)
add_user_db(DATABASE_URL, user_2)
add_pari_db(DATABASE_URL, pari_1)


def start():

    app = Flask(__name__)


    @app.route('/', methods=['POST', 'GET'])
    def index():
        show = pari_list.show()
        return render_template('ind.html', show=show)


    @app.route('/<pari_id>', methods=['POST', 'GET'])
    def pari_view(pari_id):
        pari = pari_list.search_pari_by_id(pari_id)
        return render_template('pari.html', pari=pari)


    @app.route('/<pari_id>/add_like', methods=['POST', 'GET'])
    def add_like(pari_id):
        pari = pari_list.search_pari_by_id(pari_id)
        pari.likes =+ 1
        update_pari_db(DATABASE_URL, pari)
        return render_template('pari.html', pari=pari)


    @app.route('/<pari_id>/join_to_pari', methods=['POST', 'GET'])
    def join_to_pari(pari_id):
        if request.method == 'GET':
            pari = pari_list.search_pari_by_id(pari_id)
            return render_template('join_to_pari.html', pari=pari)
        if request.method == 'POST':
            pari = pari_list.search_pari_by_id(pari_id)
            name = request.form['name']
            bet = int(request.form['bet'])
            side = request.form['side']
            user = user_list.search_by_name(name)
            if user == None:
                warning = "Некорректное имя"
                return render_template('join_to_pari.html', pari=pari, warning=warning)

            if bet<=0 or bet > user.balance:
                warning = "Введена некорректная сумма"
                return render_template('join_to_pari.html', pari=pari, warning=warning)

            if side == '1':
                pari.duel_rivals_name_1.append(user.name)
                pari.duel_sum_pers_1 = {name:bet}
                pari.duel_sum_1 += bet
                user.change_balance(-bet)
                update_pari_db(DATABASE_URL, pari)
                return render_template('pari.html', pari=pari)

            if side == '2':
                pari.duel_rivals_name_2.append(user.name)
                pari.duel_sum_pers_2 = {name:bet}
                pari.duel_sum_2 += bet
                user.change_balance(-bet)
                update_pari_db(DATABASE_URL, pari)
                return render_template('pari.html', pari=pari)



    @app.route('/create_pari', methods=['POST', 'GET'])
    def create_pari():
        if request.method == 'GET':
            return render_template('pariadd.html')

        if request.method == 'POST':
            title = request.form['title']
            author = request.form['author']
            bet = int(request.form['bet'])
            pruf = user_list.search_by_name(author)
            if pruf == None:
                warning = "Некорректное имя пользователя"
                return render_template('pariadd.html', warning = warning)
            if bet <=0 or bet > pruf.balance:
                warning = "Некорректная сумма ставки"
                return render_template('pariadd.html', warning=warning)
            else:
                pari = Pari(str(title), pruf, bet)
                pari_list.add_to_pari_list(pari)
                add_pari_db(DATABASE_URL, pari)
                return render_template('pari.html', pari=pari)


    @app.route('/<pari_id>/result', methods=['POST', 'GET'])
    def pari_result(pari_id):
        pari = pari_list.search_pari_by_id(pari_id)
        print(pari.duel_rivals_name_1)
        winner_side = request.form['winner']
        if winner_side == '1':
            pari.pari_payment(1, user_list)# not pr
            pari.pari_result(1,user_list)#not pr
            for name in pari.duel_rivals_name_1:
                user = user_list.search_by_name(name)
                update_user_db(DATABASE_URL, user)

            for name in pari.duel_rivals_name_2:
                user = user_list.search_by_name(name)
                update_user_db(DATABASE_URL, user)

            pari = pari_list.search_pari_by_id(pari_id)
            update_pari_db(DATABASE_URL,pari)
            return render_template('pari.html', pari=pari)

        if winner_side == '2':
            pari.pari_payment(2, user_list)# not pr
            pari.pari_result(2,user_list)# not pr
            for name in pari.duel_rivals_name_2:
                user = user_list.search_by_name(name)
                update_user_db(DATABASE_URL, user)
            for name in pari.duel_rivals_name_1:
                user = user_list.search_by_name(name)
                update_user_db(DATABASE_URL, user)

        # update_pari_db(DATABASE_URL, pari, pari)

            pari = pari_list.search_pari_by_id(pari_id)
            update_pari_db(DATABASE_URL,pari)
            return render_template('pari.html', pari=pari)



    @app.route('/userlist')
    def user_view():
        user_list_1 = user_list.items
        return render_template('userlist.html', user_list=user_list_1)


    @app.route('/userlist/<user_id>/delete', methods=['POST'])
    def delete_user(user_id):
        user_list.del_user(user_id)
        user_list_1 = user_list.items
        drop_user_db(DATABASE_URL, user_id)
        return render_template('userlist.html', user_list=user_list_1)


    @app.route('/userlist/create_user', methods=['GET', 'POST'])
    def create_user():
        if request.method == 'GET':
            return render_template('user_new.html')
        if request.method == 'POST':
            name = request.form['name']
            card_number = request.form['card_number']
            name_pruf = user_list.search_by_name(name)
            if name_pruf != None:
                warning = "Логин уже существует, предложите другой"
                return render_template('user_new.html', warning=warning)
            new_user = User(name=name, card_number=card_number)
            user_list.add_to_user_list(new_user)
            add_user_db(DATABASE_URL, new_user)
            return render_template('userlist.html', user_list=user_list.items)



    @app.route('/userlist/<user_id>/change_balance', methods=['POST', 'GET'])
    def add_balance(user_id):
        if request.method == 'GET':
            user = user_list.search_by_id(user_id)
            return render_template('add_balance.html', user=user)
        if request.method == 'POST':
            user = user_list.search_by_id(user_id)
            sum_in = int(request.form['sum_in'])
            user_list_1 = user_list.items
            user.change_balance(sum_in)
            update_user_db(DATABASE_URL, user)
            return render_template('userlist.html', user_list=user_list_1)

    if os.getenv('APP_ENV') == 'PROD' and os.getenv('PORT'):
        waitress.serve(app, port=os.getenv('PORT'))
    else:
        app.run(port=9876, debug=True)


if __name__ == '__main__':
    start()
