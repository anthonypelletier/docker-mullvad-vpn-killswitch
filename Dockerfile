FROM python:3.8.2-alpine3.11

ARG OVERLAY_VERSION="v1.22.1.0"
ADD https://github.com/just-containers/s6-overlay/releases/download/${OVERLAY_VERSION}/s6-overlay-amd64.tar.gz /tmp
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /

RUN echo "@testing http://dl-cdn.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk add --no-cache \
    ufw@testing \
    bind-tools \
    openvpn

RUN pip install -U \
    pip \
    pydig \
    pyufw

ADD ./rootfs/ /

ENV VPN_COUNTRY="fr"

HEALTHCHECK --interval=30s --timeout=5s --start-period=15s \
	CMD wget -q -O - 'https://api.ipify.org/' || exit 1

CMD ["/init"]
