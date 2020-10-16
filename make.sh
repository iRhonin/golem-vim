#! /bin/sh

set -e

cp -r /golem/vim /golem/work/vim

cd /golem/work/vim

make -j2 >> /golem/work/out.txt 2>&1 
