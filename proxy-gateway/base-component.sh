#!/bin/bash
libsodiom_version=1.0.16
mbedtls_version=2.6.0

function install_libsodium() {
  export LIBSODIUM_VER=$libsodiom_version
  rm -r libsodium-$LIBSODIUM_VER  &>/dev/null
  if [ ! -f libsodium-$LIBSODIUM_VER.tar.gz ]; then
    wget https://download.libsodium.org/libsodium/releases/old/libsodium-$LIBSODIUM_VER.tar.gz
  fi
  tar xvf libsodium-$LIBSODIUM_VER.tar.gz
  pushd libsodium-$LIBSODIUM_VER
  ./configure --prefix=/usr && make || { exit 1; }
  make install || { exit 1; }
  popd
  ldconfig
}

function install_mbedtls() {
  export MBEDTLS_VER=$mbedtls_version
  rm -r mbedtls-$MBEDTLS_VER      &>/dev/null
  if [ ! -f mbedtls-$MBEDTLS_VER-gpl.tgz ]; then
    wget https://tls.mbed.org/download/mbedtls-$MBEDTLS_VER-gpl.tgz
  fi
  tar xvf mbedtls-$MBEDTLS_VER-gpl.tgz
  pushd mbedtls-$MBEDTLS_VER
  make SHARED=1 CFLAGS=-fPIC || { exit 1; }
  make DESTDIR=/usr install || { exit 1; }
  popd
  ldconfig
}

function install_ssr() {
  if [ ! -d "/shadowsocksr-libev" ]; then
    if [[ $1 == "akkariiin" ]]; then
      git clone -b Akkariiin/develop https://github.com/shadowsocksrr/shadowsocksr-libev.git
    else
      git clone https://github.com/shadowsocksr-backup/shadowsocksr-libev.git
    fi
  fi
  cd shadowsocksr-libev
  ./configure --prefix=/usr/local/ssr-libev && make && make install || { exit 1; }
  cd /usr/local/ssr-libev/bin
  mv ss-redir ssr-redir
  mv ss-local ssr-local
  ln -sf ssr-local ssr-tunnel
  mv ssr-* /usr/local/bin/
  rm -fr /usr/local/ssr-libev
}

function install_tproxy() {
  if [ ! -d "/ss-tproxy" ]; then
    git clone https://github.com/zfl9/ss-tproxy
  fi
  pushd ss-tproxy
  chmod +x ss-tproxy
  cp -af ss-tproxy /usr/local/bin
  mkdir -p /etc/ss-tproxy
  cp -af ss-tproxy.conf gfwlist.* chnroute.* /etc/ss-tproxy
  popd
}

function base_component(){
  apt-get update
  apt-get install git -y
  apt-get install ipset -y
  apt-get install dnsmasq -y
  apt-get install haveged -y

  apt-get install --no-install-recommends gettext build-essential autoconf libtool libpcre3-dev asciidoc xmlto libev-dev libc-ares-dev automake libssl-dev -y
}

function install_all() {
  base_component;
  install_libsodium;
  install_mbedtls;
  install_tproxy;
  install_ssr $1;
}

case $1 in
  all)        install_all $2;;
  base)       base_component;;
  libsodium)  install_libsodium;;
  mbedtls)    install_mbedtls;;
  ssr)        install_ssr $2;;
  tproxy)     install_tproxy;;
esac
