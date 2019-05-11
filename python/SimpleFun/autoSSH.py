server = {
  "name":{
    "addr":"1.1.1.1", 
    "user":"root", 
    "pass","ssh_passwd", 
    "port":22
  }
}

def ssh(name):
    global server;

    if name in server:
        host = server[name];

        c = pexpect.spawn("ssh -p %s %s@%s" %
                (host['port'], host['user'], host['pass']));
        r = c.expect([pexpect.TIMEOUT, "yes/no", '[P|p]assword']);

        try:
            if r == 0:
                raise Exception();
            if r == 1:
                c.sendline ('yes');
                if not c.expect([pexpect.TIMEOUT, 'password: ']):
                    raise Exception();
            #if r == 2:
            c.sendline(k);
            c.interact();
        except Exception:
            print c.before, c.after
            return None;



try:
    ssh(sys.argv[1]);
except:
    for name in server:
        print name;
