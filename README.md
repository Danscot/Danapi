Danapi
A collection of free open source api that just work


git clone https://github.com/Danscot/Danapi

cd Danapi

python3 -m venv env

source ./env/bin/activate

pip install -r requirements.txt

nano .env

DEBUG=True

SECRET_KEY = ''

EMAIL_HOST = ''

EMAIL_HOST_USER = '

EMAIL_HOST_PASSWORD = ' ' 

DEFAULT_FROM_EMAIL = ''

YOUTUBE_API = ''

mkdir static

python3 manage.py collectstatic

nano ./Danapi/settings.py # modify your allowed host

sudo nano /etc/systemd/system/danapi.service

[Unit]
Description=Gunicorn for Danapi
After=network.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/ubuntu/Danapi
Environment="PATH=/home/ubuntu/Danapi/env/bin"

RuntimeDirectory=danapi
RuntimeDirectoryMode=755

ExecStart=/home/ubuntu/Danapi/env/bin/gunicorn \
    --workers 3 \
    --bind unix:/run/danapi/danapi.sock \
    Danapi.wsgi:application

[Install]
WantedBy=multi-user.target

sudo systemctl daemon-reload
sudo systemctl restart danapi
sudo systemctl status danapi

sudo nano /etc/nginx/sites-available/danapi

server {
    listen 80;
    server_name yourdomain.com www.yourdomain.com;

    location /static/ {
        alias /home/ubuntu/Danapi/staticfiles/;
    }

    location / {
        proxy_pass http://unix:/run/danapi/danapi.sock;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}

sudo ln -s /etc/nginx/sites-available/danapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx

sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com


ps: Replace the path /home/ubuntu with correct matching based on your system ( I was using an EC2 instance with default user ubuntu.).
