
Captcha
=======

The Captcha class deals with displaying and solving captcha puzzles for server 
calls that require them.

While you certainly *can* use this class in your scripts, you generally won't 
need to -- if you make a call that requires a captcha, and you haven't solved 
one on the account your script is using in the past 30 minutes, the script 
will automatically pop up a captcha image and ask you to solve it.

.. automodule:: lacuna.captcha
   :members:
   :show-inheritance:

