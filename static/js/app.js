'use strict';

// Declare app level module which depends on filters, and services
angular.module('tictactoe', [
    'ngRoute',
    'ngCookies',
    'tictactoe.services',
    'tictactoe.controllers',
    'tictactoe.filters']).
  config(['$routeProvider', '$httpProvider', function($routeProvider, $httpProvider) {
    $routeProvider.when('/', {templateUrl: '/static/partials/game.html', controller: 'GameController'});
    $routeProvider.otherwise({redirectTo: '/'});

    // Add csrf support for POST requests
    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken'; 
  }]);
