#!/bin/sh

qmake && make -j 4 $MAKEFLAGS || exit $?
cp src/webkit_server webkit_server
