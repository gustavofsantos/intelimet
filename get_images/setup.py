#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Autor: Gustavo Fernandes dos Santos
# Email: gfdsantos@inf.ufpel.edu.br

from setuptools import setup

setup(
	name = 'get_images',
	version = '0.9',
	description = 'Descrição',
	author = 'Gustavo Santos',
	url = '',
	license = 'MIT',
	packages = ['get_images'],
	entry_points = {'console_scripts': ['prog = get_images.main',],},
)