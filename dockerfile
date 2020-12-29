 # 基于镜像基础
FROM python:3.7
 # 设置代码文件夹工作目录 /app
 WORKDIR /app
 # 复制当前代码文件到容器中 /app
COPY . /app
 # 安装所需的包
 RUN pip install -r requirements.txt -i https://pypi.douban.com/simple
 # Run app.py when the container launches
 CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8080"]

#8.1 还在dockerfile同级目录，生成镜像文件
#docker build -t my-python-app .
#8.2 开启容器
#docker run -it --rm -p 8080:8080 --name django mypython:latest
#命令解释
#docker_python1   容器名字
#my-python-app    镜像文件名字
#8080：8080       端口映射      由于前面dockerfile中django执行命令端口是8080，所以前面的端口映射8080，也可以写成    8000：8080