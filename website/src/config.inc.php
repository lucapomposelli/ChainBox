<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */

// Debug
if (! defined('_FC_MODE_DEV_')) {
    define('_FC_MODE_DEV_', true);
}

if (_FC_MODE_DEV_ === true) {
    @ini_set('display_errors', 'on');
    @error_reporting(E_ALL | E_STRICT);
} else {
    @ini_set('display_errors', 'off');
}

if (! defined('PHP_VERSION_ID')) {
    $version = explode('.', PHP_VERSION);
    define('PHP_VERSION_ID', ($version[0] * 10000 + $version[1] * 100 + $version[2]));
}

// Improve PHP configuration to prevent issues
ini_set('default_charset', 'utf-8');
ini_set('magic_quotes_runtime', 0);
ini_set('magic_quotes_sybase', 0);

// Correct Apache charset
if (! headers_sent()) {
    header('Content-Type: text/html; charset=utf-8');
}

session_start();

require_once '../src/functions.php';