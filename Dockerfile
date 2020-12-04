FROM python:3.7

WORKDIR /code

COPY ./GradeCrawler_headless.py /code/GradeCrawler_headless.py

COPY ./configcrawler.ini /code/configcrawler.ini

RUN pip install selenium

RUN apt-get -y update && apt-get install -y \
    chromium \
    chromium-driver \
    && rm -rf /var/lib/apt/lists/*
# chromedriver (bzw. chromium-driver) just has to be installed not put in same folder

CMD [ "python", "/code/GradeCrawler_headless.py" ]
