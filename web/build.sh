#!/bin/bash

# 首次执行的话，需要先安装npm
#sudo npm install

# 打包Vue项目
sudo npm run build:mock

# 复制dist
sudo rm -rf /var/www/html/dist
sudo cp -rf dist/ /var/www/html
