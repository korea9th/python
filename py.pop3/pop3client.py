################################################################## pop3 client   ########################################################################

#!/usr/local/bin/python
#
# This script is a helper to clean POP3 mailboxes
# containing malformed mails that hangs MUA's, that
# are too large, or whatever...
#
# It iterates over the non-retrieved mails, prints
# selected elements from the headers and prompt the
# user to delete bogus messages.
#
# Written by Xavier Defrang <xavier.defrang@brutele.be>
#

#
import getpass, poplib, re, os
import email

# Change this to your needs
POPHOST = "127.0.0.1"
POPUSER = "kisa"
POPPASS = "kisa"

#POPHOST = "127.0.0.1"
#POPUSER = "jdoe"
#POPPASS = "1"

# How many lines of message body to retrieve
MAXLINES = 50


# Headers we're actually interrested in
rx_headers  = re.compile(r"^(From|To|Subject)")

try:
    poplib._MAXLINE = 204800
    
    if not os.path.exists('download_emls'):
        os.makedirs('download_emls')

    # Connect to the POPer and identify user
    pop = poplib.POP3(POPHOST, 3110)#110)
    pop.user(POPUSER)

    if not POPPASS:
        # If no password was supplied, ask for it
        POPPASS = getpass.getpass("Password for %s@%s:" % (POPUSER, POPHOST))

    # Authenticate user
    pop.pass_(POPPASS)

    # Get some general informations (msg_count, box_size)
    stat = pop.stat()

    # Print some useless information
    print ("Logged in as %s@%s" % (POPUSER, POPHOST))
    print ("Status: %d message(s), %d bytes" % (stat[0], stat[1]))
#    print ("Status: %d message(s), %d bytes" % stat)

    response, filenames, size = pop.list()
    
    print(filenames)

    bye = 0
    count_del = 0
    for n in range(stat[0]):
        msgnum = n+1

        print("Before         retr : " + str(msgnum))

        # Retrieve headers
        response, lines, bytes = pop.retr(msgnum)

        print("After         retr")


#        response, lines, bytes = pop.top(msgnum, MAXLINES)
#        f = open('download_emls/'+ str(filenames[n]), "wb")
        f = open('download_emls/'+ filenames[n].decode('utf-8'), "wb")
#        for line in lines:
#            f.write("%s\n" % line)
        for line in lines:
            f.write(line)
            f.write('\n'.encode())
        f.close()
#        print(lines)
        # Print message info and headers we're interrested in
        print ("Message %d (%d bytes) [%s]" % (msgnum, bytes, filenames[n]))
        print ("-" * 30)
#        print ("\n".join(filter(rx_headers.match, lines)))
        print ("-" * 30)

    # Input loop
    """
    while 1:
        k = input("(q=quit) What?")
        if k in "qQ":
            bye = 1
            break

        # Time to say goodbye?
        if bye:
            print ("Bye")
            break
    """

    """
    while 1:
        k = input("(d=delete, s=skip, v=view, q=quit) What?")
        if k in "dD":
            # Mark message for deletion
            k = input("Delete message %d? (y/n)" % msgnum)
            if k in "yY":
                pop.dele(msgnum)
                print ("Message %d marked for deletion" % msgnum)
                count_del += 1
            break
        elif k in "sS":
            print ("Message %d left on server" % msgnum)
            break
        elif k in "vV":
            print ("-" * 30)
            print ("\n".join(lines))
            print ("-" * 30)
        elif k in "qQ":
            bye = 1
            break

        # Time to say goodbye?
        if bye:
            print ("Bye")
            break
    """
    # Summary
    print ("Deleting %d message(s) in mailbox %s@%s" % (count_del, POPUSER, POPHOST))

    # Commit operations and disconnect from server
    print ("Closing POP3 session")
    pop.quit()

except (poplib.error_proto) as e:

    # Fancy error handling
    print ("POP3 Protocol Error:" ,e)
    
except Exception as ex:
    print(ex)
