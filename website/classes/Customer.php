<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
class Customer
{

    private $dbConn;

    private $ds;

    function __construct()
    {
        require_once 'Db.php';
        $this->ds = new Db(true);
    }

    public function getCustomersList() {
        $query = 'SELECT cu.`id_customer`, pd.`fiscalcode`, pd.`vatnumber`
            FROM `fc_customer` as cu
            LEFT JOIN `fc_personaldata` as pd ON pd.`id_personaldata` = cu.`id_personaldata`
            WHERE cu.`id_customer` != 1 AND cu.`active` = 1';
        
        $customers = $this->ds->select($query);

        $cList = '';
        foreach ($customers as $row) {
            $thisCustomer = '';
            $id = $row['id_customer'];
            $vat = $row['vatnumber'];
            $fc = $row['fiscalcode'];

            if ($vat && $fc) {
                $thisCustomer = 'PIVA: ' . $vat . ' | Codice fiscale: ' . $fc;
            } else if ($vat && ! $fiscal_code) {
                $thisCustomer = 'PIVA: ' . $vat;
            } else {
                $thisCustomer = 'Codice fiscale: ' . $fc;
            }

            $cList .= '<option value="' . $id . '">' . $thisCustomer . '</option>';
        }

        return $cList;
    }

    public function getCustomerById($id_customer) {
        $queryData = 'SELECT cu.id_customer, pd.*, wa.`public_key`
            FROM `fc_customer` as cu
            LEFT JOIN `fc_personaldata` as pd ON pd.`id_personaldata` = cu.`id_personaldata`
            LEFT JOIN `fc_wallet` as wa ON wa.`id_wallet` = cu.`id_wallet`
            WHERE cu.`id_customer` = ?';
        
        $paramType = 'i';
        $paramArray = array(
            $id_customer
        );
        $cData = $this->ds->select($queryData, $paramType, $paramArray);

        $token = new \Token();
        $tkC = $token->getTokensAndSerialByIdCustomer($id_customer);
        if ($tkC == NULL)
            $tkC = array();
        $tokens = count($tkC);

        $cData[0]['tokens'] = $tokens;
    
        return $cData;
    }
}