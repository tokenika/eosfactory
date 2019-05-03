/**
 *  @file
 *  @copyright defined in eos/LICENSE.txt
 */

#include "include/tic_tac_toe.hpp"

namespace eosio {

   /**
    * @brief Check if cell is empty
    * @param cell - value of the cell (should be either 0, 1, or 2)
    * @return true if cell is empty
    */
   bool is_empty_cell(const uint8_t& cell) {
      return cell == 0;
   }

   /**
    * @brief Check for valid movement
    * @detail Movement is considered valid if it is inside the board and done 
    * on empty cell
    * @param row - the row of movement made by the player
    * @param column - the column of movement made by the player
    * @param board - the board on which the movement is being made
    * @return true if movement is valid
    */
   bool is_valid_movement(const uint16_t& row, const uint16_t& column, const std::vector<uint8_t>& board) {
      uint32_t movement_location = row * tic_tac_toe::game::board_width 
               + column;
      bool is_valid = movement_location < board.size() && is_empty_cell(board[movement_location]);
      return is_valid;
   }

   /**
    * @brief Get winner of the game
    * @detail Winner of the game is the first player who made three consecutive 
    * aligned movement
    * @param current_game - the game which we want to determine the winner of
    * @return winner of the game (can be either none/ draw/ account name of 
    * host/ account name of challenger)
    */
   name get_winner(const tic_tac_toe::game& current_game) {
      auto& board = current_game.board;

      bool is_board_full = true;
      
      // Use bitwise AND operator to determine the consecutive values of each 
      // column, row and diagonal
      // Since 3 == 0b11, 2 == 0b10, 1 = 0b01, 0 = 0b00
      std::vector<uint32_t> consecutive_column(
                                          tic_tac_toe::game::board_width, 3 );
      std::vector<uint32_t> consecutive_row(
                                          tic_tac_toe::game::board_height, 3 );
      uint32_t consecutive_diagonal_backslash = 3;
      uint32_t consecutive_diagonal_slash = 3;
      for (uint32_t i = 0; i < board.size(); i++) {
         is_board_full &= is_empty_cell(board[i]);
         uint16_t row = uint16_t(i / tic_tac_toe::game::board_width);
         uint16_t column = uint16_t(i % tic_tac_toe::game::board_width);

         // Calculate consecutive row and column value
         consecutive_row[column] = consecutive_row[column] & board[i]; 
         consecutive_column[row] = consecutive_column[row] & board[i];
         // Calculate consecutive diagonal \ value
         if (row == column) {
            consecutive_diagonal_backslash 
                                 = consecutive_diagonal_backslash & board[i];
         }
         // Calculate consecutive diagonal / value
         if ( row + column == tic_tac_toe::game::board_width - 1) {
            consecutive_diagonal_slash = consecutive_diagonal_slash & board[i]; 
         }
      }

      // Inspect the value of all consecutive row, column, and diagonal and 
      // determine winner
      std::vector<uint32_t> aggregate = { consecutive_diagonal_backslash, consecutive_diagonal_slash };
      aggregate.insert(
                              aggregate.end(), consecutive_column.begin(), 
                              consecutive_column.end());
      aggregate.insert(
            aggregate.end(), consecutive_row.begin(), consecutive_row.end());
            
      for (auto value: aggregate) {
         if (value == 1) {
            return current_game.host;
         } else if (value == 2) {
            return current_game.challenger;
         }
      }
      // Draw if the board is full, otherwise the winner is not determined yet
      return is_board_full ? name("draw") : name("none");
   }

   /**
    * @brief Apply create action
    */
   void tic_tac_toe::create(const name& challenger, const name& host) {
      require_auth(host);
      check(
         challenger != host, "challenger shouldn't be the same as host");

      // Check if game already exists
      games existing_host_games(_self, host.value);
      auto itr = existing_host_games.find( challenger.value);
      check(itr == existing_host_games.end(), "game already exists");

      existing_host_games.emplace(host, [&]( auto& g ) {
         g.challenger = challenger;
         g.host = host;
         g.turn = host;
      });
   }

   /**
    * @brief Apply restart action
    */
   void tic_tac_toe::restart(
               const name& challenger, const name& host, const name& by) {
      require_auth(by);

      // Check if game exists
      games existing_host_games(_self, host.value);
      auto itr = existing_host_games.find( challenger.value );
      check(itr != existing_host_games.end(), "game doesn't exists");

      // Check if this game belongs to the action sender
      check(
         by == itr->host || by == itr->challenger, "this is not your game!");

      // Reset game
      existing_host_games.modify(itr, itr->host, []( auto& g ) {
         g.reset_game();
      });
   }

   /**
    * @brief Apply close action
    */
   void tic_tac_toe::close(const name& challenger, const name& host) {
      require_auth(host);

      // Check if game exists
      games existing_host_games(_self, host.value);
      auto itr = existing_host_games.find( challenger.value );
      check(itr != existing_host_games.end(), "game doesn't exists");

      // Remove game
      existing_host_games.erase(itr);
   }

   /**
    * @brief Apply move action
    */
   void tic_tac_toe::move(
         const name& challenger, const name& host, const name& by, 
         const uint16_t& row, const uint16_t& column ) {
      require_auth(by);

      // Check if game exists
      games existing_host_games(_self, host.value);
      auto itr = existing_host_games.find( challenger.value );
      check(itr != existing_host_games.end(), "game doesn't exists");

      // Check if this game hasn't ended yet
      check(itr->winner == name("none"), "the game has ended!");
      // Check if this game belongs to the action sender
      check(
         by == itr->host || by == itr->challenger, "this is not your game!");
      // Check if this is the  action sender's turn
      check(by == itr->turn, "it's not your turn yet!");


      // Check if user makes a valid movement
      check(
         is_valid_movement(row, column, itr->board), "not a valid movement!");

      // Fill the cell, 1 for host, 2 for challenger
      const uint8_t cell_value = itr->turn == itr->host ? 1 : 2;
      const auto turn = itr->turn == itr->host ? itr->challenger : itr->host;
      existing_host_games.modify(itr, itr->host, [&]( auto& g ) {
         g.board[row * tic_tac_toe::game::board_width + column] = cell_value;
         g.turn = turn;
         g.winner = get_winner(g);
      });
   }

}