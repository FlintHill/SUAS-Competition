-- phpMyAdmin SQL Dump
-- version 4.7.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: May 09, 2017 at 12:35 PM
-- Server version: 5.7.18-log
-- PHP Version: 7.1.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `tile`
--

-- --------------------------------------------------------

--
-- Table structure for table `defaults`
--

CREATE TABLE `defaults` (
  `id` int(11) NOT NULL,
  `description` text NOT NULL,
  `sha1` text NOT NULL COMMENT 'Hash',
  `image` blob NOT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8 COMMENT='Images that are often repeated are enumerated here';

--
-- Dumping data for table `defaults`
--

INSERT INTO `defaults` (`id`, `description`, `sha1`, `image`) VALUES
(0, 'ocean', 'c9bc878a43ceba4bb9367aabf87db2f32f1c0789', 0x89504e470d0a1a0a0000000d494844520000010000000100010300000066bc3a2500000003504c5445b5d0d0630416ea0000001f494441546881edc1010d000000c2a0f74f6d0e37a00000000000000000be0d210000019a60e1d50000000049454e44ae426082),
(1, 'empty land', 'c226ca747874fb1307eef853feaf9d8db28cef2b', 0x89504e470d0a1a0a0000000d494844520000010000000100010300000066bc3a2500000003504c5445f2efe9110a2f9b0000001f494441546881edc1010d000000c2a0f74f6d0e37a00000000000000000be0d210000019a60e1d50000000049454e44ae426082);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `defaults`
--
ALTER TABLE `defaults`
  ADD PRIMARY KEY (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
