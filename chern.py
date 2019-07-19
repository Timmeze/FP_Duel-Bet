@app.route('/<pari_id>/result', methods=['POST', 'GET'])
def pari_result(pari_id):
    pari = pari_list.search_pari_by_id(pari_id)
    winner_side = request.form['winner']
    if winner_side == 1:
        pari.pari_payment(1, user_list)
        pari.pari_result(1)
        for name in pari.duel_rivals_name_1:
            pari.duel_winners.append(name)
            print(pari.duel_winners)
            user = user_list.search_by_name(name)
            update_user_db(DATABASE_URL, 'users', user)
        for name in pari.duel_rivals_name_2:
            pari.duel_loosers.append(name)
            user = user_list.search_by_name(name)
            # update_user_db(DATABASE_URL, 'users', user)

            pari = pari_list.search_pari_by_id(pari_id)
            return render_template('pari.html', pari=pari)

    if winner_side == 2:
        pari.pari_payment(2, user_list)
        pari.pari_result(2)
        for name in pari.duel_rivals_name_2:
            pari.duel_winners.append(name)
            user = user_list.search_by_name(name)
            # update_user_db(DATABASE_URL, 'users', user)
        for name in pari.duel_rivals_name_1:
            pari.duel_loosers.append(name)
            user = user_list.search_by_name(name)
            # update_user_db(DATABASE_URL, 'users', user)

    # update_pari_db(DATABASE_URL, pari, pari)

    pari = pari_list.search_pari_by_id(pari_id)
    return render_template('pari.html', pari=pari)
