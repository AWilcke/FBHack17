<?php
	include "php/functions.php";
	include "php/db_connect.php";
	include "analysis.php";
	$key=getValue("key");
	if(!$key)
			sendError(403,"You didn't provide a key in the URL!");
	$q=db_get("SELECT `fb_id` FROM `user` WHERE `token`='$key'");
	if(empty($q))
		sendError(400,"We don't have anything for this token yet...");
	$fb_id=$q['fb_id'];
	$q=db_get_array("SELECT * FROM `alerts` WHERE `u_id`='$fb_id' AND `used`=0");
	//if(empty($q)) sendError(400,"You don't have any alerts set yet");
?>
<html>
	<head>
		<title>Anyone Can Trade!</title>
		<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/css/materialize.min.css"/>
		<link href="https://fonts.googleapis.com/icon?family=Material+Icons" rel="stylesheet">
		<input type="hidden" id="key" value="<?=$key?>" /></script>
		<script type="text/javascript" src="https://code.jquery.com/jquery-2.1.1.min.js"></script>		
		<script type="text/javascript" src="https://cdnjs.cloudflare.com/ajax/libs/materialize/0.98.0/js/materialize.min.js"></script>
		<script type="text/javascript" src="dashboard.js"></script>
	</head>
	<body class="container">
		<h2>Your Alerts:</h2>
		<table class="highlight">
			<thead>
				<tr>
					<th>Symbol</th>
					<th>Price</th>
					<th>Alert</th>
					<th>High</th>
					<th>Low</th>
				</tr>
			</thead>
			<tbody>
				<?php
				foreach($q as $alert){
					$stock=$alert["stock"];
					$a=$alert["a"];
					$b=$alert["b"];
					if(isset($dictionary[$a]))$a=$dictionary[$a];
					if(isset($dictionary[$b]))$b=$dictionary[$b];
					$id=$alert["id"];
					$row = get_row($stock);
					echo '<tr id="row-"'.$id.'"><td>'.$stock.'</td><td>'.$row['price']."</td>";
					echo "<td><b>$a</b> is greater than <b>$b</b></td>";
					echo "<td>".$row['high']."</td>";
					echo "<td>".$row['low']."</td>";
					echo '<td><div class="btn red" style="float:right" onclick="deleteAlert('.$id.')">Delete</div></td></tr>';
				}
				?>					
			</tbody>
		</table>
		<div class="card-panel teal lighten-5" style="margin-top: 70px; margin-bottom: 40px;">
		<div class="row">
			<div class="input-field col s9">
				<input placeholder="Create Alert" id="alert" type="text" class="validate">
				<label for="alert">Query text</label>				
			</div>
			<div class="col s3" style="margin-top: 16px">
				<div class="btn green waves-effect waves-light" onclick="createAlertText()">Create</div>
			</div>
		</div>
		</div>

<div class="card-panel teal lighten-5">
<div class="row">
	<div class="col s4">
		<span style="float: left;">Notify me when</span>
		<input type="text" placeholder="Symbol" id="stock" value="" class="browser-default" style="float:left; margin-left: 5px; margin-right: 5px; margin-top: -10px; width:20%;" >
		<span style="float:left;">'s </span>
	</div>
	<div class="col s3">
		<div class="input-field col s12">
			<select id="metric1" value="" class="" style="float:left; margin-left 5px; margin-right: 5px; margin-top: -10px; width:20%;">
				<option value="" disabled selected>Metric</option>
				<option value="value">Value</option>
				<option value="volume">Volume</option>
				<option value="move10">Simple 10 day average</option>
				<option value="move30">Simple 30 day average</option>
				<option value="move50">Simple 50 day average</option>
				<option value="weight10">Weighted 10 day average</option>
				<option value="weight30">Weighted 30 day average</option>
				<option value="weight50">Weighted 50 day average</option>
				<option value="momentum">Momentum</option>
				<label>Metric</label>
			</select>
		</div>
	</div>
	<div class="col s3">
		<div class="input-field col s12">
			<select id="comparison" onchange="changeComparison()" style="float:left; margin-left 5px; margin-right: 5px; margin-top: -10px; width:20%;">
				<option value="" disabled selected>Comparison</option>
				<option value="increase">increases</option>
				<option value="decrease">decreases</option>
				<option value="greater">is greater than</option>
				<option value="less">is less than</option>
				<label>Comparison</label>				
			</select>
		</div>
	</div>
</div>
		<div class="row">
			<div id="m2h" class="col s4" style="position:relative;">
				<p style="position:absolute; top:-32px;left:-6px" id="radio1">
					<input class="with-gap" name="met-cho" type="radio" id="met-cho1" value="1" onchange="changeRadio(1)" checked/>
					<label for="met-cho1"></label>
				</p>
				<div class="input-field col s12">		
					<select id="metric2">
						<option value="" disabled selected>Metric</option>
						<option value="value">Value</option>
						<option value="volume">Volume</option>
						<option value="move10">Simple 10 day average</option>
						<option value="move30">Simple 30 day average</option>
						<option value="move50">Simple 50 day average</option>
						<option value="weight10">Weighted 10 day average</option>
						<option value="weight30">Weighted 30 day average</option>
						<option value="weight50">Weighted 50 day average</option>
						<option value="momentum">Momentum</option>
					</select>
					<label>Metric</label>
				</div>
			</div>
			<div class="col s2" id="or"><center>OR</center></div>
			<div class="col s6" id="blankspace" style="display:none"></div>
			<div class="col s2" style="position:relative;">
				<p style="position:absolute; top:-32px;left:-6px">
					<input class="with-gap" name="met-cho" type="radio" id="met-cho2" value="2" onchange="changeRadio(2)"/>
					<label for="met-cho2"></label>
				</p>
				<input disabled id="constant" type="number" placeholder="constant">
			</div>
			<div class="col s2">
				<div class="input-field col s12">
				<select id="type" class="">
					<option value="">Type</option>
					<option value="usd">USD</option>
					<option value="percent">Percent</option>
				</select>
				</div>
			</div>
		</div>
		<div class="row">
			<div class="col s2 offset-s5">
				<div class="btn green waves-effect waves-light" style="width:100%;" onclick="createAlertBuilder()">
					Create Alert
				</div>
			</div>
		</div>
		</div>
	</body>
</html>