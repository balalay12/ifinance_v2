var app = angular.module('app', ['ngRoute', 'ngResource', 'ui.bootstrap']);

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
//    $routeProvider.when('/logout/', {
//        controller: 'LogoutController'
//    });
    $routeProvider.otherwise(
        {redirectTo: '/'}
    );
//    $locationProvider.html5Mode(true);
});

app.config(['$resourceProvider', function($resourceProvider) {
  $resourceProvider.defaults.stripTrailingSlashes = false;
}]);

app.factory('Post', ['$resource', function($resource) {
    return $resource('/crud/');
}]);

app.factory('Category', ['$resource', function($resource) {
    return $resource('/get_categorys/');
}]);

app.controller('MainController', ['$scope', '$location', 'Post',function($scope, $location, Post) {
    var res = Post.query(function() {
        $scope.operations = res;
        console.log(res)
    }, function(errResponse) {
        $location.path('/')
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
                $log.warn(data)
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

app.controller('CreateFormController',
                ['$scope', '$location', '$filter', 'Category', 'Post', 
                function($scope, $location, $filter, Category, Post) {
    Category.query(function(cat) {
        $scope.data = cat;
    }, function(errResponse) {
//        $location.path('/')
    });

    $scope.today = function() {
        $scope.date = $filter('date')(Date.now(), 'yyyy-MM-dd');
    };
    $scope.today();

    $scope.clear = function() {
        $scope.date = null;
    };

    $scope.disabled = function(date, mode) {
        return (mode === 'day' && (date.getDay() === 0 || date.getDay() === 6));
    };

    // $scope.toggleMin = function() {
    //     $scope.midDate = $scope.minDate ? null : new Date();
    // };

    $scope.open = function($event) {
        $event.preventDefault();
        $event.stopPropagation();

        $scope.opened = true;
    };

    $scope.dateOptions = {
        formatYear: 'yyyy',
        startingDay: 1
    };

    $scope.formats = ['yyyy-MM-dd'];
    $scope.format = $scope.formats[0];

    $scope.submit = function() {
        var res = Post.save({add:$scope.add},function() {
            $location.path('/')
        }, function(errResponse) {
            console.log(errResponse)
        });
    };
}]);

app.controller('UpdateFormController', ['$scope', '$routeParams', '$log', '$location', 'Post', 'Category', function($scope, $routeParams, $log, $location, Post, Category) {

    Post.query({id:$routeParams.operId}, function(upd) {
        $scope.obj = upd[0];
    });

    Category.query(function(cat) {
        $scope.category = cat;
    });

    $scope.submit = function() {
        Post.save({update: $scope.obj, id: $routeParams.operId}, function() {
            $location.path('/');
        });
    };
}]);

app.controller('DeleteFormController',
                ['$scope', '$http', '$routeParams', '$log', '$location', 'Post',
                function($scope, $http, $routeParams, $log, $location, Post) {
	Post.query({id: $routeParams.operId}, function(del) {
		$scope.del = del[0];
	});

	$scope.submit = function() {
		Post.delete({id: $routeParams.operId}, function() {
			$location.path('/');
		});
	};
}]);

//app.controller('LogoutController', ['$http', function($http, $location) {
//    $http.get('/logout/');
//}]);
