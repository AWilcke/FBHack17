<?php
include "../php/functions.php";
include "../php/db_connect.php";

file_put_contents("test.txt", "\n".json_encode($_REQUEST), FILE_APPEND);

if(isset($_REQUEST['password'])){
	if($_REQUEST['password']!="5QrFz5N2Casjhq3eYDBh9qKk")
		sendError(403, "Incorrect password");
		
		$u_id=sanitize($_REQUEST["u_id"]);
		$key=db_get("SELECT `token` FROM `user` WHERE `fb_id`='$u_id'");
		if(!empty($key)){
			$key=$key['token'];
		}else{
			$key=cryptobytes(20);
			db_exec("INSERT INTO `user`(`fb_id`, `token`) VALUES ('$u_id','$key')");
		}
		$url="http://www.anyonetrades.com/dashboard.php?key=$key";
		$arr=db_get(
			"SELECT count(`id`) FROM `alerts` WHERE `used`=0 AND `u_id`='$u_id'","both");
		$num=$arr[0];
		echo json_encode(
			array(
				"num"=>$num,
				"url"=>$url
			)
		);
}