var stock;
var metric1;
var metric2;
var operation;

function changeComparison(){
	var comparison = $('#comparison').val();
	if(comparison == 'increase' || comparison == 'decrease'){
		$("#m2h").hide();
		$("#or").hide();
		$("#radio1").hide();
		$("#blankspace").show();
		$("#constant").prop('disabled',false);
    	$("#metric2").prop('disabled',true);
		$("#met-cho2").prop('checked',true);
	}
	else{
		$("#or").show();
		$("#m2h").show();
		$("#radio1").show();
		$("#blankspace").hide();
	}
}

function changeRadio(val){
    console.log(val);
    if(val == 1){
    	$("#constant").prop('disabled',true);
    	$("#type").prop('disabled',true);
    	$("#metric2").prop('disabled',false);
    }
    else{
    	$("#constant").prop('disabled',false);
    	$("#type").prop('disabled',false);
    	$("#metric2").prop('disabled',true);
    }
}

function deleteAlert(id){
	console.log(id);
	$.ajax({
		url:"webtools/delete.php",
		method:"GET",
		data:{
			key:$("#key").val(),
			alert_id:id
		}
	}).done(function(data){
		$("#row-" + id).remove();
		location.reload();
	});
}

function createAlertText(){
	var text = $("#alert").val();
	if(text.length == 0){return;}
	$.ajax({
		url:"webtools/toWit.php",
		method:"GET",
		data:{
			key:$("#key").val(),
			text:text
		}
	}).done(function(data){
		location.reload();
	});
}

function createAlertBuilder(){
	var stock = $("#stock").val();
	var met1 = $("#metric1").val();
	var comparison = $("#comparison").val();
	var rad = $('input[name=met-cho]:checked').val(); // 1:2 vars, 2:constant
	var met2 = $("#metric2").val();
	var cons = $("#constant").val();
	var type = $("#type").val();

	if(rad==1) var reqType="variables"
	else if (comparison=="greater"||comparison=="less") var reqType="absolute"
	else if (type=="percent") var reqType="percent"
	else if (type=="usd") var reqType="relative"
	else alert("ERROR");
	if(reqType=="variables") {
		if(comparison=="less"){
			var b=met1
			var met1=met2
		}else
			var b=met2
	}
	else var b=cons 

	if(comparison=="decrease")b=-b

	//console.log(data);
	$.ajax({
		url:"webtools/create_alert.php",
		method:"GET",
		data:{
			key:$("#key").val(),
			stock: stock,
			a: met1,
			b: b,
			type: reqType
		}
	}).done(function(data){
		location.reload();
	});
}
$(document).ready(function() {
    $('select').material_select();
  });