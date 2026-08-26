from flask import Flask
import deadstock.config as config

def create_app(__name__):

    config.initialize(
        env_path=".env",
        json_path="./deadstock/config/config.json"
    )

    app = Flask(__name__)

    return app