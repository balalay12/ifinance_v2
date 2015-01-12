var app = angular.module('reg_app', ['ngRoute']);

app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.config(['$routeProvider', function($routeProvider) {
	$routeProvider
		.when('', {
			templateUtl: '../templates/base.html'
		});
}]);

app.controller('RegFormController', ['$scope', '$http', function($scope, $http) {
	$scope.submit = function() {
		var in_data = {user: $scope.user};
		console.log(in_data);
		$http.post('', angular.toJson(in_data))
			.success(function(data, status) {
				console.log("OK " + data);
			})
			.error(function(data, status) {
				console.log("Not ok " + data);
			});
	};
}]);