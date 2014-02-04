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

#### ssh

```
~dcw/tmp/git-clone-test/raspberry-pi-wifi/ssh-pi 80:1f:02:af:31:19
```

#### scp via MAC Address

```
bash -c 'export PERL5LIB=/homes/dcw/tmp/git-clone-test/raspberry-pi-wifi/PERSISTENT_TUPLES; ~/robot/scp-pi 80:1f:02:af:31:19'
```

#### Adding aliases

To simplify connecting via MAC address you should add the following lines to ~/.cshrc

```
alias pi "~dcw/tmp/git-clone-test/raspberry-pi-wifi/ssh-pi 80:1f:02:af:31:19"
alias pithon "bash -c 'export PERL5LIB=/homes/dcw/tmp/git-clone-test/raspberry-pi-wifi/PERSISTENT_TUPLES; ./scp-pi 80:1f:02:af:31:19'"
```
