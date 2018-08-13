# Documentation Update #40

https://github.com/tokenika/eosfactory/issues/40

## Q 

* I was looking to try and list the accounts in the sess.wallet object, but 
couldn't find any documentation on this.
* I tried finding this in the documentation, but maybe I missed it. What is the 
procedure for running unit tests against a smart contract?

## A

jakub-zarembinski commented 4 days ago

What is the procedure for running unit tests against a smart contract? 
See tutorials:

* 02.InteractingWithEOSContractsInEOSFactory
* 03.BuildingAndDeployingEOSContractsInEOSFactory
* 04.WorkingWithEOSContractsUsingEOSFactoryInVSC

We will explain the issue better in a new edition, soon.

Now, you can see new exampled and articles on this issue in the branch 'dev' of 
the repository.

The code in the branch 'dev' is tested and operational, most often. However, note 
that the branch 'dev' is not consistent yet. Especially, the tutorials are not
updated. But you can rely the articles in the 'docs/source/cases/' directory 
(most of them can be run as python scripts), and on tests in the 'tests/' 
directory.