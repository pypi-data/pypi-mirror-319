"""Class for shotfiles writing"""

import os, datetime, warnings, logging
import ctypes as ct
import numpy as np
from aug_sfutils import sfmap, str_byt, config
from aug_sfutils.sfmap import oid

logger = logging.getLogger('aug_sfutils.ww')
#logger.setLevel(logging.INFO)
#logger.setLevel(logging.DEBUG)

wwlib = os.path.join(config.sfLib, 'libddww8.so')
libddww = ct.cdll.LoadLibrary(wwlib)

LOGICAL = sfmap.typeMap('descr', 'SFtyp', 'LOGICAL')


def getError(error):

    """ Check if an error/warning occured
    """

    try:
        err = ct.c_int32(error)
    except TypeError:
        err = ct.c_int32(error.value)
    isError = libddww.xxsev_(ct.byref(err)) == 1
    isWarning = libddww.xxwarn_(ct.byref(err)) == 1
    if isError or isWarning:
        id = ct.c_char_p(b'')
        lid = ct.c_uint64(0)
        text = ct.c_char_p(b' '*255)
        ltext = ct.c_uint64(255)
        unit = ct.byref(ct.c_int32(-1))
        ctrl = ct.byref(ct.c_uint32(3))
        libddww.xxerrprt_(unit, text, ct.byref(err), ctrl, id, ltext, lid);
        logger.error(text.value.decode().strip())

    return isError


class WW:

    """py-WW for shotfile writing
    Wrapper around libddww8.so
    """

    def Open(self, exp, diag, nshot, edition=-1, mode='new'):
        """Equivalent of wwopen
        Prepares output shotfile.
        """
        self.Close()
        if exp.lower() != 'augd':
            outDir = '%s/%s/%s' %(config.sfBasepath, exp.lower(), diag.upper())
            edDir  = '%s/edcntl_dir' %outDir
            if not os.path.isdir(outDir):
                os.mkdir(outDir)
            if not os.path.isdir(edDir):
                os.mkdir(edDir)
        if nshot > 0:
            date = datetime.date.strftime(datetime.datetime.today(),'%y.%m.%d;%H:%M:%S')

            exp  = str_byt.to_byt(exp)
            diag = str_byt.to_byt(diag)
            mode = str_byt.to_byt(mode)
            date = str_byt.to_byt(date)

            self.edition = ct.c_int32(edition)
            error        = ct.c_int(0)
            diaref       = ct.c_int32(0)
            shot         = ct.c_uint32(nshot)
            cexp         = ct.c_char_p(exp )
            cdiag        = ct.c_char_p(diag)
            cmode        = ct.c_char_p(mode)
            cdate        = ct.c_char_p(date)
            _error       = ct.byref(error)
            _nshot       = ct.byref(shot)
            _edition     = ct.byref(self.edition)
            self._diaref = ct.byref(diaref)
            lexpr = ct.c_uint64(len(exp ))
            ldiag = ct.c_uint64(len(diag))
            lmode = ct.c_uint64(len(mode))
            ldate = ct.c_uint64(len(date))

            result = libddww.wwopen_(_error, cexp, cdiag, _nshot, cmode, _edition, \
                                     self._diaref, cdate, lexpr, ldiag, lmode, ldate)
            if getError( error ):
                del self._diaref
                del self.edition
                raise Exception('ww: Error Opening Shotfile %(error)s' % {'error':error.value})
        return hasattr(self, '_diaref')


    def Close(self):
        """Equivalent of wwclose.
        Terminates the file stream and deletes some attributes
        """
        if hasattr(self, '_diaref'):
            error = ct.c_int32(0)
            disp  = b'lock'
            space = b'maxspace'
            ldisp  = ct.c_uint64(len(disp))
            lspace = ct.c_uint64(len(space))
            _error = ct.byref(error)
            _disp  = ct.c_char_p( disp )
            _space = ct.c_char_p( space )

            result = libddww.wwclose_(_error , self._diaref , _disp , _space , ldisp , lspace )
            logger.info('Close: %d, Error: %d, Edition: %d', result, error.value, self.edition.value)
            if getError( error ):
                raise Exception('ww: Error Closing Shotfile')
            del self._diaref
            del self.edition


    def _wwoinfo(self, signame):
        """Wrapping wwoinfo_
        """

        if hasattr(self, '_diaref'):
            signame = str_byt.to_byt(signame)

            error   = ct.c_int32(0)
            name    = ct.c_char_p(signame)
            lname   = ct.c_uint64(len(signame))
            typ     = ct.c_uint32(0)
            format  = ct.c_uint16(0)
            ntval   = ct.c_uint32(0)
            items   = ct.c_uint32(0)
            _items  = ct.byref(items)
            c_indices = (ct.c_uint32 * 4)()
            _error   = ct.byref(error)
            _typ     = ct.byref(typ)
            _ntval   = ct.byref(ntval)
            _format  = ct.byref(format)
            _indices = ct.byref(c_indices)

#            logger.debug(signame)
            result = libddww.wwoinfo_(_error, self._diaref, name, _typ, \
                     _format, _ntval, _items, _indices, lname)

            if getError(error):
                raise Exception('ww: Error wwoinfo %s' %signame)

            return {'otype': typ.value, 'format': format.value, 'leng': ntval.value, \
                    'items': items.value, 'indices': c_indices}


    def GetParameterInfo(self, pset, pnam):
        """Returns information about the parameter 'pnam' of the parameter set 'pset'."""

        if hasattr(self, '_diaref'):
            par_name = str_byt.to_byt(pnam)
            set_name = str_byt.to_byt(pset)
            error   = ct.c_int32(0)
            _error  = ct.byref(error)
            pset    = ct.c_char_p(set_name)
            par     = ct.c_char_p(par_name)
            items   = ct.c_uint32(0)
            _items  = ct.byref(items)
            format  = ct.c_uint16(0)
            _format = ct.byref(format)
            lpar = ct.c_uint64(len(par_name))
            lset = ct.c_uint64(len(set_name))
            result = libddww.dd_prinfo_(_error, self._diaref, pset, par, _items, _format, lset, lpar)
            return {'items': items.value, 'format': format.value}


    def SetObject(self, signame, data, tim_axis=None):
        """Stores 'data'-array of a given object named 'signame' of type 
        Signal, SigGroup or Areabase to the target shotfile
        """

        logger.info('Setting %s', signame)
        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(signame)
            otype = info['otype']
            if otype in (oid['Signal'], oid['TimeBase']):
                self.SetSignal(signame, data)
            elif otype == oid['SignalGroup']:
                self.SetSignalGroup(signame, data)
            elif otype == oid['AreaBase']:
                self.SetAreabase(signame, data, tim_axis=tim_axis)


    def SetSignal(self, signame, data, indices=None):
        """Stores 'data'-array of a given Signal or TimeBase named 'signame'
        to the target shotfile
        """

        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(signame)
            dfmt = info['format']
            otype = info['otype']
            if dfmt in sfmap.fmt2len:
                lbuf = sfmap.fmt2len[dfmt]
                lsbuf = ct.c_uint64(lbuf)
                sf_dtype = 6 #CHAR
            else:
                lbuf = np.size(data)
                sf_dtype = sfmap.typeMap('SFfmt', 'SFtyp', dfmt)

            signame = str_byt.to_byt(signame)

            error   = ct.c_int32(0)
            name    = ct.c_char_p(signame )
            lname   = ct.c_uint64(len(signame))
            clbuf   = ct.c_uint32(lbuf)
            stride  = ct.c_uint32(1)
            _error  = ct.byref(error)
            _type   = ct.byref(ct.c_uint32(sf_dtype))
            _lbuf   = ct.byref(clbuf)
            _stride = ct.byref(stride)
            if indices is not None:
                _indices = np.array(indices, dtype=np.int32).ctypes.data_as(ct.POINTER(ct.c_uint32))

            if dfmt in sfmap.fmt2len:
                slen = sfmap.fmt2len[dfmt]
#                stride  = ct.c_uint32(slen)
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                if type(data) == type('str'):
                    sbuf = data.ljust(slen)
                else: #string array
                    sbuf = ''
                    for entry in data:
                        sbuf += entry.ljust(slen)

                sbuf = str_byt.to_byt(sbuf)
                lbuf = ct.c_uint32(len(sbuf))
                _lbuf = ct.byref(lbuf)
                lsbuf = ct.c_uint64(len(sbuf)) 
                buffer = ct.c_char_p(sbuf)
                if otype == oid['Signal']:
                    result = libddww.wwsignal_( \
                             _error, self._diaref, name, _type, _lbuf, buffer, \
                             _stride, lname, lsbuf)
                elif otype == oid['SignalGroup']:
                    result = libddww.wwinsert_( \
                             _error, self._diaref, name, _type, _lbuf, buffer, \
                             _stride, _indices, lname, lsbuf)
            else:
                ctyp = sfmap.typeMap('SFfmt', 'ct', dfmt)
                data = np.atleast_1d(data)
                data = np.array(data, dtype=sfmap.typeMap('SFfmt', 'np', dfmt))
                if otype == oid['Signal']:
                    result = libddww.wwsignal_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, lname)
                elif otype == oid['TimeBase']:
                    result = libddww.wwtbase_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, lname)
                elif otype == oid['SignalGroup']:
                    result = libddww.wwinsert_( \
                             _error, self._diaref, name, _type, _lbuf, \
                             data.ctypes.data_as(ct.POINTER(ctyp)), \
                             _stride, _indices, lname)

            if otype in (oid['Signal'], oid['TimeBase']):
                sign = signame.decode('utf8')
                if getError( error ):
                    raise Exception('ww: Error Writing %s' %sign)
                else:
                    logger.info('Written %s', sign)


    def SetSignalGroup(self, signame, data):
        """Stores 'data'-array of a given SignalGroup named 'signame'
        to the target shotfile
        """

        info  = self._wwoinfo(signame)
        dfmt = info['format']
        if dfmt in sfmap.fmt2len:
            for i, dat in enumerate(data):
                dat = dat.ljust(info['leng'])
                indices = [i + 1, 1, 1]
                self.SetSignal(signame, dat, indices=indices)
        else:
            if data.ndim < 2:
                raise Exception('ww: SetSignalGroup array %s has only %d dims' %(signame, data.ndim))
                return False
            if data.ndim == 2:
                for i in range(data.shape[1]):
                    indices = [i + 1, 1, 1]
                    self.SetSignal(signame, data[:, i], indices=indices)
            if data.ndim == 3:
                for i in range(data.shape[1]):
                    for j in range(data.shape[2]):
                        indices = [1 + i, 1 + j, 1]
                        self.SetSignal(signame, data[:, i, j], indices=indices)
        logger.info('Written Signal Group %s', signame)

        return True


    def SetAreabase(self, areaname, data, sizes=None, tim_axis=None):
        """Stores 'data'-array of a given Areabase named 'areaname'
        to the target shotfile
        """

        if hasattr(self, '_diaref'):
            info  = self._wwoinfo(areaname)
            dfmt = info['format']
            if dfmt in sfmap.fmt2len:
                raise Exception('AB cannot have string-like data')
            sf_dtype = sfmap.typeMap('SFfmt', 'SFtyp', dfmt)
            ctyp  = sfmap.typeMap('SFfmt', 'ct', dfmt) # data have to be numerical for AB

            data = np.array(data, dtype=sfmap.typeMap('SFfmt', 'np', dfmt))
            areaname = str_byt.to_byt(areaname)     
            csizes = (ct.c_uint32 * 3)()
            if tim_axis is not None and tim_axis != 0:
                logger.error('tim_axis can be only None or 0, not %d', tim_axis)
                return

            if data.ndim > 2:
                logger.error('AB %s hat %d dims: only a time and a space dependence are allowed, flatten the space data', areaname, data.ndim)
                return

            if tim_axis is None:
                nt = 1
                data = np.atleast_2d(data).T
            else:
                if tim_axis == 0:
                    data = data.T
                nt = data.shape[1]

            if sizes is None:
                csizes[0] = data.shape[0]
            else:
                nx = len(sizes)
                csizes[:nx] = sizes[:nx]


            logger.debug('AB %s, %d, %d, %d, %d, %d', areaname, sf_dtype, nt, *csizes)

            error  = ct.c_int32(0)
            name   = ct.c_char_p(areaname)
            lname  = ct.c_uint64(len(areaname))
            k1     = ct.c_uint32(1) # c_long
            k2     = ct.c_uint32(nt)
            _k1    = ct.byref(k1)
            _k2    = ct.byref(k2)
            _type  = ct.byref(ct.c_uint32(sf_dtype))
            _error = ct.byref(error)
            _sizes = ct.byref(csizes)

            libddww.wwainsert_(_error, self._diaref, name, _k1, _k2, _type, \
                               data.ctypes.data_as(ct.POINTER(ctyp)), \
                               _sizes, lname)

            if getError(error):
                raise Exception('ww.shotfile.SetAreabase: Error writing areabase %s' %areaname)
            else:
                logger.info('Written Areabase %s, sizes %d %d %d', areaname, *csizes[:3])


    def SetParameter(self, set_name, par_name, data):

        """ ww.shotfile().SetParameter( SetName , ParameterName , data )
        types: 0=raw 1=integer 2=float 3=double 4=complex 5=logical 6=character
        The data type is derived from the 00000 shotfile.
        """

        if hasattr(self, '_diaref'):
            info = self.GetParameterInfo(set_name, par_name)
            dfmt = info['format']
            if dfmt in sfmap.fmt2len:
                sf_dtype = 6 #CHAR
            else:
                sf_dtype = sfmap.typeMap('SFfmt', 'SFtyp', dfmt)
            set_name = str_byt.to_byt(set_name)
            par_name = str_byt.to_byt(par_name)
            logger.info('PN %s', par_name)
            data = np.atleast_1d(data)
            ndata = len(data)
            nitem = info['items']
            if ndata > nitem:
                logger.error('Too many %d entries for par_nam %s, more than in sfh %d', ndata, par_name, nitem)
                return
            if ndata == 0:
                logger.error('No data for par_nam %s', par_name)
                return
#            if ndata < nitem:
#                data = np.zeros(nitem, dtype=sfmap.typeMap('SFtyp', 'np', sf_dtype)
            error   = ct.c_int32(0)
            pset    = ct.c_char_p(set_name)
            par     = ct.c_char_p(par_name)
            lset    = ct.c_uint64(len(set_name))
            lpar    = ct.c_uint64(len(par_name))
            _type   = ct.byref(ct.c_uint32(sf_dtype))
            _error  = ct.byref(error)
            if dfmt in sfmap.fmt2len: # string or string array
                slen = sfmap.fmt2len[dfmt]
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                if type(data) == type('str'):
                    sbuf = data.ljust(slen)
                else: #string array
                    sbuf = ''
                    for entry in data:
                        sbuf += entry.ljust(slen)

                sbuf = str_byt.to_byt(sbuf)
                lbuf = ct.c_uint32(len(sbuf))
                _lbuf = ct.byref(lbuf)
                lsbuf = ct.c_uint64(len(sbuf)) 
                buffer = ct.c_char_p(sbuf)
                result = libddww.wwparm_(_error, self._diaref, pset, par, _type, _lbuf, \
                                         buffer, _stride, lset, lpar, lsbuf)
            else: # numerical data
                ctyp  = sfmap.typeMap('SFfmt', 'ct', dfmt)
                datanp = np.array(data, dtype=sfmap.typeMap('SFfmt', 'np', dfmt))
                if ndata < nitem:
                    datanp = np.append(datanp, np.zeros(nitem - ndata))
                stride  = ct.c_uint32(1)
                _stride = ct.byref(stride)
                lbuf = ct.c_uint32(nitem)
                _lbuf = ct.byref(lbuf)
                if nitem == 1 and sf_dtype == LOGICAL:
                    buffer = ctyp(datanp)
                else:
                    buffer = ctyp.from_buffer(datanp)
                _buffer = ct.byref(buffer)
                result = libddww.wwparm_(_error, self._diaref, pset, par, _type, _lbuf, \
                                         _buffer, _stride, lset, lpar)
            if getError( error ):
                raise Exception('ww: Error Writing Parameters into %s -> %s' %(set_name, par_name) )
            else:
                logger.info('   PN %s', par_name.decode('utf8'))


def write_sf(nshot, data_d, sfhdir, diag, exp='AUGD'):
    """Function for writing a full shotfile from a data dict

    Input:
        nshot    int   Shotnumber
        data_d   dict  Dictionary with all relevant objects;
            Keys are object names - they must match the names in the 00000-SFH
            Values are object arrays or dictionaries for ParSets. The data
            types must be the numpy equivalents of the types declared in the
            00000-SFH.
            The array sizes (dict values) have to be consistent among them
            and with the relations in the 00000-SFH, but they do not need
            to be equal to the ones in the 00000-SFH: if the aren't, 
            run sfh.Mod* ahead
        sfhdir   str  Full path of the 00000-SFH
        diag     str  Diagnostic name
        exp(opt) str  Exp name
    """

    import os

    ww = WW()

    os.chdir(sfhdir)
    logger.info('Exp: %s, diag: %s, nshot: %d', exp, diag, nshot)
    if not ww.Open(exp, diag, nshot):
        logger.error('Problems opening shotfile')
        return

    otype = {}
    for obj, data in data_d.items():
        otype[obj] = ww._wwoinfo(obj)['otype']
        if otype[obj] == oid['TimeBase']:
            ww.SetObject(obj, data)

    for obj, data in data_d.items():
        if otype[obj] == oid['AreaBase']:
            if data.ndim == 1:
                tim_ax = None
            else:
                tim_ax = 0
            ww.SetObject(obj, data, tim_axis=tim_ax)

    for obj, data in data_d.items():
        if otype[obj] == oid['ParamSet']:
            logger.info('Writing PS %s', obj)
            for pn, pdata in data.items():
                ww.SetParameter(obj, pn, pdata)
        if otype[obj] in (oid['Signal'], oid['SignalGroup']):
            ww.SetObject(obj, data)

    ww.Close()
