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
    $routeProvider.when('/login/', {
        templateUrl: 'static/templates/login.html',
        controller: 'LoginFormController'
    });
    $routeProvider.when('/add/', {
        templateUrl: 'static/templates/add.html',
        controller: 'CreateFormController'
    });
    $routeProvider.otherwise({redirectTo: '/'});
});

app.controller('MainController', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $http.post('/')
        .success(function(data, status) {
            console.log('status -> OK -> ' + status);
            console.log('DATA -> ' + data);
            $scope.data = data;
        })
        .error(function(data, status) {
            console.log('status -> NOT_OK -> ' + status);
            $location.path("/login");
        });
}]);

app.controller('RegFormController', ['$scope', '$http', '$location', function($scope, $http, $location) {
	$scope.submit = function() {
		var in_data = {reg: $scope.reg};
		console.log(in_data);
		$http.post('/reg/', angular.toJson(in_data))
			.success(function(data, status) {
				console.log("OK " + data);
				$location.path("/login")
			})
			.error(function(data, status) {
				console.log("Not ok " + data);
			});
	};
}]);

app.controller('LoginFormController', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $scope.submit = function() {
        var in_data = {login: $scope.login};
        $http.post('/login/', angular.toJson(in_data))
            .success(function(data, status) {
                console.log(data + status);
                $location.path("/main");
            })
            .error(function(data, status) {
                console.log(data + status);
            });
    };
}]);

app.controller('CreateFormController', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $http.post('/add/')
        .success(function(data, status) {
//            console.log('status -> OK -> ' + status);
//            console.log('DATA -> ' + data);
            $scope.data = data;
        })
        .error(function(data, status) {
            console.log('status -> NOT_OK -> ' + status);
            //$location.path("/login");
        });

    $scope.submit = function() {
        var in_data = {add: $scope.add};
        console.log(in_data)
        $http.post('/add/', angular.toJson(in_data))
            .success(function(data, status) {
                console.log(data + status);
                //$location.path("/main");
            })
            .error(function(data, status) {
                console.log(data + status);
            });
    };
}]);