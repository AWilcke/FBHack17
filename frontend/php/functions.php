<?php
function db_exec($query,$test=0){
	$query=rtrim($query, ";").";";
	if($test)echo $query;
	global $con;
	$result = mysqli_query($con,$query);
	return $result;
}
function db_get($query, $type="both"){
	global $con;
	$result = mysqli_query($con,$query);
	if($result===FALSE){
		return FALSE;
	}
	$result=mysqli_fetch_array($result);
	switch($type){
		case "both":
			break;
		case "numbers":
			foreach($result as $key=>$elm){
				if(!is_numeric($key))
					unset($result[$key]);
			}
			break;
		case "keys":
			foreach($result as $key=>$elm){
				if(is_numeric($key))
					unset($result[$key]);
			}
			break;
	}
	return $result;
}
function db_get_array($query, $type="both"){
	global $con;
	$result = mysqli_query($con,$query);
	$return=array();if($result)
	while($row = mysqli_fetch_array($result))
	{
		switch($type){
			case "both":
				break;
			case "numbers":
				foreach($row as $key=>$elm){
					if(!is_numeric($key))
						unset($row[$key]);
				}
				break;
			case "keys":
				foreach($row as $key=>$elm){
					if(is_numeric($key))
						unset($row[$key]);
				}
				break;
		}
		array_push($return,$row);
	}
	return $return;
}
function findsqlerror(){
	global $con;
	return mysql_errno() . ": " . mysql_error();
}
function goToPage($page){
	$host  = $_SERVER['HTTP_HOST'];
	$uri   = rtrim(dirname($_SERVER['PHP_SELF']), '/\\');
	header("Location: http://$host$uri/$page");
	exit;
}
function goToPageRaw($page){
	header("Location: $page");
	exit;
}
function varVal($name, $defaultVal=false){
	if (!isset($GLOBALS[$name])) {
        return $defaultVal;
    }
    return $GLOBALS[$name];	
}
function arrayVal($array,$key) { 
    	if(!isset($array)){
		    return false;
    	}
    	if(!isset($array[$key])){
    		return false;
    	}
    	$val=$array[$key];
    	if(empty($val)){
    		return false;
    	}
    	return $val;
}
function getValue($key, $defaultVal=false) {
    if (!isset($_GET[$key])) {
        return $defaultVal;
    }
    return $_GET[$key];
}
function sessionValue($key, $defaultVal=false) {
    if (!isset($_SESSION[$key])) {
        return $defaultVal;
    }
    return $_SESSION[$key];
}
function postValue($key,$defaultVal=false) {
    if (!isset($_POST[$key])) {
        return $defaultVal;
    }
    return $_POST[$key];
}
function encodeGet($except){
	$vars="";
	foreach($_GET as $i=>$getvar){
		if(!in_array($i,$except)){
			$vars.=$i."=".urlencode($getvar)."&";
		}
	}$vars=rtrim($vars,"&");	
	return $vars;
}
function mailtoHTML($email){
	return "<a href=\"mailto:".$email."\">".$email."</a>";
}

function sql_dump_array($array, $includenums=0){
	$return='';
	foreach($array as $key => $value){
		if(is_array($value)){
			$return.="$key =><br>";
			$return.="<p style='padding-left: 50px;'>";
			$return.= sql_dump_array($value, $includenums);
			$return.= "</p>";
		}
		else if(!is_numeric($key) || $includenums){
			$return.= "$key => $value <br>";
		}
	}	
	return $return;
}
function cryptobytes($len,$mode="length"){//Returns pesudorandom bytes in base 36
	$bytes=0;
	if($mode=="bytes")$bytes=$len;
	else $bytes=ceil($len/(log(36)/log(8)));
	return base_convert(bin2hex(openssl_random_pseudo_bytes($bytes)),16,36);
}
$alert="";

function sendError($num,$text){
	switch($num){
		case 400:
			header("HTTP/1.0 400 Bad Request");
			break;
		case 401:
			header("HTTP/1.0 401 Unauthorized");
			break;
		case 403:
			header("HTTP/1.0 403 Forbidden");
			break;
		case 404:
			header("HTTP/1.0 404 Not Found");
			break;
		case 405:
			header("HTTP/1.0 405 Method Not Allowed");
			break;
		case 429:
			header("HTTP/1.0 429 Too Many Requests");
			break;
	}
	echo $text,"\r\n<br>";
//	echo sql_dump_array(debug_backtrace());
	$debug=debug_backtrace()[0];
	echo "$debug[file]: $debug[line]";
	
	die;
}

function db_number_rows($query){
	 	global $con;
		$result = mysqli_query($con,$query);
	 	$rowcount=mysqli_num_rows($result);
	 	return $rowcount;
	}


function validate_email($data) {
	return filter_var($data, FILTER_VALIDATE_EMAIL);
}

function sanitize($input){
	global $con;
	return $con->real_escape_string($input);
}