from flask import *
from currency import * 
from language import *
from resume import *
from flask_cors import CORS

app = Flask(__name__)
app.register_blueprint(currencyy)
app.register_blueprint(translation)
app.register_blueprint(resumee)

CORS(app)

@app.route('/')
def index():
    return render_template('index.html')
if __name__ == '__main__':
    app.run(debug=True)
