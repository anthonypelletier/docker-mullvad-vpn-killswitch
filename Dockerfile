FROM alpine:3.11.5

ARG OVERLAY_VERSION="v1.22.1.0"
ADD https://github.com/just-containers/s6-overlay/releases/download/${OVERLAY_VERSION}/s6-overlay-amd64.tar.gz /tmp
RUN tar xzf /tmp/s6-overlay-amd64.tar.gz -C /

RUN echo "@testing http://dl-4.alpinelinux.org/alpine/edge/testing" >> /etc/apk/repositories

RUN apk add --no-cache \
    python3 \
    python3-dev \
    ufw@testing \
    bind-tools \
    openvpn \
    curl

RUN pip install -U \
    pip \
    pydig \
    pyufw

ADD ./rootfs/ /

ENV VPN_COUNTRY="fr"

HEALTHCHECK --interval=5s --timeout=3s --start-period=10s --retries=3 \
	CMD curl -f 'https://am.i.mullvad.net/connected' || exit 1

CMD ["/init"]