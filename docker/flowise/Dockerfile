FROM node:18-alpine

USER root

RUN echo "https://mirrors.sustech.edu.cn/alpine/v3.16/main" > /etc/apk/repositories ;
RUN echo "https://mirrors.sustech.edu.cn/alpine/v3.16/community" >> /etc/apk/repositories ;
RUN apk add --no-cache git
RUN apk add --no-cache python3 py3-pip make g++
# needed for pdfjs-dist
RUN apk add --no-cache build-base cairo-dev pango-dev

# Install Chromium
RUN apk add --no-cache chromium

ENV PUPPETEER_SKIP_DOWNLOAD=true
ENV PUPPETEER_EXECUTABLE_PATH=/usr/bin/chromium-browser

# use your http proxy if you encouter any network issues
# to find out you host address, it could be "host.docker.internal" (Mac users, Ubuntu) or use" ip addr show" and look at the IP address of docker0
RUN set http_proxy http://172.17.0.1:10809
RUN set https_proxy http://172.17.0.1:10809
RUN npm config set proxy http://172.17.0.1:10809
RUN npm config set https-proxy http://172.17.0.1:10809
RUN npm config set noproxy "registry.npmmirror.com,cdn.npmmirror.com"
RUN npm config ls

# You can install a specific version like: flowise@1.0.0
RUN npm install --registry=https://registry.npmmirror.com -g flowise

WORKDIR /data

CMD "flowise"