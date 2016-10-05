#!/usr/bin/env python

# Copyright 2015 Google Inc. All rights reserved.
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


import webapp2

import logging as std_logging

std_logging.basicConfig()

custom_formatter = std_logging.Formatter('%(created)f\t%(message)s')
custom_handler = std_logging.FileHandler('/var/log/app_engine/custom_logs/custom.log')
custom_handler.setFormatter(custom_formatter)
custom_logging = std_logging.getLogger('custom')
custom_logging.addHandler(custom_handler)

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('Welcome to the "Distributed Load Testing Using Kubernetes" sample web app\n')


class LoginHandler(webapp2.RequestHandler):
    def post(self):
        deviceid = self.request.get('deviceid')
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/login - device: {}\n'.format(deviceid))
        custom_logging.info('/login - device: {}'.format(deviceid))


class MetricsHandler(webapp2.RequestHandler):
    def post(self):
        deviceid = self.request.get('deviceid')
        timestamp = self.request.get('timestamp')
        
        self.response.headers['Content-Type'] = 'text/plain'
        self.response.write('/metrics - device: {}, timestamp: {}\n'.format(deviceid, timestamp))
        custom_logging.info('/metrics - device: {}, timestamp: {}'.format(deviceid, timestamp))


app = webapp2.WSGIApplication([
    (r'/', HomeHandler),
    (r'/login', LoginHandler),
    (r'/metrics', MetricsHandler),
])
