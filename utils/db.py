# Copyright (c) the Eagle authors and contributors.
# All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python
# -*- coding: utf-8 -*-
# flake8: noqa

import os
import imp
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app_conf = imp.load_source('app_conf', os.getenv('EAGLE_HOME', '..') + '/eagle_cfg.py')

SQLALCHEMY_DATABASE_URI =\
    'postgresql+pg8000://'+app_conf.DB_USERNAME + ':' + \
    app_conf.DB_PASSWORD + '@' + app_conf.DB_HOST + \
    ':'+app_conf.DB_PORT + '/' + app_conf.DB_NAME

engine = create_engine(SQLALCHEMY_DATABASE_URI)
Session = sessionmaker(bind=engine)

if __name__ == '__main__':
    user1 = session.query(User).first()
    print user1.password
