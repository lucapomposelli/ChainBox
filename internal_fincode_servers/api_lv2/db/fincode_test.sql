-- phpMyAdmin SQL Dump
-- version 5.1.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Creato il: Lug 22, 2021 alle 18:23
-- Versione del server: 10.4.19-MariaDB
-- Versione PHP: 7.3.28

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `fincode`
--
CREATE DATABASE IF NOT EXISTS `fincode` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `fincode`;

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_contract`
--

DROP TABLE IF EXISTS `fc_contract`;
CREATE TABLE IF NOT EXISTS `fc_contract` (
  `id_contract` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `symbol` varchar(10) NOT NULL,
  `address` varchar(255) NOT NULL,
  `active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_contract`),
  UNIQUE KEY `name` (`name`,`symbol`,`address`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_contract`
--

INSERT INTO `fc_contract` (`id_contract`, `name`, `symbol`, `address`, `active`) VALUES
(1, 'FinCode', 'FC', '0x4eE72d96768f9aa2e1047f07a74d14991CEC1BcE', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_country`
--

DROP TABLE IF EXISTS `fc_country`;
CREATE TABLE IF NOT EXISTS `fc_country` (
  `id_country` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `iso_code` varchar(3) NOT NULL,
  `call_prefix` int(10) NOT NULL DEFAULT 0,
  `active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `contains_states` tinyint(1) NOT NULL DEFAULT 0,
  `need_zip_code` tinyint(1) NOT NULL DEFAULT 1,
  `zip_code_format` varchar(12) NOT NULL DEFAULT '',
  PRIMARY KEY (`id_country`),
  KEY `country_iso_code` (`iso_code`)
) ENGINE=InnoDB AUTO_INCREMENT=245 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_country`
--

INSERT INTO `fc_country` (`id_country`, `iso_code`, `call_prefix`, `active`, `contains_states`, `need_zip_code`, `zip_code_format`) VALUES
(1, 'DE', 49, 0, 0, 1, 'NNNNN'),
(2, 'AT', 43, 0, 0, 1, 'NNNN'),
(3, 'BE', 32, 0, 0, 1, 'NNNN'),
(4, 'CA', 1, 0, 1, 1, 'LNL NLN'),
(5, 'CN', 86, 0, 0, 1, 'NNNNNN'),
(6, 'ES', 34, 0, 0, 1, 'NNNNN'),
(7, 'FI', 358, 0, 0, 1, 'NNNNN'),
(8, 'FR', 33, 0, 0, 1, 'NNNNN'),
(9, 'GR', 30, 0, 0, 1, 'NNNNN'),
(10, 'IT', 39, 1, 1, 1, 'NNNNN'),
(11, 'JP', 81, 0, 1, 1, 'NNN-NNNN'),
(12, 'LU', 352, 0, 0, 1, 'NNNN'),
(13, 'NL', 31, 0, 0, 1, 'NNNN LL'),
(14, 'PL', 48, 0, 0, 1, 'NN-NNN'),
(15, 'PT', 351, 0, 0, 1, 'NNNN-NNN'),
(16, 'CZ', 420, 0, 0, 1, 'NNN NN'),
(17, 'GB', 44, 0, 0, 1, ''),
(18, 'SE', 46, 0, 0, 1, 'NNN NN'),
(19, 'CH', 41, 0, 0, 1, 'NNNN'),
(20, 'DK', 45, 0, 0, 1, 'NNNN'),
(21, 'US', 1, 0, 1, 1, 'NNNNN'),
(22, 'HK', 852, 0, 0, 0, ''),
(23, 'NO', 47, 0, 0, 1, 'NNNN'),
(24, 'AU', 61, 0, 1, 1, 'NNNN'),
(25, 'SG', 65, 0, 0, 1, 'NNNNNN'),
(26, 'IE', 353, 0, 0, 0, ''),
(27, 'NZ', 64, 0, 0, 1, 'NNNN'),
(28, 'KR', 82, 0, 0, 1, 'NNNNN'),
(29, 'IL', 972, 0, 0, 1, 'NNNNNNN'),
(30, 'ZA', 27, 0, 0, 1, 'NNNN'),
(31, 'NG', 234, 0, 0, 1, ''),
(32, 'CI', 225, 0, 0, 1, ''),
(33, 'TG', 228, 0, 0, 1, ''),
(34, 'BO', 591, 0, 0, 1, ''),
(35, 'MU', 230, 0, 0, 1, ''),
(36, 'RO', 40, 0, 0, 1, 'NNNNNN'),
(37, 'SK', 421, 0, 0, 1, 'NNN NN'),
(38, 'DZ', 213, 0, 0, 1, 'NNNNN'),
(39, 'AS', 0, 0, 0, 1, ''),
(40, 'AD', 376, 0, 0, 1, 'CNNN'),
(41, 'AO', 244, 0, 0, 0, ''),
(42, 'AI', 0, 0, 0, 1, ''),
(43, 'AG', 0, 0, 0, 1, ''),
(44, 'AR', 54, 0, 1, 1, 'LNNNNLLL'),
(45, 'AM', 374, 0, 0, 1, 'NNNN'),
(46, 'AW', 297, 0, 0, 1, ''),
(47, 'AZ', 994, 0, 0, 1, 'CNNNN'),
(48, 'BS', 0, 0, 0, 1, ''),
(49, 'BH', 973, 0, 0, 1, ''),
(50, 'BD', 880, 0, 0, 1, 'NNNN'),
(51, 'BB', 0, 0, 0, 1, 'CNNNNN'),
(52, 'BY', 0, 0, 0, 1, 'NNNNNN'),
(53, 'BZ', 501, 0, 0, 0, ''),
(54, 'BJ', 229, 0, 0, 0, ''),
(55, 'BM', 0, 0, 0, 1, ''),
(56, 'BT', 975, 0, 0, 1, ''),
(57, 'BW', 267, 0, 0, 1, ''),
(58, 'BR', 55, 0, 0, 1, 'NNNNN-NNN'),
(59, 'BN', 673, 0, 0, 1, 'LLNNNN'),
(60, 'BF', 226, 0, 0, 1, ''),
(61, 'MM', 95, 0, 0, 1, ''),
(62, 'BI', 257, 0, 0, 1, ''),
(63, 'KH', 855, 0, 0, 1, 'NNNNN'),
(64, 'CM', 237, 0, 0, 1, ''),
(65, 'CV', 238, 0, 0, 1, 'NNNN'),
(66, 'CF', 236, 0, 0, 1, ''),
(67, 'TD', 235, 0, 0, 1, ''),
(68, 'CL', 56, 0, 0, 1, 'NNN-NNNN'),
(69, 'CO', 57, 0, 0, 1, 'NNNNNN'),
(70, 'KM', 269, 0, 0, 1, ''),
(71, 'CD', 242, 0, 0, 1, ''),
(72, 'CG', 243, 0, 0, 1, ''),
(73, 'CR', 506, 0, 0, 1, 'NNNNN'),
(74, 'HR', 385, 0, 0, 1, 'NNNNN'),
(75, 'CU', 53, 0, 0, 1, ''),
(76, 'CY', 357, 0, 0, 1, 'NNNN'),
(77, 'DJ', 253, 0, 0, 1, ''),
(78, 'DM', 0, 0, 0, 1, ''),
(79, 'DO', 0, 0, 0, 1, ''),
(80, 'TL', 670, 0, 0, 1, ''),
(81, 'EC', 593, 0, 0, 1, 'CNNNNNN'),
(82, 'EG', 20, 0, 0, 1, 'NNNNN'),
(83, 'SV', 503, 0, 0, 1, ''),
(84, 'GQ', 240, 0, 0, 1, ''),
(85, 'ER', 291, 0, 0, 1, ''),
(86, 'EE', 372, 0, 0, 1, 'NNNNN'),
(87, 'ET', 251, 0, 0, 1, ''),
(88, 'FK', 0, 0, 0, 1, 'LLLL NLL'),
(89, 'FO', 298, 0, 0, 1, ''),
(90, 'FJ', 679, 0, 0, 1, ''),
(91, 'GA', 241, 0, 0, 1, ''),
(92, 'GM', 220, 0, 0, 1, ''),
(93, 'GE', 995, 0, 0, 1, 'NNNN'),
(94, 'GH', 233, 0, 0, 1, ''),
(95, 'GD', 0, 0, 0, 1, ''),
(96, 'GL', 299, 0, 0, 1, ''),
(97, 'GI', 350, 0, 0, 1, ''),
(98, 'GP', 590, 0, 0, 1, ''),
(99, 'GU', 0, 0, 0, 1, ''),
(100, 'GT', 502, 0, 0, 1, ''),
(101, 'GG', 0, 0, 0, 1, 'LLN NLL'),
(102, 'GN', 224, 0, 0, 1, ''),
(103, 'GW', 245, 0, 0, 1, ''),
(104, 'GY', 592, 0, 0, 1, ''),
(105, 'HT', 509, 0, 0, 1, ''),
(106, 'HM', 0, 0, 0, 1, ''),
(107, 'VA', 379, 0, 0, 1, 'NNNNN'),
(108, 'HN', 504, 0, 0, 1, ''),
(109, 'IS', 354, 0, 0, 1, 'NNN'),
(110, 'IN', 91, 0, 1, 1, 'NNN NNN'),
(111, 'ID', 62, 0, 1, 1, 'NNNNN'),
(112, 'IR', 98, 0, 0, 1, 'NNNNN-NNNNN'),
(113, 'IQ', 964, 0, 0, 1, 'NNNNN'),
(114, 'IM', 0, 0, 0, 1, 'CN NLL'),
(115, 'JM', 0, 0, 0, 1, ''),
(116, 'JE', 0, 0, 0, 1, 'CN NLL'),
(117, 'JO', 962, 0, 0, 1, ''),
(118, 'KZ', 7, 0, 0, 1, 'NNNNNN'),
(119, 'KE', 254, 0, 0, 1, ''),
(120, 'KI', 686, 0, 0, 1, ''),
(121, 'KP', 850, 0, 0, 1, ''),
(122, 'KW', 965, 0, 0, 1, ''),
(123, 'KG', 996, 0, 0, 1, ''),
(124, 'LA', 856, 0, 0, 1, ''),
(125, 'LV', 371, 0, 0, 1, 'C-NNNN'),
(126, 'LB', 961, 0, 0, 1, ''),
(127, 'LS', 266, 0, 0, 1, ''),
(128, 'LR', 231, 0, 0, 1, ''),
(129, 'LY', 218, 0, 0, 1, ''),
(130, 'LI', 423, 0, 0, 1, 'NNNN'),
(131, 'LT', 370, 0, 0, 1, 'NNNNN'),
(132, 'MO', 853, 0, 0, 0, ''),
(133, 'MK', 389, 0, 0, 1, ''),
(134, 'MG', 261, 0, 0, 1, ''),
(135, 'MW', 265, 0, 0, 1, ''),
(136, 'MY', 60, 0, 0, 1, 'NNNNN'),
(137, 'MV', 960, 0, 0, 1, ''),
(138, 'ML', 223, 0, 0, 1, ''),
(139, 'MT', 356, 0, 0, 1, 'LLL NNNN'),
(140, 'MH', 692, 0, 0, 1, ''),
(141, 'MQ', 596, 0, 0, 1, ''),
(142, 'MR', 222, 0, 0, 1, ''),
(143, 'HU', 36, 0, 0, 1, 'NNNN'),
(144, 'YT', 262, 0, 0, 1, ''),
(145, 'MX', 52, 0, 1, 1, 'NNNNN'),
(146, 'FM', 691, 0, 0, 1, ''),
(147, 'MD', 373, 0, 0, 1, 'C-NNNN'),
(148, 'MC', 377, 0, 0, 1, '980NN'),
(149, 'MN', 976, 0, 0, 1, ''),
(150, 'ME', 382, 0, 0, 1, 'NNNNN'),
(151, 'MS', 0, 0, 0, 1, ''),
(152, 'MA', 212, 0, 0, 1, 'NNNNN'),
(153, 'MZ', 258, 0, 0, 1, ''),
(154, 'NA', 264, 0, 0, 1, ''),
(155, 'NR', 674, 0, 0, 1, ''),
(156, 'NP', 977, 0, 0, 1, ''),
(157, 'AN', 599, 0, 0, 1, ''),
(158, 'NC', 687, 0, 0, 1, ''),
(159, 'NI', 505, 0, 0, 1, 'NNNNNN'),
(160, 'NE', 227, 0, 0, 1, ''),
(161, 'NU', 683, 0, 0, 1, ''),
(162, 'NF', 0, 0, 0, 1, ''),
(163, 'MP', 0, 0, 0, 1, ''),
(164, 'OM', 968, 0, 0, 1, ''),
(165, 'PK', 92, 0, 0, 1, ''),
(166, 'PW', 680, 0, 0, 1, ''),
(167, 'PS', 0, 0, 0, 1, ''),
(168, 'PA', 507, 0, 0, 1, 'NNNNNN'),
(169, 'PG', 675, 0, 0, 1, ''),
(170, 'PY', 595, 0, 0, 1, ''),
(171, 'PE', 51, 0, 0, 1, ''),
(172, 'PH', 63, 0, 0, 1, 'NNNN'),
(173, 'PN', 0, 0, 0, 1, 'LLLL NLL'),
(174, 'PR', 0, 0, 0, 1, 'NNNNN'),
(175, 'QA', 974, 0, 0, 1, ''),
(176, 'RE', 262, 0, 0, 1, ''),
(177, 'RU', 7, 0, 0, 1, 'NNNNNN'),
(178, 'RW', 250, 0, 0, 1, ''),
(179, 'BL', 0, 0, 0, 1, ''),
(180, 'KN', 0, 0, 0, 1, ''),
(181, 'LC', 0, 0, 0, 1, ''),
(182, 'MF', 0, 0, 0, 1, ''),
(183, 'PM', 508, 0, 0, 1, ''),
(184, 'VC', 0, 0, 0, 1, ''),
(185, 'WS', 685, 0, 0, 1, ''),
(186, 'SM', 378, 0, 0, 1, 'NNNNN'),
(187, 'ST', 239, 0, 0, 1, ''),
(188, 'SA', 966, 0, 0, 1, ''),
(189, 'SN', 221, 0, 0, 1, ''),
(190, 'RS', 381, 0, 0, 1, 'NNNNN'),
(191, 'SC', 248, 0, 0, 1, ''),
(192, 'SL', 232, 0, 0, 1, ''),
(193, 'SI', 386, 0, 0, 1, 'C-NNNN'),
(194, 'SB', 677, 0, 0, 1, ''),
(195, 'SO', 252, 0, 0, 1, ''),
(196, 'GS', 0, 0, 0, 1, 'LLLL NLL'),
(197, 'LK', 94, 0, 0, 1, 'NNNNN'),
(198, 'SD', 249, 0, 0, 1, ''),
(199, 'SR', 597, 0, 0, 1, ''),
(200, 'SJ', 0, 0, 0, 1, ''),
(201, 'SZ', 268, 0, 0, 1, ''),
(202, 'SY', 963, 0, 0, 1, ''),
(203, 'TW', 886, 0, 0, 1, 'NNNNN'),
(204, 'TJ', 992, 0, 0, 1, ''),
(205, 'TZ', 255, 0, 0, 1, ''),
(206, 'TH', 66, 0, 0, 1, 'NNNNN'),
(207, 'TK', 690, 0, 0, 1, ''),
(208, 'TO', 676, 0, 0, 1, ''),
(209, 'TT', 0, 0, 0, 1, ''),
(210, 'TN', 216, 0, 0, 1, ''),
(211, 'TR', 90, 0, 0, 1, 'NNNNN'),
(212, 'TM', 993, 0, 0, 1, ''),
(213, 'TC', 0, 0, 0, 1, 'LLLL NLL'),
(214, 'TV', 688, 0, 0, 1, ''),
(215, 'UG', 256, 0, 0, 1, ''),
(216, 'UA', 380, 0, 0, 1, 'NNNNN'),
(217, 'AE', 971, 0, 0, 1, ''),
(218, 'UY', 598, 0, 0, 1, ''),
(219, 'UZ', 998, 0, 0, 1, ''),
(220, 'VU', 678, 0, 0, 1, ''),
(221, 'VE', 58, 0, 0, 1, ''),
(222, 'VN', 84, 0, 0, 1, 'NNNNNN'),
(223, 'VG', 0, 0, 0, 1, 'CNNNN'),
(224, 'VI', 0, 0, 0, 1, ''),
(225, 'WF', 681, 0, 0, 1, ''),
(226, 'EH', 0, 0, 0, 1, ''),
(227, 'YE', 967, 0, 0, 1, ''),
(228, 'ZM', 260, 0, 0, 1, ''),
(229, 'ZW', 263, 0, 0, 1, ''),
(230, 'AL', 355, 0, 0, 1, 'NNNN'),
(231, 'AF', 93, 0, 0, 1, 'NNNN'),
(232, 'AQ', 0, 0, 0, 1, ''),
(233, 'BA', 387, 0, 0, 1, ''),
(234, 'BV', 0, 0, 0, 1, ''),
(235, 'IO', 0, 0, 0, 1, 'LLLL NLL'),
(236, 'BG', 359, 0, 0, 1, 'NNNN'),
(237, 'KY', 0, 0, 0, 1, ''),
(238, 'CX', 0, 0, 0, 1, ''),
(239, 'CC', 0, 0, 0, 1, ''),
(240, 'CK', 682, 0, 0, 1, ''),
(241, 'GF', 594, 0, 0, 1, ''),
(242, 'PF', 689, 0, 0, 1, ''),
(243, 'TF', 0, 0, 0, 1, ''),
(244, 'AX', 0, 0, 0, 1, 'NNNNN');

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_customer`
--

DROP TABLE IF EXISTS `fc_customer`;
CREATE TABLE IF NOT EXISTS `fc_customer` (
  `id_customer` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_personaldata` int(10) UNSIGNED NOT NULL COMMENT 'fc_personaldata',
  `id_wallet` int(10) UNSIGNED NOT NULL COMMENT 'fc_wallet',
  `email` varchar(255) NOT NULL,
  `passwd` varchar(512) NOT NULL,
  `last_passwd_gen` timestamp NOT NULL DEFAULT current_timestamp(),
  `secure_key` varchar(256) NOT NULL DEFAULT '-1',
  `active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `deleted` tinyint(1) NOT NULL DEFAULT 0,
  `date_add` datetime NOT NULL,
  `date_upd` datetime NOT NULL,
  `reset_password_token` varchar(40) DEFAULT NULL,
  `reset_password_validity` datetime DEFAULT NULL,
  PRIMARY KEY (`id_customer`),
  KEY `customer_email` (`email`),
  KEY `customer_login` (`email`,`passwd`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_customer`
--

INSERT INTO `fc_customer` (`id_customer`, `id_personaldata`, `id_wallet`, `email`, `passwd`, `last_passwd_gen`, `secure_key`, `active`, `deleted`, `date_add`, `date_upd`, `reset_password_token`, `reset_password_validity`) VALUES
(1, 1, 1, 'fincode@fincode.it', 'fincode', '2021-06-11 10:43:55', '-1', 0, 0, '0000-00-00 00:00:00', '0000-00-00 00:00:00', NULL, NULL),
(2, 2, 0, 'lucapomposelli@gmail.com', 'luca', '2021-06-30 09:30:28', '-1', 1, 0, '2021-06-30 11:30:13', '2021-06-30 11:30:13', NULL, '2021-06-30 11:30:13'),
(3, 3, 2, 'ricky.monte91@gmail.com', 'riccardo', '2021-07-01 09:56:47', '-1', 1, 0, '2021-07-01 11:56:31', '2021-07-01 11:56:31', NULL, '2021-07-01 11:56:31');

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_employee`
--

DROP TABLE IF EXISTS `fc_employee`;
CREATE TABLE IF NOT EXISTS `fc_employee` (
  `id_employee` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `passwd` varchar(512) NOT NULL,
  `last_passwd_gen` timestamp NOT NULL DEFAULT current_timestamp(),
  `secure_key` varchar(256) NOT NULL DEFAULT '-1',
  `permissions` int(10) UNSIGNED NOT NULL DEFAULT 1,
  `active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `deleted` tinyint(1) NOT NULL DEFAULT 0,
  `date_add` datetime NOT NULL DEFAULT current_timestamp(),
  `date_upd` datetime NOT NULL DEFAULT current_timestamp(),
  `reset_password_token` varchar(40) DEFAULT NULL,
  `reset_password_validity` datetime DEFAULT NULL,
  PRIMARY KEY (`id_employee`),
  KEY `customer_email` (`username`),
  KEY `customer_login` (`username`,`passwd`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `fc_employee`
--

INSERT INTO `fc_employee` (`id_employee`, `username`, `passwd`, `last_passwd_gen`, `secure_key`, `permissions`, `active`, `deleted`, `date_add`, `date_upd`, `reset_password_token`, `reset_password_validity`) VALUES
(1, 'Fincode', 'fincode', '2021-06-14 10:06:53', '-1', 1, 1, 0, '2021-06-14 12:06:29', '2021-06-14 12:06:29', NULL, '2021-06-14 12:06:29');

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_log`
--

DROP TABLE IF EXISTS `fc_log`;
CREATE TABLE IF NOT EXISTS `fc_log` (
  `id_log` bigint(20) NOT NULL AUTO_INCREMENT,
  `id_token` bigint(20) NOT NULL COMMENT 'fc_token',
  `tx_hash` varchar(255) NOT NULL,
  `block_hash` varchar(255) NOT NULL,
  `block_number` int(10) NOT NULL,
  `token_id` varchar(255) NOT NULL,
  `amount` int(11) NOT NULL,
  `tx_operator` varchar(255) NOT NULL,
  `tx_from` varchar(255) NOT NULL,
  `tx_to` varchar(255) NOT NULL,
  `tx_timestamp` datetime NOT NULL,
  `event_type` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id_log`)
) ENGINE=InnoDB AUTO_INCREMENT=43 DEFAULT CHARSET=utf8mb4;

--
-- Dump dei dati per la tabella `fc_log`
--

INSERT INTO `fc_log` (`id_log`, `id_token`, `tx_hash`, `block_hash`, `block_number`, `token_id`, `amount`, `tx_operator`, `tx_from`, `tx_to`, `tx_timestamp`, `event_type`) VALUES
(1, 1, '0x81dc5fb7c2141659bc8043c2356d5438fb853a31153f848be8d80153f3a6dfbd', '0xf2eb1d91fd7d82a771fa4635e55d77cdafd4e936d9dffe6d6b47860f29ca1da3', 10541668, '29520048689716280352655451354235906086059037734827535516925325694808021658944', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 15:21:40', 'TransferSingle'),
(2, 2, '0x67f2e2130bd5cd436b5459b8ec504fc9962f1b2d8f85513a6dffda15c8f03ca0', '0xfee1a58218b2538329f8b1ed1342612a9eb81cf06185d05a00f58bfcbf24b4e3', 10541740, '46403958275193458266975297881582994970520021456220028044114053020941229374379', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 15:35:26', 'TransferSingle'),
(3, 3, '0x582f40a6a5ddff666c87dca8562a26f9f0b326cfd5025bcb3794ff079caf3cf2', '0x5c033f0b0f384a11098ceeb2a98fafc919c68cfaf4b367b2c49a83e76953d245', 10541771, '79336648385410365718221376414228135944004813289083412245135142390765427722997', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 15:42:45', 'TransferSingle'),
(4, 4, '0x194a9c989f35e986e18a5fab1756f72dd5fb6c5c3484a663c1f7c2d9e87ac90d', '0x9c78b767b98031e209c00f0b4884f86f0978301685faee7350b8da8fa6487b4c', 10541791, '94339585643254216348620500034391771391757155786875423646154522240465928983675', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 15:45:07', 'TransferSingle'),
(5, 5, '0x36d388e46179d490077da773d1a58ade3f5d47bff6ac4a0eab88648afd31717c', '0x64995f9609e355147eef71f0ddd0372fde855206e03ea4377f3e169d520b6d84', 10573867, '76486783791243656012208814967027932960560090321128666753406343867175372756984', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-05 18:01:57', 'TransferSingle'),
(6, 5, '0xec811c9b4d6fe3f2c7587a7307c2fd457ec93f003ee0b41877b9341968cc8aa4', '0x51609a153eb288cd882c1093531a748996ac7e139a2e629e116b791a970b7b59', 10589148, '76486783791243656012208814967027932960560090321128666753406343867175372756984', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-07 16:19:57', 'TransferSingle'),
(7, 6, '0x0584f8b390a6c2ae4a6943c9ad7a7163c21f8283b79685138c6f783d5df2bb0f', '0x9eeb1526b47e6b298b3eed0126df652d714b44c0134a313e223808da522812d0', 10595652, '59628537338862633137897523508706990554735901209885757108007870196761780315620', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 15:48:58', 'TransferSingle'),
(8, 7, '0xa757064fc6107656138ff6dba1dcbb5506a881c58c208b399b095918a58a1303', '0x5ada0bf60a3a4db9bd6dd4ff9f1878d65bf8468b761b2a545c2a37d07f2695a1', 10541924, '44691560987565177768018343240706799101909759292502073093970653589710018405828', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 16:12:13', 'TransferBatch'),
(9, 8, '0xa757064fc6107656138ff6dba1dcbb5506a881c58c208b399b095918a58a1303', '0x5ada0bf60a3a4db9bd6dd4ff9f1878d65bf8468b761b2a545c2a37d07f2695a1', 10541924, '92819204267081540188982067660806543042242016655266119840127135856092316356222', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 16:12:13', 'TransferBatch'),
(10, 9, '0xa757064fc6107656138ff6dba1dcbb5506a881c58c208b399b095918a58a1303', '0x5ada0bf60a3a4db9bd6dd4ff9f1878d65bf8468b761b2a545c2a37d07f2695a1', 10541924, '9917659466536298446794062312245175793528370418676817912499887292631224652990', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-06-30 16:12:13', 'TransferBatch'),
(11, 10, '0xa73593e98e3ac7e803e8dc4579436971f1f88a22a7d3faa3497c94725d3c1d1c', '0x45cc109f7f7b5544f817eeb55c118fd7fbabdc9f6ef9ab6f08c1926f4501fc76', 10590015, '68207369123817625001555599539241369659383358356236813030960878673483118278103', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-07 19:15:34', 'TransferBatch'),
(12, 11, '0xa73593e98e3ac7e803e8dc4579436971f1f88a22a7d3faa3497c94725d3c1d1c', '0x45cc109f7f7b5544f817eeb55c118fd7fbabdc9f6ef9ab6f08c1926f4501fc76', 10590015, '113461546263921660958037388046824578982739146301890776277454934762464253232711', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-07 19:15:34', 'TransferBatch'),
(13, 12, '0xa73593e98e3ac7e803e8dc4579436971f1f88a22a7d3faa3497c94725d3c1d1c', '0x45cc109f7f7b5544f817eeb55c118fd7fbabdc9f6ef9ab6f08c1926f4501fc76', 10590015, '61714982739692458892444497324346722764108135837890174561614242560262475135232', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-07 19:15:34', 'TransferBatch'),
(14, 13, '0xa73593e98e3ac7e803e8dc4579436971f1f88a22a7d3faa3497c94725d3c1d1c', '0x45cc109f7f7b5544f817eeb55c118fd7fbabdc9f6ef9ab6f08c1926f4501fc76', 10590015, '67387105676195063506776420946239003302104130385533139627853270697508869802771', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-07 19:15:34', 'TransferBatch'),
(15, 14, '0xa73593e98e3ac7e803e8dc4579436971f1f88a22a7d3faa3497c94725d3c1d1c', '0x45cc109f7f7b5544f817eeb55c118fd7fbabdc9f6ef9ab6f08c1926f4501fc76', 10590015, '379734865057979698825482345394973482874517258978149569339456172654809491046', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-07 19:15:34', 'TransferBatch'),
(16, 15, '0xfd65f2dc580aa2ce70631f99b66fe1166f6d76b24b9fa08020a486f474be6658', '0x6a490902d5dfb6ac86b6c321d49b7fd1655ec1fa65573ed275b85b1d41e5be12', 10595655, '39403687621671783838434718685545471959377993794846510088180180341196147166887', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:49:26', 'TransferBatch'),
(17, 16, '0xfd65f2dc580aa2ce70631f99b66fe1166f6d76b24b9fa08020a486f474be6658', '0x6a490902d5dfb6ac86b6c321d49b7fd1655ec1fa65573ed275b85b1d41e5be12', 10595655, '79929879546080327845718549405307399522150133817094017281402572702486983471864', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:49:26', 'TransferBatch'),
(18, 17, '0xfd65f2dc580aa2ce70631f99b66fe1166f6d76b24b9fa08020a486f474be6658', '0x6a490902d5dfb6ac86b6c321d49b7fd1655ec1fa65573ed275b85b1d41e5be12', 10595655, '102280892599416758407260907247049242819853264117714286970998151223849001231454', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:49:26', 'TransferBatch'),
(19, 18, '0xfd65f2dc580aa2ce70631f99b66fe1166f6d76b24b9fa08020a486f474be6658', '0x6a490902d5dfb6ac86b6c321d49b7fd1655ec1fa65573ed275b85b1d41e5be12', 10595655, '621111636395968569115640768766919521439596801913586964102008047093634461178', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:49:26', 'TransferBatch'),
(20, 19, '0xfd65f2dc580aa2ce70631f99b66fe1166f6d76b24b9fa08020a486f474be6658', '0x6a490902d5dfb6ac86b6c321d49b7fd1655ec1fa65573ed275b85b1d41e5be12', 10595655, '103762585979216769164004350816322168495393069116299101210335708602427271626846', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:49:26', 'TransferBatch'),
(22, 10, '0x01b758fd78c290adc8cf158d7cdf4a7af097aff68bc52965568b93f17f93b72d', '0x5cc98ea4f634703e81bc718c7cc3afd3fcf2c08195b43aef295ef2fbec606524', 10595662, '68207369123817625001555599539241369659383358356236813030960878673483118278103', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 15:50:32', 'TransferSingle'),
(23, 6, '0xfdf7d9f2b9252f3533b3045bfd31067b145ec19fbe67ca87a8b901be7fd2f2c6', '0xef7801532b24d6e805ddee0b0c6637b1456791dea8faf4e1b7643e57a1d6d29a', 10596289, '59628537338862633137897523508706990554735901209885757108007870196761780315620', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:17:08', 'TransferSingle'),
(24, 6, '0xfdf7d9f2b9252f3533b3045bfd31067b145ec19fbe67ca87a8b901be7fd2f2c6', '0xc416cacd82a706058f0c94c83dc274f8c2d54b1b6d76169c7b53385d935ffb38', 10596362, '59628537338862633137897523508706990554735901209885757108007870196761780315620', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:30:37', 'TransferSingle'),
(25, 11, '0x64fbb6083b095e4f7dc43a87acfadafc194818d94f8c39d38bea99cc11c53d54', '0xc416cacd82a706058f0c94c83dc274f8c2d54b1b6d76169c7b53385d935ffb38', 10596362, '113461546263921660958037388046824578982739146301890776277454934762464253232711', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:30:37', 'TransferBatch'),
(26, 12, '0x64fbb6083b095e4f7dc43a87acfadafc194818d94f8c39d38bea99cc11c53d54', '0xc416cacd82a706058f0c94c83dc274f8c2d54b1b6d76169c7b53385d935ffb38', 10596362, '61714982739692458892444497324346722764108135837890174561614242560262475135232', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:30:37', 'TransferBatch'),
(27, 13, '0x64fbb6083b095e4f7dc43a87acfadafc194818d94f8c39d38bea99cc11c53d54', '0xc416cacd82a706058f0c94c83dc274f8c2d54b1b6d76169c7b53385d935ffb38', 10596362, '67387105676195063506776420946239003302104130385533139627853270697508869802771', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:30:37', 'TransferBatch'),
(28, 14, '0x64fbb6083b095e4f7dc43a87acfadafc194818d94f8c39d38bea99cc11c53d54', '0xc416cacd82a706058f0c94c83dc274f8c2d54b1b6d76169c7b53385d935ffb38', 10596362, '379734865057979698825482345394973482874517258978149569339456172654809491046', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:30:37', 'TransferBatch'),
(29, 20, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '88594346885302787206428348744589616694348807769768335884534742379297469215412', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(30, 21, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '100834585906866474431410651601466569766412670680260902444771195349009003029347', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(31, 22, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '72994382371736574271404598452973489833505648680440967853262047419644490443570', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(32, 23, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '45350273227700275683530240413010500956481267484310062543529124605517401362298', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(33, 24, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '58559991695657794089376372681270882890385466429153504022154533084862425283705', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(34, 25, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '51094161439103591862027316291816102668924684028902524853310483983549838627899', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(35, 26, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '15741366405863789537313422002736277372458671190981225557732374219485454895019', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(36, 27, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '48786324753365155480400259507667692383894936502366436409899355180163730249639', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(37, 28, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '93551216059337361168667490505594331547937607572822811006991432753890607865794', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(38, 29, '0x20e25d857b13e5875fb6c6e3c27d121ab96ead4c01f0460bad1d4fabc5f6d0e6', '0x6764f679dd6313424cfb0f3a176c9bb5c4c44c6af5ee820d90715527df69654c', 10596370, '76004341638415710030159929733995956945675288027951067967657890711734422569903', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x0000000000000000000000000000000000000000', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '2021-07-08 18:34:26', 'TransferBatch'),
(39, 20, '0xbc24f2a99cbdd1c5b479a914bce9c5d1d7cf01d6f2e65dd8193e2cbb9439208a', '0x0d867271d91d465914ef09d7064f79932c46d0cc332505b5eddc45c18b81d4af', 10596380, '88594346885302787206428348744589616694348807769768335884534742379297469215412', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:38:45', 'TransferBatch'),
(40, 21, '0xbc24f2a99cbdd1c5b479a914bce9c5d1d7cf01d6f2e65dd8193e2cbb9439208a', '0x0d867271d91d465914ef09d7064f79932c46d0cc332505b5eddc45c18b81d4af', 10596380, '100834585906866474431410651601466569766412670680260902444771195349009003029347', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:38:45', 'TransferBatch'),
(41, 22, '0xbc24f2a99cbdd1c5b479a914bce9c5d1d7cf01d6f2e65dd8193e2cbb9439208a', '0x0d867271d91d465914ef09d7064f79932c46d0cc332505b5eddc45c18b81d4af', 10596380, '72994382371736574271404598452973489833505648680440967853262047419644490443570', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:38:45', 'TransferBatch'),
(42, 23, '0x4294d006fb82615bab5e34faa8ff58db2c9575b1887eee5920b497825ad6403e', '0xf0475b28ca59c1978bd6b3f9ed16c6d098ea27bd732b4448d8b759895dfd1744', 10596386, '45350273227700275683530240413010500956481267484310062543529124605517401362298', 1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', '2021-07-08 18:40:56', 'TransferSingle');

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_personaldata`
--

DROP TABLE IF EXISTS `fc_personaldata`;
CREATE TABLE IF NOT EXISTS `fc_personaldata` (
  `id_personaldata` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_country` int(10) UNSIGNED NOT NULL COMMENT 'fc_country',
  `id_state` int(10) UNSIGNED DEFAULT NULL COMMENT 'fc_state',
  `lastname` varchar(255) NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `birthday` date DEFAULT NULL,
  `birthplace` varchar(255) NOT NULL,
  `address` varchar(128) NOT NULL,
  `postcode` varchar(12) DEFAULT NULL,
  `city` varchar(64) NOT NULL,
  `province` varchar(255) NOT NULL,
  `phone` varchar(32) DEFAULT NULL,
  `mobile` varchar(32) DEFAULT NULL,
  `fiscalcode` varchar(16) DEFAULT NULL,
  `company` varchar(255) DEFAULT NULL,
  `vatnumber` varchar(32) DEFAULT NULL,
  `date_add` datetime NOT NULL,
  `date_upd` datetime NOT NULL,
  PRIMARY KEY (`id_personaldata`) USING BTREE
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_personaldata`
--

INSERT INTO `fc_personaldata` (`id_personaldata`, `id_country`, `id_state`, `lastname`, `firstname`, `birthday`, `birthplace`, `address`, `postcode`, `city`, `province`, `phone`, `mobile`, `fiscalcode`, `company`, `vatnumber`, `date_add`, `date_upd`) VALUES
(1, 10, 149, 'Cammarano', 'Stefano', '1998-02-26', 'Salerno', 'Via Salerno, 1', '10000', 'Salerno', 'SA', NULL, NULL, 'CMMSTF98B26C478R', 'FinCode s.r.l.', '05842598548', '0000-00-00 00:00:00', '0000-00-00 00:00:00'),
(2, 10, 183, 'Pomposelli', 'Luca', '2021-06-01', 'Salerno', 'Via Campagna, 8', '40000', 'Campagna', 'SA', NULL, NULL, 'PNPLCA98C22C405R', 'Luca Pomposelli', '07584985265', '2021-06-30 11:30:34', '2021-06-30 11:30:34'),
(3, 10, 183, 'Monterisi', 'Riccardo', '1991-02-26', 'Cernusco S/N', 'Via Monte Grappa, 1', '20054', 'Segrate', 'MI', NULL, NULL, 'MNTRCR91B26C523R', 'Riccardo Monterisi', '08947050962', '2021-07-01 11:55:39', '2021-07-01 11:55:39');

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_state`
--

DROP TABLE IF EXISTS `fc_state`;
CREATE TABLE IF NOT EXISTS `fc_state` (
  `id_state` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_country` int(11) UNSIGNED NOT NULL,
  `name` varchar(64) NOT NULL,
  `iso_code` varchar(7) NOT NULL,
  `active` tinyint(1) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id_state`),
  KEY `id_country` (`id_country`),
  KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=353 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_state`
--

INSERT INTO `fc_state` (`id_state`, `id_country`, `name`, `iso_code`, `active`) VALUES
(1, 21, 'AA', 'AA', 1),
(2, 21, 'AE', 'AE', 1),
(3, 21, 'AP', 'AP', 1),
(4, 21, 'Alabama', 'AL', 1),
(5, 21, 'Alaska', 'AK', 1),
(6, 21, 'Arizona', 'AZ', 1),
(7, 21, 'Arkansas', 'AR', 1),
(8, 21, 'California', 'CA', 1),
(9, 21, 'Colorado', 'CO', 1),
(10, 21, 'Connecticut', 'CT', 1),
(11, 21, 'Delaware', 'DE', 1),
(12, 21, 'Florida', 'FL', 1),
(13, 21, 'Georgia', 'GA', 1),
(14, 21, 'Hawaii', 'HI', 1),
(15, 21, 'Idaho', 'ID', 1),
(16, 21, 'Illinois', 'IL', 1),
(17, 21, 'Indiana', 'IN', 1),
(18, 21, 'Iowa', 'IA', 1),
(19, 21, 'Kansas', 'KS', 1),
(20, 21, 'Kentucky', 'KY', 1),
(21, 21, 'Louisiana', 'LA', 1),
(22, 21, 'Maine', 'ME', 1),
(23, 21, 'Maryland', 'MD', 1),
(24, 21, 'Massachusetts', 'MA', 1),
(25, 21, 'Michigan', 'MI', 1),
(26, 21, 'Minnesota', 'MN', 1),
(27, 21, 'Mississippi', 'MS', 1),
(28, 21, 'Missouri', 'MO', 1),
(29, 21, 'Montana', 'MT', 1),
(30, 21, 'Nebraska', 'NE', 1),
(31, 21, 'Nevada', 'NV', 1),
(32, 21, 'New Hampshire', 'NH', 1),
(33, 21, 'New Jersey', 'NJ', 1),
(34, 21, 'New Mexico', 'NM', 1),
(35, 21, 'New York', 'NY', 1),
(36, 21, 'North Carolina', 'NC', 1),
(37, 21, 'North Dakota', 'ND', 1),
(38, 21, 'Ohio', 'OH', 1),
(39, 21, 'Oklahoma', 'OK', 1),
(40, 21, 'Oregon', 'OR', 1),
(41, 21, 'Pennsylvania', 'PA', 1),
(42, 21, 'Rhode Island', 'RI', 1),
(43, 21, 'South Carolina', 'SC', 1),
(44, 21, 'South Dakota', 'SD', 1),
(45, 21, 'Tennessee', 'TN', 1),
(46, 21, 'Texas', 'TX', 1),
(47, 21, 'Utah', 'UT', 1),
(48, 21, 'Vermont', 'VT', 1),
(49, 21, 'Virginia', 'VA', 1),
(50, 21, 'Washington', 'WA', 1),
(51, 21, 'West Virginia', 'WV', 1),
(52, 21, 'Wisconsin', 'WI', 1),
(53, 21, 'Wyoming', 'WY', 1),
(54, 21, 'Puerto Rico', 'PR', 1),
(55, 21, 'US Virgin Islands', 'VI', 1),
(56, 21, 'District of Columbia', 'DC', 1),
(57, 145, 'Aguascalientes', 'AGS', 1),
(58, 145, 'Baja California', 'BCN', 1),
(59, 145, 'Baja California Sur', 'BCS', 1),
(60, 145, 'Campeche', 'CAM', 1),
(61, 145, 'Chiapas', 'CHP', 1),
(62, 145, 'Chihuahua', 'CHH', 1),
(63, 145, 'Coahuila', 'COA', 1),
(64, 145, 'Colima', 'COL', 1),
(65, 145, 'Distrito Federal', 'DIF', 1),
(66, 145, 'Durango', 'DUR', 1),
(67, 145, 'Guanajuato', 'GUA', 1),
(68, 145, 'Guerrero', 'GRO', 1),
(69, 145, 'Hidalgo', 'HID', 1),
(70, 145, 'Jalisco', 'JAL', 1),
(71, 145, 'Estado de México', 'MEX', 1),
(72, 145, 'Michoacán', 'MIC', 1),
(73, 145, 'Morelos', 'MOR', 1),
(74, 145, 'Nayarit', 'NAY', 1),
(75, 145, 'Nuevo León', 'NLE', 1),
(76, 145, 'Oaxaca', 'OAX', 1),
(77, 145, 'Puebla', 'PUE', 1),
(78, 145, 'Querétaro', 'QUE', 1),
(79, 145, 'Quintana Roo', 'ROO', 1),
(80, 145, 'San Luis Potosí', 'SLP', 1),
(81, 145, 'Sinaloa', 'SIN', 1),
(82, 145, 'Sonora', 'SON', 1),
(83, 145, 'Tabasco', 'TAB', 1),
(84, 145, 'Tamaulipas', 'TAM', 1),
(85, 145, 'Tlaxcala', 'TLA', 1),
(86, 145, 'Veracruz', 'VER', 1),
(87, 145, 'Yucatán', 'YUC', 1),
(88, 145, 'Zacatecas', 'ZAC', 1),
(89, 4, 'Ontario', 'ON', 1),
(90, 4, 'Quebec', 'QC', 1),
(91, 4, 'British Columbia', 'BC', 1),
(92, 4, 'Alberta', 'AB', 1),
(93, 4, 'Manitoba', 'MB', 1),
(94, 4, 'Saskatchewan', 'SK', 1),
(95, 4, 'Nova Scotia', 'NS', 1),
(96, 4, 'New Brunswick', 'NB', 1),
(97, 4, 'Newfoundland and Labrador', 'NL', 1),
(98, 4, 'Prince Edward Island', 'PE', 1),
(99, 4, 'Northwest Territories', 'NT', 1),
(100, 4, 'Yukon', 'YT', 1),
(101, 4, 'Nunavut', 'NU', 1),
(102, 44, 'Buenos Aires', 'B', 1),
(103, 44, 'Catamarca', 'K', 1),
(104, 44, 'Chaco', 'H', 1),
(105, 44, 'Chubut', 'U', 1),
(106, 44, 'Ciudad de Buenos Aires', 'C', 1),
(107, 44, 'Córdoba', 'X', 1),
(108, 44, 'Corrientes', 'W', 1),
(109, 44, 'Entre Ríos', 'E', 1),
(110, 44, 'Formosa', 'P', 1),
(111, 44, 'Jujuy', 'Y', 1),
(112, 44, 'La Pampa', 'L', 1),
(113, 44, 'La Rioja', 'F', 1),
(114, 44, 'Mendoza', 'M', 1),
(115, 44, 'Misiones', 'N', 1),
(116, 44, 'Neuquén', 'Q', 1),
(117, 44, 'Río Negro', 'R', 1),
(118, 44, 'Salta', 'A', 1),
(119, 44, 'San Juan', 'J', 1),
(120, 44, 'San Luis', 'D', 1),
(121, 44, 'Santa Cruz', 'Z', 1),
(122, 44, 'Santa Fe', 'S', 1),
(123, 44, 'Santiago del Estero', 'G', 1),
(124, 44, 'Tierra del Fuego', 'V', 1),
(125, 44, 'Tucumán', 'T', 1),
(126, 10, 'Agrigento', 'AG', 1),
(127, 10, 'Alessandria', 'AL', 1),
(128, 10, 'Ancona', 'AN', 1),
(129, 10, 'Aosta', 'AO', 1),
(130, 10, 'Arezzo', 'AR', 1),
(131, 10, 'Ascoli Piceno', 'AP', 1),
(132, 10, 'Asti', 'AT', 1),
(133, 10, 'Avellino', 'AV', 1),
(134, 10, 'Bari', 'BA', 1),
(135, 10, 'Barletta-Andria-Trani', 'BT', 1),
(136, 10, 'Belluno', 'BL', 1),
(137, 10, 'Benevento', 'BN', 1),
(138, 10, 'Bergamo', 'BG', 1),
(139, 10, 'Biella', 'BI', 1),
(140, 10, 'Bologna', 'BO', 1),
(141, 10, 'Bolzano', 'BZ', 1),
(142, 10, 'Brescia', 'BS', 1),
(143, 10, 'Brindisi', 'BR', 1),
(144, 10, 'Cagliari', 'CA', 1),
(145, 10, 'Caltanissetta', 'CL', 1),
(146, 10, 'Campobasso', 'CB', 1),
(147, 10, 'Carbonia-Iglesias', 'CI', 1),
(148, 10, 'Caserta', 'CE', 1),
(149, 10, 'Catania', 'CT', 1),
(150, 10, 'Catanzaro', 'CZ', 1),
(151, 10, 'Chieti', 'CH', 1),
(152, 10, 'Como', 'CO', 1),
(153, 10, 'Cosenza', 'CS', 1),
(154, 10, 'Cremona', 'CR', 1),
(155, 10, 'Crotone', 'KR', 1),
(156, 10, 'Cuneo', 'CN', 1),
(157, 10, 'Enna', 'EN', 1),
(158, 10, 'Fermo', 'FM', 1),
(159, 10, 'Ferrara', 'FE', 1),
(160, 10, 'Firenze', 'FI', 1),
(161, 10, 'Foggia', 'FG', 1),
(162, 10, 'Forlì-Cesena', 'FC', 1),
(163, 10, 'Frosinone', 'FR', 1),
(164, 10, 'Genova', 'GE', 1),
(165, 10, 'Gorizia', 'GO', 1),
(166, 10, 'Grosseto', 'GR', 1),
(167, 10, 'Imperia', 'IM', 1),
(168, 10, 'Isernia', 'IS', 1),
(169, 10, 'L\'Aquila', 'AQ', 1),
(170, 10, 'La Spezia', 'SP', 1),
(171, 10, 'Latina', 'LT', 1),
(172, 10, 'Lecce', 'LE', 1),
(173, 10, 'Lecco', 'LC', 1),
(174, 10, 'Livorno', 'LI', 1),
(175, 10, 'Lodi', 'LO', 1),
(176, 10, 'Lucca', 'LU', 1),
(177, 10, 'Macerata', 'MC', 1),
(178, 10, 'Mantova', 'MN', 1),
(179, 10, 'Massa', 'MS', 1),
(180, 10, 'Matera', 'MT', 1),
(181, 10, 'Medio Campidano', 'VS', 1),
(182, 10, 'Messina', 'ME', 1),
(183, 10, 'Milano', 'MI', 1),
(184, 10, 'Modena', 'MO', 1),
(185, 10, 'Monza e della Brianza', 'MB', 1),
(186, 10, 'Napoli', 'NA', 1),
(187, 10, 'Novara', 'NO', 1),
(188, 10, 'Nuoro', 'NU', 1),
(189, 10, 'Ogliastra', 'OG', 1),
(190, 10, 'Olbia-Tempio', 'OT', 1),
(191, 10, 'Oristano', 'OR', 1),
(192, 10, 'Padova', 'PD', 1),
(193, 10, 'Palermo', 'PA', 1),
(194, 10, 'Parma', 'PR', 1),
(195, 10, 'Pavia', 'PV', 1),
(196, 10, 'Perugia', 'PG', 1),
(197, 10, 'Pesaro-Urbino', 'PU', 1),
(198, 10, 'Pescara', 'PE', 1),
(199, 10, 'Piacenza', 'PC', 1),
(200, 10, 'Pisa', 'PI', 1),
(201, 10, 'Pistoia', 'PT', 1),
(202, 10, 'Pordenone', 'PN', 1),
(203, 10, 'Potenza', 'PZ', 1),
(204, 10, 'Prato', 'PO', 1),
(205, 10, 'Ragusa', 'RG', 1),
(206, 10, 'Ravenna', 'RA', 1),
(207, 10, 'Reggio Calabria', 'RC', 1),
(208, 10, 'Reggio Emilia', 'RE', 1),
(209, 10, 'Rieti', 'RI', 1),
(210, 10, 'Rimini', 'RN', 1),
(211, 10, 'Roma', 'RM', 1),
(212, 10, 'Rovigo', 'RO', 1),
(213, 10, 'Salerno', 'SA', 1),
(214, 10, 'Sassari', 'SS', 1),
(215, 10, 'Savona', 'SV', 1),
(216, 10, 'Siena', 'SI', 1),
(217, 10, 'Siracusa', 'SR', 1),
(218, 10, 'Sondrio', 'SO', 1),
(219, 10, 'Taranto', 'TA', 1),
(220, 10, 'Teramo', 'TE', 1),
(221, 10, 'Terni', 'TR', 1),
(222, 10, 'Torino', 'TO', 1),
(223, 10, 'Trapani', 'TP', 1),
(224, 10, 'Trento', 'TN', 1),
(225, 10, 'Treviso', 'TV', 1),
(226, 10, 'Trieste', 'TS', 1),
(227, 10, 'Udine', 'UD', 1),
(228, 10, 'Varese', 'VA', 1),
(229, 10, 'Venezia', 'VE', 1),
(230, 10, 'Verbano-Cusio-Ossola', 'VB', 1),
(231, 10, 'Vercelli', 'VC', 1),
(232, 10, 'Verona', 'VR', 1),
(233, 10, 'Vibo Valentia', 'VV', 1),
(234, 10, 'Vicenza', 'VI', 1),
(235, 10, 'Viterbo', 'VT', 1),
(236, 111, 'Aceh', 'ID-AC', 1),
(237, 111, 'Bali', 'ID-BA', 1),
(238, 111, 'Banten', 'ID-BT', 1),
(239, 111, 'Bengkulu', 'ID-BE', 1),
(240, 111, 'Gorontalo', 'ID-GO', 1),
(241, 111, 'Jakarta', 'ID-JK', 1),
(242, 111, 'Jambi', 'ID-JA', 1),
(243, 111, 'Jawa Barat', 'ID-JB', 1),
(244, 111, 'Jawa Tengah', 'ID-JT', 1),
(245, 111, 'Jawa Timur', 'ID-JI', 1),
(246, 111, 'Kalimantan Barat', 'ID-KB', 1),
(247, 111, 'Kalimantan Selatan', 'ID-KS', 1),
(248, 111, 'Kalimantan Tengah', 'ID-KT', 1),
(249, 111, 'Kalimantan Timur', 'ID-KI', 1),
(250, 111, 'Kalimantan Utara', 'ID-KU', 1),
(251, 111, 'Kepulauan Bangka Belitug', 'ID-BB', 1),
(252, 111, 'Kepulauan Riau', 'ID-KR', 1),
(253, 111, 'Lampung', 'ID-LA', 1),
(254, 111, 'Maluku', 'ID-MA', 1),
(255, 111, 'Maluku Utara', 'ID-MU', 1),
(256, 111, 'Nusa Tengara Barat', 'ID-NB', 1),
(257, 111, 'Nusa Tenggara Timur', 'ID-NT', 1),
(258, 111, 'Papua', 'ID-PA', 1),
(259, 111, 'Papua Barat', 'ID-PB', 1),
(260, 111, 'Riau', 'ID-RI', 1),
(261, 111, 'Sulawesi Barat', 'ID-SR', 1),
(262, 111, 'Sulawesi Selatan', 'ID-SN', 1),
(263, 111, 'Sulawesi Tengah', 'ID-ST', 1),
(264, 111, 'Sulawesi Tenggara', 'ID-SG', 1),
(265, 111, 'Sulawesi Utara', 'ID-SA', 1),
(266, 111, 'Sumatera Barat', 'ID-SB', 1),
(267, 111, 'Sumatera Selatan', 'ID-SS', 1),
(268, 111, 'Sumatera Utara', 'ID-SU', 1),
(269, 111, 'Yogyakarta', 'ID-YO', 1),
(270, 11, 'Aichi', '23', 1),
(271, 11, 'Akita', '05', 1),
(272, 11, 'Aomori', '02', 1),
(273, 11, 'Chiba', '12', 1),
(274, 11, 'Ehime', '38', 1),
(275, 11, 'Fukui', '18', 1),
(276, 11, 'Fukuoka', '40', 1),
(277, 11, 'Fukushima', '07', 1),
(278, 11, 'Gifu', '21', 1),
(279, 11, 'Gunma', '10', 1),
(280, 11, 'Hiroshima', '34', 1),
(281, 11, 'Hokkaido', '01', 1),
(282, 11, 'Hyogo', '28', 1),
(283, 11, 'Ibaraki', '08', 1),
(284, 11, 'Ishikawa', '17', 1),
(285, 11, 'Iwate', '03', 1),
(286, 11, 'Kagawa', '37', 1),
(287, 11, 'Kagoshima', '46', 1),
(288, 11, 'Kanagawa', '14', 1),
(289, 11, 'Kochi', '39', 1),
(290, 11, 'Kumamoto', '43', 1),
(291, 11, 'Kyoto', '26', 1),
(292, 11, 'Mie', '24', 1),
(293, 11, 'Miyagi', '04', 1),
(294, 11, 'Miyazaki', '45', 1),
(295, 11, 'Nagano', '20', 1),
(296, 11, 'Nagasaki', '42', 1),
(297, 11, 'Nara', '29', 1),
(298, 11, 'Niigata', '15', 1),
(299, 11, 'Oita', '44', 1),
(300, 11, 'Okayama', '33', 1),
(301, 11, 'Okinawa', '47', 1),
(302, 11, 'Osaka', '27', 1),
(303, 11, 'Saga', '41', 1),
(304, 11, 'Saitama', '11', 1),
(305, 11, 'Shiga', '25', 1),
(306, 11, 'Shimane', '32', 1),
(307, 11, 'Shizuoka', '22', 1),
(308, 11, 'Tochigi', '09', 1),
(309, 11, 'Tokushima', '36', 1),
(310, 11, 'Tokyo', '13', 1),
(311, 11, 'Tottori', '31', 1),
(312, 11, 'Toyama', '16', 1),
(313, 11, 'Wakayama', '30', 1),
(314, 11, 'Yamagata', '06', 1),
(315, 11, 'Yamaguchi', '35', 1),
(316, 11, 'Yamanashi', '19', 1),
(317, 24, 'Australian Capital Territory', 'ACT', 1),
(318, 24, 'New South Wales', 'NSW', 1),
(319, 24, 'Northern Territory', 'NT', 1),
(320, 24, 'Queensland', 'QLD', 1),
(321, 24, 'South Australia', 'SA', 1),
(322, 24, 'Tasmania', 'TAS', 1),
(323, 24, 'Victoria', 'VIC', 1),
(324, 24, 'Western Australia', 'WA', 1),
(325, 110, 'Andhra Pradesh', 'AP', 1),
(326, 110, 'Arunachal Pradesh', 'AR', 1),
(327, 110, 'Assam', 'AS', 1),
(328, 110, 'Bihar', 'BR', 1),
(329, 110, 'Chhattisgarh', 'CT', 1),
(330, 110, 'Goa', 'GA', 1),
(331, 110, 'Gujarat', 'GJ', 1),
(332, 110, 'Haryana', 'HR', 1),
(333, 110, 'Himachal Pradesh', 'HP', 1),
(334, 110, 'Jharkhand', 'JH', 1),
(335, 110, 'Karnataka', 'KA', 1),
(336, 110, 'Kerala', 'KL', 1),
(337, 110, 'Madhya Pradesh', 'MP', 1),
(338, 110, 'Maharashtra', 'MH', 1),
(339, 110, 'Manipur', 'MN', 1),
(340, 110, 'Meghalaya', 'ML', 1),
(341, 110, 'Mizoram', 'MZ', 1),
(342, 110, 'Nagaland', 'NL', 1),
(343, 110, 'Odisha', 'OR', 1),
(344, 110, 'Punjab', 'PB', 1),
(345, 110, 'Rajasthan', 'RJ', 1),
(346, 110, 'Sikkim', 'SK', 1),
(347, 110, 'Tamil Nadu', 'TN', 1),
(348, 110, 'Telangana', 'TG', 1),
(349, 110, 'Tripura', 'TR', 1),
(350, 110, 'Uttar Pradesh', 'UP', 1),
(351, 110, 'Uttarakhand', 'UT', 1),
(352, 110, 'West Bengal', 'WB', 1);

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_token`
--

DROP TABLE IF EXISTS `fc_token`;
CREATE TABLE IF NOT EXISTS `fc_token` (
  `id_token` bigint(20) UNSIGNED NOT NULL AUTO_INCREMENT,
  `id_wallet` int(10) UNSIGNED NOT NULL COMMENT 'fc_wallet',
  `id_contract` int(10) UNSIGNED NOT NULL DEFAULT 1,
  `token_id` varchar(255) NOT NULL,
  `serial_number` bigint(20) UNSIGNED NOT NULL,
  `burned` tinyint(1) NOT NULL DEFAULT 0,
  `date_add` datetime NOT NULL DEFAULT current_timestamp(),
  `date_burn` datetime DEFAULT NULL,
  PRIMARY KEY (`id_token`),
  UNIQUE KEY `data` (`token_id`)
) ENGINE=InnoDB AUTO_INCREMENT=30 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_token`
--

INSERT INTO `fc_token` (`id_token`, `id_wallet`, `id_contract`, `token_id`, `serial_number`, `burned`, `date_add`, `date_burn`) VALUES
(1, 2, 1, '29520048689716280352655451354235906086059037734827535516925325694808021658944', 1, 0, '2021-06-30 15:21:40', NULL),
(2, 2, 1, '46403958275193458266975297881582994970520021456220028044114053020941229374379', 2, 0, '2021-06-30 15:35:26', NULL),
(3, 2, 1, '79336648385410365718221376414228135944004813289083412245135142390765427722997', 3, 0, '2021-06-30 15:42:45', NULL),
(4, 2, 1, '94339585643254216348620500034391771391757155786875423646154522240465928983675', 4, 0, '2021-06-30 15:45:07', NULL),
(5, 2, 1, '76486783791243656012208814967027932960560090321128666753406343867175372756984', 5, 0, '2021-07-05 18:01:57', NULL),
(6, 2, 1, '59628537338862633137897523508706990554735901209885757108007870196761780315620', 6, 0, '2021-07-08 15:48:58', NULL),
(7, 2, 1, '44691560987565177768018343240706799101909759292502073093970653589710018405828', 7, 0, '2021-06-30 16:12:13', NULL),
(8, 2, 1, '92819204267081540188982067660806543042242016655266119840127135856092316356222', 8, 0, '2021-06-30 16:12:13', NULL),
(9, 2, 1, '9917659466536298446794062312245175793528370418676817912499887292631224652990', 9, 0, '2021-06-30 16:12:13', NULL),
(10, 2, 1, '68207369123817625001555599539241369659383358356236813030960878673483118278103', 10, 0, '2021-07-07 19:15:34', NULL),
(11, 2, 1, '113461546263921660958037388046824578982739146301890776277454934762464253232711', 11, 0, '2021-07-07 19:15:34', NULL),
(12, 2, 1, '61714982739692458892444497324346722764108135837890174561614242560262475135232', 12, 0, '2021-07-07 19:15:34', NULL),
(13, 2, 1, '67387105676195063506776420946239003302104130385533139627853270697508869802771', 27, 1, '2021-07-07 19:15:34', NULL),
(14, 2, 1, '379734865057979698825482345394973482874517258978149569339456172654809491046', 14, 0, '2021-07-07 19:15:34', NULL),
(15, 2, 1, '39403687621671783838434718685545471959377993794846510088180180341196147166887', 15, 0, '2021-07-08 15:49:26', NULL),
(16, 2, 1, '79929879546080327845718549405307399522150133817094017281402572702486983471864', 16, 0, '2021-07-08 15:49:26', NULL),
(17, 2, 1, '102280892599416758407260907247049242819853264117714286970998151223849001231454', 17, 0, '2021-07-08 15:49:26', NULL),
(18, 2, 1, '621111636395968569115640768766919521439596801913586964102008047093634461178', 18, 0, '2021-07-08 15:49:26', NULL),
(19, 2, 1, '103762585979216769164004350816322168495393069116299101210335708602427271626846', 19, 0, '2021-07-08 15:49:26', NULL),
(20, 2, 1, '88594346885302787206428348744589616694348807769768335884534742379297469215412', 20, 0, '2021-07-08 18:34:26', NULL),
(21, 2, 1, '100834585906866474431410651601466569766412670680260902444771195349009003029347', 21, 0, '2021-07-08 18:34:26', NULL),
(22, 2, 1, '72994382371736574271404598452973489833505648680440967853262047419644490443570', 22, 0, '2021-07-08 18:34:26', NULL),
(23, 2, 1, '45350273227700275683530240413010500956481267484310062543529124605517401362298', 23, 1, '2021-07-08 18:34:26', NULL),
(24, 1, 1, '58559991695657794089376372681270882890385466429153504022154533084862425283705', 24, 1, '2021-07-08 18:34:26', NULL),
(25, 1, 1, '51094161439103591862027316291816102668924684028902524853310483983549838627899', 25, 0, '2021-07-08 18:34:26', NULL),
(26, 1, 1, '15741366405863789537313422002736277372458671190981225557732374219485454895019', 26, 0, '2021-07-08 18:34:26', NULL),
(27, 1, 1, '48786324753365155480400259507667692383894936502366436409899355180163730249639', 27, 0, '2021-07-08 18:34:26', NULL),
(28, 1, 1, '93551216059337361168667490505594331547937607572822811006991432753890607865794', 28, 0, '2021-07-08 18:34:26', NULL),
(29, 1, 1, '76004341638415710030159929733995956945675288027951067967657890711734422569903', 29, 0, '2021-07-08 18:34:26', NULL);

-- --------------------------------------------------------

--
-- Struttura della tabella `fc_wallet`
--

DROP TABLE IF EXISTS `fc_wallet`;
CREATE TABLE IF NOT EXISTS `fc_wallet` (
  `id_wallet` int(10) UNSIGNED NOT NULL AUTO_INCREMENT,
  `public_key` varchar(256) NOT NULL,
  `private_key` varchar(256) DEFAULT NULL,
  `active` tinyint(1) UNSIGNED NOT NULL DEFAULT 0,
  `date_add` datetime NOT NULL,
  PRIMARY KEY (`id_wallet`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8;

--
-- Dump dei dati per la tabella `fc_wallet`
--

INSERT INTO `fc_wallet` (`id_wallet`, `public_key`, `private_key`, `active`, `date_add`) VALUES
(1, '0xc679D778B948dC9e605F55438e3017f55Bfbbcd1', NULL, 1, '2021-06-25 16:38:47'),
(2, '0x2DD72D6840986dDf46d7e44db2BDa0bd530e9Ad0', NULL, 1, '2021-07-01 11:57:20');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
