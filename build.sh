#!/bin/sh

qmake && make $MAKEFLAGS || exit $?
cp src/webkit_server webkit_server
