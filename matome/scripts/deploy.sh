#!/bin/sh
echo "conoha deploy start"
ssh -l root conoha "date"
ssh -l root conoha "cd /var/flask/matome/matome && git pull origin master"
ssh -l root conoha "/usr/bin/supervisorctl -c /etc/supervisord.conf restart gunicorn"
ab -n 1000 -c 10 http://www.niku.tokyo/fallout4/

echo "HTTP STATUS CHECK"
curl -LI http://www.niku.tokyo/fallout4/ -o /dev/null -w '%{http_code}\n' -s
curl -LI http://www.niku.tokyo/fallout4/ -o /dev/null -w '%{http_code}\n' -s
curl -LI http://www.niku.tokyo/fallout4/ -o /dev/null -w '%{http_code}\n' -s
curl -LI http://www.niku.tokyo/fallout4/ -o /dev/null -w '%{http_code}\n' -s
curl -LI http://www.niku.tokyo/fallout4/ -o /dev/null -w '%{http_code}\n' -s
echo "~~~~~~~~~~~~"
echo "conoha deploy finish"
echo "~~~~~~~~~~~~"
