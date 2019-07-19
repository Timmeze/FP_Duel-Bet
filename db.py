import sqlite3
from classes import User, Pari

def open_db(db_url):
    db = sqlite3.connect(db_url)
    db.row_factory = sqlite3.Row
    return db

def add_user_db(db_url, user):
    db = open_db(db_url)
    cards = '|'.join(user.cards)
    updated_container = db.cursor().execute('insert into users values (:id, :name, :balance, :win_duel, :loss_duel, :win_money, :loss_money, :cards)',
    {'id': user.id, 'name': user.name, 'balance': user.balance, 'win_duel': user.win_duel, 'loss_duel': user.loss_duel,'win_money': user.win_money, 'loss_money': user.loss_money, 'cards':cards})
    db.commit()
    db.close()
    return updated_container


def update_user_db(db_url, user):
    db = open_db(db_url)
    cards = '|'.join(user.cards)
    updated_container = db.cursor().execute('update users set id = :id, name = :name, balance = :balance, win_duel = :win_duel, loss_duel = :loss_duel, win_money = :win_money, loss_money = :loss_money, cards = :cards where id = :id',
                                            {'id': user.id, 'name': user.name, 'balance': user.balance, 'win_duel': user.win_duel, 'loss_duel': user.loss_duel,
                                            'win_money': user.win_money, 'loss_money': user.loss_money, 'cards': cards})
    db.commit()
    db.close()
    return updated_container


def drop_user_db(db_url, user_id):
    db = open_db(db_url)
    updated_container = db.cursor().execute('delete from users where id = :id', {'id': user_id})
    db.commit()
    db.close()
    return updated_container



def add_pari_db(db_url, pari):
    db = open_db(db_url)
    duel_rivals_name_1 = '|'.join(pari.duel_rivals_name_1)
    duel_rivals_name_2 = '|'.join(pari.duel_rivals_name_2)
    duel_winners = '|'.join(pari.duel_winners)
    duel_loosers = '|'.join(pari.duel_loosers)
    duel_sum_pers_1 = str(pari.duel_sum_pers_1)
    duel_sum_pers_2 = str (pari.duel_sum_pers_2)

    updated_container = db.cursor().execute('insert into pari values (:id, :name, :author_id, :author_name, :duel_rivals_name_1, :duel_sum_pers_1, '
                        ':duel_rivals_name_2, :duel_sum_pers_2, :duel_sum_1, :duel_sum_2, :duel_winners, :duel_loosers, :likes )',
        {'id': pari.id, 'author_name': pari.author_name, 'name': pari.name, 'author_id': pari.author_id, 'duel_rivals_name_1': duel_rivals_name_1,
         'duel_sum_pers_1': duel_sum_pers_1, 'duel_rivals_name_2': duel_rivals_name_2, 'duel_sum_pers_2': duel_sum_pers_2,
         'duel_sum_1': pari.duel_sum_1, 'duel_sum_2': pari.duel_sum_2, 'duel_winners': duel_winners,'duel_loosers': duel_loosers, 'likes': pari.likes})
    db.commit()
    db.close()
    return updated_container


def update_pari_db(db_url, pari):
    db = open_db(db_url)
    duel_rivals_name_1 = '|'.join(pari.duel_rivals_name_1)
    duel_rivals_name_2 = '|'.join(pari.duel_rivals_name_2)
    duel_winners = '|'.join(pari.duel_winners)
    duel_loosers = '|'.join(pari.duel_loosers)
    duel_sum_pers_1 = str(pari.duel_sum_pers_1)
    duel_sum_pers_2 = str(pari.duel_sum_pers_2)
    updated_container = db.cursor().execute('update pari set id = :id, name = :name, author_id = :author_id, author_name = :author_name, duel_rivals_name_1 = :duel_rivals_name_1, duel_sum_pers_1 = :duel_rivals_name_1, duel_rivals_name_2 = :duel_rivals_name_2, duel_sum_pers_2 = :duel_sum_pers_2, duel_sum_1 = :duel_sum_1, duel_sum_2 = :duel_sum_2, duel_winners = :duel_winners, duel_loosers = :duel_loosers, likes = :likes where id = :id',
                                            {'id': pari.id, 'author_name': pari.author_name, 'name': pari.name,
                                             'author_id': pari.author_id, 'duel_rivals_name_1': duel_rivals_name_1,
                                             'duel_sum_pers_1': duel_sum_pers_1,
                                             'duel_rivals_name_2': duel_rivals_name_2,
                                             'duel_sum_pers_2': duel_sum_pers_2,
                                             'duel_sum_1': pari.duel_sum_1, 'duel_sum_2': pari.duel_sum_2,
                                             'duel_winners': duel_winners, 'duel_loosers': duel_loosers, 'likes': pari.likes,
                                             })
    db.commit()
    db.close()
    return updated_container


def get_pari(db_url, container, page=1):
    db = open_db(db_url)
    limit = 10
    offset = limit * (page - 1)
    notes = db.cursor().execute('select name, id from container limit :limit offset :offset',
                        {'limit': limit, 'offset': offset, 'container':container}).fetchall()
    db.commit()
    db.close()
    return notes


