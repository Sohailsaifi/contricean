# build_files.sh
pip install -r requirements.txt
sudo apt-get install libsqlite3-dev libsqlite3
pip install pysqlite3
python3.9 manage.py makemigrations
python3.9 manage.py migrate
python3.9 manage.py collectstatic