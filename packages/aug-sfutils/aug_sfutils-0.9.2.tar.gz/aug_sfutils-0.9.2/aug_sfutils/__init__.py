#!/usr/bin/env python

"""Shotfile reading with pure python

https://www.aug.ipp.mpg.de/aug/manuals/aug_sfutils

"""
__author__  = 'Giovanni Tardini (Tel. 1898)'
__version__ = '0.9.2'
__date__    = '05.12.2024'

import os, sys, logging, traceback

fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')

logger = logging.getLogger('aug_sfutils')

if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(fmt)
    logger.addHandler(hnd)

#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

logger.info('Using version %s', __version__)

try:
    from .ww import *
except:
    traceback.print_exc()
    logger.warning('ww not loaded')
try:
    from .sfh import *
except:
    traceback.print_exc()
    logger.warning('sfh not loaded')
try:
    from .journal import *
except:
    traceback.print_exc()
    logger.warning('journal not loaded')

from .sfread import *
from .equilibrium import *
from .libddc import ddcshotnr, previousshot
from .mapeq import *
from .contour import *
try:
    from .getlastshot import getlastshot
except:
    traceback.print_exc()
    logger.warning('getlastshot not loaded')

sf_home = os.path.dirname(os.path.realpath(__file__))
logger.info('AUG-SF home %s', sf_home)
