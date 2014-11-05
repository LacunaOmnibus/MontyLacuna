
import lacuna.bc

class Inbox(lacuna.bc.LacunaObject):

    path = 'inbox'

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def view_inbox( self, opts: 'struct' = {}, *args, **kwargs ):
        """ Returns an integer message cont, and a list of messages (list of structs, 
        one message per struct).

        The 'opts' argument is optional.  Allowed members are:
            'page_number'
                Which 25 messages should be returned?  25 per page, this 
                defaults to '1'.
            'tags'
                Only messages containing these tags will be returned or included in 
                the message_count.  Allowed tags:
                    Tutorial, Correspondence, Medal, Intelligence, Alert, Attack, 
                    Colonization, Complaint, Excavator, Mission, Parliament, Probe, 
                    Spies, Trade
                Sending an invalid tag will not throw an exception, it'll merely 
                return 0 messages.


        Only returns 25 messages at a time.  You cannot change this, but you can
        control which 25 messages you'll get.
        
        rv['message_count'] is message count.  This is the total number of messages
        that satisfy your current filter.
            eg You have 1000 total messages.  200 of them are 'attack' messages.  A
            call to view_inbox() filtered by 'attack' will only return 25 messages, 
            but the 'message_count' will be 200.

        rv['messages'] is the list of message structs.  Each struct follows this format:
                    {
                        'body_preview': 'Our defensive forces were able',
                        'date': '14 10 2014 11:26:49 +0000',
                        'from': 'tmtowtdi',
                        'from_id': '23598',
                        'has_read': '0',
                        'has_replied': '0',
                        'id': '68002437',
                        'subject': 'Target Neutralized',
                        'tags': ['Attack'],
                        'to': 'tmtowtdi',
                        'to_id': '23598'
                    },
        """
        pass

    """The arguments to and return values from each of view_archived(), view_sent(),
    and view_trashed() are all identical to those to/from view_inbox().
    """
    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def view_archived( self, opts: 'struct' = {}, *args, **kwargs ):
        pass
    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def view_sent( self, opts: 'struct' = {}, *args, **kwargs ):
        pass
    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def view_trashed( self, opts: 'struct' = {}, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def read_message( self, message_id:int, *args, **kwargs ):
        """ Returns all details about a single message, and marks the message
        as read.

        rv['message'] = {
            'attachments': None,
            'body': 'The parliamentary vote for the proposition '
                    'titled *Upgrade Warehouse (5,-4)* has passed '
                    'with 23 votes for and 0 votes against. As a '
                    'reminder, here are the particulars:\n'
                    '\n'
                    'Upgrade Warehouse (5,-4) on {Planet 831912 SASS '
                    'Retribution} from level 6 to 7.\n'
                    '\n',
            'date': '14 10 2014 17:02:32 +0000',
            'from': 'tmtowtdi',
            'from_id': '23598',
            'has_archived': '0',
            'has_read': '1',
            'has_replied': '0',
            'id': '68029602',
            'in_reply_to': None,
            'recipients': ['tmtowtdi'],
            'subject': 'Pass: Upgrade Warehouse (5,-4)',
            'tags': ['Parliament'],
            'to': 'tmtowtdi',
            'to_id': '23598'
        },

        'attachments' will generally be None, but if not, it can contain:
                "attachments" : {
                    "image" : {
                        "url" : "http://www.example.com/path/image.jpg",
                        "title" : "Some Title",
                        "link" : "http://www.lacunaexpanse.com/", # optional link to somewhere
                    "link" : {
                        "url" : "http://www.lacunaexpanse.com/",
                        "label" : "The Lacuna Expanse Website"
                    }
                    "table" : [
                        [ "Hostname", "IP Address" ], # first row is always a header
                        [ "example.lacunaexpanse.com", "192.168.1.24" ],
                        ...
                    ],
                    "map" : {
                        "surface" : "surface-6",
                        "buildings" : [
                            {
                                "x" : -3,
                                "y" : 4,
                                "image" : "apples4"
                            }
                            ...
                        ]
                    }
                }

            No more than one of each of those attachments is allowed per mail.
        """
        pass    # read_message

    """archive_messages() and trash_messages() work identically.
    They both take a list of message IDs to either archive or trash.

    Both return a struct containing:
                {
                    success : [id, id, id, ...]
                    failure : [id, id, id, ...]
                    status : { ... }
                }
        There's no indication why any given message movement succeeded or failed, just
        that they did.
    """
    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def archive_messages( self, messages:list, *args, **kwargs ):
        pass
    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def trash__messages( self, messages:list, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def send_message( self, recipients:str, subject:str, body:str, options:'struct' = {}, *args, **kwargs ):
        """
        recipients
            Comma-separated string containing names of empires to receive your message.
            NOT A LIST, a comma-separated string.
        subject
            No "special characters", < 100 chars in length.  Specifically cannot contain
            any of 
                &, @, ;, <, or >
            There's no explanation of what "special characters" mean in the docs.  I've sent 
            a message with a unicode snowman in both the subject and body, so that's not it.
        body
            Limit of 200,000 characters.  < and > are disallowed.
            Also, anything that Regexp::Common::profanity registers as profane disallows the 
            entire message.  This profanity filter can be irritating - it's very sensitive, 
            and you're not informed what word it's triggering on.  "crap" (along with other 
            pretty mild language) is considered profane.
        options['in_reply_to']
            A message ID that this message is a reply to.
        options['forward']
            A message ID to forward.  This almost certainly DOES NOT work the way you think
            it should.
            Any attachments from the message ID we're forwarding are automatically attached
            to our current message.  However, the body of the forwarded message is NOT 
            included in the current message.  If you want that to happen, you'll need to 
            do it yourself.

        Return Value
            Hands back a struct with (afaict) two keys (the rv is not documented, so I'm
            just reporting the results of a few tests here).

            For a message sent to recipients "tmtowtdi,Infinate Ones,no_such_player":
            {
                'sent': ['tmtowtdi', 'Infinate Ones'],
                'unknown': ['no_such_player']
            }

        Message Formatting
            This is rarely-enough used and the docs are wordy enough that it's not worth
            repeating it all here.  See
                https://us1.lacunaexpanse.com/api/Inbox.html#Message_Formatting
        """
        pass




