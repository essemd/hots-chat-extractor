#!/usr/bin/env python

from __future__ import print_function

import argparse
import sys
import json
import mpyq
import pprint
import protocol88122 as protocol # update this with each new protocol release
from datetime import timedelta

#from .versions import build, latest


class EventLogger:
    def __init__(self):
        self._event_stats = {}

    def log(self, output, event):
        # update stats
        if '_event' in event and '_bits' in event:
            stat = self._event_stats.get(event['_event'], [0, 0])
            stat[0] += 1  # count of events
            stat[1] += event['_bits']  # count of bits
            self._event_stats[event['_event']] = stat
        # write structure
        pprint.pprint(event, stream=output, width=120)

    def log_stats(self, output):
        for name, stat in sorted(self._event_stats.items(), key=lambda x: x[1][1]):
            print('"%s", %d, %d,' % (name, stat[0], stat[1] / 8), file=output)


def main():
    archive = mpyq.MPQArchive(sys.argv[1])

    logger = EventLogger()

    # Read the protocol header, this can be read with any protocol
    #contents = archive.header['user_data_header']['content']
    #header = protocol.decode_replay_header(contents)

    # The header's baseBuild determines which protocol to use
    #baseBuild = header['m_version']['m_baseBuild']
    #try:
    #    protocol = build(baseBuild)
    #except:
    #    print('Unsupported base build: %d' % baseBuild, file=sys.stderr)
    #    sys.exit(1)

    playerinfo_by_id = {} 

    f = open('output', 'w')

    # Print game events and/or game events stats
    #contents = archive.read_file('replay.game.events')
    #for event in protocol.decode_replay_game_events(contents):
    #    logger.log(f, event)

    contents = archive.read_file('replay.details')
    details = protocol.decode_replay_details(contents)
    player_list = details['m_playerList']
    
    # figure out player names 
    if hasattr(protocol, 'decode_replay_tracker_events'):
        contents = archive.read_file('replay.tracker.events')
        for event in protocol.decode_replay_tracker_events(contents):
            if event['_event'] == 'NNet.Replay.Tracker.SStatGameEvent' and event['m_eventName'] == b'PlayerSpawned':
                    info = {}

                    index = event['m_intData'][0]['m_value'] - 1 # not sure why this is off by 1 but we hack fix it

                    #info['hero'] = event['m_stringData'][0]['m_value']
                    info['hero'] = player_list[index]['m_hero']
                    info['name'] = player_list[index]['m_name']
                    info['team'] = player_list[index]['m_teamId']

                    playerinfo_by_id[index] = info 

    # print prettified chat messages
    contents = archive.read_file('replay.game.events')
    for event in protocol.decode_replay_game_events(contents):
        if event['_event'] == 'NNet.Game.STriggerChatMessageEvent':        
            index = event['_userid']['m_userId']

            hero = playerinfo_by_id[index]['hero'].decode('utf-8') 
            name = playerinfo_by_id[index]['name'].decode('utf-8')
            team = playerinfo_by_id[index]['team']
            message = event['m_chatMessage'].decode('utf-8')
            timestamp = timedelta(seconds = round(event['_gameloop'] / 16))

            output_str = f'[{timestamp}] {name}<{team}> ({hero}): {message}'

            logger.log(f, output_str)
        
    # Print attributes events
    #attributes = protocol.decode_replay_attributes_events(contents)
    #logger.log(f, attributes)

    # Print stats
    #logger.log_stats(sys.stderr)
    
if __name__ == "__main__":
    main()    
