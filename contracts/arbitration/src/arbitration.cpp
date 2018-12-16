#include <eosiolib/eosio.hpp>
#include <eosiolib/asset.hpp>
#include <eosiolib/print.hpp>
#include <eosiolib/time.hpp>

#define DEBUG
#include <eoside/logger.hpp>

using namespace eosio;
using namespace std;

time_point current_time_point();

class [[eosio::contract("arbitration")]] dep : public contract {
  public:
      using contract::contract;
    
      static constexpr uint32_t refund_delay_sec = 3;
      const asset zero = asset(0, symbol("SYS", 4));


      // listens for transfer to smartcontract's EOS account
      // and populates deposits with sent money;
      // memo should be seller account name.
      [[eosio::action]]
      void transfer(name from, name to, asset quantity, string memo);

      // opens deposit to hold tokens from buyer to seller;
      // balance is set to zero; right know deposit is identified by
      // (buyer, seller) pair which means only one deal beatween the two
      // can be in progress. We should add deposit names in the future.
      [[eosio::action]]
      void opendeposit(name buyer, name seller);


      // buyer can request his money back (in case the seller faild 
      // to fullfill contract); withdraw money are not transfered imedetely
      // (buyer should call "refund" acction)
      [[eosio::action]]
      void withdraw(name buyer, name seller);

      // seller can claim money hild in ascrow; money are not transfered
      // immediately to seller account (he should use "refund" method 
      // to initiate transfer)
      [[eosio::action]]
      void claim(name buyer, name seller);

      // once money are claimed (or withdrawn) seller (or buyer) can
      // request refund and initate transfer to his account; 
      // transfer can not be initiated before "refund_delay_sec" second after
      // calime (witdraw)
      [[eosio::action]]
      void refund(name buyer, name seller);

      // seller or buyer can hold transfers from escrow;
      [[eosio::action]]
      void hold(name buyer, name seller);

      // hold transfers are conflicts that should be resolved by 
      // arbitrator with "resolve" action; user is the account name
      // to which money should be transfered
      [[eosio::action]]
      void resolve(name buyer, name seller, name user);

  private:
      struct [[eosio::table]] dep_rec {
          asset    amount;
          name     seller;
          uint64_t primary_key() const { return seller.value; }
      };

      struct [[eosio::table]] claim_rec {
          name            buyer;
          name            seller;
          asset           amount; 
          time_point_sec  request_time;
          bool            is_withdrawal;
          bool            on_hold;
          uint64_t        primary_key() const {return seller.value;}
      };

      typedef eosio::multi_index< "claims"_n, claim_rec > claims;
      typedef eosio::multi_index< "deposits"_n, dep_rec > deposits;
      void sub_balance(name buyer, name seller, asset value);
      void add_balance(name buyer, name seller, asset value);
      void create_claim(name buyer, name seller, bool is_withdrawal);
};

void dep::transfer(name from, name to, asset quantity, string memo) {
    logger_info();    
    if (from == _self || to != _self) {
        return;
    }
    eosio_assert(quantity.symbol == symbol("SYS", 4), 
                                "I think you're looking for another contract");
    eosio_assert(quantity.is_valid(), "Are you trying to corrupt me?");
    eosio_assert(quantity.amount > 0, "When pigs fly");
    deposits db(_self, from.value);
    auto to_acnt = db.find(name(memo).value);
    logger_info("name(memo) ", name(memo));
    logger_info("name(memo).value ", name(memo).value);
    eosio_assert(to_acnt != db.end(), 
                        "Don't send us your money before opening account" );
    add_balance(from, name(memo), quantity);
}

void dep::opendeposit(name buyer, name seller) {
    require_auth(buyer);
    deposits db(_self, buyer.value );
    auto it = db.find(seller.value);
    eosio_assert(it == db.end(), "Deposit already exists");
    add_balance(buyer, seller, zero);
}

void dep::withdraw(name buyer, name seller) {
    require_auth(buyer);
    create_claim(buyer, seller, true);
}

void dep::claim(name buyer, name seller) {
    require_auth(seller);
    create_claim(buyer, seller, false);
}

void dep::create_claim(name buyer, name seller, bool is_withdrawal) {
    deposits dep_db(_self, buyer.value);
    auto deposit = dep_db.find(seller.value);
    eosio_assert(deposit != dep_db.end(), "Deposit not found");
    eosio_assert(seller == deposit->seller, "seller missmatch");
    asset amount = deposit->amount;
    dep_db.erase(deposit);

    claims claims_db(_self, buyer.value);
    auto request = claims_db.find(seller.value);
    if (request == claims_db.end()) {
        claims_db.emplace(is_withdrawal?buyer:seller, [&](auto &claim) {
            claim.buyer = buyer;
            claim.seller = seller;
            claim.request_time = current_time_point();
            claim.amount = amount;
            claim.is_withdrawal = is_withdrawal;
            claim.on_hold = false;
        });
    } else {
        claims_db.modify(request, same_payer, [&](auto &req) {
            req.amount += amount;
            req.request_time = current_time_point();
        });
    }
}
void dep::hold(name buyer, name seller) {
    claims db(_self, buyer.value);
    auto request = db.find(seller.value);
    eosio_assert(request != db.end(), "No such claim");
    eosio_assert(buyer == request->buyer && seller == request->seller, "seller/buyer missmatch");
    name user = request->is_withdrawal?request->seller:request->buyer;
    require_auth(user);
    if (request->on_hold) return;
    db.modify(request, user, [&](auto &req) {
        req.on_hold = true;
    });
}

void dep::refund(name buyer, name seller) {
    claims db(_self, buyer.value);
    auto request = db.find(seller.value);
    eosio_assert(request != db.end(), "No claim request found");
    name account = request->is_withdrawal?buyer:seller;
    require_auth(account);
    eosio_assert(buyer == request->buyer && seller == request->seller, "seller/buyer missmatch");
    eosio_assert(!request->on_hold, "Request is hold");
    eosio_assert(request->request_time + seconds(refund_delay_sec) <= current_time_point(),
            "Refund is not available yet" );
    action transfer = action(
        permission_level{get_self() ,"active"_n},
        "eosio.token"_n,
        "transfer"_n,
        std::make_tuple(get_self(), account, request->amount, std::string("Here are your tokens"))
    );
    transfer.send();
    db.erase(request);
}

void dep::resolve(name buyer, name seller, name user) {
    require_auth(_self);
    claims db(_self, buyer.value);
    auto request = db.find(seller.value);
    eosio_assert(request != db.end(), "No claim request found");
    eosio_assert(buyer == request->buyer && seller == request->seller, "seller/buyer missmatch");
    eosio_assert(request->request_time + seconds(refund_delay_sec) <= current_time_point(),
            "Refund is not available yet" );
    eosio_assert(request->on_hold, "Request is not hold");
    action transfer = action(
        permission_level{get_self() ,"active"_n},
        "eosio.token"_n,
        "transfer"_n,
        std::make_tuple(get_self(), user, request->amount, std::string(
                                                    "Here are your tokens"))
    );
    transfer.send();
    db.erase(request);
}

void dep::add_balance(name buyer, name seller, asset value) {
    deposits db(_self, buyer.value);
    auto dep = db.find(seller.value);
    if(dep == db.end()) {
        db.emplace(buyer, [&]( auto& a ){
            a.seller = seller;
            a.amount = value;
        });
    } else {
        db.modify(dep, same_payer, [&]( auto& a ) {
            a.amount += value;
        });
    }
}

extern "C" {
    void apply(uint64_t receiver, uint64_t code, uint64_t action) {
        auto self = receiver;
        if(code == self && action == name("opendeposit").value) {
              execute_action(name(receiver), name(code), &dep::opendeposit); 
        } else if(code == self && action == name("withdraw").value) {
              execute_action(name(receiver), name(code), &dep::withdraw); 
        } else if(code == self && action == name("claim").value) {
              execute_action(name(receiver), name(code), &dep::claim); 
        } else if(code == self && action == name("hold").value) {
              execute_action(name(receiver), name(code), &dep::hold); 
        } else if(code == self && action == name("refund").value) {
              execute_action(name(receiver), name(code), &dep::refund); 
        } else if(code == self && action == name("hold").value) {
              execute_action(name(receiver), name(code), &dep::hold); 
        } else if(code == self && action == name("resolve").value) {
              execute_action(name(receiver), name(code), &dep::resolve); 
        } else if(code == name("eosio.token").value 
                                    && action == name("transfer").value) {
              execute_action(name(receiver), name(code), &dep::transfer); 
        } else{
            eosio_assert(false, (string("Ooops - action not configured: ")
                + name(action).to_string()).c_str());
        }
    }
}

time_point current_time_point() {
   const static time_point ct{ 
       microseconds{ static_cast<int64_t>( current_time() ) } };
   return ct;
}