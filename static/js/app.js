var app = angular.module('formApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

app.controller('formCtrl', function($scope,$http) {
   $scope.delimiter = {
    select:null,
    availableOptions: [
      {id: '1', name: 'comma',value:","},
      {id: '2', name: 'semi-comma',value:";"},
      {id: '3', name: 'pip',value:"|"}
      ],
    };
    $scope.datatype = [
      {id:"1",name: 'string',value:""},
      {id:"2",name: 'int',value:"^^<http://www.w3.org/2001/XMLSchema#int>"},
      {id:"3",name: 'date',value:"^^<http://www.w3.org/2001/XMLSchema#date"}
      ];
    $scope.header=[];
    $scope.data=[];
    $scope.headerline=0;
    $scope.startline=1;
    $scope.endline='';
    $scope.csvText = '';
    $scope.entityPrefix='';
    $scope.subjPrefix='';
    $scope.predPrefix='';
    $scope.namespace='@prefix data:';
    // $scope.fileName='';
    // $scope.entityPrefix="http://localhost/"+$scope.fileName+"/data#"+$scope.fileName
    // $scope.subjPrefix="http://localhost/"+$scope.fileName+"/data/"
    // $scope.predPrefix="http://localhost/"+$scope.fileName+"/data#"
     $scope.fileChanged = function() {
       // define reader
      var reader = new FileReader();

      // A handler for the load event (just defining it, not executing it right now)
      reader.onload = function(e) {
          $scope.$apply(function() {
              $scope.csvText = reader.result;
          });
      };

      // get <input> element and the selected file 
      var csvFileInput = document.getElementById('csvFile');    
      var csvFile = csvFileInput.files[0];
      $scope.fileName=csvFileInput.files[0].name;
      $scope.entityPrefix="http://localhost/"+$scope.fileName+"/data#"+$scope.fileName
      $scope.subjPrefix="http://localhost/"+$scope.fileName+"/data/"
      $scope.predPrefix="http://localhost/"+$scope.fileName+"/data#"
      $scope.namespace=$scope.namespace+"<"+$scope.predPrefix+">"
      // use reader to read the selected file
      // when read operation is successfully finished the load event is triggered
      // and handled by our reader.onload function
      reader.readAsText(csvFile);
   };
   $scope.parseJson=function(){
     // console.log($scope.header);
     // console.log($scope.data);
     // console.log($scope.startline);
     // console.log($scope.endline);
     // console.log($scope.namespace);
     var data={
      "header": $scope.header,
      "tableau": $scope.data,
      "datatype":$scope.datatype,
      "start" :$scope.startline,
      "end" : $scope.endline,
      "entity": $scope.entityPrefix,
      "subjPrefix":$scope.subjPrefix,
      "predPrefix":$scope.predPrefix,
      "namespace":$scope.namespace
     }

    $http.post('/process', JSON.stringify(data)).
      success(function(results) {
        $scope.turtle=results;
      }).
      error(function(error) {
        console.log(error)
      });
   }
   $scope.parseCSV=function(){
      var lines;
      $scope.data = [];
      $scope.header = [];
      lines = $scope.csvText.split('\n');
      lines=lines.filter(Boolean);
      var header=lines[$scope.headerline].split($scope.delimiter.select);
      if(lines[1].split($scope.delimiter.select).length==header.length){
        header.forEach(function(e){
          $scope.header.push({
              name:e,
              typeId:'1' 
          })
        });
        $scope.endline=lines.length
      } 
      for (var i=1; i<lines.length  ; i++) {
        var datalist = lines[i].split($scope.delimiter.select);
        if (datalist.length == $scope.header.length) {
            var tarr = [];
            for (var j=0; j<$scope.header.length; j++) {
                tarr.push(datalist[j]);
            }
            $scope.data.push(tarr);
        }
      }
      if($scope.data.length==lines.length-1) $scope.parseJson();
      else $scope.turtle='';
   }
   $scope.$watchGroup(["csvText","delimiter.select","headerline"], function() {
      if($scope.delimiter.select!=null) $scope.parseCSV();
   });
   $scope.$watchGroup(["entity","subjPrefix","predPrefix","startline","endline","namespace"], function() {
      if ($scope.header.length>0) $scope.parseJson();
   });
   $scope.updateType=function(){
      if ($scope.header.length>0) $scope.parseJson();
   }
});

// app.directive('fileReader', function() {
//   return {
//     scope: {
//       fileReader:"="
//     },
//     link: function(scope, element) {
//       $(element).on('change', function(changeEvent) {
//         var files = changeEvent.target.files;
//         if (files.length) {
//           var r = new FileReader();
//           r.onload = function(e) {
//               var contents = e.target.result;
//               scope.$apply(function () {
//                 scope.fileReader = contents;
//               });
//           };
          
//           r.readAsText(files[0]);
//         }
//       });
//     }
//   };
// });