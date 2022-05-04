<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
class Token
{

    private $dbConn;

    private $ds;

    function __construct()
    {
        require_once 'Db.php';
        $this->ds = new Db(false);
    }

    function getTokenGenerated()
    {
        $query = 'SELECT COUNT(`token_id`) as t_generated
            FROM `fc_token`';
        
        $tAmount = $this->ds->select($query);

        return $tAmount[0]['t_generated'];
    }

    function getTokenAssigned()
    {
        $query = 'SELECT COUNT(t1.token_id) as t_assigned FROM fc_token as t1 WHERE t1.token_id IN (SELECT DISTINCT t.token_id as t_assigned FROM `fc_log` as l 
            INNER JOIN `fc_token` as t ON l.token_id = t.token_id
            WHERE t.burn_date IS NULL AND tx_to != 1)';
        
        $tAmount = $this->ds->select($query);

        return $tAmount[0]['t_assigned'];

    }

    function getTokenBurned()
    {
        $query = 'SELECT COUNT(*) as t_burned
            FROM `fc_token`
            WHERE `burn_date` IS NOT NULL';
        
        $tAmount = $this->ds->select($query);

        return $tAmount[0]['t_burned'];

    }

    function getSerialNumber($amount = 1)
    {
        $allSerialN = array();

        // $query = 'SELECT fc1.`serial_number`
        //         FROM `fc_token` as fc1
        //         WHERE fc1.`mint_date` = (
        //             SELECT MAX(fc2.`mint_date`)
        //             FROM `fc_token` as fc2
        //             WHERE fc1.`serial_number` = fc2.`serial_number`)
        //         AND fc1.`burn_date` IS NOT NULL
        //     ';
        
        // $bSerialN = $this->ds->select($query);
        // if ($bSerialN == NULL)
        //     $bSerialNGood = 0;
        // else
        //     $bSerialNGood = count($bSerialN);

        // for($n=0; $n < min($bSerialNGood,$amount) ; $n++) {
        //     array_push($allSerialN, (int)$bSerialN[$n]['serial_number']);
        // }

        // $mSerialN = abs(count($allSerialN) - $amount);
        // if ($mSerialN > 0) {
        //     //Get last token serial_number
          
        // }

        $query = 'SELECT `serial_number`
        FROM `fc_token`
        ORDER BY serial_number DESC
        LIMIT 1';
    
        $maxSerialN = $this->ds->select($query);

        for($n=1; $n <= $amount; $n++) {
            array_push($allSerialN, (int)$maxSerialN[0]['serial_number'] + $n);
        }

            return $allSerialN;
    }

    function getTokensAndSerialByIdCustomer($id_customer, $amount = 0)
    {
        $this->ds = new Db(true);

        $wQuery = 'SELECT wa.`public_key` FROM `fc_customer` c INNER JOIN `fc_wallet` wa ON c.`id_wallet` = wa.`id_wallet` WHERE c.`id_customer` = ?';

        $paramType = 'i';
        $paramArray = array(
            $id_customer
        );

        $wData = $this->ds->select($wQuery, $paramType, $paramArray);
        
        $this->ds = new Db(false);

        $query = 'SELECT token_id, serial_number 
        FROM (
            SELECT l1.token_id, t1.serial_number, COUNT(l1.token_id) as c 
            FROM `fc_log` as l1 
            INNER JOIN fc_token t1 ON t1.token_id = l1.token_id 
            WHERE tx_to = ? AND t1.token_id NOT IN 
                (
                    SELECT token_id 
                    FROM fc_log as l2 
                    WHERE l2.tx_to = "0x0000000000000000000000000000000000000000" || l2.tx_from != "0x0000000000000000000000000000000000000000"
                )
            GROUP BY token_id
        ) 
        as temp  
        ORDER BY `temp`.`serial_number` ASC';

        if ($amount != 0) { 
            $query .= ' LIMIT ' . $amount;
        }
        
        if ($wData == NULL)
            return array();

        $paramType = 's';
        $paramArray = array(
            $wData[0]["public_key"]
        );
        
        $tData = $this->ds->select($query, $paramType, $paramArray);

        return $tData;
    }
    
    function getLogs() {
        $queryLog = 
            'SELECT token_id as Token, serial_number as Seriale, tx_to as Wallet 
             FROM (
                 SELECT l1.token_id, t1.serial_number, tx_to, COUNT(l1.token_id) as c 
                 FROM `fc_log` as l1 
                 INNER JOIN fc_token t1 ON t1.token_id = l1.token_id 
                 WHERE t1.token_id NOT IN ( 
                     SELECT token_id 
                     FROM fc_log as l2 
                     WHERE 
                        l2.tx_to = "0x0000000000000000000000000000000000000000" 
                        || l2.tx_from != "0x0000000000000000000000000000000000000000" 
                 ) 
                 GROUP BY token_id 
             ) as temp 
             ORDER BY `temp`.`serial_number` 
             ASC
            '
        ;

        $this->ds = new Db(false);
        $logData = $this->ds->select($queryLog);

        if ($logData == NULL)
            return array();

        $pDataQuery = 
            'SELECT concat(lastname, " ", firstname) as Nominativo, fiscalcode as CF, vatnumber as PIVA, company as Compagnia, w.public_key as Wallet 
            FROM `fc_personaldata` p 
            INNER JOIN `fc_customer` c ON p.id_personaldata = c.id_personaldata 
            INNER JOIN `fc_wallet` w ON c.id_wallet = w.id_wallet
            '
        ;

        $this->ds = new Db(true);
        $customerData = $this->ds->select($pDataQuery);

        for ($n = 0; $n < count($logData); $n++) {
            foreach($customerData as $customer) {
                if ($customer['Wallet'] == $logData[$n]['Wallet']) {
                    $logData[$n]['Nominativo'] = $customer['Nominativo'];
                    $logData[$n]['CF'] = $customer['CF'];
                    $logData[$n]['PIVA'] = $customer['PIVA'];
                    $logData[$n]['Compagnia'] = $customer['Compagnia'];
                }
            }
        }

        // var_dump(json_encode($logData));
        return $logData;
    }

    function getLogsBurned() {
        $queryLog = 
            'SELECT token_id as Token, serial_number as Seriale, tx_to as Wallet 
             FROM (
                 SELECT l1.token_id, t1.serial_number, tx_to, COUNT(l1.token_id) as c 
                 FROM `fc_log` as l1 
                 INNER JOIN fc_token t1 ON t1.token_id = l1.token_id 
                 WHERE t1.token_id IN ( 
                     SELECT token_id 
                     FROM fc_log as l2 
                     WHERE 
                        l2.tx_to = "0x0000000000000000000000000000000000000000" 
                        || l2.tx_from != "0x0000000000000000000000000000000000000000" 
                 ) 
                 GROUP BY token_id 
             ) as temp 
             ORDER BY `temp`.`serial_number` 
             ASC
            '
        ;

        $this->ds = new Db(false);
        $logData = $this->ds->select($queryLog);

        if ($logData == NULL)
            return array();

        $pDataQuery = 
            'SELECT concat(lastname, " ", firstname) as Nominativo, fiscalcode as CF, vatnumber as PIVA, company as Compagnia, w.public_key as Wallet 
            FROM `fc_personaldata` p 
            INNER JOIN `fc_customer` c ON p.id_personaldata = c.id_personaldata 
            INNER JOIN `fc_wallet` w ON c.id_wallet = w.id_wallet
            '
        ;

        $this->ds = new Db(true);
        $customerData = $this->ds->select($pDataQuery);

        for ($n = 0; $n < count($logData); $n++) {
            foreach($customerData as $customer) {
                if ($customer['Wallet'] == $logData[$n]['Wallet']) {
                    $logData[$n]['Nominativo'] = $customer['Nominativo'];
                    $logData[$n]['CF'] = $customer['CF'];
                    $logData[$n]['PIVA'] = $customer['PIVA'];
                    $logData[$n]['Compagnia'] = $customer['Compagnia'];
                }
            }
        }

        // var_dump(json_encode($logData));
        return $logData;
    }
}