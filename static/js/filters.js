'use strict';


angular.module('tictactoe.filters', [])
  .filter('gamemove', function() {
    return function(input) {
      if ( input === 0 ) {
        return '';
      } else if ( input == 'p' ) {
        return 'X';
      } else if ( input == 'c' ) {
        return 'O';
      }
    };
  });