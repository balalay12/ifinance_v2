var app = angular.module('app', ['ngRoute']);

app.config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

app.config(['$httpProvider', function($httpProvider) {
	$httpProvider.defaults.xsrfCookieName = 'csrftoken';
    $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
    $httpProvider.defaults.headers.post['Content-Type'] = 'application/x-www-form-urlencoded';
    $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
}]);

app.config(function($routeProvider, $locationProvider) {
    $routeProvider.when('/', {
        templateUrl: 'static/templates/main.html',
        controller: 'MainController'
    });
    $routeProvider.when('/reg/', {
        templateUrl: 'static/templates/reg.html',
        controller: 'RegFormController'
    });
    $routeProvider.when('/login', {
        templateUrl: 'static/templates/login.html',
        controller: 'LoginFormController'
    });
    $routeProvider.when('/add/', {
        templateUrl: 'static/templates/add.html',
        controller: 'CreateFormController'
    });
    $routeProvider.when('/update/:operId', {
        templateUrl: 'static/templates/update.html',
        controller: 'UpdateFormController',
    });
    $routeProvider.when('/delete/:operId', {
        templateUrl: 'static/templates/delete.html',
        controller: 'DeleteFormController',
    });
    $routeProvider.when('/read/', {
        templateUrl: 'static/templates/login.html',
        controller: 'ReadFormController',
    });
    $routeProvider.when('/logout/', {
        controller: 'LogoutController'
    });
    $routeProvider.otherwise(
        {redirectTo: '/'}
    );
//    $locationProvider.html5Mode(true);
});

app.controller('MainController', ['$scope', '$http', '$location', function($scope, $http, $location) {
    $http.post('/')
        .success(function(data, status) {
            console.log('MAIN PAGE -> OK -> ' + status);
            console.log('DATA -> ' + data);
            $scope.name = data['name']
            $scope.operations = data['operations']
            console.log($scope.operations)
        })
        .error(function(data, status) {
            console.log('MAIN PAGE -> NOT_OK -> ' + status);
            $location.path("/login");
        });
}]);

app.controller('RegFormController', ['$scope', '$http', '$location', '$log', function($scope, $http, $location, $log) {
	$scope.submit = function() {
        $scope.submitted = true;
		var in_data = {reg: $scope.reg};
		console.log(in_data);
		$http.post('/reg/', angular.toJson(in_data))
			.success(function(data, status) {
				console.log("OK " + data);
				$location.path("/login")
			})
			.error(function(data, status) {
//				errors = angular.fromJson(data);
                $log.warn(data.error);
                $scope.e = data.error;
			});
	};
}]);

app.controller('LoginFormController', ['$scope', '$http', '$location', '$log', function($scope, $http, $location, $log) {
    $scope.submit = function() {
        $scope.submitted = true;
        var in_data = {login: $scope.login};
        $http(
            {
                method: 'POST',
                url: '/login/',
                data: in_data
            }
        )
        .success(function(data, status) {
            $location.path("/");
        })
        .error(function(data, status) {
            errors = angular.fromJson(data)
            $log.warn(data.error);
            $scope.e = data.error;
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

app.controller('UpdateFormController',
                ['$scope', '$http', '$routeParams', '$log', '$location',
                function($scope, $http, $routeParams, $log, $location) {
    var _id = {pk: $routeParams.operId};
    $http.post('/update/', angular.toJson(_id))
    .success(function(data, status) {
        $log.debug('Success: data -> ' + data + ' :: status -> ' + status);
        obj = angular.fromJson(data);
        $scope.obj = obj.operation[0];
        $scope.category = obj.categories
        $log.log(obj)
    })
    .error(function(data, status) {
        $location.path('/')
        console.log('Error: data -> ' + data + ' :: status -> ' + status);
    });

    $scope.submit = function() {
        var in_data = {update: $scope.obj, pk: $routeParams.operId};
        $http.post('/update/', angular.toJson(in_data))
        .success(function(data, status) {
            $location.path('/');
        })
        .error(function(data, status) {
            $log.warn(data);
        });
    };
}]);

app.controller('DeleteFormController',
                ['$scope', '$http', '$routeParams', '$log', '$location',
                function($scope, $http, $routeParams, $log, $location) {
    var _id = {pk: $routeParams.operId};
    $http.post('/delete/', angular.toJson(_id))
    .success(function(data, status) {
        $log.debug('Success: data -> ' + data + ' :: status -> ' + status);
        obj = angular.fromJson(data);
        $scope.del = obj[0]
    })
    .error(function(data, status) {
        $location.path('/')
        console.log('Error: data -> ' + data + ' :: status -> ' + status);
    });

    $scope.submit = function() {
        var in_data = {delete: true, pk: $routeParams.operId};
        $http.post('/delete/', angular.toJson(in_data))
        .success(function(data, status) {
            $location.path('/');
        })
        .error(function(data, status) {
            $log.warn(data);
        });
    };
}]);

app.controller('ReadFormController',
                ['$scope', '$http', '$routeParams', '$log', '$location',
                function($scope, $http, $routeParams, $log, $location) {
//    var _id = {id: 5};
    $http.post('/read/')// angular.toJson(_id))
    .success(function(data, status) {
        $log.debug('Success: data -> ' + data + ' :: status -> ' + status);
    })
    .error(function(data, status) {
        console.log('Error: data -> ' + data + ' :: status -> ' + status);
    });
}])

app.controller('LogoutController', ['$http', '$location', function($http, $location) {
    $http.get('/logout/')
}]);