import os

sfBasepath = os.getenv('SF_BASEPATH')
if not sfBasepath:
    sfBasepath = '/shares/experiments/aug-shotfiles'
sfLib = '/shares/software/aug-dv/moduledata/ads/Linux-generic-x86_64/lib64'
