
import lacuna.bc

class Inbox(lacuna.bc.LacunaObject):
    """ Represents your mailbox.
    
.. _valid_msg_tags:

Several methods allow a `tags` argument.  Valid message tags:
    Alert, Attack, Complaint, Colonization, Correspondence, Excavator, 
    Intelligence, Medal, Mission, Parliament, Probe, Spies, Trade,
    Tutorial

    """

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
            self.get_type(result['message_count']),
        )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_inbox( self, opts:dict = {}, *args, **kwargs ):
        """ View the messages in your empire's inbox, 25 messages per page.
        
        Args:
            opts (optional dict): With the keys::

              'page_number': Integer page number to return.  Defaults to 1.
              'tags': List of :ref:`tags <valid_msg_tags>` to filter by.
        Returns:
            tuple: Inbox::

                - messages -- List of :class:`lacuna.inbox.MessageSummary` objects
                - count -- Integer total number of messages in the inbox

        The tags you passed in are joined with 'or'.  So for this call, you'll 
        get back both excavator and correspondence messages::

                msgs, ttl = mail.view_inbox({
                    "page_number": 3,
                    "tags": ["excavator", "correspondence"]
                })

        Sending an invalid tag will not throw an exception, it'll merely 
        return 0 messages.
        """
        return self._set_mail_return( kwargs['rslt'] )


    @lacuna.bc.LacunaObject.call_returning_meth
    def view_archived( self, opts:dict = {}, *args, **kwargs ):
        """  View archived messages.
        
        Args:
            opts (optional dict): containing::

              'page_number': Integer page number to return.  Defaults to 1.
              'tags': List of :ref:`tags <valid_msg_tags>` to filter by.

        Returns:
            tuple: Archived messages

                - messages -- List of :class:`lacuna.inbox.MessageSummary` objects
                - count -- Integer total number of messages in the inbox
        """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_sent( self, opts:dict = {}, *args, **kwargs ):
        """  View sent messages.
        
        Args:
            opts (optional dict): containing:

              'page_number': Integer page number to return.  Defaults to 1.
              'tags': List of :ref:`tags <valid_msg_tags>` to filter by.

        Returns:
            tuple: Sent messages

                - messages -- List of :class:`lacuna.inbox.MessageSummary` objects
                - count -- Integer total number of messages in the inbox
        """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def view_trashed( self, opts:dict = {}, *args, **kwargs ):
        """  View trashed messages.

        Args:
            opts (optional dict): containing:

              'page_number': Integer page number to return.  Defaults to 1.
              'tags': List of :ref:`tags <valid_msg_tags>` to filter by.

        Returns:
            tuple: Sent messages

                - messages -- List of :class:`lacuna.inbox.MessageSummary` objects
                - count -- Integer total number of messages in the inbox
        """
        return self._set_mail_return( kwargs['rslt'] )

    @lacuna.bc.LacunaObject.call_returning_meth
    def read_message( self, message_id:int, *args, **kwargs ):
        """ Reads a message.

        Args:
            message_id (int): ID of the message to read
        Returns:
            lacuna.inbox.Message: The requested message
        """
        return Message(self.client, kwargs['rslt']['message'])

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def archive_messages( self, messages:list, *args, **kwargs ):
        """ Archives one or more messages.

        Args:
            messages (list of ints): IDs of messages to archive
        Returns:
            dict: containing the keys::

                'success': [ List of message IDs that were archived successfully ]
                'failure': [ List of message IDs that failed to be archived ]

        There's no indication why any given message movement succeeded or 
        failed, just that they did.
        """
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def trash_messages( self, messages:list, *args, **kwargs ):
        """ Trashes (deletes) one or more messages.

        Args:
            messages (list of ints): IDs of messages to delete
        Returns:
            dict: containing the keys::

            'success': [ List of message IDs that were archived successfully ]
            'failure': [ List of message IDs that failed to be archived ]

        There's no indication why any given message movement succeeded or 
        failed, just that they did.
        """
        pass
        pass

    @lacuna.bc.LacunaObject.set_empire_status
    @lacuna.bc.LacunaObject.call_member_meth
    def send_message( self, recipients:str, subject:str, body:str, options:dict = {}, *args, **kwargs ):
        """ Sends an in-game mail message.

        Args:
            recipients (str): Comma-separated string containing names of empires 
                to receive your message.  NOT A LIST, a comma-separated string.
            subject (str): < 100 chars in length.  Cannot contain any of &, @, 
                ;, <, or > Unicode is OK (I've mailed myself a snowman).
            body (str): Limit of 200,000 characters.  < and > are disallowed.  
                Also, anything that Regexp::Common::profanity registers as profane disallows the entire message.  This profanity filter can be irritating - it's very sensitive, and you're not informed what word it's triggering on.  "crap" (along with other pretty mild language) is considered profane.
            options (dict): containing::

              'in_reply_to': A message ID to reply to.
              'forward': A message ID to forward.

        Returns:
            dict: containing::

                'sent': ['tmtowtdi', 'Infinate Ones'],
                'unknown': ['no_such_player'] 
            
        The return value is not documented by the API, so what's shown above is 
        the result of a few tests here.  Looks right.

        When forwarding a message, any attachments from the message ID we're 
        forwarding are automatically attached to our current message.  However, 
        the body of the forwarded message is NOT included in the current 
        message.  If you want that to happen, you'll need to do it yourself.

        **Message Formatting**
            This is rarely-enough used and the docs are wordy enough that it's not worth
            repeating it all here.  See https://us1.lacunaexpanse.com/api/Inbox.html#Message_Formatting
        """
        pass



class MessageSummary(lacuna.bc.SubClass):
    """ This is the message summary you get when viewing a list of messages.

    Object Attributes::

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

    **NOTE** The TLE API actually returns the sender's name in a key named 
    ``from``.  Since ``from`` is a Python reserved word and cannot be used as 
    an attribute name, the attribute above has been changed to ``from_name``.
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

    Object Attributes::

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
                            "image" : { "url" : "http://www.example.com/path/image.jpg",
                                        "title" : "Some Title",
                                        "link" : "http://www.lacunaexpanse.com/", # optional link to somewhere   },
                            "link" : {  "url" : "http://www.lacunaexpanse.com/",
                                        "label" : "The Lacuna Expanse Website"   }
                            "table" : [
                                [ "Hostname", "IP Address" ], # first row is always a header
                                [ "example.lacunaexpanse.com", "192.168.1.24" ],
                                [ "another hostname', "another IP" ],
                            ],
                            "map" : {   "surface" : "surface-6",
                                        "buildings" : [{    "x" : -3,
                                                            "y" : 4,
                                                            "image" : "apples4"  }]
                                    }
                        }
    """
    pass

