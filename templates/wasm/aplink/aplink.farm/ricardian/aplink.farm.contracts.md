<h1 class="contract">lease</h1>

---
spec_version: "0.1.0"
title: aplink farming
summary: 'lease a land for cropping APL'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

lord can lease a land to farmer for croping APL to customer


<h1 class="contract">setlord</h1>
---
spec_version: "0.1.0"
title: set lord for lands
summary: 'set a lord to manage all lands'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

lord can lease and reclaim land
jamfactory is used to collect expired apples
lands can be disabled by lord

<h1 class="contract">reclaim</h1>
---
spec_version: "0.1.0"
title: reclaim a land
summary: 'reclaim a land and return all apples to recipient'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---
reclaim a disabled land, and send apples to recipient

<h1 class="contract">setstatus</h1>
---
spec_version: "0.1.0"
title: change a land's status
summary: 'Enable/Disable a land'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

param status  0:NONE 1:Enable 2:Disable

<h1 class="contract">plant</h1>
---
spec_version: "0.1.0"
title: farmer plant apples to an apple
summary: 'farmer plant apples and send to a customer'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

farmer ripen apples to an apple and send it to farmer

<h1 class="contract">pick</h1>
---
spec_version: "0.1.0"
title: farmer pick apples
summary: 'farmer pick apples or collect expired apples'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

farmer pick apples or collect expired apples


<h1 class="contract">ontransfer</h1>
---
spec_version: "0.1.0"
title: lord plant apples to a land
summary: 'lord plant apples to a land'
icon: http://127.0.0.1/ricardian_assets/amax.contracts/icons/
---

lord plant apples to a land
