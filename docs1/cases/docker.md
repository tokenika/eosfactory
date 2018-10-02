If you don't alredy have docker installed, you can download it [here](https://www.docker.com/community-edition): 

## Step 1: Get the docker image
The below statement will download an Ubuntu image which contains the compiled software.
```shell
$ docker pull eosio/eos
```

## Step 2: Boot Node and Wallet

```shell
$ docker run --name eosio \
  --publish 7777:7777 \
  --publish 127.0.0.1:5555:5555 \
  --volume /c/Workspaces/EOS/contracts:/c/Workspaces/EOS/contracts \
  --detach \
  eosio/eos \
  /bin/bash -c \
  "keosd --http-server-address=0.0.0.0:5555 & exec nodeos -e -p eosio --plugin eosio::producer_plugin --plugin eosio::history_plugin --plugin eosio::chain_api_plugin --plugin eosio::history_plugin --plugin eosio::history_api_plugin --plugin eosio::http_plugin -d /mnt/dev/data --config-dir /mnt/dev/config --http-server-address=0.0.0.0:7777 --access-control-allow-origin=* --contracts-console --http-validate-host=false --filter-on='*'"
```

With the settings above, it make sense the following:

```shell
$ docker exec -it eosio bash
```

```shell
root@cad472d46ffb:/# cleos --wallet-url http://127.0.0.1:5555 wallet list keys
```

```shell
root@cad472d46ffb:/# cleos --wallet-url http://127.0.0.1:5555 --url http://127.0.0.1:7777 get info

root@cad472d46ffb:/# cleos --wallet-url http://127.0.0.1:5555 --url http://127.0.0.1:7777 get block 56
```

```shell
$ docker container ls --all
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS                    PORTS               NAMES
cad472d46ffb        eosio/eos           "/bin/bash -c 'keosd…"   23 hours ago        Exited (0) 21 hours ago                       eosio
```

```shell
$ docker start eosio
eosio
```

```shell
$ docker container ls --all
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                              NAMES
cad472d46ffb        eosio/eos           "/bin/bash -c 'keosd…"   23 hours ago        Up 13 seconds       127.0.0.1:5555->5555/tcp, 0.0.0.0:7777->7777/tcp   eosio
```

```shell
$ ps
      PID    PPID    PGID     WINPID   TTY         UID    STIME COMMAND
    13068       1   13068      14112  cons0     197608 15:25:45 /usr/bin/bash
    14360   13068   14360      16020  cons0     197608 19:05:49 /usr/bin/ps
```

## With Windows

See [here](https://stackoverflow.com/questions/42866013/docker-toolbox-localhost-not-working).

```shell
$ docker run -p 80:80 nginx
Unable to find image 'nginx:latest' locally
latest: Pulling from library/nginx
802b00ed6f79: Pull complete
c16436dbc224: Pull complete
683eac851b28: Pull complete
Digest: sha256:e8ab8d42e0c34c104ac60b43ba60b19af08e19a0e6d50396bdfd4cef0347ba83
Status: Downloaded newer image for nginx:latest
```

```shell
$ docker ps -a
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                              NAMES
564d3a1ea601        nginx               "nginx -g 'daemon of…"   28 seconds ago      Up 26 seconds       0.0.0.0:80->80/tcp                                 epic_mirzakhani
cad472d46ffb        eosio/eos           "/bin/bash -c 'keosd…"   26 hours ago        Up 3 hours          127.0.0.1:5555->5555/tcp, 0.0.0.0:7777->7777/tcp   eosio

```

```shell
/mnt/c/Workspaces/EOS/eos/build/programs/cleos/cleos --url http://192.168.99.100:7777 get block 56

{
  "timestamp": "2018-09-30T15:15:03.000",
  "producer": "eosio",
  "confirmed": 0,
  "previous": "00000037cddd269a2a06ca6a716b0ab2ae6f39fbf1fbf0898773d31ad6a02405",
  "transaction_mroot": "0000000000000000000000000000000000000000000000000000000000000000",
  "action_mroot": "5f4f6a0e560e945eed6529560eeb87a998b82760ec1b8302f63148cbb2d1ac8a",
  "schedule_version": 0,
  "new_producers": null,
  "header_extensions": [],
  "producer_signature": "SIG_K1_JvKEKop86duMMYbyThxi1hKGPpqyKmUNRgWFPWYHyqePqeDyjDgpiTqwxazDVP4uc8tVFh5JCrvVvpUTujX4dT8BWF2uTt",
  "transactions": [],
  "block_extensions": [],
  "id": "0000003810175bc01efa007cc33137646c045274efdc2abdff17a362bed5e2df",
  "block_num": 56,
  "ref_block_prefix": 2080438814
}
```