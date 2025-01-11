from flask import (current_app as app, 
				   session, 
				   request, 
				   Response, 
				   url_for, 
				   json,
				   render_template, 
				   flash, 
				   jsonify, 
				   redirect, 
				   abort, 
				   make_response, 
				   session)

from flask_login import (current_user as worker, 
						 login_required)

from . import bp, logging

import random, os
import time
import pickle
import base64
import hashlib
import binascii
import subprocess

from datetime import datetime
from datetime import timedelta

from urllib.parse import urlparse

from .device import (origin_authentication_key_collision,
					 origin_authentication_failure_invalid_signature,
					 origin_authentication_is_successful,
					 origin_authentication_rekeying_demand,
					 origin_authentication_rekeying_nonce_mismatch,
					 origin_authentication_empty_token,
					 origin_authentication_empty_signature)

@bp.route('/identity/<string:token>', methods=['GET'])
def identity(token=None):
	return binascii.hexlify(os.urandom(64))

@bp.route("/exchange", methods=['POST'])
def exchange():
	if not isinstance(request.json.get('key'), list):
		return dict()
	if not isinstance(request.json.get('hash'), list):
		return dict()
	with app.app_context():
		if keys := request.device.exchange(bytes(request.json.get('key')),
										   bytes(request.json.get('hash'))):
			return keys
	return dict()

@bp.route("/validate", methods=['POST'])
def validate():
	if request.device.nonce:
		if request.json.get('nonce') and bytes(request.json.get('nonce')) != request.device.nonce:
			origin_authentication_rekeying_nonce_mismatch.send(json=request.json.get('nonce'),
															   device=request.device.nonce)
		origin_authentication_rekeying_demand.send()
		if token := request.device.rekeying(request.device.nonce):
			request.device.nonce = bytes()
	if not request.json.get('x-key-token'):
		origin_authentication_empty_token.send()
	if not request.json.get('x-key-signature'):
		origin_authentication_empty_signature.send()
	if signature := request.device.verify(bytes(request.json.get('x-key-token', bytes())),
										  bytes(request.json.get('x-key-signature', bytes()))):
		if token := request.device.validate(bytes(request.json.get('x-key-token'))):
			origin_authentication_is_successful.send(signature=signature,
													 token=token)
			return dict(status=True, authenticated=worker.is_authenticated, url=None, timeout=0)
		logging.error('Invalid token. (%s, %s) Erasing keys...', signature, token)
		origin_authentication_key_collision.send(signature=signature,
												 token=token)
		return dict(status=False, authenticated=worker.is_authenticated, url=None, timeout=0)
	logging.error('Invalid signature. (%s) Erasing keys...', signature)
	origin_authentication_failure_invalid_signature.send(signature=signature)
	return dict(status=False, authenticated=worker.is_authenticated, url=None, timeout=0)

@bp.route('/relock.js', methods=['GET'])
def js(content=bytes()):
	__static__ = os.path.join(os.path.dirname(__file__), 'static')
	for file in ('noble-hashes.js', 'noble-curves.js', 'utils.js', 'gcm.js', 'relock.js'):
		with open(os.path.join(__static__, file)) as js_file:
			content += bytes(js_file.read(),'utf-8')
	return Response(content, status=200, content_type='application/javascript; charset=utf-8')

@bp.route("/clear", methods=['POST'])
def clear():
	return dict(status=request.device.clear())