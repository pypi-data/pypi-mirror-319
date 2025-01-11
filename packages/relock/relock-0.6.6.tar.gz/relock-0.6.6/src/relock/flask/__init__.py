import os
import sys
import logging
import binascii

logging = logging.getLogger(__name__)

from flask import (Blueprint,
				   current_app as app, 
				   has_request_context,
				   request,
				   session)

from flask_login import (current_user as worker,
						 user_logged_in,
					     user_logged_out,
					     user_loaded_from_cookie,
					     user_loaded_from_request,
					     user_login_confirmed,
					     user_unauthorized,
					     user_needs_refresh,
					     user_accessed,
					     session_protected)

from .login import AnonymousUserMixin
from .signals import Signals

from ..tcp import TCP
from ..thread import Thread

bp = os.environ.get('SENTINEL_ROUTE', 'relock')
bp = Blueprint(bp, __name__, url_prefix='/%s' % bp,
							 template_folder='templates',
							 static_folder='static',
							 static_url_path='/static/%s' % bp)

class Flask(Signals):

	def __init__(self, app=None, host=None,
								 port=None,
								 pool=1,
								 ping=False,
								 timeout=30):
		if app is not None:
			self.init_app(app)
		self.tcp = None

	def init_app(self, app, add_context_processor=True):
		"""
		Configures an application. This registers an `before_request` call, and
		attaches this `SessionSentinel` to it as `app.session_sentinel`.

		:param app: The :class:`flask.Flask` object to configure.
		:type app: :class:`flask.Flask`
		:param add_context_processor: Whether to add a context processor to
			the app that adds a `current_user` variable to the template.
			Defaults to ``True``.
		:type add_context_processor: bool
		"""
		app.session_sentinel = self

		if not hasattr(app, 'login_manager'):
			raise RuntimeError('Session Sentinel requires Flask-Login to start first.')

		app.login_manager.anonymous_user = AnonymousUserMixin

		app.config.setdefault('SESSION_SENTINEL_HOST', str(os.environ.get('SESSION_SENTINEL_HOST', '127.0.0.1')))
		app.config.setdefault('SESSION_SENTINEL_PORT', int(os.environ.get('SESSION_SENTINEL_PORT', 8111)))
		app.config.setdefault('SESSION_SENTINEL_POOL', int(os.environ.get('SESSION_SENTINEL_POOL', 1)))
		app.config.setdefault('SESSION_SENTINEL_PING', bool(os.environ.get('SESSION_SENTINEL_PING', False)))
		app.config.setdefault('SESSION_SENTINEL_TIMEOUT', int(os.environ.get('SESSION_SENTINEL_TIMEOUT', 30)))

		app.config.setdefault('SESSION_CACHE', 'sentinel')
		app.config.setdefault('SESSION_MAX_TIME', 60 * 60)
		
		app.config.setdefault('LOGIN_COOKIE_NAME', 'relock')
		app.config.setdefault('LOGIN_COOKIE_SAMESITE', 'lax')
		app.config.setdefault('STAMP_COOKIE_NAME', 'stamp')
		app.config.setdefault('STAMP_COOKIE_SAMESITE', 'lax')

		if not app.config.get('SESSION_REDIS'):
			raise RuntimeError('Session Sentinel requires a Reids-type session.')

		app.config.setdefault('SENTINEL_NOTIFY_ALL_REQUESTS', False)

		with app.app_context():
			try:
				self.tcp = TCP(host=app.config.get('SESSION_SENTINEL_HOST'),
							   port=app.config.get('SESSION_SENTINEL_PORT'),
							   pool=app.config.get('SESSION_SENTINEL_POOL'),
							   ping=app.config.get('SESSION_SENTINEL_PING'),
							   timeout=app.config.get('SESSION_SENTINEL_TIMEOUT'))
			except (SystemExit, KeyboardInterrupt):
				sys.exit()
			except Exception as e:
				raise RuntimeError('Session Sentinel host is not available.')
			else:

				from .device import Device
				from .routes import (identity,
									 exchange,
									 validate,
									 clear)

				app.register_blueprint(bp)

				if add_context_processor:
					app.before_request(Device.load_cookie)
					app.after_request(Device.update_cookie)

					@app.context_processor
					def x_key_nonce_processor():
						def x_key_nonce():
							if hasattr(request, 'device'):
								if not request.device.nonce and request.device.session:
									request.device.nonce = os.urandom(16)
								if request.device.nonce:
									return binascii.hexlify(request.device.nonce).decode()
							return str()
						return dict(x_key_nonce=x_key_nonce)

					@app.context_processor
					def x_key_signature_processor():
						def x_key_signature():
							if hasattr(request, 'device'):
								if nonce := request.device.nonce:
									if signature := request.device.sign(nonce):
										return binascii.hexlify(signature).decode()
							return str()
						return dict(x_key_signature=x_key_signature)

	@classmethod
	def signal(cls):
		pass