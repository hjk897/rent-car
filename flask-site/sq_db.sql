PRAGMA foreign_keys = ON;

CREATE TABLE IF NOT EXISTS mainmenu (
id integer PRIMARY KEY AUTOINCREMENT, 
title text NOT NULL, 
url text NOT NULL
);

CREATE TABLE IF NOT EXISTS users (
uid integer PRIMARY KEY AUTOINCREMENT,
name text NOT NULL,
contact text NOT NULL,
email text NOT NULL,
psw text NOT NULL,
time integer NOT NULL
);

CREATE TABLE IF NOT EXISTS cars (
carid integer PRIMARY KEY AUTOINCREMENT,
carname text NOT NULL,
platenumber text NOT NULL,
power text NOT NULL,
picture BLOB DEFAULT NULL,
price integer NOT NULL,
status integer NOT NULL
);

CREATE TABLE IF NOT EXISTS rent(
carid integer,
uid integer,
days integer NOT NULL,
FOREIGN KEY (carid) REFERENCES cars(carid),
FOREIGN KEY (uid) REFERENCES users(uid)     
);

CREATE TABLE IF NOT EXISTS usersandcars(
    uid integer,
    carid integer,
    FOREIGN KEY (uid) REFERENCES users(uid),
    FOREIGN KEY (carid) REFERENCES cars(carid)

);

CREATE TABLE IF NOT EXISTS contact(
    name text NOT NULL,
    email text NOT NULL,
    message text NOT NULL
);