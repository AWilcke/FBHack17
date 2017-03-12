<?php
include "php/functions.php";
include "php/db_connect.php";

if(isset($_POST['password'])){
	if($_POST['password']!="5QrFz5N2Casjhq3eYDBh9qKk")
		sendError(403, "Incorrect password");
	$u_id=postValue("u_id");
	$stock=postValue("stock");
	$a=postValue("a");
	$b=postValue("b");
	$b_type=postValue("b_type");
}

/*
POST:{
	u_id:" "
	stock:"GOOG",
	a:"day-high",
	b:"52-week-average",
	b_type:"variable"
	password:"5QrFz5N2Casjhq3eYDBh9qKk"
}
*/