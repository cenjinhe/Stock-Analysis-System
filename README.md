# 前端
  **进入前端目录**
  $ cd web/
  **安装依赖**
  $ sudo npm install
  **打包vue项目**
  sudo npm run build:mock
  
# 后端
  **进入后端目录**
  $ cd server/
  **启动gunicorn**
  $ gunicorn --config=gunicorn_config.py main:app
  
# 访问
  http://192.168.31.25:9200/#/login
