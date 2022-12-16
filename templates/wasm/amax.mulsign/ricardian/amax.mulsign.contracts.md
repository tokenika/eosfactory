<h1 class="contract">init</h1>

---
spec_version: "0.1.0"
title: set a collector for fee
summary: 'set a collector for fee'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---
set a collector for fee



<h1 class="contract">setmulsignm</h1>

---
spec_version: "0.1.0"
title: update a mulsign wallet proposal approve votes
summary: 'update a mulsign wallet proposal approve votes'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

update a mulsign wallet proposal approve votes


<h1 class="contract">setmulsigner</h1>
---
spec_version: "0.1.0"
title: set a multisigner to a multisign wallet
summary: 'set a multisigner to a multisgin wallet that has been created'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

a multisign wallet owner can add or update a multisigner to his or her wallet according to the limit of n co-signer;

<h1 class="contract">delmulsigner</h1>
---
spec_version: "0.1.0"
title: delete a multisigner
summary: 'delete a multisginer from a multisign wallet'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

a multisign wallet owner can choose to delete a multisigner from his or her wallet


<h1 class="contract">setwapexpiry</h1>
---
spec_version: "0.1.0"
title: set a multisign wallet max expire time
summary: 'set a multisign wallet max expire time'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

set proposal expiry time in seconds for a given wallet


<h1 class="contract">ontransfer</h1>
---
spec_version: "0.1.0"
title: transfer notify 
summary: 'transfer amax to create wallet or deposite asset for a mulsign wallet'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

memo: 
1) create:$title transfer fee to create a wallet, title size should less than 128
2) lock:$wallet_id  transfer asset to a mulsign wallet, all type of arc20 token supported


<h1 class="contract">propose</h1>
---
spec_version: "0.1.0"
title: propose an action for a mulsign wallet
summary: 'mulsigner can propose an action'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---
mulsign wallet operation: include 'transfer','setmulsignm','setmulsigner','delmulsigner'
operation's params, settings with string: 
    transefer: name from, name to, asset quantity, memo, contract
    setmulsignm: uint8_t m
    setmulsigner: name mulsigner, uint8_t weight
    delmulsigner: name mulsigner


<h1 class="contract">cancel</h1>
---
spec_version: "0.1.0"
title: cancel a proposal before it expires
summary: 'cancel a proposal before it expires'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

cancel a proposal before it expires


<h1 class="contract">respond</h1>
---
spec_version: "0.1.0"
title: respond result for a multisign wallet proposal
summary: 'respond result for a multisign wallet proposal'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

respond result for a multisign wallet proposal
vote type: 0, against; 1, approve



<h1 class="contract">execute</h1>
---
spec_version: "0.1.0"
title: execute a proposal action
summary: 'execute a proposal action'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

execute a proposal action
