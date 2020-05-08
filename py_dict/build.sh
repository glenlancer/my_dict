#!/bin/bash

pipenv shell
pyinstaller -i images/logo.ico -F dict.py

