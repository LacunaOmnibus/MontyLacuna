
import lacuna, lacuna.binutils.libbin, lacuna.types
import lacuna.exceptions as err
import argparse, datetime, os, re, sys
import lacuna.exceptions as err

class MailCompile(lacuna.binutils.libbin.Script):

    def __init__(self):
        self.version    = '0.1'
        self.now        = datetime.datetime.now()
        self.utils      = lacuna.utils.Utils()

        parser = argparse.ArgumentParser(
            description = 'This will build as many of a single type of ship as you want, up to the maximum that can be built across all shipyards on your planet.  If there are already ships in your build queue, this will figure that out and only build what it can.',
            epilog      = "Full docs can be found at http://tmtowtdi.github.io/MontyLacuna/scripts/build_ships.html",
        )
        parser.add_argument( 'subject', 
            metavar     = '<subject>',
            action      = 'store',
            help        = 'Messages matching this subject will be compiled.'
        )
        parser.add_argument( '--tag', 
            metavar     = '<tag>',
            action      = 'store',
            type        = str,
            default     = None,
            choices     = [
                'Alert', 'Attack', 'Complaint', 'Colonization', 'Correspondence', 'Excavator', 
                'Intelligence', 'Medal', 'Mission', 'Parliament', 'Probe', 'Spies', 'Trade', 
                'Tutorial'
            ],
            help        = "Defaults to no tag."
        )
        parser.add_argument( '--day', 
            metavar     = '<day>',
            action      = 'store',
            type        = int,
            default     = self.now.day,
            help        = ""
        )
        parser.add_argument( '--month', 
            metavar     = '<month>',
            action      = 'store',
            type        = int,
            default     = self.now.month,
            help        = ""
        )
        parser.add_argument( '--year', 
            metavar     = '<year>',
            action      = 'store',
            type        = int,
            default     = self.now.year,
            help        = ""
        )
        super().__init__(parser)
        self.client.cache_on("my_inbox")
        self.inbox = self.client.get_inbox()

    def date_matches( self, dt:datetime.datetime ):
        if dt.day == self.args.day and dt.month == self.args.month and dt.year == self.args.year:
            return True
        return False

    def find_start_id( self, msgs:list ):
        """ Given a list of messages, returns the ID of the first message that matches
        our requested date.  If none of the messages matches, returns None.
        """
        for m in msgs:
            dt = self.utils.tle2time( m.date )
            if self.date_matches( dt ):
                return m.id
        return None

    def find_end_id( self, msgs:list, start_id:int ):
        """ Given a list of messages, returns the ID of the last message that matches
        our requested date.  If none of the messages matches, returns None.
        """
        last_id = start_id
        for m in msgs:
            if m.id >= last_id: # newer messages will have higher IDs
                continue
            dt = self.utils.tle2time( m.date )
            if self.date_matches( dt ):
                last_id = m.id
            else:
                return last_id
        return None

    def get_dated_summaries( self ):
        """ Returns the summaries of the messages that fall on our requested date.

        Returns:
            messages (list): :class:`lacuna.inbox.MessageSummary` objects
        """
        start_id        = None
        end_id          = None
        all_messages    = []
        for i in range(1, 11):
            ### Only reading the first 10 pages is arbitrary, but seems 
            ### reasonable.
            opts = {}
            opts['page_number'] = i
            if self.args.tag:
                opts['tags'] = [ self.args.tag ]
            page_messages, count = self.inbox.view_inbox( opts )
            if not start_id:
                start_id = self.find_start_id( page_messages )
            if start_id and not end_id:
                end_id = self.find_end_id( page_messages, start_id )
            all_messages += page_messages
            if start_id and end_id:
                break

        ### If the requested date goes past the first 10 pages, we're going to 
        ### punt and still only return messages that appear on those first 10 
        ### pages.
        if not start_id:
            raise KeyError("I could not find messages from the requested date within the first 10 pages of messages.")
        if not end_id:
            end_id = all_messages[-1].id

        ### I keep thinking linearly.  In my head, if start_id is 1, then 
        ### end_id should be 5.
        ###
        ### WRONG -- the end_id message is older than the start_id message, so 
        ### end_id will always be SMALLER than start_id.
        matching_messages = []
        for m in all_messages:
            if m.id <= start_id:
                if m.id >= end_id:
                    matching_messages.append(m)
                else:
                    break
        return matching_messages

    def get_matching_summaries( self, messages:list ):
        """ Returns a list of messages whose subject line matches the requested subject.

        Arguments:
            messages (list): :class:`lacuna.inbox.MessageSummary` to comb through
        Returns:
            matches (list): :class:`lacuna.inbox.MessageSummary` whose subject matched
        """
        matches = []
        pat     = re.compile( self.args.subject, re.IGNORECASE )
        for m in messages:
            if pat.search( m.subject ):
                matches.append(m)
        return matches

    def compile_full_messages( self, summaries:list ):
        msgs    = []
        for s in summaries:
            message = self.inbox.read_message( s.id )
            mbody   = message.body
            if 'table' in message.attachments:
                mbody += "\n\nTABLE FOLLOWS:\n"
                for row in message.attachments['table']:
                    strrow = [str(i) for i in row]
                    mbody += ','.join(strrow) + "\n"
            msgs.append(mbody)
        report = "\n\n===================\n\n".join(msgs)
        return report

