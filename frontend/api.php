<?php
include "php/functions.php";
include "php/db_connect.php";

file_put_contents("test.txt", "\n".json_encode($_REQUEST), FILE_APPEND);

if(isset($_REQUEST['password'])){
	if($_REQUEST['password']!="5QrFz5N2Casjhq3eYDBh9qKk")
		sendError(403, "Incorrect password");
	$u_id=sanitize($_REQUEST["u_id"]);
	switch($_REQUEST['request']){
		case "create_alert":
			$stock=sanitize(postValue("stock"));
			$a=sanitize(postValue("a"));
			$b=sanitize(postValue("b"));
			$b_type=sanitize(postValue("b_type"));
			db_exec("INSERT INTO `alerts`(`u_id`,`type`,`stock`, `a`, `b`) VALUES ('$u_id','$b_type','$stock','$a','$b')");
			echo "Success";
			break;
		case "get_alerts":
			$arr=db_get_array("SELECT * FROM `alerts` WHERE `used`=0 AND `u_id`='$u_id'","keys");
			echo json_encode($arr);
			break;
		case "get_url":
			echo getToken($u_id);
			break;
		default:
			sendError(400, "Unknown Request");
			break;
	}
}

function getToken($u_id){
	$key=db_get("SELECT `token` FROM `user` WHERE `fb_id`='$u_id'");
	if(!empty($key)){
		$key=$key['token'];
	}else{
		$key=cryptobytes(12);
		db_exec("INSERT INTO `user`(`fb_id`, `token`) VALUES ('$u_id','$key')");
	}
	return "http://anyonetrades.com/dashboard.php?key=$key";
}