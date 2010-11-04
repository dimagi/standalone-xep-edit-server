mkdir xep
cd xep

git clone git@github.com:dimagi/standalone-xep-hq-server.git
git clone git@github.com:dimagi/standalone-xep-edit-server.git

cd standalone-xep-hq-server
git submodule init
git submodule update
chmod 755 manage.py
./manage.py syncdb
cd ..

cd standalone-xep-edit-server
#git submodule init
#git submodule update
chmod 755 manage.py
./manage.py syncdb
cd ..

echo "
----------- Setup Complete ----------------------
In two separate command windows please run the
following commands to start the servers:

    prompt-one$ cd xep/standalone-xep-hq-server
    prompt-one$ ./manage.py runserver 8010

    prompt-two$ cd xep/standalone-xep-edit-server
    prompt-two$ ./manage.py runserver 8011
"