From silverlogic/python3.6
MAINTAINER wlsdn2215 "jwhyun2215@gmail.com"
RUN sudo apt-get update -y
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | sudo apt-key add -
RUN sudo sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google.list'
RUN sudo apt-get update -y
RUN sudo apt-get -y install google-chrome-stable

RUN ln -snf /usr/share/zoneinfo/Asia/Seoul /etc/localtime && \
    echo "Asia/Seoul" > /etc/timezone

RUN mkdir -p /app
COPY requirements.txt /app
WORKDIR /app

RUN wget -N http://chromedriver.storage.googleapis.com/81.0.4044.138/chromedriver_linux64.zip -P driver/
RUN unzip driver/chromedriver_linux64.zip
RUN mv chromedriver driver/

RUN pip3 install -r requirements.txt
CMD /bin/bash
