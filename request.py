import logging
import requests
from extractor import Extractor
from reporter import MysqlReporter
import time

class WebWrapper:
    web = None
    endpoint = None
    server = None
    conf = None
    logger = logging.getLogger("Requests")
    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.97 Safari/537.36',
        'upgrade-insecure-requests': '1'
    }
    
    def __init__(self, server="pl179", endpoint="plemiona.pl"):
        self.web = requests.session()
        self.server = server
        self.endpoint = endpoint
        
    
    def prep_url(self, url):
        return(f"https://{self.server}.{self.endpoint}/{url}")
    
    
    def get_url(self, url, headers=None):
        if not headers:
            headers = self.headers
        try:
            url = self.prep_url(url)
            res = self.web.get(url)
            self.logger.debug("GET %s [%d]" % (url, res.status_code))
            if 'data-bot-protect="forced"' in res.text:
                self.logger.warning("Bot protection hit! cannot continue")
                self.reporter.report(0, "TWB_RECAPTCHA", "Stopping bot, press any key once captcha has been solved")
                input("Press any key...")
                return self.get_url(url, headers)
            return res
        except Exception as e:
            self.logger.warning("GET %s: %s" % (url, str(e)))
            return None
    
    
    def post_url(self, url, headers=None):
        pass
    
    
    def run(self, guild, players = []):
        resault = []
        for player in players:
            res = self.get_url(f"guest.php?screen=ranking&mode=in_a_day&type=scavenge&name={player}")
            scav = Extractor.player_savenge_farm(res)
            time.sleep(0.7)
            res = self.get_url(f"guest.php?screen=ranking&mode=in_a_day&type=loot_res&name={player}")
            farm = Extractor.player_savenge_farm(res)
            resault.append([player, scav, farm, guild])
            time.sleep(0.6)
        return resault