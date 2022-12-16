<h1 class="contract">init</h1>

---
spec_version: "0.1.0"
title: initialize otcbook
summary: 'Init AMA OTCStore'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---
Initialize otcbook

<h1 class="contract">setmerchant</h1>

---
spec_version: "0.1.0"
title: Set merchant info
summary: 'Set merchant's info'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

Merchant to set one's info including selling conditions/memo

<h1 class="contract">openorder</h1>

---
spec_version: "0.1.0"
title: open an order
summary: 'Open an OTC order'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

Open an OTC order. Currently only merchant orders are allowed to open.

<h1 class="contract">closeorder</h1>

---
spec_version: "0.1.0"
title: close order
summary: 'Close one's order'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

Close one's order to stop from others to deal with it.
Once the order has been fully fulfilled, it can be also triggered to be closed.
When the order is in a closed status, it can no longer be entered by any counterparty.

<h1 class="contract">opendeal</h1>

---
spec_version: "0.1.0"
title: open deal
summary: 'Open a deal to an order'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

A counterparty can actively seek through a list of open orders and claim one
to deal with. Once a deal is openned, a certain amount of funds will be thus frozen
or locked in the order from others to spend it until either the fund is unfrozne or settled.


<h1 class="contract">closedeal</h1>

---
spec_version: "0.1.0"
title: close a deal
summary: 'Close a deal to an order'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

A deal creator can actively close a deal such that either the correspondig order locked funds
has been either settled or unfrozen.

<h1 class="contract">processdeal</h1>

---
spec_version: "0.1.0"
title: pass a deal
summary: 'Pass a deal to an order'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

A deal that is processed by a maker/taker or admin.

<h1 class="contract">withdraw</h1>

---
spec_version: "0.1.0"
title: withdraw balance amount
summary: 'Merchant to withdraw balance amount from the otcbook contract'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---
After a merchant wants to stop making orders, remaining amount must be withdrawn in order to reach
merchant's personal account
