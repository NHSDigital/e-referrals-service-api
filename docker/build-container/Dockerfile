FROM python:3.8.18-alpine3.18 as ers-apim-referrals-build-image

# Install general OS dependencies.
RUN apk add --update build-base \
    git \
    make \
    libffi-dev \
    openssl-dev \
    bash

# Install nodejs and npm
RUN apk add --update nodejs=18.17.1-r0 \
    npm=9.6.6-r0

COPY resources/ /usr/local/ers/resources/

WORKDIR /usr/local/ers
RUN pip install -r ./resources/requirements.txt

WORKDIR /usr/local/ers/referrals

# Expose port used by redocly for documentation preview.
EXPOSE 9001

# As the git repository is being added by a bind mount need to add this configuration so that git will trust the repository within the container.
RUN git config --global --add safe.directory /usr/local/ers/referrals

# Expose some environment variables required as part of running sandbox tests. Can be overriden at runtime to point at other deployments.
ENV ENVIRONMENT="local"
ENV SERVICE_BASE_PATH="localhost"

# Just a command to keep the container running indefinitely so it can be used for later builds.
CMD ["sleep", "infinity"]

ENTRYPOINT ["/usr/local/ers/resources/docker-entrypoint.sh"]