## Installing eosjs

Install packages globally on your operating system.

`yarn global add eosjs`

To use the installed packages, the install location has to be added to the PATH environment variable of your shell. For bash for example, you can add this line at the end of your .bashrc:

`export PATH="$(yarn global bin):$PATH"`