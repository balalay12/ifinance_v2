var app = angular.module('app', ['ngRoute']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
}]);

app.config(function($routeProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/templates/main.html' ,
        controller: 'MainController'
    });
    $routeProvider.when('/reg/', {
        templateUrl: 'static/templates/reg.html',
        controller: 'RegFormController'
    });
    $routeProvider.otherwise({redirectTo: '/'});
});

app.controller('MainController', function($scope) {});

app.controller('RegFormController', ['$scope', '$http', function($scope, $http) {
	$scope.submit = function() {
		var in_data = {user: $scope.user};
		console.log(in_data);
		$http.post('/reg/', angular.toJson(in_data))
			.success(function(data, status) {
				console.log("OK " + data);
			})
			.error(function(data, status) {
				console.log("Not ok " + data);
			});
	};
}]);