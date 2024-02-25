# encoding=utf-8
#
# To run: python3 app.py

import os.path
import cherrypy
import json
import hashlib
import sqlite3 as sql
import time
import processo

cherrypy.config.update({"server.socket_port": 10007,})

# The absolute path to this file's base directory
baseDir = os.path.abspath(os.path.dirname(__file__))

# Dictionary with this application's static directories configuration
config = {
	"/":		{"tools.staticdir.root": baseDir},
	"/html":	{"tools.staticdir.on": True, "tools.staticdir.dir": "html"},
	"/js":		{"tools.staticdir.on": True, "tools.staticdir.dir": "js"},
	"/css":		{"tools.staticdir.on": True, "tools.staticdir.dir": "css"},
	"/images":	{"tools.staticdir.on": True, "tools.staticdir.dir": "images"},
	"/uploads":	{"tools.staticdir.on": True, "tools.staticdir.dir": "uploads"}, 
	"/tmp":     {"tools.staticdir.on": True, "tools.staticdir.dir": "tmp"}
}
class Users(object):
	# Login	
	@cherrypy.expose
	def login(self, username, password):
		db = sql.connect('database.db')
		result = db.execute("SELECT username FROM users WHERE username=? AND password=?", (username, password)).fetchone()
		db.close()

		if result != None: 
			user = "User found"
		else: 
			user = "User not found"

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"user": user}).encode("utf8")

	# Register
	@cherrypy.expose
	def register(self, username, password):
		db = sql.connect('database.db')
		result = db.execute("SELECT username FROM users WHERE username=? AND password=?", (username, password)).fetchone()
		db.close()

		if result != None: 
			user = "User already exists"
		else:
			db = sql.connect('database.db')
			db.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
			db.commit()
			db.close()
			user = "User created"

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"user": user}).encode("utf8")

class Root(object):
	def __init__(self):
		self.users = Users()

	@cherrypy.expose
	def index(self):
		return open("html/index.html")

	# UpLoad image
	@cherrypy.expose
	def upload(self, myFile, myName, myAuthor):
		h = hashlib.sha256()
		filename = "uploads/" + myFile.filename
		fileout = open(filename, "wb")
		while True:
			data = myFile.file.read(8192)
			if not data: break
			fileout.write(data)
			h.update(data)
		fileout.close()

		ext = myFile.filename.split(".")[-1]
		# final path of the image and changing the filename
		path = "uploads/" + h.hexdigest() + "." + ext
		os.rename(filename, path)
		
		# nameImg and authorImg are input parameters of this method
		# obtain the date and time of loading
		datetime = time.strftime('date:%d-%m-%Y time:%H:%M:%S')

		# insert the file information in the images table
		# eventually initialize the votes tables

		db = sql.connect('database.db')
		db.execute("INSERT INTO images (name, author, path, datetime) VALUES ( ? , ? , ? , ? )", ((myName), (myAuthor), (path), (datetime)))
		db.commit()
		row = db.execute("SELECT * FROM images WHERE path = ?", (path,))
		row = row.fetchone()
		db.execute("INSERT INTO votes (idimg, ups, downs) VALUES ( ? , ? , ? )", (row[0], 0, 0))
		db.commit()
		db.close()

	# List requested images
	@cherrypy.expose
	def list(self, id):
		db = sql.connect('database.db')
		if (id == "all"):
			result = db.execute("SELECT * FROM images")
		else:
			result = db.execute("SELECT * FROM images WHERE author = ?", (id,))			
		rows = result.fetchall()
		db.close()

		# Generate result (list of dictionaries) from rows (list of tuples)
		result = []
		for row in rows:
			result.append({"id": row[0], "name": row[1], "author": row[2], "path": row[3], "datetime": row[4]})
		# eventually sort result by image name before return
		result.sort(key=lambda x: x["id"], reverse=True)

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"images": result}).encode("utf-8")

	# List comments
	@cherrypy.expose
	def comments(self, idimg):
		db = sql.connect('database.db')
		# result = db.execute(query of type SELECT for image of the id idimg)
		result = db.execute("SELECT * FROM images WHERE id = ?", (idimg,))
		row = result.fetchone()
		
		# Generate output dictionary with image information
		imageinfo = dict()
		imageinfo["id"] = row[0]
		imageinfo["name"] = row[1]
		imageinfo["author"] = row[2]
		imageinfo["path"] = row[3]
		imageinfo["datetime"] = row[4]

		# result = db.execute(query of type SELECT for all comments of the id idimg)
		result = db.execute("SELECT * FROM comments WHERE idimg = ?", (idimg,))
		# Generate output dictionary with image comments list
		comments = []
		rows = result.fetchall()
		for row in rows:
			comments.append({"user": row[2], "comment": row[3], "datetime": row[4]})

		# result = db.execute(query of type SELECT for votes of the id idimg)
		result = db.execute("SELECT * FROM votes WHERE idimg = ?", (idimg,))
		row = result.fetchone()
		db.close()

		# Generate output dictionary with image votes
		imagevotes = dict()
		imagevotes["thumbs_up"] = row[2]
		imagevotes["thumbs_down"] = row[3]

		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"image": imageinfo, "comments": comments, "votes": imagevotes}).encode("utf-8")

	# UpLoad comment
	@cherrypy.expose
	def newcomment(self, idimag, username, newcomment):
		db = sql.connect('database.db')
		datetime = time.strftime('date:%d-%m-%Y time:%H:%M:%S')
		# insert the comment information in the comments table
		db.execute("INSERT INTO comments (idimg, user, comment, datetime) VALUES ( ? , ? , ? , ? )", (idimag, username, newcomment, datetime))
		db.commit()
		db.close()
  
	# Increment Up votes
	@cherrypy.expose
	def upvote(self, idimag):
		db = sql.connect('database.db')
		# update the vote information in the votes table
		db.execute("UPDATE votes SET ups = ups + 1 WHERE idimg = ?", (idimag,))
		db.commit()
		db.close()

	# Increment Down votes
	@cherrypy.expose
	def downvote(self, idimag):
		db = sql.connect('database.db')
		# update the vote information in the votes table
		db.execute("UPDATE votes SET downs = downs + 1 WHERE idimg = ?", (idimag,))
		db.commit()
		db.close()
  
	@cherrypy.expose
	def imageproc(self , idimg, filter):
		db = sql.connect('database.db')
		result = db.execute("SELECT * FROM images WHERE id = ?", (idimg,))
		row = result.fetchone()
		db.close()
		result={"id": row[0], "name": row[1], "author": row[2], "path": row[3], "datetime": row[4]}
		path2 = result["path"]
  
		if filter == "option1":
			processo.blackAndWhite(path2)
			path3 = "tmp/blackandwhite.jpg"
		elif filter == "option2":
			processo.sepia(path2)
			path3 = "tmp/sepia.jpg"
		elif filter == "option3":
			processo.borders(path2)
			path3 = "tmp/borders.jpg"

		result2={"path2": path3}
  
		cherrypy.response.headers["Content-Type"] = "application/json"
		return json.dumps({"image": result, "image2":result2}).encode("utf-8")

cherrypy.quickstart(Root(), "/", config)
