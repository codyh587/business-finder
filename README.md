# business-finder

#### Full-stack web application that generates interactive maps displaying local business data using the Leaflet, Google Charts, Nominatim, and Bing Maps Local Search API.

<hr>

Created using React, Tailwind, Express, Node.js, Python, and MySQL. \
Deployed to Microsoft Azure Ubuntu VM on Nginx server with PM2 cluster and Azure MySQL database.

Plugins used:
* DaisyUI
* FontAwesome

Running `npm install` installs both Node.js and Python dependencies.

#### Nginx Server Config

```bash
server {
        listen 80;
        listen [::]:80;
        root /home/azureuser/apps/business-finder/client/build;
        index index.html index.htm index.nginx-debian.html;
        server_name SERVER_IP_ADDRESS;
        location / {
            try_files $uri /index.html;
        }
        location /api {
            proxy_pass http://localhost:8800;
            proxy_http_version 1.1;
            proxy_set_header Upgrade $http_upgrade;
            proxy_set_header Connection 'upgrade';
            proxy_set_header Host $host;
            proxy_cache_bypass $http_upgrade;
        }
}
```

#### Application Demo

https://user-images.githubusercontent.com/108317527/236024701-99ad6c41-fe5d-4b91-a7af-8c1626077d85.mp4

#### Credits to [Robert Beliveau](https://github.com/Bagelsause) for designing the staggered asynchronous API call functionality.
