# Copyright 2016, 2017 John J. Rofrano. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# https://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
Microservice module
This module contains the microservice code for
    server
    models
"""
from flask import Flask

app = Flask(__name__)
app.config.from_object('config')
#print('Database URI {}'.format(app.config['SQLALCHEMY_DATABASE_URI']))

import server, models, custom_exceptions
