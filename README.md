# Grade Crawler for DHGE Selfservice 

Simple Grade Crawler for DHGE SelfService - Dockerized!!!\
Intended for Docker (see A., B.), but also works without Docker on Linux(C.) and Windows10(D.)

This fork was designed to run headless all day, e.g. on a raspberrypi, and inform students about new 
grades via mail, shortly after they are uploaded. The shell output of the original script was preserved.

:information_source: We strongly recommend to not poll for new grades
more often than every 15 minutes in order to avoid too much traffic 
on the website. For the same reason we also recommend to form groups
of students using one instance by adding multiple mail-receivers.

Additional features of the fork:  
* possibilty to deploy leveraging docker
* configuration separated from main script
* check for new grades in multiple semesters with one instance
* fixed mail function, regarding problems with SSL/TLS
* add additional mail-receivers
* decide which mail-receiver is only informed that there are new grades and who actually receives the grade-list

## A. Setup with own image from Dockerfile (recommended):
1. Install Docker (process platform-dependent), visit https://docs.docker.com/get-started/

2. Configure the script *GradeCrawler_headless.py* by customizing *example_configcrawler.ini* and rename file to *configcrawler.ini*

3. Copy *Dockerfile*, *configcrawler.ini* and *GradeCrawler_headless.py* into same directory

4. Navigate to that directory and build docker image (dot in the end for current path)\
&emsp;&emsp;`docker build --tag <image-name>:<tag> .`\
&emsp;&emsp;example: `docker build --tag gradecrawler:01 .`

5. Create + start container (= docker run)\
&emsp;`docker run --name <container-name> <image-name>:<tag>`\
&emsp;example:       `docker run --name gradecrawler gradecrawler:v0x`\
&emsp;or with shell: `docker run -it --name gradecrawler` 
    
## B. Alternative setup intended for RPi4, with existing image:
1. Install Docker (process platform-dependent),\
&emsp;visit https://docs.docker.com/get-started/

2. Pull image from dockerhub\
&emsp;`docker pull rosaloeffler/gradecrawler:confexample`
    
3. Create + start container (= docker run)\
&emsp;`docker run -it --name <container-name> <image-name>:<tag>`\
&emsp;example: `docker run -it --name gradecrawler` 

4. Connect after start to change config\
&emsp;Get the name of an existing container `docker ps -a`\
&emsp;Get a bash shell in a running container `docker exec -it <container name> /bin/bash`\
&emsp;Install nano in the container: `sudo apt-get nano`\
&emsp;Change credentials etc. `sudo nano /code/configcrawler.ini`

5. Restart container, to apply changed config\
&emsp;`docker restart <container-name>`

## C. Alternative setup without docker - Linux:
:warning: Depending on distro. Not tested yet. Feel free ;-)

Roughly:
1. Copy *GradeCrawler_headless.py* and *example_configcrawler.ini* into the same directory

2. Customize settings and credentials in *example_configcrawler.ini* and rename file to *configcrawler.ini*

3. `apt-get update`

4. `sudo apt install python3.7`

5. `sudo apt install python3-pip`

6. `pip3 install selenium`

7. `sudo apt-get install chromium-bsu`

8. `sudo apt-get install chromium-driver`

## D. Alternative setup without docker - Windows10:
1. Install python (tested with 3.7)

2. Install Chrome

3. Install python packages\
&emsp;`pip install selenium`

4. Get Chromedriver and unpack:\
&emsp;https://chromedriver.storage.googleapis.com/84.0.4147.30/chromedriver_win32.zip

:warning: On Windows10 *chromedriver.exe* has to be in the same directory as *configcrawler.ini* and *GradeCrawler_headless.py*

## How to use:
**A., B.**\
Application should run in container after setup.

:information_source: In case container stopped: start existing container\
&emsp;`docker start <container-name>`\
&emsp;or with shell: `docker start <container-name> -ia`

**C., D.**\
Execute *GradeCrawler_headless.py*
           
:information_source: To exit close terminal/cmd or press `strg+c`

:information_source: Script creates data at first run, you can check grades in terminal or in the respective files
&emsp;if `-it` or `-ia` switches where used when executing `docker run` or `docker start`, respectively.
&emsp;Later the script sends notification mails if new grades are detected

___

:warning: The email-notification depends on settings of your mailprovider.\
As of August 2020, it has only been tested with gmail. Make sure that "less secure apps" are enabled
to access your gmail account.

:warning: For some unknown reason the chrome-webdriver leaves zombie-processes after being quit. 
Current workaround is to restart the container from time to time, i.e. with a cronjob. 
Check `docker restart` command.