
import binutils.libbin
import argparse, lacuna, os, sys

class RecallShips(binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Recall all ships that are either orbiting or defending other planets.  This is not selective - it recalls everything the current planet has out.',
            epilog      = 'EXAMPLE: python bin/recall_all_ships.py Earth',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        parser.add_argument( '--quiet', 
            dest        = 'quiet',
            action      = 'store_true',
            help        = "Silence all output."
        )
        super().__init__(parser)

        if not self.args.quiet:
            self.client.user_log_stream_handler.setLevel('INFO')

    def show_report(self, ships):
        l = self.client.user_logger
        if ships:
            shiptypes = {}
            for i in ships:
                key = i.type_human + i.returning_from['name']
                if key in shiptypes:
                    shiptypes[key]['num'] += 1
                else:
                    shiptypes[key] = {"num":1, "name":i.type_human, "origin":i.returning_from['name']}
            for key, md in shiptypes.items():
                l.info( "{:04d} {} returning from {}.".format(md['num'], md['name'], md['origin']) )
            l.info( "--------------" )
            l.info( "{:04d} total ships are on their way back to {}.".format(len(ships), self.args.name) )
        else:
            l.info( "You don't have any ships out defending or orbiting." )

