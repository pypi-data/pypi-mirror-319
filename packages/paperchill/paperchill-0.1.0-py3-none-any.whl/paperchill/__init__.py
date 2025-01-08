from flask import Flask, request

from paperchill.wrapp import WrApp
from paperchill.pdf_convert import pdf_convert

# TODO: Use a secure location for file uploads
UPLOAD_FOLDER = '/tmp'  # nosec


def create_app() -> Flask:
    app = Flask('paperchill')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    wrapp = WrApp(app)

    @app.route('/', methods=['GET', 'POST'])
    def upload():
        return wrapp.upload(request)

    @app.route('/uploads/<name>')
    def download(name: str):
        return wrapp.display_file(name)

    @app.route('/questions', methods=['POST'])
    def questions():
        return wrapp.get_answer()

    return app
