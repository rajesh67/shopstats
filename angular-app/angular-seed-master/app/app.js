'use strict';

// Declare app level module which depends on views, and components
var app=angular.module('shopstatsApp', [
  'ngRoute',
  'ngCookies',
  'shopstatsApp.productListView',
  'shopstatsApp.productView',
  'shopstatsApp.version'
])

.config(['$routeProvider','$httpProvider' ,function($routeProvider,$httpProvider) {

    $httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;

  	$routeProvider.otherwise({redirectTo: '/'});
}]);

