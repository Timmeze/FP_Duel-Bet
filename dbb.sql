create table users (
    id text not null unique ,
    name text not null ,
    balance integer not null,
    win_duel integer not null check ( win_duel >= 0 ),
    loss_duel integer not null check (loss_duel >= 0),
    win_money integer,
    loss_money integer,
    cards text
);

create table pari (
    id text primary key not null,
    name text not null ,
    author_id text references users,
    author_name text references users,
    duel_rivals_name_1 text,
    duel_sum_pers_1 text,
    duel_sum_1 integer,
    duel_rivals_name_2 text,
    duel_sum_pers_2 text,
    duel_sum_2 integer,
    duel_winners text,
    duel_loosers text,
    likes integer
);

drop table users;

drop table pari;

