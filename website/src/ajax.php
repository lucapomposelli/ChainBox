<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
require_once '../src/config.inc.php';

$method = $_GET;
if ($_POST) {
    $method = $_POST;
}

$function = $method['target'];


if ($function == 'doLogin') {
    require_once '../classes/Employee.php';

    $username = filter_var($method['username'], FILTER_SANITIZE_STRING);
    $password = filter_var($method['password'], FILTER_SANITIZE_STRING);

    $employee = new Employee();
    $isLoggedIn = $employee->processLogin($username, $password);
    if (! $isLoggedIn) {
        exit(json_encode(array(
            'error' => 'Utente o password errati'
        )));
    }

    echo json_encode('success');
}


if ($function == 'getCustomerData') {
    require_once '../classes/Customer.php';

    $customer = new Customer();
    $cData = $customer->getCustomerById($_GET['id']);

    echo json_encode($cData[0]);
}

if ($function == 'generatePDF') {
    require_once '../classes/Customer.php';
    require_once '../classes/Token.php';
    require_once '../tools/fpdm/fpdm.php';
    require_once '../tools/phpseclib/Math/BigInteger.php';

    $pdfs = array();
    $token = new Token();
    $customer = new Customer();
    $cData = $_GET['cData'];

    $zip = new \ZipArchive();
    $path_sfp = '../docs/tmp/';
    $filename = "{$path_sfp}{$cData['fiscalcode']}.zip";
    $zip->open($filename, (ZipArchive::CREATE | ZipArchive::OVERWRITE));

    if(!isset($_GET['serials'])) {
        $serialN = $token->getSerialNumber($_GET['tokens']);
    } else {
        $serialN = $_GET['serials'];
    }

    for($n=0; $n < $_GET['tokens']; $n++) {
         $thisSerial = $serialN[$n];

        $fields = array(
            'denomination' => strtoupper("{$cData['lastname']} {$cData['firstname']}"),
            'birth_date' => strtoupper("{$cData['birthplace']} - ") . date('d/m/Y', strtotime($cData['birthday'])),
            'fiscal_code' => $cData['fiscalcode'],
            'address' => strtoupper("{$cData['address']}\r\n{$cData['postcode']} {$cData['city']} ({$cData['province']})"),
            'serial' => "SFP CODE - {$thisSerial} di 8.000.000",
            'par_value' => 'Euro 1,00 (UNO)',
            'conversion_date' => date('d/m/Y'),
            'forfeit' => '90%'
        );

        $pdf = new FPDM('../docs/modulosfp.pdf');
        $pdf->Load($fields, true);
        $pdf->Merge();

        //Generate tmp PDF
        $pdf_tmp = "{$path_sfp}{$cData['fiscalcode']}_{$thisSerial}.pdf";
        $pdf->Output('F', $pdf_tmp, true);

         // Add PDf to Zip
         $zip->addFile($pdf_tmp,basename($pdf_tmp));

         array_push($pdfs, $thisSerial);
    }

    $zip->close();

    echo json_encode($pdfs);
}

if ($function == 'getTokensToTransfer') {
    require_once '../classes/Token.php';

    $ids = array();
    $serials = array();
    $token = new Token();
    $tData = $token->getTokensAndSerialByIdCustomer($_GET['id'], $_GET['tokens']);

    for($n=0; $n < count($tData); $n++) {
        array_push($ids, $tData[$n]['token_id'] . '_' . $tData[$n]['serial_number']);
    }

    echo json_encode($ids);
}