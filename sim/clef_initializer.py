# This connects to the openbsd ftp site and
# downloads the recursive directory listing.
import pexpect
child = pexpect.spawn('clef --keystore  ./node2/keystore/ --chainid 31051992')
child.expect('> ')
child.sendline('ok')
print(child.before)
child.expect('>')
child.sendline('0123456789')
print(child.before)
child.interact()