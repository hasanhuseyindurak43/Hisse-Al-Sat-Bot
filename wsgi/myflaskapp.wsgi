#!/usr/bin/python
import sys
import logging
import site
site.addsitedir('/var/www/html/flaskapp/venv/lib/python3.11/site-packages')
logging.basicConfig(stream=sys.stderr)
activate_this = "/var/www/html/flaskapp/venv/bin/activate_this.py"
with open(activate_this) as source_file:
    exec(source_file.read(), dict(__file__=activate_this))
# with open("/var/www/html/flaskapp/venv/bin/activate_this.py", "rb",) as source_file:
#     code = compile(source_file.read(), "/var/www/html/flaskapp/venv/bin/activate_this.py", "exec")
# exec(code)
sys.path.insert(0, '/var/www/html/flaskapp')
from main import app as application
