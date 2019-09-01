/*
Account object name: ALICE
name: tppt1eqgjks3
created: 2019-08-02T07:19:31.500
permissions:
     owner     1:    1 ALICE@owner
        active     1:    1 ALICE@active
memory:
     quota:       unlimited  used:      2.66 KiB

net bandwidth:
     used:               unlimited
     available:          unlimited
     limit:              unlimited

cpu bandwidth:
     used:               unlimited
     available:          unlimited
     limit:              unlimited
*/

/*
Account object name: MASTER
name: nukjygmgkn3x
created: 2019-02-20T16:11:09.500
permissions:
     owner     1:    1 MASTER@owner
        active     1:    1 MASTER@active
memory:
     quota:     5.341 KiB    used:     5.209 KiB

net bandwidth:
     staked:          1.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:               337 bytes
     available:        131.4 KiB
     limit:            131.8 KiB

cpu bandwidth:
     staked:          1.0000 EOS           (total stake delegated from account to self)
     delegated:       0.0000 EOS           (total staked delegated to account from others)
     used:             1.233 ms
     available:        46.24 ms
     limit:            47.48 ms

EOS balances:
     liquid:          123.4027 EOS
     staked:            2.0000 EOS
     unstaking:         0.0000 EOS
     total:           125.4027 EOS

producers:     <not voted>
 */

void get_account(const string &accountName, const string &coresym, bool json_format)
{
    fc::variant json;
    if (coresym.empty())
    {
        json = call(get_account_func, fc::mutable_variant_object("account_name", accountName));
    }
    else
    {
        json = call(get_account_func, fc::mutable_variant_object("account_name", accountName)("expected_core_symbol", symbol::from_string(coresym)));
    }

    auto res = json.as<eosio::chain_apis::read_only::get_account_results>();
    if (!json_format)
    {
        asset staked;
        asset unstaking;

        if (res.core_liquid_balance.valid())
        {
            unstaking = asset(0, res.core_liquid_balance->get_symbol()); // Correct core symbol for unstaking asset.
            staked = asset(0, res.core_liquid_balance->get_symbol());    // Correct core symbol for staked asset.
        }

        std::cout << "created: " << string(res.created) << std::endl;

        if (res.privileged)
            std::cout << "privileged: true" << std::endl;

        constexpr size_t indent_size = 5;
        const string indent(indent_size, ' ');

////////////////////////////////////////////////////////////////////////////////
        std::cout << "permissions: " << std::endl;
////////////////////////////////////////////////////////////////////////////////

        unordered_map<name, vector<name> /*children*/> tree;
        vector<name> roots; //we don't have multiple roots, but we can easily handle them here, so let's do it just in case
        unordered_map<name, eosio::chain_apis::permission> cache;
        for (auto &perm : res.permissions)
        {
            if (perm.parent)
            {
                tree[perm.parent].push_back(perm.perm_name);
            }
            else
            {
                roots.push_back(perm.perm_name);
            }
            auto name = perm.perm_name; //keep copy before moving `perm`, since thirst argument of emplace can be evaluated first
            // looks a little crazy, but should be efficient
            cache.insert(std::make_pair(name, std::move(perm)));
        }
        std::function<void(account_name, int)> dfs_print = [&](account_name name, int depth) -> void {
            auto &p = cache.at(name);
            std::cout << indent << std::string(depth * 3, ' ') << name << ' ' << std::setw(5) << p.required_auth.threshold << ":    ";
            const char *sep = "";
            for (auto it = p.required_auth.keys.begin(); it != p.required_auth.keys.end(); ++it)
            {
                std::cout << sep << it->weight << ' ' << string(it->key);
                sep = ", ";
            }
            for (auto &acc : p.required_auth.accounts)
            {
                std::cout << sep << acc.weight << ' ' << string(acc.permission.actor) << '@' << string(acc.permission.permission);
                sep = ", ";
            }
            std::cout << std::endl;
            auto it = tree.find(name);
            if (it != tree.end())
            {
                auto &children = it->second;
                sort(children.begin(), children.end());
                for (auto &n : children)
                {
                    // we have a tree, not a graph, so no need to check for already visited nodes
                    dfs_print(n, depth + 1);
                }
            } // else it's a leaf node
        };
        std::sort(roots.begin(), roots.end());
        for (auto r : roots)
        {
            dfs_print(r, 0);
        }

        auto to_pretty_net = [](int64_t nbytes, uint8_t width_for_units = 5) {
            if (nbytes == -1)
            {
                // special case. Treat it as unlimited
                return std::string("unlimited");
            }

            string unit = "bytes";
            double bytes = static_cast<double>(nbytes);
            if (bytes >= 1024 * 1024 * 1024 * 1024ll)
            {
                unit = "TiB";
                bytes /= 1024 * 1024 * 1024 * 1024ll;
            }
            else if (bytes >= 1024 * 1024 * 1024)
            {
                unit = "GiB";
                bytes /= 1024 * 1024 * 1024;
            }
            else if (bytes >= 1024 * 1024)
            {
                unit = "MiB";
                bytes /= 1024 * 1024;
            }
            else if (bytes >= 1024)
            {
                unit = "KiB";
                bytes /= 1024;
            }
            std::stringstream ss;
            ss << setprecision(4);
            ss << bytes << " ";
            if (width_for_units > 0)
                ss << std::left << setw(width_for_units);
            ss << unit;
            return ss.str();
        };

////////////////////////////////////////////////////////////////////////////////
        std::cout << "memory: " << std::endl
////////////////////////////////////////////////////////////////////////////////
                  << indent << "quota: " << std::setw(15) << to_pretty_net(res.ram_quota) << "  used: " << std::setw(15) << to_pretty_net(res.ram_usage) << std::endl
                  << std::endl;

////////////////////////////////////////////////////////////////////////////////
        std::cout << "net bandwidth: " << std::endl;
////////////////////////////////////////////////////////////////////////////////
        if (res.total_resources.is_object())
        {
            auto net_total = to_asset(res.total_resources.get_object()["net_weight"].as_string());

            if (net_total.get_symbol() != unstaking.get_symbol())
            {
                // Core symbol of nodeos responding to the request is different than core symbol built into cleos
                unstaking = asset(0, net_total.get_symbol()); // Correct core symbol for unstaking asset.
                staked = asset(0, net_total.get_symbol());    // Correct core symbol for staked asset.
            }

            if (res.self_delegated_bandwidth.is_object())
            {
                asset net_own = asset::from_string(res.self_delegated_bandwidth.get_object()["net_weight"].as_string());
                staked = net_own;

                auto net_others = net_total - net_own;

                std::cout << indent << "staked:" << std::setw(20) << net_own
                          << std::string(11, ' ') << "(total stake delegated from account to self)" << std::endl
                          << indent << "delegated:" << std::setw(17) << net_others
                          << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
            }
            else
            {
                auto net_others = net_total;
                std::cout << indent << "delegated:" << std::setw(17) << net_others
                          << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
            }
        }

        auto to_pretty_time = [](int64_t nmicro, uint8_t width_for_units = 5) {
            if (nmicro == -1)
            {
                // special case. Treat it as unlimited
                return std::string("unlimited");
            }
            string unit = "us";
            double micro = static_cast<double>(nmicro);

            if (micro > 1000000 * 60 * 60ll)
            {
                micro /= 1000000 * 60 * 60ll;
                unit = "hr";
            }
            else if (micro > 1000000 * 60)
            {
                micro /= 1000000 * 60;
                unit = "min";
            }
            else if (micro > 1000000)
            {
                micro /= 1000000;
                unit = "sec";
            }
            else if (micro > 1000)
            {
                micro /= 1000;
                unit = "ms";
            }
            std::stringstream ss;
            ss << setprecision(4);
            ss << micro << " ";
            if (width_for_units > 0)
                ss << std::left << setw(width_for_units);
            ss << unit;
            return ss.str();
        };

        std::cout << std::fixed << setprecision(3);
        std::cout << indent << std::left << std::setw(11) << "used:" << std::right << std::setw(18) << to_pretty_net(res.net_limit.used) << "\n";
        std::cout << indent << std::left << std::setw(11) << "available:" << std::right << std::setw(18) << to_pretty_net(res.net_limit.available) << "\n";
        std::cout << indent << std::left << std::setw(11) << "limit:" << std::right << std::setw(18) << to_pretty_net(res.net_limit.max) << "\n";
        std::cout << std::endl;

////////////////////////////////////////////////////////////////////////////////
        std::cout << "cpu bandwidth:" << std::endl;
////////////////////////////////////////////////////////////////////////////////

        if (res.total_resources.is_object())
        {
            auto cpu_total = to_asset(res.total_resources.get_object()["cpu_weight"].as_string());

            if (res.self_delegated_bandwidth.is_object())
            {
                asset cpu_own = asset::from_string(res.self_delegated_bandwidth.get_object()["cpu_weight"].as_string());
                staked += cpu_own;

                auto cpu_others = cpu_total - cpu_own;

                std::cout << indent << "staked:" << std::setw(20) << cpu_own
                          << std::string(11, ' ') << "(total stake delegated from account to self)" << std::endl
                          << indent << "delegated:" << std::setw(17) << cpu_others
                          << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
            }
            else
            {
                auto cpu_others = cpu_total;
                std::cout << indent << "delegated:" << std::setw(17) << cpu_others
                          << std::string(11, ' ') << "(total staked delegated to account from others)" << std::endl;
            }
        }

        std::cout << std::fixed << setprecision(3);
        std::cout << indent << std::left << std::setw(11) << "used:" << std::right << std::setw(18) << to_pretty_time(res.cpu_limit.used) << "\n";
        std::cout << indent << std::left << std::setw(11) << "available:" << std::right << std::setw(18) << to_pretty_time(res.cpu_limit.available) << "\n";
        std::cout << indent << std::left << std::setw(11) << "limit:" << std::right << std::setw(18) << to_pretty_time(res.cpu_limit.max) << "\n";
        std::cout << std::endl;

        if (res.refund_request.is_object())
        {
            auto obj = res.refund_request.get_object();
            auto request_time = fc::time_point_sec::from_iso_string(obj["request_time"].as_string());
            fc::time_point refund_time = request_time + fc::days(3);
            auto now = res.head_block_time;
            asset net = asset::from_string(obj["net_amount"].as_string());
            asset cpu = asset::from_string(obj["cpu_amount"].as_string());
            unstaking = net + cpu;

            if (unstaking > asset(0, unstaking.get_symbol()))
            {
                std::cout << std::fixed << setprecision(3);
                std::cout << "unstaking tokens:" << std::endl;
                std::cout << indent << std::left << std::setw(25) << "time of unstake request:" << std::right << std::setw(20) << string(request_time);
                if (now >= refund_time)
                {
                    std::cout << " (available to claim now with 'eosio::refund' action)\n";
                }
                else
                {
                    std::cout << " (funds will be available in " << to_pretty_time((refund_time - now).count(), 0) << ")\n";
                }
                std::cout << indent << std::left << std::setw(25) << "from net bandwidth:" << std::right << std::setw(18) << net << std::endl;
                std::cout << indent << std::left << std::setw(25) << "from cpu bandwidth:" << std::right << std::setw(18) << cpu << std::endl;
                std::cout << indent << std::left << std::setw(25) << "total:" << std::right << std::setw(18) << unstaking << std::endl;
                std::cout << std::endl;
            }
        }

        if (res.core_liquid_balance.valid())
        {
////////////////////////////////////////////////////////////////////////////////
            std::cout << res.core_liquid_balance->get_symbol().name() << " balances: " << std::endl;
////////////////////////////////////////////////////////////////////////////////
            std::cout << indent << std::left << std::setw(11)
                      << "liquid:" << std::right << std::setw(18) << *res.core_liquid_balance << std::endl;
            std::cout << indent << std::left << std::setw(11)
                      << "staked:" << std::right << std::setw(18) << staked << std::endl;
            std::cout << indent << std::left << std::setw(11)
                      << "unstaking:" << std::right << std::setw(18) << unstaking << std::endl;
            std::cout << indent << std::left << std::setw(11) << "total:" << std::right << std::setw(18) << (*res.core_liquid_balance + staked + unstaking) << std::endl;
            std::cout << std::endl;
        }

        if (res.voter_info.is_object())
        {
            auto &obj = res.voter_info.get_object();
            string proxy = obj["proxy"].as_string();
            if (proxy.empty())
            {
                auto &prods = obj["producers"].get_array();
////////////////////////////////////////////////////////////////////////////////
                std::cout << "producers:";
////////////////////////////////////////////////////////////////////////////////

                if (!prods.empty())
                {
                    for (size_t i = 0; i < prods.size(); ++i)
                    {
                        if (i % 3 == 0)
                        {
                            std::cout << std::endl
                                      << indent;
                        }
                        std::cout << std::setw(16) << std::left << prods[i].as_string();
                    }
                    std::cout << std::endl;
                }
                else
                {
                    std::cout << indent << "<not voted>" << std::endl;
                }
            }
            else
            {
                std::cout << "proxy:" << indent << proxy << std::endl;
            }
        }
        std::cout << std::endl;
    }
    else
    {
        std::cout << fc::json::to_pretty_string(json) << std::endl;
    }
}
