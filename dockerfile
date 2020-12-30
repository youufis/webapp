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
