CREATE TABLE images (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    name TEXT,
    author TEXT,
    path TEXT,
    datetime TEXT
);

CREATE TABLE comments (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    idimg INTEGER, 
    user TEXT,
    comment TEXT,
    datetime TEXT
);

CREATE TABLE votes (
    id INTEGER PRIMARY KEY AUTOINCREMENT, 
    idimg INTEGER, 
    ups INTEGER,
    downs INTEGER
);

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT,
    password TEXT
);