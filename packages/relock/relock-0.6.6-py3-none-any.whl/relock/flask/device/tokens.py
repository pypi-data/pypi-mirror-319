import logging
import binascii

from flask import (current_app as app, 
				   has_request_context,
				   session)

from .signals import (token_invalid_fails_when_unpacking,
					  token_invalid_does_not_match_server,
					  token_invalid_reuse_of_token,
					  token_validation_throw_error,
					  token_validation_successful)

class Tokens(object):

	def token(self) -> bool:
		return self.kdm.token()

	def validate(self, token:bytes, valid:bool = False) -> bool:
		try:
			if isinstance(token, str) and int(token, 16):
				token = binascii.unhexlify(token)
		except:
			token_invalid_fails_when_unpacking.send()
		else:
			try:
				valid = self.kdm.validate(token)
			except:
				token_validation_throw_error.send()
			else: 
				if valid:
					token_validation_successful.send()
				else:
					token_invalid_does_not_match_server.send()
		finally:
			if cache := app.config.get('SESSION_CACHE', 'cache'):
				if not cache in session:
					session[cache] = list()
				if token in session[cache]:
					valid = False; token_invalid_reuse_of_token.send()
				else:
					session[cache].append(token)
		return valid