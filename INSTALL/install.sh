!/usr/bin/sh

echo "Localhost izinleri ayarlanılıyor..."

cd /

chmod 7777 -R /var/www/html/

echo 

echo "Localhost izinleri ayarlanıldı."

echo

echo "Dosyalar oluşturuluyor..."

cd /var/www/html/

rm rf *.*

mkdir flaskapp

mkdir logapp

echo

echo "Dosyalar oluşturuldu."

echo

echo "Klosör oluşturuluyor..."

cd flaskapp

touch myflaskapp.wsgi

echo """
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
from main import app as application""" > myflaskapp.wsgi

cd ..

cd logapp

mkdir log

sudo apt-get install libapache2-mod-wsgi-py3

a2enmod wsgi

chmod 7777 -R /etc/apache2

cd /etc/apache2/sites-available

touch flaskapp.conf

echo """
<VirtualHost *:80>
	ServerName hissealsatbot.com
	DocumentRoot /var/www/html/flaskapp/

	WSGIDaemonProcess flaskapp user=www-data group=www-data threads=5 python-home=/var/www/html/flaskapp/venv
	WSGIScriptAlias / /var/www/html/flaskapp/myflaskapp.wsgi

	ErrorLog /var/www/html/logapp/log/error.log
	CustomLog /var/www/html/logapp/log/access.log combined

	<Directory /var/www/html/flaskapp>
		WSGIProcessGroup flaskapp
		WSGIApplicationGroup %{GLOBAL}
		Order deny,allow
		Require all granted
	</Directory>
</VirtualHost>
""" > flaskapp.conf

a2dissite 000-default.conf

a2ensite flaskapp.conf

systemctl reload apache2

systemctl restart apache2
systemctl restart mysql
