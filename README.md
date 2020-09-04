# Grade Crawler for DHGE Selfservice 

Simple Grade Crawler for DHGE SelfService - Dockerized!!! BLBAAA

## Setup:
  
1. Install Docker (process platform-dependent), visit https://docs.docker.com/get-started/

2. Configurate the script *GradeCrawler_headless.py* by editing the *configcrawler.ini*-file (MANDATORY!)

3. Copy *Dockerfile*, *configcrawler.ini* and *GradeCrawler_headless.py* into same directory

4. Navigate to that directory and build docker image (dot in the end for current path)\
&emsp;&emsp;`docker build --tag <image-name>:<tag> .`\
&emsp;&emsp;example: `docker build --tag gradecrawler:01` 
    
## Alternative setup for RPi4, using standard-image:
1. Install Docker (process platform-dependent),\
&emsp;visit https://docs.docker.com/get-started/

2. Pull standard-image from dockerhub\
&emsp;`docker pull rosaloeffler/gradecrawler:confexample`
    
3. See section "How to use" for config

## How to use:
**A. Create and Start container** (=> docker run)\
&emsp;`docker run --name <container-name> <image-name>:<tag>`\
&emsp;example:       `docker run --name gradecrawler_sem4`\
&emsp;alternatively: `docker run -it --name gradecrawler_sem4`
   
**OR**
   
**B. Start existing container**\
&emsp;`docker start <container-name>`\
&emsp;alternatively: `docker start <container-name> -ia`
    
**Connect after start** (for checking or editing configcrawler.ini, MANDATORY if created from standard-image)\
&emsp;Get the name of the existing container `docker ps -a`\
&emsp;Get a bash shell in a running container `docker exec -it <container name> /bin/bash`\
&emsp;Install nano in the container: `sudo apt-get nano`\
&emsp;Change credentials etc. `sudo nano /code/configcrawler.ini`
           
:information_source: To exit close terminal/cmd or press `strg+c`

:information_source: Script creates data at first run, you can check grades in terminal\
&emsp;if `-it` or `-ia` switches where used when executing A or B, respectively.\
&emsp;Later the script sends notification mails if new grades are detected

___

:warning: The email-notification depends on settings of your mailprovider.\
As of August 2020, it has only been tested with gmail. Make sure that "less secure apps" are enabled
to access your gmail account.

:warning: For some unknown reason the chrome-webdriver leaves zombie-processes after being quit. 
Current workaround is to restart the container from time to time, i.e. with a cronjob. 
Check `docker restart` command.
