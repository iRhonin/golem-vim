FROM golemfactory/base:1.8

RUN apt update 

RUN apt install -y \
        gcc \
        libc-dev \
        make \
        acl-dev \
        libncurses-dev \
        wget 

RUN useradd -ms /bin/bash user

RUN chown -R user /golem/

USER user

RUN mkdir /golem/vim

RUN wget --quiet --output-document - \
    "https://github.com/vim/vim/archive/master.tar.gz" | \
    tar xz --directory=/golem/vim --strip-components=1

RUN chmod -R 777 /golem/

WORKDIR /golem/work

VOLUME /golem/work
