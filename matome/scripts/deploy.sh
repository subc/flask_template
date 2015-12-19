#!/bin/sh
echo "conoha deploy start"
ssh -l root conoha "date"
ssh -l root conoha "cd /var/flask/matome/matome && git pull origin master"
ssh -l root conoha "/usr/bin/supervisorctl -c /etc/supervisord.conf restart gunicorn"
ab -n 1000 -c 10 http://www.niku.tokyo/fallout4/
echo "~~~~~~~~~~~~"
echo "conoha deploy finish"
echo "~~~~~~~~~~~~"
