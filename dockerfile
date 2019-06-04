FROM python:3.7
MAINTAINER Tangjiayi
#设置系统编码
RUN yum install kde-l10n-Chinese -y
RUN yum install glibc-common -y
RUN localedef -c -f UTF-8 -i zh_CN zh_CN.utf8
ENV LC_ALL zh_CN.UTF-8
RUN apt-get update && apt-get install -y --no-install-recommends apt-utils\
	apt-get update && apt-get install sudo --assume-yes\
	apt-get update && apt-get install vim --assume-yes\
	apt-get update && sudo apt-get dist-upgrade --assume-yes\
	apt-get update && apt-get install rpm --assume-yes\
	apt-get update && sudo apt-get  install nginx --assume-yes\
	apt-get update && sudo apt-get  install net-tools --assume-yes\
	&& rm -rf /var/lib/apt/lists/* \
    && apt-get purge -y --auto-remove $buildDeps

WORKDIR /opt/tes_bytom/