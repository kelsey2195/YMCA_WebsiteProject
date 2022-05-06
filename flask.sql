-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: May 06, 2022 at 01:55 PM
-- Server version: 10.4.22-MariaDB
-- PHP Version: 8.0.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `flask`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts`
--

CREATE TABLE `accounts` (
  `account_id` int(11) NOT NULL,
  `associated_user` varchar(255) NOT NULL,
  `account_first_name` varchar(255) NOT NULL,
  `account_last_name` varchar(255) NOT NULL,
  `account_birth_day` date NOT NULL,
  `active` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `associated_user`, `account_first_name`, `account_last_name`, `account_birth_day`, `active`) VALUES
(1000005, 'doe@anonmail.com', 'Jane', 'Doe', '1999-01-06', 1),
(1000007, 'ander@gmail.com', 'Luke', 'Anderson', '2010-02-18', 1),
(1000008, 'ander@gmail.com', 'Aini', 'Anderson', '2012-05-23', 1);

-- --------------------------------------------------------

--
-- Table structure for table `account_in_program`
--

CREATE TABLE `account_in_program` (
  `account_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `account_in_program`
--

INSERT INTO `account_in_program` (`account_id`, `program_id`) VALUES
(1000005, 19),
(1000005, 22),
(1000007, 20),
(1000007, 21),
(1000008, 22);

-- --------------------------------------------------------

--
-- Table structure for table `employees`
--

CREATE TABLE `employees` (
  `employee_id` int(11) NOT NULL,
  `employee_first_name` varchar(255) NOT NULL,
  `employee_last_name` varchar(255) NOT NULL,
  `employee_password` varchar(255) NOT NULL,
  `manager_or_not` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `employees`
--

INSERT INTO `employees` (`employee_id`, `employee_first_name`, `employee_last_name`, `employee_password`, `manager_or_not`) VALUES
(1000000, 'Manny', 'Geer', 'manpass', 1),
(1000001, 'Piere', 'Hellman', 'helper', 0),
(1000002, 'Cooper', 'Ramos', '1234', 0);

-- --------------------------------------------------------

--
-- Table structure for table `programs`
--

CREATE TABLE `programs` (
  `program_id` int(11) NOT NULL,
  `name_program` varchar(255) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `location` varchar(255) NOT NULL,
  `description` varchar(9999) NOT NULL,
  `min_swim_level` varchar(255) DEFAULT NULL,
  `member_price` int(11) NOT NULL,
  `nonmember_price` int(11) NOT NULL,
  `num_total_people` int(11) NOT NULL,
  `num_signed_up` int(11) NOT NULL,
  `active` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `programs`
--

INSERT INTO `programs` (`program_id`, `name_program`, `start_date`, `end_date`, `location`, `description`, `min_swim_level`, `member_price`, `nonmember_price`, `num_total_people`, `num_signed_up`, `active`) VALUES
(19, 'Shark', '2022-05-22', '2022-06-26', 'YMCA Onalaska pool', 'Participants must have passed pike level before.', 'Pike', 48, 96, 8, 0, 1),
(20, 'Shark', '2022-05-22', '2022-06-26', 'YMCA Onalaska pool', 'Participants must have passed pike level before.', 'Pike', 65, 130, 8, 0, 1),
(21, 'Log Rolling', '2022-05-22', '2022-05-26', 'YMCA Onalaska pool', 'Log Rolling', 'N/A', 100, 200, 1, 0, 1),
(22, 'Log Rolling', '2022-05-22', '2022-06-26', 'YMCA Onalaska pool', 'Log Rolling', 'N/A', 100, 200, 1, 0, 1);

-- --------------------------------------------------------

--
-- Table structure for table `program_schedule`
--

CREATE TABLE `program_schedule` (
  `program_id` int(11) NOT NULL,
  `day_of_week` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `program_schedule`
--

INSERT INTO `program_schedule` (`program_id`, `day_of_week`, `start_time`, `end_time`) VALUES
(19, 0, '17:00:00', '17:40:00'),
(20, 1, '18:00:00', '18:40:00'),
(20, 3, '18:00:00', '18:40:00'),
(21, 0, '17:00:00', '17:40:00'),
(22, 1, '18:00:00', '18:40:00');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `mem_display_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `member_or_not` tinyint(1) NOT NULL DEFAULT 0,
  `active` int(11) NOT NULL DEFAULT 1
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`email`, `mem_display_name`, `password`, `member_or_not`, `active`) VALUES
('ander@gmail.com', 'Andersons', 'password', 1, 1),
('doe@anonmail.com', 'DoeDoe', 'password', 1, 1);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts`
--
ALTER TABLE `accounts`
  ADD PRIMARY KEY (`account_id`);

--
-- Indexes for table `employees`
--
ALTER TABLE `employees`
  ADD PRIMARY KEY (`employee_id`);

--
-- Indexes for table `programs`
--
ALTER TABLE `programs`
  ADD PRIMARY KEY (`program_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`email`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts`
--
ALTER TABLE `accounts`
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1000009;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1000003;

--
-- AUTO_INCREMENT for table `programs`
--
ALTER TABLE `programs`
  MODIFY `program_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
