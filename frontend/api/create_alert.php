<?php
include "../php/functions.php";
include "../php/db_connect.php";
include "../analysis.php";

file_put_contents("test.txt", "\n".json_encode($_REQUEST), FILE_APPEND);

if(isset($_REQUEST['password'])){
	if($_REQUEST['password']!="5QrFz5N2Casjhq3eYDBh9qKk")
		sendError(403, "Incorrect password");
	$u_id=sanitize($_REQUEST["u_id"]);
	$stock=sanitize(postValue("stock"));
	$a=sanitize(postValue("a"));
	$b=sanitize(postValue("b"));
	$change=sanitize(postValue("change"));
	if($change=="down")$b=-$b;
	$type=sanitize(postValue("type"));
	$current=get_info($stock,$a);
	switch ($type) {
		case 'absolute':
			$neg=$b<$current?1:0;
			$t="constant";
			break;
		case 'relative':
			$neg=$b<0?1:0;
			$b+=$current;
			$t="constant";
			break;
		case 'percent':
			$neg=$b<0?1:0;
			$b/=100;
			$b=($b*$current)+$current;
			$t="constant";
			break;
		case 'variables':
			$neg=0;
			$t="variable";
			break;
		default:
			sendError(400,"I'm not sure what kind of request that is");
			break;
	}
	$q="INSERT INTO `alerts`(`u_id`,`type`,`stock`, `a`, `b`,`neg`) VALUES ('$u_id','$t','$stock','$a','$b','$neg')";
	db_exec($q);
	file_put_contents("test.txt", "\n".$q, FILE_APPEND);

	if(isset($dictionary[$a]))$a=$dictionary[$a];
	if(isset($dictionary[$b]))$b=$dictionary[$b];
	echo "Okay, I'll let you know when $stock's ".$a. ($neg?" goes below ":" goes above ").$b;

	}

?>