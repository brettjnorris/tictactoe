'use strict';

/* Services */


// Demonstrate how to register services
// In this case it is a simple value service.
angular.module('tictactoe.services', ['ngResource']).
  factory('Game', ['$resource', function($resource) {
    return $resource('/api/games/:gameId', {}, {});
  }]).
  factory('Move', ['$resource', function($resource) {
    return $resource('/api/moves', {}, {});
  }]);