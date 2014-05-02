'use strict';

/* Controllers */


angular.module('tictactoe.controllers', []).
  controller('GameController', ['$scope', 'Game', function($scope, Game) {
    $scope.game = Game.get({ gameId: 1 }, function(game) {
      var board = JSON.parse(game.board);

      var tiles = [];
      for ( var i = 0; i < 9; i++ ) {
        var tile = {
          val: board[i],
          disabled: board[i] != 0,
        };

        tiles.push(tile);
      }

      $scope.tiles = tiles;
    });
  }]);
