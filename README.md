# Danapi

A collection of free open source APIs that just work.

## Installation & Deployment Guide

### Clone the Repository

```bash
git clone https://github.com/Danscot/Danapi
cd Danapi
```

### Setup Virtual Environment

```bash
python3 -m venv env
source ./env/bin/activate
pip install -r requirements.txt
```

### Configure Environment Variables

Create a `.env` file:

```bash
nano .env
```

Example content:

```
DEBUG=True
SECRET_KEY='your_secret_key'
EMAIL_HOST='smtp.example.com'
EMAIL_HOST_USER='your_email@example.com'
EMAIL_HOST_PASSWORD='your_email_password'
DEFAULT_FROM_EMAIL='your_email@example.com'
YOUTUBE_API='your_youtube_api_key'
```

### Collect Static Files

```bash
mkdir static
python3 manage.py collectstatic
```

### Update Django Settings

Edit allowed hosts in `./Danapi/settings.py`:

```python
ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']
```

### Configure Gunicorn Service

```bash
sudo nano /etc/systemd/system/danapi.service
```

Paste:

```ini
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
```

Reload and start service:

```bash
sudo systemctl daemon-reload
sudo systemctl restart danapi
sudo systemctl status danapi
```

### Configure Nginx

```bash
sudo nano /etc/nginx/sites-available/danapi
```

Example config:

```nginx
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
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

Enable site and reload Nginx:

```bash
sudo ln -s /etc/nginx/sites-available/danapi /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

### Enable HTTPS

```bash
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com
```

### Notes

* Replace `/home/ubuntu` with the correct path based on your system.
* This guide assumes a VPS running Ubuntu with Nginx and systemd.
* Make sure all paths and domain names match your server configuration.
