<?php
include "php/functions.php";
include "php/db_connect.php";
include "analysis.php";

$alerts=db_get_array("SELECT * FROM `alerts` WHERE `used`=0","keys");
foreach($alerts as $alert){
	$u_id=$alert['u_id'];
	$a_id=$alert['id'];
	$stock=$alert['stock'];
	$a=$alert['a'];
	$b=$alert['b'];
	$type=$alert['type'];
	$neg=$alert['neg'];
	$q=analyze($stock, $a, $b, $type=="constant");

	if ($q!=$neg) {
		$postData=array(
			"u_id"=>$u_id,
			"text"=>$stock."'s ".$a.($neg?" is less than ":" is greater than ").$b."."
		);
		echo sql_dump_array($json);
		sendHeroku($postData);
		db_exec("UPDATE `alerts` SET `used`=1 WHERE `id`='$a_id'");
	}
};

/*
sendHeroku(array(
	"u_id":"1626652780683777",
	"text":"TestSend"
));
*/
function sendHeroku($postparams){
	$url="https://anyonetrades.herokuapp.com/notify";
	$ch = curl_init();
	curl_setopt($ch, CURLOPT_HEADER, 0);
	curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
	curl_setopt($ch, CURLOPT_URL, $url);
	curl_setopt($ch, CURLOPT_POSTFIELDS, $postparams);
	$result=curl_exec($ch);
	curl_close($ch);
	print_r($postparams);
	return $result;
}?>
