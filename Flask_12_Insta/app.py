from flask import Flask, send_from_directory

from Flask_12_Insta.loader.views import loader_blueprint
from Flask_12_Insta.main.views import main_blueprint

app = Flask(__name__)

app.register_blueprint(main_blueprint)
app.register_blueprint(loader_blueprint)


@app.route('/uploads/images/<path:path>')
def static_dir(path):
    return send_from_directory('uploads/images', path)


app.run()
