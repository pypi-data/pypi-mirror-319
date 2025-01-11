import re
import json
import os
import time
import hashlib
import xxhash
import binascii
import base64
import secrets
import logging
import pickle

from flask import (current_app as app, 
				   url_for, 
				   redirect, 
				   request,
				   has_request_context,
				   session, 
				   Response)

from flask_login import (current_user as worker,
						 UserMixin, 
						 login_user, 
						 logout_user)

from datetime import (datetime,
					  timedelta)
from uuid import uuid4
from typing import Any

from ...crypto import KDM
from ...crypto import GCM

from .logic import Logic
from .core import Core
from .signals import *

class Device(Logic, Core):

	def __init__(self, key: str, 
					   value: Any = None,
					   addr: str = str(),
					   pattern: str = 'default', **kwargs):

		super().__init__(key, 				 #server side public key
						 value, 			 #server side private key
						 pattern, 
						 **kwargs)

		self.__cache = list()
		self.__kdm   = KDM(self.value,	 	 #ed25519 private key
						   self.client,	 	 #client ed25519 public key
						   self.session,	 #last session key
						   self.secret,		 #actual secret key
						   power=128)

		if kwargs.get('addr') or has_request_context():
			self.addr  = kwargs.get('addr', request.remote_addr) #actual remote_addr

	def __enter__(self):
		return self
 
	def __exit__(self, *args):
		pass

	@property
	def kdm(self):
		return self.__kdm

	""" use self.user_callback
	"""
	def login(self, user:object = None) -> bool:
		if not user:
			user = User(self.user)
		if user and login_user(user, remember=False, 
									 duration=timedelta(minutes=app.config.get('SESSION_MAX_TIME')),
									 force=True):
			self.seen = time.time()
			if self.update():
				return worker.is_authenticated
		return worker.is_authenticated

	def logout(self) -> bool:
		self.seen = time.time()
		if device := self.update() if logout_user() else None:
			del self.challange
			return True
		return False

	def register(self, user:object = None) -> bool:
		if user and self.user:
			return user.get_id() == self.user
		if user and user.get_id() and not self.user:
			self.user = user.get_id()
			if self.update():
				return user.get_id() == self.user
		return False

	@property
	def id(self):
		return self.kdm.identity.decode()
