
import lacuna, lacuna.binutils.libbin
import argparse, os, sys

class RecallShips(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version = '0.1'
        parser = argparse.ArgumentParser(
            description = 'Recall all ships that are either orbiting or defending other planets.  This is not selective - it recalls everything the current planet has out.',
            epilog      = 'Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/recall_all_ships.html',
        )
        parser.add_argument( 'name', 
            metavar     = '<planet>',
            action      = 'store',
            help        = 'All spies from this planet will be recalled.'
        )
        super().__init__(parser)
        self.bodyname = self.abbrv.get_name(self.args.name)

    def show_report(self, ships):
        """ Displays a report on what ships have been recalled.

        Arguments:
            - ships -- A list of ``lacuna.ship.IncomingShip`` objects as returned by 
              ``lacuna.building.spaceport.recall_all()``
        """
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
            l.info( "{:04d} total ships are on their way back to {}.".format(len(ships), self.bodyname) )
        else:
            l.info( "You don't have any ships out defending or orbiting." )

