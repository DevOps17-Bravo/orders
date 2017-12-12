from flask import Flask
from flasgger import Swagger
# Create the Flask aoo
app = Flask(__name__)

app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "specs": [
        {
            "version": "1.0.0",
            "title": "DevOps Swagger Orders App",
            "description": "This is a sample server Order store server.",
            "endpoint": 'v1_spec',
            "route": '/v1/spec'
        }
    ]
}
# Load Configurations
app.config.from_object('config')

Swagger(app)

import server
import models
import custom_exceptions