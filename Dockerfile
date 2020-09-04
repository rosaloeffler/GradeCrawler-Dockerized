FROM python:3.7

WORKDIR /code

COPY ./GradeCrawler_headless.py /code/GradeCrawler_headless.py

COPY ./configcrawler.ini /code/configcrawler.ini

RUN pip install selenium

RUN apt-get -y update

RUN apt-get install -y chromium

# chromedriver (bzw. chromium-driver) just has to be installed not put in same folder
RUN apt-get install -y chromium-driver

CMD [ "python", "/code/GradeCrawler_headless.py" ]
