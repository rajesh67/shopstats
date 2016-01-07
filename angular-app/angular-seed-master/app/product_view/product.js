'use strict';

angular.module('shopstatsApp.productView', ['ngRoute'])

.config(['$routeProvider', function($routeProvider) {
  $routeProvider.when('/product/:productId', {
    templateUrl: 'product_view/product.html',
    controller: 'productViewCtrl'
  });
}])

.service('ProductDataService',['$http','$cookies',function($http,$cookies){
	var getData=function(){
		return $http({method:'GET',url:'http://localhost:8090/api/products/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
			return result;
		});
	};
	return {getData:getData};
}])

.controller('productViewCtrl', ['$scope','$routeParams','ProductDataService',
	function($scope,$routeParams,ProductDataService) {
		$scope.productId=$routeParams.productId;
		
}]);