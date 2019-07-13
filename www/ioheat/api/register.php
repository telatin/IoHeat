<?php
  include('db.php');
	$answer = array();
	// usage: register.php?device=$ID

  $uuid    = $_REQUEST['uuid'];

  // check input

  $debug   = $_REQUEST['debug'];
  if (!isset($uuid)) {
    $answer['message'] = "Input UUID not specified";
    exit;
  }

  $query   = "SELECT * FROM devices WHERE uuid LIKE '$uuid'";
  $results = $db->query($query);
  $device  = $results->fetchArray();

  if ($device['uuid']) {
    $answer['message'] = "Device alreedy registered: " . $device['uuid'];
  } else {
    $answer['message'] = "Input UUID not found now to register: $uuid";
    $insert_query      = "INSERT INTO devices ('uuid') VALUES ('$uuid')";
    $answer['query']   = $insert_query;
    $db->exec($insert_query);

  }


  print json_encode($answer);
?>
