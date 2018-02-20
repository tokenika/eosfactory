#pragma once
namespace eosio { namespace types {
    typedef name                             account_name;
    typedef name                             permission_name;
    typedef name                             func_name;
    typedef fixed_string32                   message_name;
    typedef fixed_string32                   type_name;
    struct account_permission { 
        account_permission() = default;
        account_permission(const account_name& account, const permission_name& permission)
           : account(account), permission(permission) {}

        account_name                     account;
        permission_name                  permission;
    };

    template<> struct get_struct<account_permission> { 
        static const struct_t& type() { 
           static struct_t result = { "account_permission", "", {
                {"account", "account_name"},
                {"permission", "permission_name"},
              }
           };
           return result;
         }
    };

    struct message { 
        message() = default;
        message(const account_name& code, const func_name& type, const vector<account_permission>& authorization, const bytes& data)
           : code(code), type(type), authorization(authorization), data(data) {}

        account_name                     code;
        func_name                        type;
        vector<account_permission>       authorization;
        bytes                            data;
    };

    template<> struct get_struct<message> { 
        static const struct_t& type() { 
           static struct_t result = { "message", "", {
                {"code", "account_name"},
                {"type", "func_name"},
                {"authorization", "account_permission[]"},
                {"data", "bytes"},
              }
           };
           return result;
         }
    };

    struct account_permission_weight { 
        account_permission_weight() = default;
        account_permission_weight(const account_permission& permission, const uint16& weight)
           : permission(permission), weight(weight) {}

        account_permission               permission;
        uint16                           weight;
    };

    template<> struct get_struct<account_permission_weight> { 
        static const struct_t& type() { 
           static struct_t result = { "account_permission_weight", "", {
                {"permission", "account_permission"},
                {"weight", "uint16"},
              }
           };
           return result;
         }
    };

    struct transaction { 
        transaction() = default;
        transaction(const uint16& ref_block_num, const uint32& ref_block_prefix, const time& expiration, const vector<account_name>& scope, const vector<account_name>& read_scope, const vector<message>& messages)
           : ref_block_num(ref_block_num), ref_block_prefix(ref_block_prefix), expiration(expiration), scope(scope), read_scope(read_scope), messages(messages) {}

        uint16                           ref_block_num;
        uint32                           ref_block_prefix;
        time                             expiration;
        vector<account_name>             scope;
        vector<account_name>             read_scope;
        vector<message>                  messages;
    };

    template<> struct get_struct<transaction> { 
        static const struct_t& type() { 
           static struct_t result = { "transaction", "", {
                {"ref_block_num", "uint16"},
                {"ref_block_prefix", "uint32"},
                {"expiration", "time"},
                {"scope", "account_name[]"},
                {"read_scope", "account_name[]"},
                {"messages", "message[]"},
              }
           };
           return result;
         }
    };

    struct signed_transaction : public transaction { 
        signed_transaction() = default;
        signed_transaction(const vector<signature>& signatures)
           : signatures(signatures) {}

        vector<signature>                signatures;
    };

    template<> struct get_struct<signed_transaction> { 
        static const struct_t& type() { 
           static struct_t result = { "signed_transaction", "transaction", {
                {"signatures", "signature[]"},
              }
           };
           return result;
         }
    };

    struct key_permission_weight { 
        key_permission_weight() = default;
        key_permission_weight(const public_key& key, const uint16& weight)
           : key(key), weight(weight) {}

        public_key                       key;
        uint16                           weight;
    };

    template<> struct get_struct<key_permission_weight> { 
        static const struct_t& type() { 
           static struct_t result = { "key_permission_weight", "", {
                {"key", "public_key"},
                {"weight", "uint16"},
              }
           };
           return result;
         }
    };

    struct authority { 
        authority() = default;
        authority(const uint32& threshold, const vector<key_permission_weight>& keys, const vector<account_permission_weight>& accounts)
           : threshold(threshold), keys(keys), accounts(accounts) {}

        uint32                           threshold;
        vector<key_permission_weight>    keys;
        vector<account_permission_weight> accounts;
    };

    template<> struct get_struct<authority> { 
        static const struct_t& type() { 
           static struct_t result = { "authority", "", {
                {"threshold", "uint32"},
                {"keys", "key_permission_weight[]"},
                {"accounts", "account_permission_weight[]"},
              }
           };
           return result;
         }
    };

    struct blockchain_configuration { 
        blockchain_configuration() = default;
        blockchain_configuration(const uint32& max_blk_size, const uint32& target_blk_size, const uint64& max_storage_size, const share_type& elected_pay, const share_type& runner_up_pay, const share_type& min_eos_balance, const uint32& max_trx_lifetime, const uint16& auth_depth_limit, const uint32& max_trx_runtime, const uint16& in_depth_limit, const uint32& max_in_msg_size, const uint32& max_gen_trx_size)
           : max_blk_size(max_blk_size), target_blk_size(target_blk_size), max_storage_size(max_storage_size), elected_pay(elected_pay), runner_up_pay(runner_up_pay), min_eos_balance(min_eos_balance), max_trx_lifetime(max_trx_lifetime), auth_depth_limit(auth_depth_limit), max_trx_runtime(max_trx_runtime), in_depth_limit(in_depth_limit), max_in_msg_size(max_in_msg_size), max_gen_trx_size(max_gen_trx_size) {}

        uint32                           max_blk_size;
        uint32                           target_blk_size;
        uint64                           max_storage_size;
        share_type                       elected_pay;
        share_type                       runner_up_pay;
        share_type                       min_eos_balance;
        uint32                           max_trx_lifetime;
        uint16                           auth_depth_limit;
        uint32                           max_trx_runtime;
        uint16                           in_depth_limit;
        uint32                           max_in_msg_size;
        uint32                           max_gen_trx_size;
    };

    template<> struct get_struct<blockchain_configuration> { 
        static const struct_t& type() { 
           static struct_t result = { "blockchain_configuration", "", {
                {"max_blk_size", "uint32"},
                {"target_blk_size", "uint32"},
                {"max_storage_size", "uint64"},
                {"elected_pay", "share_type"},
                {"runner_up_pay", "share_type"},
                {"min_eos_balance", "share_type"},
                {"max_trx_lifetime", "uint32"},
                {"auth_depth_limit", "uint16"},
                {"max_trx_runtime", "uint32"},
                {"in_depth_limit", "uint16"},
                {"max_in_msg_size", "uint32"},
                {"max_gen_trx_size", "uint32"},
              }
           };
           return result;
         }
    };

    struct type_def { 
        type_def() = default;
        type_def(const type_name& new_type_name, const type_name& type)
           : new_type_name(new_type_name), type(type) {}

        type_name                        new_type_name;
        type_name                        type;
    };

    template<> struct get_struct<type_def> { 
        static const struct_t& type() { 
           static struct_t result = { "type_def", "", {
                {"new_type_name", "type_name"},
                {"type", "type_name"},
              }
           };
           return result;
         }
    };

    struct action { 
        action() = default;
        action(const name& action_name, const type_name& type)
           : action_name(action_name), type(type) {}

        name                             action_name;
        type_name                        type;
    };

    template<> struct get_struct<action> { 
        static const struct_t& type() { 
           static struct_t result = { "action", "", {
                {"action_name", "name"},
                {"type", "type_name"},
              }
           };
           return result;
         }
    };

    struct table { 
        table() = default;
        table(const name& table_name, const type_name& index_type, const vector<field_name>& key_names, const vector<type_name>& key_types, const type_name& type)
           : table_name(table_name), index_type(index_type), key_names(key_names), key_types(key_types), type(type) {}

        name                             table_name;
        type_name                        index_type;
        vector<field_name>               key_names;
        vector<type_name>                key_types;
        type_name                        type;
    };

    template<> struct get_struct<table> { 
        static const struct_t& type() { 
           static struct_t result = { "table", "", {
                {"table_name", "name"},
                {"index_type", "type_name"},
                {"key_names", "field_name[]"},
                {"key_types", "type_name[]"},
                {"type", "type_name"},
              }
           };
           return result;
         }
    };

    struct abi { 
        abi() = default;
        abi(const vector<type_def>& types, const vector<struct_t>& structs, const vector<action>& actions, const vector<table>& tables)
           : types(types), structs(structs), actions(actions), tables(tables) {}

        vector<type_def>                 types;
        vector<struct_t>                 structs;
        vector<action>                   actions;
        vector<table>                    tables;
    };

    template<> struct get_struct<abi> { 
        static const struct_t& type() { 
           static struct_t result = { "abi", "", {
                {"types", "type_def[]"},
                {"structs", "struct_t[]"},
                {"actions", "action[]"},
                {"tables", "table[]"},
              }
           };
           return result;
         }
    };

    struct transfer { 
        transfer() = default;
        transfer(const account_name& from, const account_name& to, const uint64& amount, const string& memo)
           : from(from), to(to), amount(amount), memo(memo) {}

        account_name                     from;
        account_name                     to;
        uint64                           amount;
        string                           memo;
    };

    template<> struct get_struct<transfer> { 
        static const struct_t& type() { 
           static struct_t result = { "transfer", "", {
                {"from", "account_name"},
                {"to", "account_name"},
                {"amount", "uint64"},
                {"memo", "string"},
              }
           };
           return result;
         }
    };

    struct nonce { 
        nonce() = default;
        nonce(const string& value)
           : value(value) {}

        string                           value;
    };

    template<> struct get_struct<nonce> { 
        static const struct_t& type() { 
           static struct_t result = { "nonce", "", {
                {"value", "string"},
              }
           };
           return result;
         }
    };

    struct lock { 
        lock() = default;
        lock(const account_name& from, const account_name& to, const share_type& amount)
           : from(from), to(to), amount(amount) {}

        account_name                     from;
        account_name                     to;
        share_type                       amount;
    };

    template<> struct get_struct<lock> { 
        static const struct_t& type() { 
           static struct_t result = { "lock", "", {
                {"from", "account_name"},
                {"to", "account_name"},
                {"amount", "share_type"},
              }
           };
           return result;
         }
    };

    struct unlock { 
        unlock() = default;
        unlock(const account_name& account, const share_type& amount)
           : account(account), amount(amount) {}

        account_name                     account;
        share_type                       amount;
    };

    template<> struct get_struct<unlock> { 
        static const struct_t& type() { 
           static struct_t result = { "unlock", "", {
                {"account", "account_name"},
                {"amount", "share_type"},
              }
           };
           return result;
         }
    };

    struct claim { 
        claim() = default;
        claim(const account_name& account, const share_type& amount)
           : account(account), amount(amount) {}

        account_name                     account;
        share_type                       amount;
    };

    template<> struct get_struct<claim> { 
        static const struct_t& type() { 
           static struct_t result = { "claim", "", {
                {"account", "account_name"},
                {"amount", "share_type"},
              }
           };
           return result;
         }
    };

    struct newaccount { 
        newaccount() = default;
        newaccount(const account_name& creator, const account_name& name, const authority& owner, const authority& active, const authority& recovery, const asset& deposit)
           : creator(creator), name(name), owner(owner), active(active), recovery(recovery), deposit(deposit) {}

        account_name                     creator;
        account_name                     name;
        authority                        owner;
        authority                        active;
        authority                        recovery;
        asset                            deposit;
    };

    template<> struct get_struct<newaccount> { 
        static const struct_t& type() { 
           static struct_t result = { "newaccount", "", {
                {"creator", "account_name"},
                {"name", "account_name"},
                {"owner", "authority"},
                {"active", "authority"},
                {"recovery", "authority"},
                {"deposit", "asset"},
              }
           };
           return result;
         }
    };

    struct setcode { 
        setcode() = default;
        setcode(const account_name& account, const uint8& vm_type, const uint8& vm_version, const bytes& code, const abi& code_abi)
           : account(account), vm_type(vm_type), vm_version(vm_version), code(code), code_abi(code_abi) {}

        account_name                     account;
        uint8                            vm_type;
        uint8                            vm_version;
        bytes                            code;
        abi                              code_abi;
    };

    template<> struct get_struct<setcode> { 
        static const struct_t& type() { 
           static struct_t result = { "setcode", "", {
                {"account", "account_name"},
                {"vm_type", "uint8"},
                {"vm_version", "uint8"},
                {"code", "bytes"},
                {"code_abi", "abi"},
              }
           };
           return result;
         }
    };

    struct setproducer { 
        setproducer() = default;
        setproducer(const account_name& name, const public_key& key, const blockchain_configuration& configuration)
           : name(name), key(key), configuration(configuration) {}

        account_name                     name;
        public_key                       key;
        blockchain_configuration         configuration;
    };

    template<> struct get_struct<setproducer> { 
        static const struct_t& type() { 
           static struct_t result = { "setproducer", "", {
                {"name", "account_name"},
                {"key", "public_key"},
                {"configuration", "blockchain_configuration"},
              }
           };
           return result;
         }
    };

    struct okproducer { 
        okproducer() = default;
        okproducer(const account_name& voter, const account_name& producer, const int8& approve)
           : voter(voter), producer(producer), approve(approve) {}

        account_name                     voter;
        account_name                     producer;
        int8                             approve;
    };

    template<> struct get_struct<okproducer> { 
        static const struct_t& type() { 
           static struct_t result = { "okproducer", "", {
                {"voter", "account_name"},
                {"producer", "account_name"},
                {"approve", "int8"},
              }
           };
           return result;
         }
    };

    struct setproxy { 
        setproxy() = default;
        setproxy(const account_name& stakeholder, const account_name& proxy)
           : stakeholder(stakeholder), proxy(proxy) {}

        account_name                     stakeholder;
        account_name                     proxy;
    };

    template<> struct get_struct<setproxy> { 
        static const struct_t& type() { 
           static struct_t result = { "setproxy", "", {
                {"stakeholder", "account_name"},
                {"proxy", "account_name"},
              }
           };
           return result;
         }
    };

    struct updateauth { 
        updateauth() = default;
        updateauth(const account_name& account, const permission_name& permission, const permission_name& parent, const authority& new_authority)
           : account(account), permission(permission), parent(parent), new_authority(new_authority) {}

        account_name                     account;
        permission_name                  permission;
        permission_name                  parent;
        authority                        new_authority;
    };

    template<> struct get_struct<updateauth> { 
        static const struct_t& type() { 
           static struct_t result = { "updateauth", "", {
                {"account", "account_name"},
                {"permission", "permission_name"},
                {"parent", "permission_name"},
                {"new_authority", "authority"},
              }
           };
           return result;
         }
    };

    struct deleteauth { 
        deleteauth() = default;
        deleteauth(const account_name& account, const permission_name& permission)
           : account(account), permission(permission) {}

        account_name                     account;
        permission_name                  permission;
    };

    template<> struct get_struct<deleteauth> { 
        static const struct_t& type() { 
           static struct_t result = { "deleteauth", "", {
                {"account", "account_name"},
                {"permission", "permission_name"},
              }
           };
           return result;
         }
    };

    struct linkauth { 
        linkauth() = default;
        linkauth(const account_name& account, const account_name& code, const func_name& type, const permission_name& requirement)
           : account(account), code(code), type(type), requirement(requirement) {}

        account_name                     account;
        account_name                     code;
        func_name                        type;
        permission_name                  requirement;
    };

    template<> struct get_struct<linkauth> { 
        static const struct_t& type() { 
           static struct_t result = { "linkauth", "", {
                {"account", "account_name"},
                {"code", "account_name"},
                {"type", "func_name"},
                {"requirement", "permission_name"},
              }
           };
           return result;
         }
    };

    struct unlinkauth { 
        unlinkauth() = default;
        unlinkauth(const account_name& account, const account_name& code, const func_name& type)
           : account(account), code(code), type(type) {}

        account_name                     account;
        account_name                     code;
        func_name                        type;
    };

    template<> struct get_struct<unlinkauth> { 
        static const struct_t& type() { 
           static struct_t result = { "unlinkauth", "", {
                {"account", "account_name"},
                {"code", "account_name"},
                {"type", "func_name"},
              }
           };
           return result;
         }
    };

}} // namespace eosio::types
FC_REFLECT( eosio::types::account_permission               , (account)(permission) )
FC_REFLECT( eosio::types::message                          , (code)(type)(authorization)(data) )
FC_REFLECT( eosio::types::account_permission_weight        , (permission)(weight) )
FC_REFLECT( eosio::types::transaction                      , (ref_block_num)(ref_block_prefix)(expiration)(scope)(read_scope)(messages) )
FC_REFLECT_DERIVED( eosio::types::signed_transaction, (eosio::types::transaction), (signatures) )
FC_REFLECT( eosio::types::key_permission_weight            , (key)(weight) )
FC_REFLECT( eosio::types::authority                        , (threshold)(keys)(accounts) )
FC_REFLECT( eosio::types::blockchain_configuration         , (max_blk_size)(target_blk_size)(max_storage_size)(elected_pay)(runner_up_pay)(min_eos_balance)(max_trx_lifetime)(auth_depth_limit)(max_trx_runtime)(in_depth_limit)(max_in_msg_size)(max_gen_trx_size) )
FC_REFLECT( eosio::types::type_def                         , (new_type_name)(type) )
FC_REFLECT( eosio::types::action                           , (action_name)(type) )
FC_REFLECT( eosio::types::table                            , (table_name)(index_type)(key_names)(key_types)(type) )
FC_REFLECT( eosio::types::abi                              , (types)(structs)(actions)(tables) )
FC_REFLECT( eosio::types::transfer                         , (from)(to)(amount)(memo) )
FC_REFLECT( eosio::types::nonce                            , (value) )
FC_REFLECT( eosio::types::lock                             , (from)(to)(amount) )
FC_REFLECT( eosio::types::unlock                           , (account)(amount) )
FC_REFLECT( eosio::types::claim                            , (account)(amount) )
FC_REFLECT( eosio::types::newaccount                       , (creator)(name)(owner)(active)(recovery)(deposit) )
FC_REFLECT( eosio::types::setcode                          , (account)(vm_type)(vm_version)(code)(code_abi) )
FC_REFLECT( eosio::types::setproducer                      , (name)(key)(configuration) )
FC_REFLECT( eosio::types::okproducer                       , (voter)(producer)(approve) )
FC_REFLECT( eosio::types::setproxy                         , (stakeholder)(proxy) )
FC_REFLECT( eosio::types::updateauth                       , (account)(permission)(parent)(new_authority) )
FC_REFLECT( eosio::types::deleteauth                       , (account)(permission) )
FC_REFLECT( eosio::types::linkauth                         , (account)(code)(type)(requirement) )
FC_REFLECT( eosio::types::unlinkauth                       , (account)(code)(type) )
