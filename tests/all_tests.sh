#!/usr/bin/env bash

python3 tests/hello_world.py &&\
python3 tests/new_hello_world.py &&\
python3 tests/eosio_token.py &&\
python3 tests/tic_tac_toe.py &&\

eosfactory/pythonmd.sh docs/cases/account.md &&\
eosfactory/pythonmd.sh docs/cases/master_account.md &&\
eosfactory/pythonmd.sh docs/cases/symbolic_names.md &&\
eosfactory/pythonmd.sh docs/cases/wallet.md &&\
eosfactory/pythonmd.sh docs/patterns/set/set_account_permission.md &&\
eosfactory/pythonmd.sh docs/tutorials/02.InteractingWithEOSContractsInEOSFactory.md &&\

eosfactory/pythonmd.sh docs/tutorials/03.BuildingAndDeployingEOSContractsInEOSFactory.md &&\
eosfactory/pythonmd.sh docs/tutorials/04.WorkingWithEOSContractsUsingEOSFactoryInVSC.md

