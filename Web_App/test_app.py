# test_app.py

import pytest
import requests
import filecmp
import json
import sqlite3 as sql
from subprocess import PIPE
from subprocess import Popen

def test_main():
    assert requests.get('http://127.0.0.1:10007').status_code == 200

    # UPLOAD
    payload = {'myFile': ('ua.png', open('./images/ua.png','rb')), 'myName': (None, 'name0'), 'myAuthor': (None, 'name30')}
    assert requests.post('http://127.0.0.1:10007/upload', files=payload).status_code == 200
    db = sql.connect('database.db')
    mainrow = db.execute("SELECT * FROM images ORDER BY id DESC LIMIT 1").fetchone()
    assert mainrow[1:3] == ('name0', 'name30')
    assert filecmp.cmp(mainrow[3], './images/ua.png', shallow=True) == True

    # LIST
    params = {'id': (None, mainrow[2])}
    response = requests.get('http://127.0.0.1:10007/list', params=params).json()
    result0 = [{"id": mainrow[0], "name": mainrow[1], "author": mainrow[2], "path": mainrow[3], "datetime": mainrow[4]}]
    assert response == {"images": result0}

    # COMMENTS
    requests.post('http://127.0.0.1:10007/newcomment', params={'idimag': (None, mainrow[0]), 'username': (None, 'Pessoa0'), 'newcomment': (None, 'hahahaha')})
    requests.post('http://127.0.0.1:10007/onload_votes', params={'idimag': (None, mainrow[0])})
    requests.post('http://127.0.0.1:10007/upvote', params={'idimag': (None, mainrow[0])})
    requests.post('http://127.0.0.1:10007/downvote', params={'idimag': (None, mainrow[0])})
    row0 = db.execute("SELECT * FROM comments WHERE idimg = ?", (mainrow[0],)).fetchall()
    row1 = db.execute("SELECT * FROM votes WHERE idimg = ?", (mainrow[0],)).fetchall()
    response = requests.get('http://127.0.0.1:10007/comments', params={'idimg': (None, mainrow[0])}).json()
    result1 = [{"user": row0[0][2], "comment": row0[0][3], "datetime": row0[0][4]}]
    result2 = [{"thumbs_up": row1[0][2], "thumbs_down": row1[0][3]}]

    assert response == {"image": result0[0], "comments": result1, "votes": result2[0]}

    db.execute("DELETE FROM images WHERE id = ?", (mainrow[0],))