# Robotics coursework

Pedro, Piyapat, Andrei, Ryan

## Connecting to the robot

### Via IP Address

#### Password-less login/scp
ssh-copy-id pi@129.31.192.29

#### ssh

```
ssh pi@129.31.196.157
```

#### scp

```
scp ~/robot/*.py pi@129.31.196.157:~/rapp/
```

#### Mount the pi's home to ~/robot 

```
sshfs pi@129.31.196.157:/home/pi ~/robot
```

### Via MAC Address

#### Adding aliases

To simplify connecting via MAC address you should add the following lines to ~/.cshrc

```
setenv ICL_USER_PASS user:password

alias pi-ip 'curl -s --data "macaddress=80:1f:02:af:31:19" --user $ICL_USER_PASS https://www.doc.ic.ac.uk/~jrj07/robotics/index.cgi | grep -E -o "(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)\.(25[0-5]|2[0-4][0-9]|[01]?[0-9][0-9]?)" | head -n 1'
alias pi-ssh "ssh pi@`pi-ip`"
alias pi-scp "scp ./*.py pi@`pi-ip`:~/rapp/"
```

#### start server
sudo /etc/init.d/nodejs.sh start
