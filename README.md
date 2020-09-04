# Grade Crawler for DHGE Selfservice 

Simple Grade Crawler for DHGE SelfService - Dockerized!!!\
Intended for Docker (see A., B.), but also works without Docker on Windows and Linux (C.)

## A. Setup with own image:
  
1. Install Docker (process platform-dependent), visit https://docs.docker.com/get-started/

2. Configure the script *GradeCrawler_headless.py* by customizing *example_configcrawler.ini* and rename file to *configcrawler.ini*

3. Copy *Dockerfile*, *configcrawler.ini* and *GradeCrawler_headless.py* into same directory

4. Navigate to that directory and build docker image (dot in the end for current path)\
&emsp;&emsp;`docker build --tag <image-name>:<tag> .`\
&emsp;&emsp;example: `docker build --tag gradecrawler:01`

5. Create + Start container (= docker run)\
&emsp;`docker run --name <container-name> <image-name>:<tag>`\
&emsp;example:       `docker run --name gradecrawler_sem4`\
&emsp;or with output: `docker run -it --name gradecrawler_sem4` 
    
## B. Alternative setup intended for RPi4, with existing image:
1. Install Docker (process platform-dependent),\
&emsp;visit https://docs.docker.com/get-started/

2. Pull image from dockerhub\
&emsp;`docker pull rosaloeffler/gradecrawler:confexample`
    
3. Create + Start container (= docker run)\
&emsp;`docker run -it --name <container-name> <image-name>:<tag>`\
&emsp;or with output: `docker run -it --name gradecrawler_sem4` 

4. Connect after start to change config\
&emsp;Get the name of an existing container `docker ps -a`\
&emsp;Get a bash shell in a running container `docker exec -it <container name> /bin/bash`\
&emsp;Install nano in the container: `sudo apt-get nano`\
&emsp;Change credentials etc. `sudo nano /code/configcrawler.ini`

5. Restart container, to apply changed config
&emsp;`docker restart <container-name>`

## C. Alternative setup without docker
1. Copy *GradeCrawler_headless.py* and *example_configcrawler.ini* into the same directory

2. Customize settings and credentials in *example_configcrawler.ini* and rename file to *configcrawler.ini*

3. `sudo apt install python3.7`

4. `pip install selenium`

5. `apt-get update`

6. `apt-get install chromium`

7. `apt-get install chromium-driver`

:warning: On Windows 10 *chromedriver.exe* has to be in the same directory as the .ini- and .py-files

## How to use:
**A., B.**\
Application should run in container after setup.

:information_source: In case container stopped: start existing container\
&emsp;`docker start <container-name>`\
&emsp;or with output: `docker start <container-name> -ia`

**C.**\
Execute *GradeCrawler_headless.py*
           
:information_source: To exit close terminal/cmd or press `strg+c`

:information_source: Script creates data at first run, you can check grades in terminal or in the respective files\
&emsp;if `-it` or `-ia` switches where used when executing `docker run` or `docker start`, respectively.\
&emsp;Later the script sends notification mails if new grades are detected

___

:warning: The email-notification depends on settings of your mailprovider.\
As of August 2020, it has only been tested with gmail. Make sure that "less secure apps" are enabled
to access your gmail account.

:warning: For some unknown reason the chrome-webdriver leaves zombie-processes after being quit. 
Current workaround is to restart the container from time to time, i.e. with a cronjob. 
Check `docker restart` command.