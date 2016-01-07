'use strict';

/* Controllers*/
var shopstatsControllers=angular.module('shopstatsControllers',[]);


shopstatsControllers.controller('HomeCtrl',['$rootScope', '$scope', '$location', '$routeParams',
	function($scope,$routeParams,$rootScope,$location){
		$rootScope.categoryId="";
		$scope.categoryId=$rootScope.categoryId;
	}]);


shopstatsControllers.controller('ProductListCtrl',['$scope','$routeParams','CategoryListingService',
	function($scope,$routeParams,CategoryListingService){
		$scope.products=[];
		$scope.currPage=1;
		$scope.categoryId=$routeParams.categoryId;

		console.log('scope categoryId='+$routeParams.categoryId);

		var promisedData=CategoryListingService.getData(1);
		promisedData.then(function(result){
			//console.log(result.data);
			angular.forEach(result.data,function(product){
				$scope.products.push(product.fields);
				//console.log(product.fields);
			});
		});
		
		$scope.loadPage=function(){
			var dataPromise=CategoryListingService.getData($scope.currPage);
			dataPromise.then(function(result){
				$scope.products=[];
				angular.forEach(result.data,function(product){
					$scope.products.push(product.fields);
					//console.log(product.fields);
				});
			});
		};

		$scope.previousPage=function(){
			$scope.currPage--;
			$scope.loadPage();
		};

		$scope.nextPage=function(){
			$scope.currPage++;
			$scope.loadPage();
		};

	}]);




shopstatsControllers.controller('ProductDetailCtrl',['$scope','$routeParams','Product','ProductReviewsJSONService','ProductDetailsJSONService','ProductAnalyzedReviewsService',
	function($scope,$routeParams,Product,ProductReviewsJSONService,ProductDetailsJSONService,ProductAnalyzedReviewsService){
		$scope.product={};
		$scope.reviews=[]
		$scope.currPage=1;
		$scope.reviews_list=[]
		
		$scope.start=0;
		$scope.end=10;

		$scope.categoryId=$routeParams.categoryId;
		console.log("in details controller categoryId="+$routeParams.categoryId);

		var id=$routeParams.productId;
		
		var promisedData=Product.getData(id);
		promisedData.then(function(result){
			$scope.product_detail=result.data.fields;
			var data=result.data[0];
			$scope.product=data.fields;
			//console.log(data.fields);
		});
		
		//$('.danger').popover({ html : true});

		//get product json file
		var jsonPromisedData=ProductDetailsJSONService.getData();
		jsonPromisedData.then(function(result){
			angular.forEach(result.data,function(data){
				//console.log(data);
				$scope.json=data;
				$scope.details=data;
			});
		});

		//get product reviews
		var reviewsPromise=ProductReviewsJSONService.getData();
		reviewsPromise.then(function(result){
			angular.forEach(result.data,function(review){
				$scope.reviews_list.push(review);
			});
			var reviews=$scope.reviews_list.slice(0,10);
				angular.forEach(reviews,function(review){
				$scope.reviews.push(review);
			});
		});

		$scope.analyzed_reviews=[]
		$scope.analyzed_reviews_list=[];
		//get product nlp processed reviews
		var parsedReviewsPromise=ProductAnalyzedReviewsService.getData()
		parsedReviewsPromise.then(function(result){
			angular.forEach(result.data,function(review){
				$scope.analyzed_reviews_list.push(review);
			});
			var reviews=$scope.analyzed_reviews_list.slice(0,10);
			angular.forEach(reviews,function(review){
				$scope.analyzed_reviews.push(review);
			});
		});

		$scope.pos='pos';
		$scope.neg='neg';
		$scope.neutral='neutral';

		$scope.previousPage=function(){
			$scope.reviews=[];
			$scope.currPage--;			
			
			var start=$scope.currPage-1;
			$scope.start=start*10;
			$scope.end=$scope.currPage*10;

			var reviews=$scope.reviews_list.slice($scope.start,$scope.end);
			
			
			$scope.reviews=[];
			angular.forEach(reviews,function(review){
				$scope.reviews.push(review);
			});

			//nlp processed reviews
			var analyzed_reviews=$scope.analyzed_reviews_list.slice($scope.start,$scope.end);
			$scope.analyzed_reviews=[];
			angular.forEach(analyzed_reviews,function(review){
				$scope.analyzed_reviews.push(review);
			});

		};

		$scope.nextPage=function(){
			$scope.reviews=[];
			$scope.currPage++;

			var start=$scope.currPage-1;
			$scope.start=start*10;
			$scope.end=$scope.currPage*10;

			var reviews=$scope.reviews_list.slice($scope.start,$scope.end);
			angular.forEach(reviews,function(review){
				$scope.reviews.push(review);
			});


			var analyzed_reviews=$scope.analyzed_reviews_list.slice($scope.start,$scope.end);
			$scope.analyzed_reviews=[];
			angular.forEach(analyzed_reviews,function(review){
				$scope.analyzed_reviews.push(review);
			});
			
		};

		//function to get varients by id
		$scope.loadProduct=function(){
			var productId=$routeParams.productId.replace(/^\s+|\s+$/g, '');				
			var promisedData=Product.getData(productId.replace(/ /g,''));
			promisedData.then(function(result){
				var data=result.data[0];
				$scope.product=data.fields;
				console.log(data.fields);
			});
		};

		//popups 
		/* JavaScript for popover image*/
		$scope.popup = {
		  content: 'Popup content here',
		  options: {
		    title: null,
		    placement: 'right', 
		    delay: { show: 800, hide: 100 }
		  }
		}; 

}]);




