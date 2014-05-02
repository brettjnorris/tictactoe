'use strict';

// Declare app level module which depends on filters, and services
angular.module('tictactoe', [
    'ngRoute',
    'tictactoe.services',
    'tictactoe.controllers',
    'tictactoe.filters']).
  config(['$routeProvider', function($routeProvider) {
    $routeProvider.when('/game/:id', {templateUrl: '/static/partials/game.html', controller: 'GameController'});
    $routeProvider.otherwise({redirectTo: '/'});
  }]);
