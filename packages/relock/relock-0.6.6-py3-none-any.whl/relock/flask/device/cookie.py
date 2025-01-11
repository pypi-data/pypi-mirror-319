import os
import logging
import base64
import xxhash
import binascii

from datetime import (datetime,
					  timedelta)
from flask import (current_app as app, 
				   url_for, 
				   redirect, 
				   request, 
				   session, 
				   Response)
from flask_login import (current_user as worker,
						 logout_user)

from .secret import Secret
from .signals import (device_loaded_from_cookie,
					  device_cookie_and_stamp_set,
					  device_cookie_deprecated_keys_removed,
					  request_without_device_cookie,
					  device_cookie_key_not_exists,
					  device_cookie_invalid_stamp,
					  device_cookie_base64_decode_failure,
					  device_cookie_session_confirmed,
					  device_cookie_stamp_cookie_not_exists,
					  stamp_cookie_decode_failure,
					  device_session_no_longer_exists,
					  device_cookie_decryption_faild,
					  session_request_without_cookie,
					  blank_device_object_created,
					  request_processing_has_started,
					  request_processing_has_been_completed)
from ...crypto import KDM, GCM

class Cookie(Secret):

	@property
	def cookie(self):
		return hasattr(self, '__fresh_cookie')

	@cookie.setter
	def cookie(self, value:bool = True):
		setattr(self, '__fresh_cookie', True)
		if hasattr(self, '__clear_cookie'):
			delattr(request, '__clear_cookie')

	@cookie.deleter
	def cookie(self, value:bool = True):
		setattr(request, '__clear_cookie', True)
		if hasattr(self, '__fresh_cookie'):
			delattr(self, '__fresh_cookie')
		session.pop('recovery', None)
		session.pop('x25519', None)
		session.pop('device', None)
		session.pop('stamp', None)
		session.pop(app.config.get('SESSION_CACHE'), None)

	@staticmethod
	def http_only_cookie(response, name, value, samesite):
		response.set_cookie(name, value=value,
								  expires=datetime.now() + timedelta(days=365),
								  max_age=timedelta(days=365),
								  path='/',
								  secure=True, 
								  httponly=True,
								  samesite=samesite)

	def set_cookie(self, response):
		if name := app.config.get('LOGIN_COOKIE_NAME'):
			if cookie := request.cookies.get(name):
				if key := xxhash.xxh128(cookie).digest():
					if self.unassociate(key):
						device_cookie_deprecated_keys_removed.send()
			if stamp := app.config.get('STAMP_COOKIE_NAME'):
				if random := os.urandom(32):
					with GCM(random) as gcm:
						if _ := gcm.encrypt(dict(key=self.key,
												 stamp=self.hash,
												 session=self.session)):
							if bytearray := base64.b64encode(_).decode():
								if key := xxhash.xxh128(bytearray).digest():
									if self.associate(key, random):
										self.http_only_cookie(response, name, bytearray,
												  	  		  app.config.get('LOGIN_COOKIE_SAMESITE', 'lax'))
										self.http_only_cookie(response, stamp, binascii.hexlify(self.hash).decode(),
												  	  		  app.config.get('STAMP_COOKIE_SAMESITE', 'lax'))
										session[app.config.get('SESSION_CACHE')] = list()
										device_cookie_and_stamp_set.send()
		request_processing_has_been_completed.send(response=response.status,
												   status_code=response.status_code)
		return response

	@classmethod
	def load_cookie(cls, stamp=bytes()):
		# session.modified = True
		if not 'static' in request.url:
			request_processing_has_started.send()
			if name := app.config.get('LOGIN_COOKIE_NAME'):
				if stamp := app.config.get('STAMP_COOKIE_NAME'):
					if cookie := request.cookies.get(name):	
						if stamp := request.cookies.get(stamp):
							try:
								stamp = binascii.unhexlify(stamp)
							except:
								stamp_cookie_decode_failure.send()
						else:
							device_cookie_stamp_cookie_not_exists.send()
						if key := cls.associate(xxhash.xxh128(cookie).digest()):
							if session.get('x25519') == session.get('recovery'):
								if device := cls(key=session.get('device'),
												 addr=request.remote_addr,
												 agent=request.headers.get('User-Agent')):
									if stamp != device.stamp and stamp != device.prev:
										device_cookie_invalid_stamp.send()
									else:
										device_cookie_session_confirmed.send()
										return setattr(request, 'device', device)
								else:
									device_session_no_longer_exists.send()
							try:
								cookie = base64.b64decode(cookie)
							except:
								device_cookie_base64_decode_failure.send()
							else:
								with GCM(key) as gcm:
									try:
										if dict := gcm.decrypt(cookie):
											session['device'] = dict.get('key')
											session['stamp'] = dict.get('stamp')
											session['recovery'] = dict.get('session')
									except:
										device_cookie_decryption_faild.send()
									else:
										if device := cls(key=session.get('device'),
														 addr=request.remote_addr,
														 agent=request.headers.get('User-Agent')):
											return setattr(request, 'device', device)
									finally:
										if hasattr(request, 'device'):
											device_loaded_from_cookie.send()
										else:
											device_session_no_longer_exists.send()
						else:
							device_cookie_key_not_exists.send()
					else:
						if 'recovery' in session:
							session.pop('recovery', None)
							session.pop('x25519', None)
							session.pop('device', None)
							session.pop('stamp', None)
							session.pop(app.config.get('SESSION_CACHE'), None)
							session_request_without_cookie.send()
						else:
							request_without_device_cookie.send()
			# else:
			with KDM() as kdm:
				session['device'] = bytes(kdm.signer)
				session['recovery'] = bytes()
				session['stamp'] = bytes()
				setattr(request, 'device', cls(key=bytes(kdm.signer),
											   value=abs(kdm.signer),
											   addr=request.remote_addr,
											   agent=request.headers.get('User-Agent'),
											   auto_commit=False))
			blank_device_object_created.send()

	@classmethod
	def update_cookie(cls, response):
		if hasattr(request, 'device'):
			if request.device.cookie:
				return request.device.set_cookie(response)
			if hasattr(request, '__clear_cookie'):
				if name := app.config.get('LOGIN_COOKIE_NAME'):
					response.delete_cookie(name, path='/')
				if stamp := app.config.get('STAMP_COOKIE_NAME'):
					response.delete_cookie(stamp, path='/')
			request_processing_has_been_completed.send(response=response.status,
													   status_code=response.status_code)
		return response


	def clear(self):
		del self.cookie
		if logout_user():
			return bool(self.delete())
		return False