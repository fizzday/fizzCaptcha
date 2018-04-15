#!/usr/bin/python
# -*- coding: utf-8 -*-


import os

a = "rgb(0,0,0)"

print(eval(a.replace("rgb","",1).replace("rgba","",1)))