passotp is a CLI to generate time-based one-time passwords from secrets stored with Pass

Instalation
===========

::

    pip install passotp

Prepare your encrypted pass files
=================================
Edit your password file

::

    pass edit devel/test


Add a line at the end of the file containing "OTP: <secret>", It should look like this "OTP: base32secret3232" or something like this "OTP: KRBP SL73 C3RI 76GP MK3S BGHO TC4B 347A 1DYN CVXJ"

(Warning: the "OTP" is not case sensitive yet issue #1)

Usage
=====

::

    passotp <pass-name> [-c]

Example
-------

::

  ~$ pass devel/test
  VU5Z5Tok4ATyIQQdSdeO
  user: test
  OTP: base32secret3232
  ~$ passotp devel/test
  458262
