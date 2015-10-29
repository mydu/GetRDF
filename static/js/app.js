var app = angular.module('formApp', []);

app.config(['$interpolateProvider', function($interpolateProvider) {
  $interpolateProvider.startSymbol('{[');
  $interpolateProvider.endSymbol(']}');
}]);

app.controller('formCtrl', function($scope,$http) {
   // $scope.fileSelect={
   //    select:null,
   //    availableOptions:[]
   //  };
   $scope.filelist=[];
   $scope.delimiter = {
    select:null,
    availableOptions: [
      {id: '1', name: 'comma',value:","},
      {id: '2', name: 'semicolon',value:";"},
      {id: '3', name: 'pip',value:"|"},
      {id: '4', name: 'dollar sign',value:"$"},
      {id: '5', name: 'space',value:"\s"}
      ],
    };
    $scope.datatype = [
      {id:"1",name: 'string',value:""},
      {id:"2",name: 'int',value:"^^<http://www.w3.org/2001/XMLSchema#int>"},
      {id:"3",name: 'date',value:"^^<http://www.w3.org/2001/XMLSchema#date>"}
      ];
    $scope.header=[];
    $scope.data=[];
    $scope.headerline=0;
    $scope.startline=1;
    $scope.endline=1;
    $scope.csvText = '';
    $scope.entityPrefix='';
    $scope.subjPrefix='';
    $scope.predPrefix='';
    $scope.namespace='@prefix data:';
    // $scope.fileName='';
    // $scope.entityPrefix="http://localhost/"+$scope.fileName+"/data#"+$scope.fileName
    // $scope.subjPrefix="http://localhost/"+$scope.fileName+"/data/"
    // $scope.predPrefix="http://localhost/"+$scope.fileName+"/data#"
     // $scope.fileChanged = function() {
     //  // get <input> element and the selected file 
     //  $scope.filelist = document.getElementById('csvFile').files;
     //  // $scope.fileSelect.availableOptions=$scope.filelist;
     //  console.log($scope.filelist);
     //  // console.log($scope.fileSelect); 
     //  }
      $scope.fileChanged = function(element) {
        $scope.$apply(function(scope) {
          // console.log('files:', element.files);
          // Turn the FileList object into an Array
            $scope.filelist = []
            for (var i = 0; i < element.files.length; i++) {
              var extension = element.files[i].name.split(".").pop();
              if(extension=="csv") $scope.filelist.push(element.files[i])
            }
          // $("#filecount").text($scope.filelist.length + 'Selected');
          });
        console.log($scope.filelist)
      };

      $scope.checkChanged=function(e){
        document.getElementById('csvFile').webkitdirectory = $scope.checked;
        // $scope.checked=false;
      }
    //   $scope.folderChanged = function() {
    //   // get <input> element and the selected file 
    //   $scope.filelist = document.getElementById('folder').files;
    //   // $scope.fileSelect.availableOptions=$scope.filelist;
    //   console.log($scope.filelist);
    //   // console.log($scope.fileSelect); 
    // }
    
    $scope.fileSelectChanged=function() {
       // define reader
      var reader = new FileReader();
      // A handler for the load event (just defining it, not executing it right now)
      reader.onload = function(e) {
          $scope.$apply(function() {
              $scope.csvText = reader.result;
          });
      };
      // var csvFile = $scope.fileSelect.select;
      var csvFile = $scope.file;
      console.log(csvFile);
      $scope.fileName=csvFile.name;
      $scope.entityPrefix="http://localhost/"+$scope.fileName+"/data#"+$scope.fileName
      $scope.subjPrefix="http://localhost/"+$scope.fileName+"/data/"
      $scope.predPrefix="http://localhost/"+$scope.fileName+"/data#"
      $scope.namespace='@prefix data:'+"<"+$scope.predPrefix+">"
      // use reader to read the selected file
      // when read operation is successfully finished the load event is triggered
      // and handled by our reader.onload function
      reader.readAsText(csvFile);
   }

   // $scope.parseAll=function(){
   //    console.log("parseall")
   //    var data={
   //    "file": $scope.filelist,
   //   }
   //   $http.post('/processAll', JSON.stringify(data)).
   //    success(function(results) {
   //      console.log(results)
   //    }).
   //    error(function(error) {
   //      console.log(error)
   //    });
   // }
   $scope.parseJson=function(){
     // console.log($scope.header);
     // console.log($scope.data);
     // console.log($scope.startline);
     // console.log($scope.endline);
     // console.log($scope.namespace);
     console.log("here")
     var data={
      "filename":$scope.fileName,
      "header": $scope.header,
      "tableau": $scope.data,
      "datatype":$scope.datatype,
      // "start" :$scope.startline,
      // "end" : $scope.endline,
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
   // $scope.set=function(newVar,scopeVar){
   //      scopeVar=newVar;
   // }
   $scope.parseCSV=function(){
      if($scope.csvText!='' && $scope.delimiter.select!=null && $scope.startline!=null && $scope.endline!=null && $scope.headerline!=null){
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
          $scope.datalength=lines.length;//TODO need link endline and full line
        } 
        for (var i=$scope.startline; i<$scope.endline; i++) {
          var datalist = lines[i].split($scope.delimiter.select);
          if (datalist.length == $scope.header.length) {
              var tarr = [];
              for (var j=0; j<$scope.header.length; j++) {
                  tarr.push(datalist[j]);
              }
              $scope.data.push(tarr);
          }
        }
        console.log($scope.data)
        if($scope.data.length==$scope.endline-$scope.startline) $scope.parseJson();
        else $scope.turtle='';
      }  
   }
   $scope.$watchGroup(["csvText","delimiter.select","headerline","startline","endline"], function() {
      $scope.parseCSV();
   });
   $scope.$watchGroup(["entity","subjPrefix","predPrefix","namespace"], function() {
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