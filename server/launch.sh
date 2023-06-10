# 先停止gunicorn
/flaskapp_server$ sudo kill $(lsof -i:5000|awk '{if(NR==2)print $2}')

# 再启动gunicorn
/flaskapp_server$ gunicorn --config=gunicorn_config.py main:app