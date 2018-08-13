# How to set custom permissions with eosfactory? #34

https://github.com/tokenika/eosfactory/issues/34

## Q 

I am building unit tests for my contracts but some of my contracts invoke 
actions from other contracts so I need to set custom permissions in my scripts. 
Checked the documentation but couldn't find it. Is there any set permission 
functionality?

## A

With 'EOSFactory v1.1', you cannot have a multiple 'permission' argument. 
In the new version, 'EOSFactory v2.0', the 'permission' argument is fully 
served. You can see an article on this issue in the branch 'dev' of the 
repository: 'docs/source/cases/arguments.md'.

The code in the branch 'dev' is tested and operational, usually. However, note 
that the branch 'dev' is not consistent yet. Especially, the tutorials are not
updated. But you can rely the articles in the 'docs/source/cases/' directory 
(most of them can be run as python scripts), and on tests in the 'tests/' 
directory.
