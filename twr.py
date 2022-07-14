#!/usr/bin/env python3


import logging
import coloredlogs
from reporter import MysqlReporter
from request import WebWrapper
from extractor import Extractor
import sys

coloredlogs.install(
    level=logging.DEBUG if "-q" not in sys.argv else logging.INFO,
    fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logging.getLogger("requests").setLevel(logging.WARNING)
logging.getLogger("urllib3").setLevel(logging.WARNING)
    

if __name__ == '__main__':
    guilds = [471, 239]
    conf = Extractor.parse_config()
    reporter = MysqlReporter(conf)
    web = WebWrapper()
    
    for guild in guilds:
        res = web.get_url(f"guest.php?screen=info_ally&id={guild}")
        players = Extractor.get_all_guild_members(res)
        player_resault = web.run(guild, players)
        for player in player_resault:
            logging.info("Player %s, scav: %s, farm: %s" % (player[0], player[1], player[2]))
            reporter.send_metrics_to_mysql(player[0], player[1], player[2], player[3])
