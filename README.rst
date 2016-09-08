passotp is a CLI to add OTP passwords for Pass

Instalation
===========
pip install passotp

Usage
=====
passotp <pass-name> [-c]

example
-------

::

  ~$ pass devel/test
  VU5Z5Tok4ATyIQQdSdeO
  user: test
  OTP: base32secret3232
  ~$ passotp devel/test
  458262


Prepare your pass files
=======================
You shoud add a line containing "OTP: <secret>" (Warning: the "OTP" is not case sensitive yet issue #1)
