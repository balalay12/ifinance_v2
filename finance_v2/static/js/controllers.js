angular.module('reg_app', [])
    .config(function($httpProvider) {
        $httpProvider.defaults.headers.common['X-Requested-With'] = 'XMLHttpRequest';
    })
	.controller('RegFormController', ['$scope', '$http', function($scope, $http) {
		$scope.submit = function() {
			var in_data = { user: $scope.user};
			console.log(in_data);
			$http.post('/reg/', in_data)
				.success(function(out_data) {
					console.log("OK");
				})
				.error(function(out_data) {
					console.log("NOT OK");
				});
		};
	}]);

// reg_app.controller('RegFormController', function($scope) {
// 	$scope.submit = function() {
// 		var in_data = { user: $scope.user}
// 		console.log(in_data)
// 	}
// })