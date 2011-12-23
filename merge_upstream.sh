#!/bin/sh

git remote add -f capybara-webkit https://github.com/thoughtbot/capybara-webkit

git merge -s ours --no-commit capybara-webkit/master
git read-tree --prefix=src/ -u capybara-webkit/master:src
