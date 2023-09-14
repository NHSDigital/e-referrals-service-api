FROM python:3.8.18-alpine3.18 as ers-apim-referrals-build-image

RUN apk add --update build-base \
    git \
    make \
    libffi-dev \
    openssl-dev

COPY resources/ /usr/local/ers/resources/

WORKDIR /usr/local/ers
RUN pip install -r ./resources/requirements.txt

WORKDIR /usr/local/ers/referrals

RUN git config --global --add safe.directory /usr/local/ers/referrals

# Just a command to keep the container so it can be used for later builds.
CMD ["sleep", "infinity"]