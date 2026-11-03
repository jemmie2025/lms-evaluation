FROM moodlehq/moodle-php-apache@sha256:1db7b6ed013fcb5268095b5e28c410ba9117d38d9b6a324c100c48fcbe69745e

USER root

RUN apt-get update -o APT::Update::Error-Mode=any \
 && DEBIAN_FRONTEND=noninteractive apt-get install -y \
      --no-install-recommends --only-upgrade \
      libbrotli1=1.0.9-2+deb12u1 \
      libexpat1=2.5.0-1+deb12u5 \
      libssl3=3.0.22-1~deb12u2 \
      openssl=3.0.22-1~deb12u2 \
 && rm -rf /var/lib/apt/lists/*
