#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: Olivier Noguès

import os
import base64

try:
  # TODO: Use correctly requires with cryptography module
  from ares.Lib.AresImports import requires
  ares_sqlalchemy = requires("cryptography", reason='Missing Package', install='cryptography', autoImport=True, sourceScript=__file__)

  from cryptography.fernet import Fernet
  from cryptography.hazmat.backends import default_backend
  from cryptography.hazmat.primitives import hashes
  from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
except Exception as err:
  print('-------------------------------------------------------------')
  print("This cannot be used locally without the cryptography module")
  print("To install it on your computer please run the below command")
  print('pip install cryptography')
  print('-------------------------------------------------------------')
  print(err)


def crypt(aresObj, data, token, salt=None):
  """
  :category: Data Encryption
  :rubric: JS
  :type: Security
  :example: aresObj.crypt('mydata', 'mytoken')
  :dsc:
    This function will use the cryptography to ensure a secured encryption of the different credential and private data.
    This can be also used to protect data from the aresObj.
    In order to ensure the right privacy please do not store the token and the salt in the framework.
  :return: The crypted data with the salt used
  """
  salt = salt if salt is not None else os.urandom(32)
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=salt, iterations=100000, backend=default_backend())
  encrypted_key = base64.urlsafe_b64encode(kdf.derive(bytes(token.encode('utf-8'))))
  return Fernet(encrypted_key).encrypt(bytes(data.encode('latin1'))).decode('latin1'), salt.decode('latin1')

def decrypt(aresObj, crptyData, token, salt, label=''):
  """
  :category: Data Encryption
  :rubric: JS
  :type: Security
  :example: aresObj.decrypt('mydata', 'mytoken', '123')
  :dsc:
    This function will use the two keys in order to decrypt the data.
    In case of failure this function will raise an exception.
  :return: A string with the derypted data
  """
  if hasattr(aresObj, 'log'):
    # In the admin section the aresObj is not defined
    aresObj.log("SECURITY|%s|%s|password decoding" % (aresObj.run.current_user, label))
  kdf = PBKDF2HMAC(algorithm=hashes.SHA256(), length=32, salt=bytes(salt.encode('latin1')), iterations=100000, backend=default_backend())
  encrypted_key = base64.urlsafe_b64encode(kdf.derive(bytes(token.encode('utf-8'))))
  return Fernet(encrypted_key).decrypt(bytes(crptyData.encode('latin1'))).decode('utf-8')

