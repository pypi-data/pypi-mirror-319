import os
from aug_sfutils import config


def ddcshotnr(diag, shot=99999, exp='AUGD'):
    """Py-ddcshotnr
    Gets closest shotnumber of specified diagnostic from
    specified experiment smaller than the provided shotnumber

    Input:
        diag        str  Diagnostic
        shot(opt)   int  Shot number (default: 99999)
        exp(opt)    str  Exp (default: 'AUGD')
    Error codes:
        -1  :  no suitable shot found under given experiment
        -2  :  wrong input shotnumber (wrong type or out of range)
    """

    # shotnumber needs to be an int and in range, else no result
    if not isinstance(shot, int) or shot > 99999:
        return -3
    # AUGD shotfiles follow a particular path-specification
    basepath = os.path.join(config.sfBasepath, exp.lower(), diag.upper())

    # go backwards starting with directory of given shot
    for nshot1000 in range(int(shot//1000), -1, -1):
        sub_dir = '%s/%d' %(basepath, nshot1000)
        if os.path.isdir(sub_dir):
            shot_beg = min(shot, (nshot1000+1)*1000-1)
            for nshot in range(shot_beg, nshot1000*1000-1, -1):
                sfpath = '%s/%d' %(sub_dir, nshot)
                if os.path.isfile(sfpath):
                    return nshot
                for ed in range(1, 100):
                    sfpath = '%s/%d.%d' %(sub_dir, nshot, ed)
                    if os.path.isfile(sfpath):
                        return nshot
    # no result found anywhere, return -1
    return -1


def previousshot(diag, shot=99999, exp='AUGD'):
    """Alias of ddcshotnr
    """
    return ddcshotnr(diag, shot=shot, exp=exp)
