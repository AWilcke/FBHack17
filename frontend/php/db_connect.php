<?php
session_name('anyonetrades'); 
session_start();

//Database:
require(dirname(__FILE__)."/../../../pass/fbpass.php");
date_default_timezone_set("EST");
$con = new mysqli("localhost", DB_USER, DB_PASS, DB_DATABASE);
if (mysqli_connect_errno()) {
  echo "Failed to connect to MySQL: " . mysqli_connect_error();
}
$con->set_charset("utf8");


$dictionary=array(
	"move10"=>"10-day-moving-average",
	"move30"=>"30-day-moving-average",
	"move50"=>"50-day-moving-average",
	"weight10"=>"10-day-weighted-moving-average",
	"weight30"=>"30-day-weighted-moving-average",
	"weight50"=>"50-day-weighted-moving-average",
	"momentum"=>"10-day-Momentum",
	"value"=>"Value",
	"volume"=>"Volume"
);

define("STATICPASS","5QrFz5N2Casjhq3eYDBh9qKk");
?>