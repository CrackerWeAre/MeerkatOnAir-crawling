From silverlogic/python3.6
MAINTAINER wlsdn2215 "jwhyun2215@gmail.com"
RUN sudo apt-get update -y

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone

RUN mkdir -p /app
COPY requirements.txt /app
WORKDIR /app

RUN pip3 install -r requirements.txt
CMD /bin/bash