<?php
/**
 * @Author		FinCode s.r.l.
 * @Copyright	Since 2021
 * @Website		https://www.fincode.it/
 * @Contact		webmaster@fincode.it
 */
session_start();

$_SESSION['userID'] = '';
session_destroy();

header('location: login.php');