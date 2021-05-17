from flask import Flask
from image_dataset import create_image_dataset

app = Flask(__name__)


@app.route('/')
def hello_world():
    create_image_dataset("Keanu Reeves")
    return 'Hello World!'


if __name__ == '__main__':
    app.run()





