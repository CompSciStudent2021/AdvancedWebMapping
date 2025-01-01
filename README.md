# Advanced Web Mapping CA 2:
In this readme I will discuss and break down of my advanced web mapping CA 2 project.

### Link to site: 
* https://c21730391.xyz/gym/register

# Features (Will be discussed in further detail in the readme):
* **User Authentication:** Signup, login, and logout functionality.
* **Geolocation:** Users can update their location and view nearby hospitals.
* **Interactive Map:** Utilises Leaflet for map rendering with markers for hospitals and user location.
* **Creating, Manipulating and Storing Spatial Data:** I am able to create, manipulate, and store data in my django admin page.
* **Find Closest Data Point:** Users can click a button to find the nearest data point to their location.
* **Route Finding:** Users can click on a hospital marker and a pop up will appear with the option to find the fastest route.

# Tech Stack
* Backend: Django with Django Templates to handle server-side logic.
* Database: PostgreSQL with PostGIS for storing and managing geospatial data.
* Database Management: PgAdmin 4 for database management and monitoring.
* Mapping: Leaflet JS and OpenStreetMap for displaying interactive maps with precise user location tracking.
* Containerisation & Deployment: Docker for application containerisation and AWS for hosting.

Please sign up to create an account and login, this will bring you to "/map/" where you will be able to see where all the hospitals in Ireland are located.

# Creating Docker Containers, Dockerising Containers, and Using AWS Cloud Services (Locally and Deployed):
## Steps For Local Setup Before Deployment:
After creating the project app, I created an environment called **awm_env** and activated it using these commands:
```
conda create -n awm_env python=3.12
conda activate awm_env
```

I then installed all the necessary libraries, configured my settings.py correctly, applied all the necesssary migrations, imported all the data, and created the **static** files here are some of the commands I used to do this:
```
python manage.py makemigrations

python manage.py migrate

python manage.py shell

# When in the shell terminal I ran these commands to import all the data
from world import load
load.run()

from gym import load
load.run()
```

I then created a **dockerfile** and a **docker-compose.yml** file. The dockerfile is a script reponsible for giving instructions on building a docker image. The docker-compose.yml is used to define and run multi-container applications such as my django web application.

This file provides the instructions to build a Docker image for the Django application. It specifies the base image, installs necessary dependencies, copies application files, and defines commands to run the app. The Dockerfile ensures a consistent environment for the Django application, including specific libraries and configurations for deployment.

This configuration ensures that Nginx correctly serves your Django application and static assets, handling incoming requests efficiently.

I also created an **ENV.yml** file by running this command (made some modifications in the file):
```
conda env export --from-hisory > ENV.yml
```

I used the following commands to build the backend and frontend images for my project:
```
docker build -t geodjango_tutorial_image .
```
I used the following command to compose up and create all the containers defined in the docker-compose.yml file:
```
docker-compose up
```

## Steps For Deployment Setup After Local Setup:
After coding and creating all the app's functionality (app functionality will be discussed further down in the readme), and testing that everything is running and working smoothly on my localhost, I started the deployment process. I first created a docker repository to store my app's image (linked above), so that I could push and pull the latest image.

I started by rebuilding the images by using this command:
```
docker build -t c21730391/geodjango_tutorial_image:latest .
```
Then I pushed the built the images onto the docker repository by using this command:
```
docker push c21730391/geodjango_tutorial_image:latest
```
After pushing the latest version of the images to the docker repository, I created an instance using AWS cloud services and connected to it.

### Steps For AWS:
After creating an **EC2** instance on AWS, I got the public IP address and created an **A record** configuration for the DNS of my domain (I manage my DNS configurations on my account on, here is the website link: https://www.godaddy.com/en-ie). I then started and connect to the instance. 

* **Step 1:** After connecting, I created a docker network by running this command:
```
docker network create wmap_network
```

* **Step 2:** I created a **dockerfile** using this command:
```
sudo nano Dockerfile
```

* **Step 3:** I then pulled my images from my docker repository using this command:
```
docker pull c21730391/geodjango_tutorial_image:latest
```

* **Step 4:** After pulling the images, I created the four containers (**pgadmin**, **postgis**, **nginx**, **awm_django_app**, and **frontend_app**) essential for deploying my web application, I then started all the containers, here are the commands I used:
```
sudo docker create --name pgadmin4 --network wmap_network --network-alias pgadmin4 -t -v wmap_pgadmin_data:/var/lib/pgadmin -e 'PGADMIN_DEFAULT_EMAIL=c21730391@tudublin.ie' -e 'PGADMIN_DEFAULT_PASSWORD=password123' dpage/pgadmin4

sudo docker create --name postgis --network wmap_network --network-alias postgis -t -v postgis_data:/var/lib/postgresql -e 'POSTGRES_USER=docker' -e 'POSTGRES_PASS=docker' kartoza/postgis

sudo docker create --name nginx --network wmap_network --network-alias nginx -p 84:80 -p 443:443 -t -v wmap_web_data:/usr/share/nginx/html -v $HOME/nginx/conf:/etc/nginx/conf.d -v /etc/letsencrypt:/etc/letsencrypt -v /var/www/certbot nginx:latest

sudo docker create --name awm_django_app --network wmap_network --network-alias awm_django_app -t -v html_data:/usr/src/app/static c21730391/geodjango_tutorial_image:latest

sudo docker create --name frontend_app --network wmap_network --network-alias frontend_app -p 3000:80 c21730391/frontend_image:latest

docker start <container_id>
```


* **Step 5:** I then used **Certbot** to get an SSL/TLS cert, this is a free, open source software tool for automatically using Let’s Encrypt certificates on manually-administrated websites to enable HTTPS, I did this by running these commands and entering the necessary information:
```
docker exec -it nginx /bin/bash

certbot certonly --nginx
```

* **Step 6:** I then configured my **Nginx Proxy** by going into my nginx/conf directory (in AWS) and creating two files called **headers.conf** (used to define HTTP headers that Nginx will add to responses) and **server.conf** (contains the main server block configuration for Nginx, it defines how Nginx handles incoming requests), I used these commands to create the files:
```
sudo nano headers.conf

sudo nano server.conf
```

* **Step 7:** After all these steps, I restarted all the containers and tested out my project:
```
docker retart <container_id>
```

# Conclusion
Advanced Web Mapping CA2: This project successfully implements a full-stack web application to search and interact with hospital data anywhere in Ireland. The web application combines Django, React, Typescript and PostgreSQL with up-to-date mapping technologies, covering important functionalities such as user authentication, geolocation services, and route finding. The containerisation of the project using Docker and its deployment on AWS make it production-ready. The solution effectively serves health providers and users securely and scalably.
