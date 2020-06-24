from flask import Flask



UPLOAD_FOLDER = 'C://Users//saipa//Desktop//project//Data'

app = Flask(__name__)
#app.debug = True
app.secret_key = "secret key"
app.config['SECRET_KEY']
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024