# !/usr/bin/dev python
# -*- coding:utf-8 -*-

from flask import Flask
from flask.ext.bootstrap import Bootstrap
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.login import LoginManager
from flask.ext.moment import Moment
from flask.ext.pagedown import PageDown
from config import config

bootstrap = Bootstrap()
db = SQLAlchemy()
moment = Moment()
pagedown = PageDown()

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message = u'请登录以获得访问权限'


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])

    if not app.config['DEBUG'] and not app.config['TESTING']:

        # send standard logs to syslog
        import logging
        from logging.handlers import SysLogHandler
        syslog_handler = SysLogHandler()
        syslog_handler.setLevel(logging.WARNING)
        app.logger.addHandler(syslog_handler)

    bootstrap.init_app(app)
    db.init_app(app)
    moment.init_app(app)
    pagedown.init_app(app)
    login_manager.init_app(app)

    from .talks import talks as talks_blueprint
    app.register_blueprint(talks_blueprint)

    from .auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from .files import files as files_blueprint
    app.register_blueprint(files_blueprint)

    from .api_1_0 import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/1.0')

    @app.route('/')
    def jumbo():
        from flask import render_template
        return render_template('jumbo.html')
    
    @app.route('/test')
    def test():
        from flask import render_template
        return render_template('1.html')

    return app
