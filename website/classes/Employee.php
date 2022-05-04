<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
class Employee
{

    private $dbConn;

    private $ds;

    function __construct()
    {
        require_once 'Db.php';
        $this->ds = new Db(true);
    }

    function getEmployeeNameById($id)
    {
        $query = 'SELECT `username`
            FROM `fc_employee`
            WHERE `id_employee` = ?';
        
        $paramType = 's';
        $paramArray = array(
            $id
        );
        $eName = $this->ds->select($query, $paramType, $paramArray);

        return $eName[0]['username'];
    }

    public function processLogin($username, $passwd)
    {
        // $passwdHash = md5($passwd);
        $query = 'SELECT *
            FROM `fc_employee`
            WHERE `username` = ? AND `passwd` = ?';
      
        $paramType = 'ss';
        $paramArray = array(
            $username,
            $passwd
        );
        $eDataLogin = $this->ds->select($query, $paramType, $paramArray);
       
        if (! empty($eDataLogin)) {
            $_SESSION['userID'] = $eDataLogin[0]['id_employee'];
            return true;
        }
    }
}