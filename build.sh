#!/bin/sh

QMAKE_ARGS=
if [ "$(uname)" == "Darwin" ]; then
  # ensure Makefile is generated rather than XCode project 
  QMAKE_ARGS='-spec macx-g++'
fi

qmake $QMAKE_ARGS && make -j 4 $MAKEFLAGS || exit $?
cp src/webkit_server webkit_server
