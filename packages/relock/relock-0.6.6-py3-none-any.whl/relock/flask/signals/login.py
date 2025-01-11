import logging

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

class Login(object):

	#: Sent when a user is logged in. In addition to the app (which is the
	#: sender), it is passed `user`, which is the user being logged in.
	@user_logged_in.connect
	def _user_logged_in(self, *args, **kwargs):
		pass

	#: Sent when a user is logged out. In addition to the app (which is the
	#: sender), it is passed `user`, which is the user being logged out.
	@user_logged_out.connect
	def _user_logged_out(self, *args, **kwargs):
		pass

	#: Sent when the user is loaded from the cookie. In addition to the app (which
	#: is the sender), it is passed `user`, which is the user being reloaded.
	@user_loaded_from_cookie.connect
	def _user_loaded_from_cookie(self, *args, **kwargs):
		pass

	#: Sent when the user is loaded from the request. In addition to the app (which
	#: is the #: sender), it is passed `user`, which is the user being reloaded.
	@user_loaded_from_request.connect
	def _user_loaded_from_request(self, *args, **kwargs):
		pass

	#: Sent when a user's login is confirmed, marking it as fresh. (It is not
	#: called for a normal login.)
	#: It receives no additional arguments besides the app.
	@user_login_confirmed.connect
	def _user_login_confirmed(self, *args, **kwargs):
		pass

	#: Sent when the `unauthorized` method is called on a `LoginManager`. It
	#: receives no additional arguments besides the app.
	@user_unauthorized.connect
	def _user_unauthorized(self, *args, **kwargs):
		pass
		
	#: Sent when the `needs_refresh` method is called on a `LoginManager`. It
	#: receives no additional arguments besides the app.
	@user_needs_refresh.connect
	def _user_needs_refresh(self, *args, **kwargs):
		pass

	#: Sent whenever the user is accessed/loaded
	#: receives no additional arguments besides the app.
	@user_accessed.connect
	def _user_accessed(self, *args, **kwargs):
		pass

	#: Sent whenever session protection takes effect, and a session is either
	#: marked non-fresh or deleted. It receives no additional arguments besides
	#: the app.
	@session_protected.connect
	def _session_protected(self, *args, **kwargs):
		pass