'use strict';

/* Module Services*/

var shopstatsServices=angular.module('shopstatsServices',['ngResource','ngCookies']);


shopstatsServices.service('ProductReviewsJSON',['$http','$cookies',
	function($http,$cookies){
		var getData=function(file,productId){
			return $http({method:'GET',url:'http://localhost:8080/api/json/files/',params:{"file":"cameras_reviews.json","productId":productId},headers:{'x-csrftoken':$cookies.csrftoken},accept:'application/json'}).then(function(result){
				return result
			});
		};
		return {getData:getData};
	}]);


shopstatsServices.service('Product',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(id){
			return $http({method:'GET',url:'http://localhost:8080/api/product/',params:{"productId":id},headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
				return result;
			});
		};
		return {getData:getData};
}]);

shopstatsServices.service('ProductList',['$http','$cookies',
	function($http,$cookies){
		var getData=function(){
			return $http({method:'GET',url:'http://localhost:8080/api/products/',params:{"page":1},headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
				return result;
			});
		};
		return {getData:getData};
	}]);






//new services according to new apis
shopstatsServices.service('ProductDetailsDBService',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(id){
			return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/'+$routeParams.productId+'/db/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
				return result;
			});
		};
		return {getData:getData};
}]);



shopstatsServices.service('ProductDetailsJSONService',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(){
			return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/product/'+$routeParams.productId+'/json/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
				return result;
			});
		};
		return {getData:getData};
}]);


shopstatsServices.service('ProductReviewsJSONService',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(page){
				return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/product/'+$routeParams.productId+'/reviews/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
					return result;
				});
		};
		return {getData:getData};
}]);

shopstatsServices.service('ProductAnalyzedReviewsService',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(page){
				return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/product/'+$routeParams.productId+'/reviews/analyzed/',headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
					return result;
				});
		};
		return {getData:getData};
}]);


shopstatsServices.service('CategoryListingService',['$http','$routeParams','$cookies',
	function($http,$routeParams,$cookies){
		var getData=function(page){
			if(page){
				return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/products/',params:{"page":page},headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
					return result;
				});
			}else{
				return $http({method:'GET',url:'http://localhost:8080/api/'+$routeParams.categoryId+'/products/',params:{"page":1},headers:{"x-csrftoken" : $cookies.csrftoken},accept:'application/json'}).then(function(result){
					return result;
				});
			}
		};
		return {getData:getData};
}]);