#!/usr/bin/env python

from sanic import Sanic

from search_engine.config import Config
from search_engine.database.motor_base import MotorBase
from search_engine.views.bp_home import bp_home

app = Sanic(__name__)
app.blueprint(bp_home)


@app.listener('before_server_start')
def init_cache(app, loop):
    """
    初始化操作 对一些参数进行配置
    :param app:
    :param loop:
    :return:
    """
    app.config['search_engine_config'] = Config
    app.mongo_db = MotorBase(loop=loop).get_db()


if __name__ == "__main__":
    app.run(host="0.0.0.0", workers=2, port=8001, debug=False)