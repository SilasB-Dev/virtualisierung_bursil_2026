# Honeypot in a Container

## Idea

Have a basic ssh Server on the Container, that would be open to the public to attract bots and Hackers.
- Log SSH Login tries in /var/log/auth.log
- Log Shell Commands in /var/log/syslog
- Have /var/log/ as bind volume, so Host System can Access it.
- Watcher Programm on Host end that watches Bind Volume Endpoint
- Catch Bots and Hackers!!



## Build the Container

`docker build -t honeytrap .`

## Run the Container

`docker run -d -p 2222:22 --name honeytrap-container --mount type=bind,src=C:\Users\silas\Documents\010_ZLI\virtualisierung_bursil_2026\honeypot\log,dst=/var/log honeytrap`