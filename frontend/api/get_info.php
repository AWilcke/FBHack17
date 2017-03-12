<?php
include "../php/functions.php";
include "../php/db_connect.php";
include "../analysis.php";

file_put_contents("test.txt", "\n".json_encode($_REQUEST), FILE_APPEND);

if(isset($_REQUEST['password'])){
	if($_REQUEST['password']!="5QrFz5N2Casjhq3eYDBh9qKk")
		sendError(403, "Incorrect password");
		$metric=$_REQUEST['metric'];
		$stock=$_REQUEST['stock'];
		echo get_info($stock,$metric);
}

//echo get_info("MSFT","value");

?>