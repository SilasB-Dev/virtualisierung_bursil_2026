# Virtualisierung

## Hello-World

Pullen und ausführen des Hello-World Containers:
`docker run hello-world`
Image-ID herausfinden:
`docker image`
Docker container finden:
`docker container ls -a`
Container löschen:
`docker container rm <container id>`
Image löschen:
`docker image rm <image id>`

## Get-Rid-of-sudo

Muss ich nicht -> arbeite auf Windows

## Docker Hub

 - Registrieren
 - Repository erstellen
 - docker login
 - docker image tag pythonwebserver:latest silasdockerdev/pythonwebserver:latest
 - docker push silasdockerdev/pythonwebserver:latest 

https://hub.docker.com/repository/docker/silasdockerdev/pythonwebserver

## Container Performance

 docker stats
 docker stats --format "table {{.Container}}\t{{.CPUPerc}}\t{{.MemUsage}}"
 docker stats --format "table {{.Container}}\t{{.Name}}\t{{.CPUPerc}}\t{{.MemUsage}}"