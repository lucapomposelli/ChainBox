-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Versione server:              10.1.36-MariaDB - mariadb.org binary distribution
-- S.O. server:                  Win32
-- HeidiSQL Versione:            11.1.0.6116
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database fincode_internal
CREATE DATABASE IF NOT EXISTS `fincode_internal` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `fincode_internal`;

-- Dump della struttura di tabella fincode_internal.fc_log
CREATE TABLE IF NOT EXISTS `fc_log` (
  `id_log` int(11) NOT NULL AUTO_INCREMENT,
  `tx_hash` varchar(255) DEFAULT NULL,
  `block_hash` varchar(255) DEFAULT NULL,
  `block_number` int(10) DEFAULT NULL,
  `token_id` varchar(255) DEFAULT NULL,
  `token_value` int(11) DEFAULT NULL,
  `amount` int(11) DEFAULT NULL,
  `tx_operator` varchar(255) DEFAULT NULL,
  `tx_from` varchar(255) DEFAULT NULL,
  `tx_to` varchar(255) DEFAULT NULL,
  `tx_timestamp` datetime DEFAULT NULL,
  `event_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_log`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

-- L’esportazione dei dati non era selezionata.

-- Dump della struttura di tabella fincode_internal.fc_token
CREATE TABLE IF NOT EXISTS `fc_token` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `token_id` varchar(500) NOT NULL DEFAULT '0',
  `token_value` int(11) NOT NULL DEFAULT '0',
  `serial_number` int(11) NOT NULL DEFAULT '0',
  `owner` varchar(255) DEFAULT NULL,
  `mint_date` datetime DEFAULT NULL,
  `burn_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

-- L’esportazione dei dati non era selezionata.

-- Dump della struttura di tabella fincode_internal.requests
CREATE TABLE IF NOT EXISTS `requests` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type` varchar(255) DEFAULT NULL,
  `tx_operator_address` varchar(255) DEFAULT NULL,
  `tx_operator_id` int(11) DEFAULT NULL,
  `tx_from` varchar(255) DEFAULT NULL,
  `tx_to` varchar(255) DEFAULT NULL,
  `token_id` text,
  `token_value` text,
  `amount` text,
  `status` varchar(255) DEFAULT NULL,
  `description` text,
  `txhash` varchar(255) DEFAULT NULL,
  `aux_details` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8mb4;

-- L’esportazione dei dati non era selezionata.

-- Dump della struttura di tabella fincode_internal.pay_receipts
CREATE TABLE `pay_receipts` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`tx_to` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`data` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`status` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`description` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`aux_details` TEXT NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`txhash` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`block_hash` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`block_number` VARCHAR(255) NULL DEFAULT NULL COLLATE 'utf8mb4_general_ci',
	`tx_timestamp` DATETIME NULL DEFAULT NULL,
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_general_ci'
ENGINE=InnoDB
;


-- L’esportazione dei dati non era selezionata.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
