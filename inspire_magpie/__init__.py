from __future__ import absolute_import, print_function

from flask import Flask

from .rest import blueprint as rest_blueprint
from .ui import blueprint as ui_blueprint


application = Flask('magpie', static_url_path='')
application.register_blueprint(rest_blueprint)
application.register_blueprint(ui_blueprint)

__all__ = ('application',)
