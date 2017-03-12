<?php
    
    
    
	function analyze($stock, $metric1, $metric2, $is_constant){
		//assumes you want metric1 > metric2
		$stock_data = query_data($stock);
		$value1 = compute_metric($stock_data, $metric1);
		$value2 = $metric2;
		if(!$is_constant){
			$value2 = compute_metric($stock_data, $metric2);	
		}
		return $value1 > $value2;
	}
	
	function get_info($stock, $metric){
		$stock_data = query_data($stock);
		return compute_metric($stock_data, $metric);
	}
	
	function get_value($stock){
		return query_current($stock)->LastTradePriceOnly;
	}
	
	function get_row($stock){
		$data = query_data($stock);
		$row = array(
			'high' => $data['historic']['highs'][0],
			'low' => $data['historic']['lows'][0],
			'price' => $data['current']->LastTradePriceOnly
		);
		return $row;
	}
	
	function query_data($stock){
		$data = array();
		$data['current'] = query_current($stock);
		$data['historic'] = query_historic($stock);
		return $data;
	}
		
	function query_current($stock){		
		$baseurl="https://query.yahooapis.com/v1/public/yql";
		$query='select * from yahoo.finance.quotes where symbol in ("'.$stock.'")';
		$params=array(
			"q"=>$query,
			"format"=>"json",
			"env"=>"store://datatables.org/alltableswithkeys"
		);
		$reply=sendCURL($baseurl, $params);
		$json=json_decode($reply);
		$quote=$json->query->results->quote;
		return $quote;
	}
	
	function query_historic($stock){
		$baseurl='www.google.com/finance/historical';
		$query = 'www.output=xml&q=' . $stock;
		$params=array(
			"q"=>$stock,
			"output"=>"csv"
		);
		$historic = sendCURL($baseurl, $params);
		$formatted = array(
			'dates' => array(),
			'opens' => array(),
			'highs' => array(),
			'lows' => array(),
			'closes' => array(),
			'volumes' => array()
		);
		$lines=explode("\n",$historic);
		array_shift($lines);
		array_pop($lines);
		foreach($lines as &$line){
			$line=explode(",",$line);
			$formatted['dates'][] = $line[0];
			$formatted['opens'][] = $line[1];
			$formatted['highs'][] = $line[2];
			$formatted['lows'][] = $line[3];
			$formatted['closes'][] = $line[4];
			$formatted['volumes'][] = $line[5];			
		} 		
		return $formatted;
	}
	
	
	
	function sendCURL($url,$params){
		$ch = curl_init();
		curl_setopt($ch, CURLOPT_HEADER, 0);
		curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
		$get= http_build_query($params);
		$uri=$url."?".$get;
		curl_setopt($ch, CURLOPT_URL, $uri);
		$result=curl_exec($ch);
		curl_close($ch);
		return $result;
	}
	
	function compute_metric($stock_data, $metric){
		switch ($metric) {
			case 'value':
				return acquire_value($stock_data);
				break;
			case 'volume':
				return acquire_volume($stock_data);
				break;				
			case 'move10':
				return moving_average($stock_data, 10);
				break;
			case 'move30':
				return moving_average($stock_data, 30);
				break;
			case 'move50':
				return moving_average($stock_data, 50);
				break;				
			case 'weight10':
				return weighted_average($stock_data,10);
				break;
			case 'weight30':
				return weighted_average($stock_data,30);
				break;
			case 'weight50':
				return weighted_average($stock_data,50);
				break;
			case 'macd':
				return macd($stock_data);
				break;
			case 'momentum':
				return momentum($stock_data, 10);
				break;
			case 'rsi':
				return rsi($stock_data);
				break;
			default:
				return 'err1';
				break;
		}
		return 'err2';
	}
	
	function acquire_value($data){
		return $data['current']->LastTradePriceOnly;
	}
	
	function acquire_volume($data){
		return $data['historic']['volumes'][0];
	}
	
	function moving_average($data, $n=10){
		$hist = $data['historic'];
		$sum = 0;
		for($i = 0; $i < $n; $i++){
			$sum = $sum + $hist['closes'][$i];
		}
		$sum = $sum / $n;
		//echo $sum;
		return $sum;
	}
	
	function weighted_average($data, $n=10){
		$hist = $data['historic'];
		$sum = 0;
		for($i = 0; $i < $n; $i++){
			$sum = $sum + ($n - $i) * $hist['closes'][$i];
		}
		//last term is the sum from 1 to n
		$sum = $sum / (($n * ($n + 1) ) / 2);
		return $sum;
	}
	
	function macd($data){
		//unimplemented
	}
	
	function momentum($data, $n){
		$hist = $data['historic'];
		return $hist['closes'][0] - $hist['closes'][9];
	}
	
	function rsi($data){
		//unimplemented
	}

	function sendRequestYQL($stock="GOOG"){
		$baseurl="https://query.yahooapis.com/v1/public/yql";
		$query='select * from yahoo.finance.quotes where symbol in ("'.$stock.'")';
		$endstuff="&format=json&env=store://datatables.org/alltableswithkeys";
		return file_get_contents("$baseurl?q=$query$endstuff");
	}

	//echo get_info('GOOG','move10');

?>