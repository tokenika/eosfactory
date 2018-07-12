# Plan for Subsequent EOSFactory Releases

#### Improving Python interface

We plan to make EOSFactory workflow more intuitive and user-friendly. We still see some areas for improvement in this regard.

####Improving account management

We need to improve the way accounts are handled and managed, especially in case of interacting with a public testnet. As of now, it might happen that account mappings get erased and the user needs to start from scratch in terms of setting up an account on a public testnet.

#### Better integration with Visual Studio Code

There is still a lot of things we can do to make EOSFactory more tightly integrated with VSC. What's important, we still want to offer the option to perform all the tasks in a standard bash terminal & your favorite code editor or IDE, thus work entirely outside of VSC.

#### Extracting the C++ layer as a separate project

We plan to move the C++ layer's source code (i.e.`teos`) into a separate repository, so that it can also serve as a foundation for other projects. What's nice about `teos` is that it's a static library, not an executable like `cleos`, and therefore it's much more suitable for integrations.