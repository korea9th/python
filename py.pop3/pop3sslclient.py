import getpass, poplib
user = 'user' 
Mailbox = poplib.POP3_SSL('pop.naver.com', '995') 
Mailbox.user(user) 
Mailbox.pass_('password') 
numMessages = len(Mailbox.list()[1])
for i in range(numMessages):
    for msg in Mailbox.retr(i+1)[1]:
        print (msg)
Mailbox.quit()
