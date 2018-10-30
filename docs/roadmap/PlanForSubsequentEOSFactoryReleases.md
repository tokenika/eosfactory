# Plan for Subsequent EOSFactory Releases

#### Integration with EOSJS

As of now *EOSFactory* is using C++-based `cleos` to communicate with a local or remote testnet. In the future we plan to create an alternative and also use the JavaScript-based `eosjs`.

#### Flexible folder structure

We plan to make *EOSFactory* more generic, i.e. allow the user to have his own folder structure, instead of imposing our own.

#### Less invasive configuration

We'd like to avoid using `~/.profile` and `~/.bash_profile` files for storing *EOSFactory* configuration.

#### Better integration with Visual Studio Code

There is still a lot of things we can do to make *EOSFactory* more tightly integrated with VSC. What's important, we still want to offer the option to perform all the tasks in a standard bash terminal & your favorite code editor or IDE, thus work entirely outside of VSC.