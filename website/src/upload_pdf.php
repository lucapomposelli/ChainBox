<?php

use phpseclib\Math\BigInteger as BigNumber;

if (isset($_FILES['file'])) {
    require_once '../src/config.inc.php';
    require_once '../tools/phpseclib/Math/BigInteger.php';
    require_once '../classes/Customer.php';

    $path_sfp = '../docs/pdf_sfp/';

    $myFile = $_FILES['file'];
    $fileCount = count($myFile["name"]);
    
    $pdfs = array();
    for ($i = 0; $i < $fileCount; $i++) {
        $pdf_tmp = "{$path_sfp}{$myFile["name"][$i]}";

        // Upload files
        move_uploaded_file($myFile["tmp_name"][$i], $pdf_tmp);

        // Hash PDF and rename
        $out = explode(":", shell_exec("certutil -hashfile {$pdf_tmp} SHA256"));
        $out = explode("\n", $out['1']);
        $pdf_hash = new BigNumber($out['1'], 16);
        
        $pdf_hash = $pdf_hash->toString();
        $pdf_new = "{$path_sfp}{$pdf_hash}.pdf";
        rename($pdf_tmp, $pdf_new);

        array_push($pdfs, $pdf_hash);
    }

    echo json_encode($pdfs);
    exit;
}

echo json_encode(array());