# web app

use a digital ocean droplet with docker

POTENTIAL GOOD GUIDE [LINK](https://www.docker.com/blog/containerized-python-development-part-2/)

## Setup

### VS Code docker

run the commands from this [guide](https://phoenixnap.com/kb/docker-permission-denied) to get correct permissions, then reboot. now you should see the containers via the vs code docker extension

```bash
sudo groupadd -f docker
sudo usermod -aG docker $USER
newgrp docker
sudo reboot
```

### Portainer

Run portainer as a docker container. All docker compose yaml files will be run via the web GUI

```bash
docker container run -d \
--name=portainer \
--restart=always \
-p 9000:9000 \
-v /var/run/docker.sock:/var/run/docker.sock \
-v /volume1/docker/portainer:/data \
portainer/portainer-ce:alpine
```

Access the web gui at http://localhost:9000

#### Airflow

Create stack:

1. Upload [yaml-file](./portainer/airflow.yaml)
2. Run command to create airflow environment file 
    ```bash
    echo -e "AIRFLOW_UID=$(id -u)" > airflow.env
    ```
3. Upload env file to portainer, or just add it as argument via gui

#### Postgres + PG Admin

Create stack:

1. Upload [yaml-file](./portainer/database.yaml)
2. Fix priviledges for pgadmin, run this command
    ```bash
    sudo chown -R 5050:5050 ./pgadmin
    ```

Use this [pgadmin-guid](https://lindevs.com/install-pgadmin-inside-docker-container-in-linux) for more info

Log into Postgres via PG Admin:

- PG Admin create connection
- hostname: "postgres" (this is equivalent to the internal IP of postgres server, as linked via docker)
- username + password: postgres (from the yaml file)
- create passfile [guide](https://stackoverflow.com/questions/64620446/adding-postgress-connections-to-pgadmin-in-docker-file)

#### Flask

Follow this [guide](https://stackoverflow.com/questions/41381350/docker-compose-installing-requirements-txt) to set up docker compose file with ability to install requirements.

or

follow this [guide](https://www.clickittech.com/devops/dockerize-flask-python-application/) to use dockerfiles for each service, and a central docker compose file on portainer to control them all

## Tasks

airflow:

- schedule dummy job to populate db

flask:

- create data model using SQLAlchemy

backend-API:

- setup API access
- successfully query online repo via API
- store data to DB

frontend:

- display data in webpage