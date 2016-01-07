'use strict';


angular.module('shopstatsApp.productListView',['ngRoute','ngCookies'])

.config(['$routeProvider',function($routeProvider){
	$routeProvider.when('/mobiles',{
		templateUrl:'productlist_view/product_list.html',
		controller:'productListViewCtrl'
	});
}])

.service('ServerDataService',['$http','$cookies',function($http,$cookies){
	var getData=function(){
		return $http({method:'GET',url:'http://localhost:8090/api/products/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
			return result;
		});
	};
	return {getData:getData};
}])



.controller('productListViewCtrl',['$scope','$http','$cookies','ServerDataService',
	function($scope,$http,$cookies,ServerDataService){
	//write controller code here
	$scope.currentPage=1;
	$scope.numPerPage=100;
	$scope.maxSize=5;
	$scope.filteredProducts=[]

	$scope.products=[]
	
	var myDataPromise=ServerDataService.getData();
	myDataPromise.then(function(result){
		$scope.mobiles=result.data;
		console.log(result.data);
	});

	angular.forEach($scope.mobiles,function(mobile){
    		console .log(mobile.fields);
    		$scope.products.push(mobile.fields);
    });

    $scope.numPages = function () {
    	return Math.ceil($scope.products.length / $scope.numPerPage);
  	};

  	$scope.$watch("currentPage + numPerPage", function() {
    	var begin = (($scope.currentPage - 1) * $scope.numPerPage)
    	, end = begin + $scope.numPerPage;
    	$scope.filteredProducts = $scope.products.slice(begin, end);
  	});

}]);