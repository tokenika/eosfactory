mcli='amcli -u https://am1.acsiwang.com'

$mcli push action mdao.conf init '["metadao.fund",["metadao", "v1.0", "https://metadao.fan", "https://mylogo.png"],"1.00000000 AMAX","111111111111","running"]' -p mdao.conf

$mcli push action amax.token transfer '["111111111111","mdao.info","1.00000000 AMAX","amax.dao|AMAX DAO|amax.dao|https://amaxscan.io/amax.png"]' -p 111111111111
$mcli push action amax.token transfer '["111111111111","mdao.info","1.00000000 AMAX","aplink.dao|APLink DAO|aplink.dao|https://amaxscan.io/amax.png"]' -p 111111111111
$mcli push action amax.token transfer '["111111111111","mdao.info","1.00000000 AMAX","mtbl.dao|Meta Balance DAO|mtbl.dao|https://amaxscan.io/amax.png"]' -p 111111111111
$mcli push action amax.token transfer '["111111111111","mdao.info","1.00000000 AMAX","nftone.dao|NFTOne DAO|nftone.dao|https://amaxscan.io/amax.png"]' -p 111111111111

$mcli push action mdao.info updatedao '["111111111111","amax.dao","https://amaxscan.io/amax.png","amax.dao",[],"","","!weTQgZHoqBcnTgOelF:xdao.land"]' -p 111111111111

$mcli push action mdao.conf init '["metadao.fund",["metadao", "v1.0", "https://metadao.fan", "https://mylogo.png"],"1.00000000 AMAX","mdao.admin","running"]' -p mdao.conf