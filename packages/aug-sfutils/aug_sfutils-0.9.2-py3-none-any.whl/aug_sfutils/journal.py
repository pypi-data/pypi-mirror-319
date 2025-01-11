"""A class for reading and manipulating the 'augjournal' from MariaDB"""

import os, logging, datetime, time, dateutil, traceback
import pandas as pd
from sqlalchemy import create_engine

logger = logging.getLogger('journal')
fmt = logging.Formatter('%(asctime)s | %(name)s | %(levelname)s: %(message)s', '%H:%M:%S')
if len(logger.handlers) == 0:
    hnd = logging.StreamHandler()
    hnd.setFormatter(fmt)
    logger.addHandler(hnd)

#logger.setLevel(logging.DEBUG)
logger.setLevel(logging.INFO)

date_fmt = '%Y-%m-%d'


def getShotStat():
    ShotRefFile = '/shares/departments/AUG/www/local/aug_only/shotstat.txt'
    if not os.path.isfile(ShotRefFile):
        logger.error('File %s not found', ShotRefFile)
        return None
    with open(ShotRefFile, 'r') as f:
        lines = f.readlines()
    n_lines = len(lines)
    if n_lines <= 0:
        return None
    shotStat = {'shot': int(lines[0]), 'distrTime': lines[1].strip(), 'status': lines[2].strip(), 'actionTime': lines[3].strip()}
    return shotStat


def wait4shot(hour_end=19, time_sleep=60, statusList=['ABORTED', 'COMPLETED']):
    '''Returns a shotnumber after a new shot is performed, sleeps otherwise.
Optional keys:
    hour_end: hour (0-24) to stop the waiting loop (default: 19)
    time_sleep: period (in seconds) after which the program checks again for a new shot (default: 60)
    statusList: list of discharge statuses prompting a reaction of the program. Full list: ['DISTRIBUTED', 'RUNNING', 'COLLECTING', 'ABORTED', 'COMPLETED'], default is ['ABORTED', 'COMPLETED']'''
#    status = ['DISTRIBUTED', 'RUNNING', 'COLLECTING', 'ABORTED', 'COMPLETED']
    refStat = getShotStat()
    refShot = refStat['shot']
    hour = -1
    while hour < hour_end: # Quit at 7 p.m. or custom time
        logger.info('Waiting for next shot. Current shot: %d, status: %s', refShot, refStat['status'])
        logger.info('Ctrl+C to exit')
        loctime = time.localtime(time.time())
        hour = loctime[3]
        currStat = getShotStat()
        if currStat is not None:
            if currStat['status'] in statusList:
                newShot = currStat['shot']
            else:
                newShot = currStat['shot'] - 1
            if newShot > refShot:
                return newShot
        time.sleep(time_sleep)

    return None


def wait4nextShot(hour_end=19, time_sleep=60):
    '''Return a shotnumber after a new shot is performed, sleeps otherwise'''

    refShot = JOURNAL().getLastShot(trigger=True) # for reference
    hour = -1
    while hour < hour_end: # Quit at 7 p.m. or custom time
        logger.info('Waiting for the next shot (current shot %d)', refShot)
        logger.info('Ctrl+C to exit')
        loctime = time.localtime(time.time())
        hour = loctime[3]
        try:
            jou = JOURNAL()
            newShot = jou.getLastShot(trigger=True)
            jou.close()
            if newShot > refShot:
                return newShot
        except:
            logger.error('Problems reading last shot number')
            traceback.print_exc()
        time.sleep(time_sleep)

    return None


def create_url(dialect, username, password, dbhost, port, database):

    return '%s://%s:%s@%s:%d/%s' %(dialect, username, password, dbhost, port, database)


class JOURNAL:

    dialect  = 'mysql+pymysql'
    db_user  = 'augxro'
    db_pw    = 'augxro'
    db_host  = 'srv-mariadb-1.ipp.mpg.de'
    db_port  = 3306
    db_name  = 'aug_operation'
    db_table = 'augjournal'

    def __init__(self):
        self.open()

    def __call__(self, var):
        if isinstance(var, int):
            return self.getShotEntries(var)
        else:
            return self.getPrevSession(var)

    def open(self):
        self.status = 0
        try:
            self.url = create_url(self.dialect, self.db_user, self.db_pw, self.db_host, self.db_port, self.db_name)
            self.engine = create_engine(self.url, connect_args={'ssl_verify_cert':True, 'ssl':False})
            self.conn = self.engine.connect()
        except:
            traceback.print_exc()
            self.status = 1
        
    def close(self):
        '''Close the mySQL connection'''

        self.conn.close()
        self.engine.dispose()

    def dbTable(self):
        '''Read full journal database as table'''

        db = pd.read_sql_table(self.db_table, self.conn)
        return db

    def dbByValue(self, column='shotno', value=38384, pick='*'):
        '''Database query for arg1 = arg2'''
    
        sql = 'SELECT %s FROM %s WHERE %s="%s"' %(pick, self.db_table, column, value)
        return pd.read_sql_query(sql, self.conn, index_col=column)

    def dbByList(self, column='shotno', val_list=None):
        '''Database query for arg1 IN arg2 (list)'''

        suser_id = ', '.join(['"%s"' %x for x in val_list])   
        sql = "SELECT * from %s WHERE %s IN (%s)" %(self.db_table, column, suser_id)
        return pd.read_sql_query(sql, self.conn, index_col=column)

    def checkDateFmt(self, date=None, shot=None):
        """Converts the format of the input date into %Y-%m-%d.
        Default date is today.
        """

        if date is None and shot is None:
            date = datetime.date.today()
        else:
            if date is None:
                date = self.getShotDate(shot)
            else:
                date = dateutil.parser.parse(date)
        sdate = date.strftime(date_fmt)
        return sdate

    def getShotEntries(self, shot):
        """Get the journal parameters for a given shot
        Syntax:
            df = jou.getShotEntries(shot)
        Returns:
            Panda Dataframe with shot parameters
        """

        return self.dbByValue(column='shotno', value=shot) #.to_dict(orient="records")

    def isUseful(self, shot):
        """Tell whether a shot was useful or not
        Syntax:
            df = jou.isUseful(shot)
        Returns:
            True (if useful) / False
        """

        df = self.dbByValue(column='shotno', value=shot, pick='shotno, useful')
        if len(df) > 0:
            isUseful = (df['useful'].values[0] == 'yes')
        else:
            isUseful = None
        return isUseful

    def getShotEntry(self, shot, field='datum'):
        """Get a specific field for a shot from the journal DB
        Syntax:
            val = jou.getShotEntry(self, shot, 'ip')
        Ouput:
            The value val - it can be string, integer or float
        """
        df = self.dbByValue(column='shotno', value=shot, pick='shotno, %s' %field)
        return df[field].values[0]

    def getShotDate(self, shot):
        """Get the date of a shot
        Syntax:
            date = jou.getShotDate(shot)
        Output:
            date  (%Y-%m-%d string)
        """

        return self.getShotEntry(shot, field='datum')

    def selectUseful(self, df):
        '''Filter query results retaining only useful discharges'''

        df = df.set_index('shotno')
        indexReject = df[df['useful'] == 'no'].index
        df.drop(indexReject, inplace=True)
        return df

    def searchSession(self, date=None, shot=None, onlyUseful=True):
        """Get DataFrame for one session

        Syntax:
            jou.searchSession(date='2022-01-03', onlyUseful=True)
        Arguments and Options:
            date            str   Date of the session (default: today)
            shot            int   Shot number, in case date is None
            onlyUseful=F|T  bool  Flag, if only useful plasmashots ar te be searched (default: yes)
        Returns:
            pandas Dataframe. If no session is found, the Dataframe is empty (0 rows).
        """

        date = self.checkDateFmt(date=date, shot=shot)
        df = self.dbByValue(column='datum', value=date)
        if onlyUseful:
            df = self.selectUseful(df)
        else:
            df = df.set_index('shotno')
        return df

    def getPrevSession(self, date=None):
        '''Get last session before the input date.
        Syntax:
            jou.getPrevSession(date='2022-01-03')
        Returns:
            pandas Dataframe
        '''

        sdate = self.getPrevDate(date=date)
        df = self.dbByValue(column='datum', value=sdate)
        return df

    def getNextSession(self, date):
        '''Get first session after the input date.
        Syntax:
            jou.getNextSession(date='2022-01-03')
        Returns:
            pandas Dataframe
        '''

        sdate = self.getNextDate(date)
        df = self.dbByValue(column='datum', value=sdate)
        return df

    def getPrevDate(self, date=None):
        '''Get session date of the last session before the input date.
        Syntax:
            jou.getPrevDate(date='2022-01-03')
        Returns:
            Date | string
        '''

        sdate = self.checkDateFmt(date)
        sql = 'SELECT datum FROM %s WHERE datum <= "%s" ORDER BY datum DESC LIMIT 1' %(self.db_table, sdate)
        prevDate = pd.read_sql_query(sql, self.conn, index_col='datum')
        return prevDate.index[0]

    def getNextDate(self, date):
        '''Get session date of the first session after the input date.
        Syntax:
            jou.getNextDate(date='2022-01-03')
        Returns:
            Date | string
        '''

        sdate = self.checkDateFmt(date=date)
        sql = 'SELECT datum FROM %s WHERE datum >= "%s" ORDER BY datum DESC LIMIT 1' %(self.db_table, sdate)
        nextDate = pd.read_sql_query(sql, self.conn, index_col='datum')
        return nextDate.index[0]

    def getLastShot(self, onlyUseful=False, trigger=True):
        """
        Syntax:
            jou.getLastShot()
        Output:
            Last AUG shot | int
        """

        df = self.getPrevSession()
        shot = df['shotno'].iloc[-1]
        if onlyUseful:
            while not self.isUseful(shot):
                shot -= 1
        if trigger:
            if ((not df['useful'].iloc[-1]) or (df['useful'].iloc[-1] is None)) and \
                (not df[  'time'].iloc[-1]) or (df[  'time'].iloc[-1] is None):
                shot -= 1

        return shot

    def isExpDay(self, date=None):
        """
        Syntax:
            jou.isExpDay(date=...)

        Input:
            date (optional): str   Date string. If None, today is assumed
        Output:
            Int >0 if day=date is/was an experimental day, 0 otherwise
        """

        df = self.searchSession(date=date, onlyUseful=False)
        return len(df)


if __name__ == '__main__':

    jou = JOURNAL()

    shot = 38384

    entry_d = jou.getShotEntries(shot)
#    ses_d = searchSession(date='20210115')
    ses_d = jou.searchSession(shot=39649)
    print('====')
    print(ses_d)
    print('---')
    print(ses_d['funding'])
    print(ses_d['ip'])

    df_prev = jou.getPrevSession('20210106')
    logger.info('getNext')
    df_next = jou.getNextSession('20211223')
    print(df_prev['shotno'])
    print(df_next['shotno'])
    logger.info('getLastShot')
    lastShot = jou.getLastShot()
    logger.info('Done')
    print(lastShot)
    shdate = jou.getShotDate(shot)
    jou.close()
    print(shdate)
