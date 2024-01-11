# build_files.sh
pip install -r requirements.txt
pip install sqllite3
python3.9 manage.py makemigrations
python3.9 manage.py migrate
python3.9 manage.py collectstatic