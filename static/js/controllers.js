'use strict';

/* Controllers */

angular.module('tictactoe.controllers', []).
  controller('GameController', 
    ['$scope', '$routeParams', '$timeout', '$cookies', 'Game', 'Move', 
      function($scope, $routeParams, $timeout, $cookies, Game, Move) {
        

        if (!$cookies.cpu_wins) {
          $cookies.cpu_wins = 0;
        }

        if (!$cookies.player_wins) {
          $cookies.player_wins = 0;
        }

        if (!$cookies.draws) {
          $cookies.draws = 0;
        }

        $scope.wins = {
          'CPU': $cookies.cpu_wins,
          'Player': $cookies.player_wins,
          'Draw': $cookies.draws
        };

        $scope.syncGame = function(id) {
          return Game.get({gameId: id}, function(game) {
            var board = JSON.parse(game.board);
            var tiles = [];

            for (var i = 0; i < 9; i++ ) {
              var tile = {
                val: board[i],
                disabled: board[i] !== 0 || game.game_state !== 0
              };

              tiles.push(tile);
            }

            switch(game.game_state) {
              case 1:
                $scope.game_state = {
                  state: 1,
                  type: 'info',
                  message: 'The game has ended in a draw! There is no winner.'
                };

                $scope.wins.Draw++;
                break;
              case 2:
                $scope.game_state = {
                  state: 2,
                  type: 'success',
                  message: 'Congratulations, you have won!'
                };

                $scope.wins.Player++;
                break;
              case 3:
                $scope.game_state = {
                  state: 3,
                  type: 'danger',
                  message: 'Sorry, but you have lost the game. Please try again'
                };

                $scope.wins.CPU++;
                break;
              default:
                $scope.game_state = {
                  state: 0
                };
            }

            $scope.tiles = tiles;
            $scope.player_name = game.player_name;
            $scope.gameId = game.id;

            $scope.saveCookies();
          });
        };

        $scope.newGame = function() {
          var newGame = new Game({player_name: $scope.player_name}).$save(function(game) {
            $scope.syncGame(game.id);
          });
        };

        $scope.makeMove = function($event) {
          var position = parseInt($( $event.target ).attr('data-attr-index'), 10);
          var disabled = $($event.target).attr('disabled') == "disabled";

          if ($scope.game_state.state !== 0 || disabled) {
            return;
          }

          var newMove = new Move({game: $scope.gameId, position: position, player_type: 'p'}).$save(function(move) {
            $timeout(function() {
              $scope.syncGame($scope.gameId);
            }, 100, 5);
          });
        };

        $scope.saveCookies = function() {
          $cookies.cpu_wins = $scope.wins.CPU;
          $cookies.player_wins = $scope.wins.Player;
          $cookies.draws = $scope.wins.Draw;
        };
      }
    ]
  );
