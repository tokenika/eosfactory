
<h1 class="contract"> init </h1>

---
spec_version: "0.1.0"
title: init
summary: 'initilize & maintain'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

initilize & maintain contract states

<h1 class="contract"> addadmin </h1>

---
spec_version: "0.1.0"
title: Add an admin
summary: 'Add an admin who can approve advanced plans'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

{{$action.account}} agrees to create a new token with symbol {{asset_to_symbol_code maximum_supply}} to be managed by {{issuer}}.

This action will allow a new admin to be able to approve proposals.

{{issuer}} will be allowed to issue tokens into circulation, up to a maximum supply of {{maximum_supply}}.


<h1 class="contract"> deladmin </h1>

---
spec_version: "0.1.0"
title: Delete a registered admin
summary: 'Delete a registered admin from the approval admin list'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

Super admin to delete a registered admin from the approval admin list.

{{#if memo}}There is a memo attached to the transfer stating:
{{memo}}
{{/if}}


<h1 class="contract"> addplan </h1>

---
spec_version: "0.1.0"
title: create a lock plan
summary: 'create a lock plan for a particular bank asset'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

Super admin to create a lock plan to a particular bank asset


<h1 class="contract"> propose </h1>

---
spec_version: "0.2.0"
title: propose an advance-unlock
summary: 'Propose to unlock a plan with advance timepoints'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/transfer.png#5dfad0df72772ee1ccc155e670c1d124f5c5122f1d5027565df38b418042d1dd
---

Any user can propose to add advance unlock timepoints to an existing lock plan

<h1 class="contract"> approve </h1>

---
spec_version: "0.1.0"
title: Approve a proposal
summary: 'admin to approve a proposal for adding advanced-unlock timepoints'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

Admin user to approve a proposal for adding advanced-unlock timepoints. As long as
a cohort of admins agree to the proposal, it will be executed accordingly.

<h1 class="contract"> transfer </h1>

---
spec_version: "0.2.0"
title: Stake assets into contract for a benefitiary user
summary: 'Stake assets to a user but locked within the contract'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

withdraw staked assets that are redeemable belong to the user

<h1 class="contract"> withdraw </h1>

---

contract owner to withdraw staked assets that are redeemable
according to the given plan, to correct miss-staking

<h1 class="contract"> withdrawx </h1>

---

repair contract data

<h1 class="contract"> repair </h1>

---

spec_version: "0.2.0"
title: User to withdraw assets
summary: 'User to withdraw assets from the escrow contract'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/token.png#207ff68b0406eaa56618b08bda81d6a0954543f36adc328ab3065f31a5c5d654
---

User can redeem or withdraw a certain amount of assets according to the lock plan
which has accumulated ratio of unlocked assets for each user.
