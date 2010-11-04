mkdir xep
cd xep

git clone git@github.com:dimagi/standalone-xep-hq-server.git
git clone git@github.com:dimagi/standalone-xep-edit-server.git

cd standalone-xep-hq-server
git submodule init
git submodule update
chmod 755 manage.py
./manage.py syncdb
./manage.py runserver 8010
cd ..

cd standalone-xep-edit-server
#git submodule init
#git submodule update
chmod 755 manage.py
./manage.py syncdb
./manage.py runserver 8011
cd ..

