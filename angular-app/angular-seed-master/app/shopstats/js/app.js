'use strict';

/* App module */

var shopstatsApp=angular.module('shopstatsApp',[
	'ngRoute',
	'ngCookies',
	'ngResource',

	'shopstatsControllers',
	//'shopstatsFilters',
	'shopstatsServices',
]);


shopstatsApp.config(['$routeProvider','$httpProvider',function($routeProvider,$httpProvider){
	
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.withCredentials = true;

	$routeProvider.
		when('/home',{
			templateUrl:'shopstats/html/home.html',
			controller:'HomeCtrl',
		}).
		when('/products/:categoryId',{
			templateUrl:'shopstats/html/productlist.html',
			controller:'ProductListCtrl',
		}).
		when('/products/:categoryId/:productId',{
			templateUrl:'shopstats/html/product.html',
			controller:'ProductDetailCtrl',
		}).
		otherwise({
			redirectTo:'/home'
		});
}]);