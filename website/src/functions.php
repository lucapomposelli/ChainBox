<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
require_once '../classes/Customer.php';
require_once '../classes/Employee.php';
require_once '../classes/Token.php';

function getHeader($title) {
    $html = '<!DOCTYPE html>';
    $html .= '<html lang="it">';
    $html .= '<title>' . $title . '  - FinCode s.r.l.</title>';
    $html .= '<meta charset="UTF-8">';
    $html .= '<meta name="viewport" content="width=device-width, initial-scale=1">';
    $html .= '<link rel="icon" type="image/svg+xml" href="img/favicon.svg">';
    $html .= '<link rel="alternate icon" href="img/favicon.svg">';
    $html .= '<link rel="stylesheet" href="css/fonts/raleway.css" media="all">';
    $html .= '<link rel="stylesheet" href="css/w3.css" media="all">';
    $html .= '<link rel="stylesheet" href="css/style.css" media="all">';
    $html .= '<link rel="stylesheet" href="libs/tabulator/css/tabulator.min.css" media="all">';
    $html .= '<link rel="stylesheet" href="libs/tabulator/css/semantic-ui/tabulator_semantic-ui.min.css" media="all">';
    $html .= '<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css">';
    $html .= '<body id="' . basename($_SERVER['PHP_SELF'], '.php') . '">';
    $html .= '<div class="page">';

    return $html;
}

function getFooter($page = null) {
    $html = '</div>';

    switch ($page) {
        case 'dashboard':
            $html .= '<script src="js/web3.min.js"></script>';
            $html .= '<script src="js/js-web3.js"></script>';
            $html .= '<script src="js/js-dashboard.js"></script>';
            $html .= '<script src="libs/tabulator/js/tabulator.min.js"></script>';
            break;
    }

    $html .= '</body></html>';

    return $html;
}

function loadJQueryScripts($scripts = array()) {
    $html = '<script src="js/jquery/jquery.min.js"></script>';

    if ($scripts) {
        foreach ($scripts as $script) {
            switch ($script) {
                case 'select2':
                    $html .= '<script src="js/jquery/select2.min.js"></script>';
                    $html .= '<link rel="stylesheet" href="js/jquery/select2.min.css" media="all" />';
                    break;
            }
        }
    }

    return $html;
}

function employeeIsLogged() {
    if (! empty($_SESSION['userID'])) {
        header('location: dashboard.php');
    }
}

function employeeIsNotLogged() {
    if (empty($_SESSION['userID'])) {
        header('location: login.php');
    }
}

function getCustomersList() {
    $customer = new Customer();

    return $customer->getCustomersList();
}

function getEmployeeNameById($id) {
    $employee = new Employee();

    return $employee->getEmployeeNameById($id);
}

function getToken($type) {
    $token = new Token();
    if($type == 'g') {
        return $token->getTokenGenerated();
    } else if ($type == 'a') {
        return $token->getTokenAssigned();
    } else if ($type == 'b') {
        return $token->getTokenBurned();
    }
}