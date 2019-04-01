$(function(){
  var src=null;
  $('#myfile').on('change',function(e){
    var t=e.target;
    var file = t.files[0];
    var type=file.type;
    
    
    if(type.indexOf("image") <0){
      $('#error').text("画像ファイルを指定してください");
      t.value="";
      $("#img1").prop("src", "");
      e.preventDefault();
    }else{
      $('#error').text("");
      var blob=new Blob([file],{type:type});
      var url = window.URL || window.webkitURL;
      $("#img1").prop("src", url.createObjectURL(blob));
      $("#img1").prop("title", file.name);
    }
  });


  $('#f1').on('submit',function(e){
    if($('#myfile').val()===""){
      $('#error').text("ファイルを選択してください");
      e.preventDefault();
    }
  });
});