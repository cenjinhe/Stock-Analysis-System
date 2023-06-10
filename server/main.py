#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author   : jinhe Cen
# @Time     : 2023/6/10 16:13
# @File     : main.py.py

import logging
from apps import create_app
from flask import request, jsonify
app = create_app(config_name='develop')


@app.before_request
def record_request_info():
    pass


@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(error):
    msg = error.data.get("messages", ["Invalid request"])
    return jsonify({"code": 400, "status": "success", "message": msg, "result": ""})


if __name__ == '__main__':
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)
    app.logger.info(app.url_map)

