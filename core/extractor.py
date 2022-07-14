import re
import configparser


class Extractor:

    @staticmethod
    def player_savenge_farm(res):
        find_player = re.findall(
            r'<td class="lit-item">(.+?)</td>',
            res.text,
        )
        if not find_player:
            return("0")
        get_number = re.findall(
            r'\d+', str(find_player[-2])
        )
        return(''.join(get_number))
    
    @staticmethod
    def get_all_guild_members(res):
        find_player = re.findall(
            r'<a href="\/guest.php\?screen=info_player\&amp\;id=\d+">\s+?(.*)\s+?</a>',
            res.text,
        )
        nice_plaer_name = []
        for player in find_player:
            nice_plaer_name.append(player.strip())
        return(nice_plaer_name)
    
    
    @staticmethod
    def parse_config():
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config