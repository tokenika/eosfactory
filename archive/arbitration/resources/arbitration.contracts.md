<h1 class="contract">
   transfer
</h1>
### Parameters
Input parameters:

* `from` (:name, the name of the buyer)
* `to` (:name, the name of the deposit)
* `quantity` (:asset, the quantity)
* `memo` (:string, the name of seller)

Implied parameters: 

* `account_name` (:name, the name of the party invoking and signing the contract)

### Intent
INTENT. Listens for transfer to smartcontract's EOS account, and populates deposits with sent money.

### Term
TERM. This Contract expires at the conclusion of code execution.