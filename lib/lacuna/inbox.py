
import lacuna.bc

class Inbox(lacuna.bc.LacunaObject):

    path = 'inbox'

    def _set_mail_return(self, result:dict):
        """ All of the view_*() methods return the same thing, so they're 
        calling this.
        """
        mylist = []
        for i in result['messages']:
            mylist.append( MessageSummary(self.client, i) )
        return (
            mylist,
            result['message_count'],
        )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_inbox( self, opts:dict = {}, *args, **kwargs ):
        """ View the messages in your empire's inbox, 25 messages per page.
        
        Arguments:
            opts    Dict (optional)
                        page_number     Integer page number to return.  
                                        Defaults to 1.
                        tags            List of tags to filter by.

        The tags you passed in are joined with 'or'.  So for this call, you'll 
        get back BOTH excavator and correspondence messages:
            msgs, ttl = mail.view_inbox({
                "tags": ["excavator", "correspondence"]
            })

        Valid message tags:
            Alert, Attack, Complaint, Colonization, Correspondence, Excavator, 
            Intelligence, Medal, Mission, Parliament, Probe, Spies, Trade,
            Tutorial

        Sending an invalid tag will not throw an exception, it'll merely 
        return 0 messages.

        Returns:
            messages    List of inbox.MessageSummary objects
            count       Integer total number of messages in the inbox
        """
        return self._set_mail_return( kwargs['rslt'] )


    @lacuna.bc.LacunaObject.call_returning_meth
    def view_archived( self, opts:dict = {}, *args, **kwargs ):
        """  View archived messages.  Returns the same as view_inbox().  """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_sent( self, opts:dict = {}, *args, **kwargs ):
        """  View sent messages.  Returns the same as view_inbox().  """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_trashed( self, opts:dict = {}, *args, **kwargs ):
        """  View trashed messages.  Returns the same as view_inbox().  """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def read_message( self, message_id:int, *args, **kwargs ):
        """ Returns a single message by ID.
        
        Returns an inbox.Message object.
        """
        return Message(self.client, kwargs['rslt']['message'])

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
    def trash_messages( self, messages:list, *args, **kwargs ):
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def send_message( self, recipients:str, subject:str, body:str, options:dict = {}, *args, **kwargs ):
        """ Sends an in-game mail message.

        Arguments:
            recipients  Comma-separated string containing names of empires to 
                        receive your message.  NOT A LIST, a comma-separated 
                        string.
            subject     < 100 chars in length.  Cannot contain any of &, @, ;, 
                        <, or >
                        Unicode is OK (I've mailed myself a snowman).
            body        Limit of 200,000 characters.  < and > are disallowed.
                        Also, anything that Regexp::Common::profanity registers 
                        as profane disallows the entire message.  This profanity 
                        filter can be irritating - it's very sensitive, and 
                        you're not informed what word it's triggering on.  
                        "crap" (along with other pretty mild language) is 
                        considered profane.
            options     Dict:
                            'in_reply_to'   A message ID to reply to.
                            'forward'       A message ID to forward.

        When forwarding a message, any attachments from the message ID we're 
        forwarding are automatically attached to our current message.  However, 
        the body of the forwarded message is NOT included in the current 
        message.  If you want that to happen, you'll need to do it yourself.

        Return Value
            Returns a dict with (afaict) two keys (the rv is not documented, so 
            I'm just reporting the results of a few tests here).

            For a message sent to recipients 
                "tmtowtdi,Infinate Ones,no_such_player":
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



class MessageSummary(lacuna.bc.SubClass):
    """ This is the message summary you get when viewing a list of messages.

    Note that the sender's name is listed in the TLE documentation using the 
    key "from", but we're instead using "from_name".

    Attributes:
        id              "id-goes-here",
        subject         "Vaxaslim",
        date            "01 31 2010 13:09:05 +0600",
        from_name       "Dr. Stephen T. Colbert DFA",
        from_id         "id-goes-here",
        to              "Jon Stewart",
        to_id           "id-goes-here",
        has_read        1,
        has_replied     0,
        body_preview    "Just a reminder that Vaxaslim ",
        tags            "Correspondence" 
    """
    def __init__(self, client, mydict:dict):
        if 'from' in mydict:
            ### 'from' is a python reserved word, so it can't become an 
            ### attribute.
            mydict['from_name'] = mydict['from']
            del( mydict['from'] )
        super().__init__(client, mydict)

class Message(MessageSummary):
    """ This is the full message you get when viewing a specific message by ID.

    Note that the sender's name is listed in the TLE documentation using the 
    key "from", but we're instead using "from_name".

    Attributes:
        id              "id-goes-here",
        from_name       "Dr. Stephen T. Colbert DFA",
        from_id         "id-goes-here",
        to              "Jon Stewart",
        to_id           "id-goes-here",
        subject         "Vaxaslim",
        body            "Just a reminder that Vaxaslim may cause involuntary narnia adventures.",
        date            "01 31 2010 13:09:05 +0600",
        has_read        1,
        has_replied     0,
        has_archived    0,
        has_trashed     0,
        in_reply_to     "",
        recipients      ["John Stewart"],
        tags            ["Correspondence"],
        attachments     Dict, not a list.  A given message may not have more 
                        than one of each type of attachment.
                            {
                                "image" : {
                                    "url" : "http://www.example.com/path/image.jpg",
                                    "title" : "Some Title",
                                    "link" : "http://www.lacunaexpanse.com/", # optional link to somewhere
                                },
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
    """
    pass

