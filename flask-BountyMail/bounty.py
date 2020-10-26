import json, sqlite3, sys, os
from flask import Flask, jsonify, request, make_response, render_template, url_for, flash, redirect
from flask.cli import AppGroup
from datetime import datetime
from werkzeug.utils import secure_filename

UPLOAD_FOLDER = '../flask-BountyMail/static'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
databaseName = 'database.db'

# < HELPER FUNCTIONS --------------------------------------------------
@app.cli.command('init')
def init():                        
    try:
        conn = sqlite3.connect(databaseName)
        with app.open_resource('create.sql', mode='r') as f:
            conn.cursor().executescript(f.read())
        conn.commit()
        print("Database file created as {}".format(str(databaseName)))
    except:
        print("Failed to create {}".format(str(databaseName)))
        sys.exit()
app.cli.add_command(init)

def connectDB(dbName):  
    # Connects to database and returns the connection, if database is offline, program exits
    try:
        conn = sqlite3.connect(dbName)
        print("SUCCESS: CONNECTED TO {}".format(str(dbName)))
        return conn
    except:
        print("ERROR: {} OFFLINE".format(str(dbName)))
        sys.exit()

def convertToBinaryData(filename):
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

def insertBLOB(cur, conn, photo, photoPath, demand, photoName, amount):
    
    insert_blob_query = "INSERT INTO bounty(photo, photoPath, demands, photoName, amount) VALUES (?, ?, ?, ?, ?)"

    bountyPhoto = convertToBinaryData(photo)
    data_tuple = (bountyPhoto, photoPath, demand, photoName, amount)
    cur.execute(insert_blob_query, data_tuple)
    conn.commit()


def writeToFile(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("stored blob data into: ", filename, "\n")

def readBlobData(bountyID):
    conn = connectDB(databaseName)
    cur = conn.cursor()

    fetch_blob_query = "SELECT * from bounty where id = ?"
    cur.execute(fetch_blob_query, (bountyID,))
    record = cur.fetchall()
    for row in record:
        print("Id = ", row[0], "Name = ", row[4])
        photo = row[1]
        demand = row[3]

        photoPath = "../flask-BountyMail/static/images/" + str(bountyID) + ".jpg"
        writeToFile(photo, photoPath)
    cur.close()
    conn.close()

def path(id):
    photoPath = str(id)
    return photoPath

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS



@app.route('/', methods=['GET', 'POST'])
def index():
    conn = connectDB(databaseName)
    cur = conn.cursor()
    photoPath = path(1)
    bounties = cur.execute("SELECT * FROM bounty").fetchall()
    return render_template("index.html", bounties = bounties, photoPath = photoPath)

@app.route('/blacklist', methods=['GET', 'POST'])
def blacklist():
    conn = connectDB(databaseName)
    cur = conn.cursor()
    if request.method == 'POST':
        print("first")
        photoName = request.form.get("name")
        demands = request.form.get("demands")
        amount = request.form.get("amount")
        if 'file' not in request.files:
            print("second")
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print("third")
            return redirect(request.url)
        if file and allowed_file(file.filename):
            print("fourth")
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            photo = UPLOAD_FOLDER + "/"+ filename
            photoPath = path(filename)
            image_file = url_for('static', filename=photoPath)
            insertBLOB(cur, conn, photo, image_file, demands, photoName, amount)
            bounties = cur.execute("SELECT * FROM bounty").fetchall()
            return render_template("index.html", bounties = bounties, image_file = image_file, photoPath=photoPath)
    
    return render_template('post.html')

@app.route('/bounty/<int:bounty_id>')
def bounty(bounty_id):
    conn = connectDB(databaseName)
    cur = conn.cursor()

    bounty = cur.execute("SELECT * from bounty where id = :id", {"id": bounty_id}).fetchone()
    if bounty is None:
        return render_template("error.html", message="Bounty not found.")

    return render_template("bounty.html", bounty=bounty)