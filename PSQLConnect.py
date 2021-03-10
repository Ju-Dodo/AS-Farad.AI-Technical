
from alembic.config import Config

def initConn(inifile):
    """
    Creates connection information from a config.ini file

    :param inifile: name of the ini file for database connection
    :return: connection parameters for sqlalchemy engine
    """

    # create the alembic config object from inifile
    conf = Config(inifile)

    # create the sqlurl and ssl certs from the inifile
    sqlurl = conf.get_main_option('sqlurl')
    sslrootcert = conf.get_main_option('sslrootcert')
    sslcert = conf.get_main_option('sslcert')
    sslkey = conf.get_main_option('sslkey')

    # return sqlurl and ssl certs
    return sqlurl, sslrootcert, sslcert, sslkey