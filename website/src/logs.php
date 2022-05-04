<?php

require_once '../classes/Token.php';

$function = $_GET['target'];

if ($function == 'getLogs') {

    $token = new \Token();
    $data = $token->getLogs();

    echo json_encode($data);
}

if ($function == 'getLogsBurned') {

    $token = new \Token();
    $data = $token->getLogsBurned();

    echo json_encode($data);
}
