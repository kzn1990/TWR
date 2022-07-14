import pymysql.cursors
import logging


class MysqlReporter:
    enabled = False
    host = None
    user = None
    passwd = None
    db = None
    logger = logging.getLogger("RemoteLogger")

    
    def __init__(self, config=None):
        if config['mysql']['enable'] == 'True':
            self.enabled = config['mysql']['enable']
            self.host = config['mysql']['host']
            self.user = config['mysql']['user']
            self.passwd = config['mysql']['passwd']
            self.db = config['mysql']['db']
            print(self.db)
            self.logger.debug("MySQL reporter is enable: %s, %s, %s, %s" % (self.host, self.user, self.passwd, self.db))
        else:
            self.logger.debug("MySQL reporter is disabled.")
        
    
    def connection(self):
        return pymysql.connect(host=self.host, user=self.user, password=self.passwd, database=self.db)
    

    def send_metrics_to_mysql(self, player, scav, farm, guild=0):
        if self.enabled:
            try: 
                con = self.connection()
                with con.cursor() as cur:
                    cur.execute('INSERT INTO twr_metrics (player, scavenge, farm, guild) VALUES(%s, %s, %s, %s)', 
                        (player, scav, farm, guild))
                    con.commit()
            except Exception as e:
                print("Got problem with inset to db...", e)
            finally:
                con.close()