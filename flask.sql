-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 13, 2022 at 05:21 AM
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
  `account_level` int(11) NOT NULL,
  `account_birth_day` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `accounts`
--

INSERT INTO `accounts` (`account_id`, `associated_user`, `account_first_name`, `account_last_name`, `account_level`, `account_birth_day`) VALUES
(1000000, 'test@abc.com', 'Micheal', 'Ross', 1, '2002-04-01'),
(1000002, 'NEWACC@ill.com', 'Prop', 'Bear', 1, '2022-04-01');

-- --------------------------------------------------------

--
-- Table structure for table `account_in_program`
--

CREATE TABLE `account_in_program` (
  `account_id` int(11) NOT NULL,
  `program_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

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
  `description` varchar(9999) NOT NULL,
  `min_swim_level` int(11) DEFAULT NULL,
  `member_price` int(11) NOT NULL,
  `nonmember_price` int(11) NOT NULL,
  `num_total_people` int(11) NOT NULL,
  `num_signed_up` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `program_schedule`
--

CREATE TABLE `program_schedule` (
  `program_id` int(11) NOT NULL,
  `day_of_week` int(11) NOT NULL,
  `program_time_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `program_time`
--

CREATE TABLE `program_time` (
  `program_time_id` int(11) NOT NULL,
  `start_time` time NOT NULL,
  `end_time` time NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `swim_levels`
--

CREATE TABLE `swim_levels` (
  `swim_level_id` int(11) NOT NULL,
  `swim_level_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `swim_levels`
--

INSERT INTO `swim_levels` (`swim_level_id`, `swim_level_name`) VALUES
(0, 'adult'),
(1, 'Polliwog'),
(2, 'Guppy'),
(3, 'Minnow'),
(4, 'Fish'),
(5, 'Pike'),
(6, 'Shark');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `email` varchar(255) NOT NULL,
  `mem_display_name` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `member_or_not` tinyint(1) NOT NULL DEFAULT 0
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`email`, `mem_display_name`, `password`, `member_or_not`) VALUES
('email@email.com', 'newUser', 'pass', 0),
('NEWACC@ill.com', 'newAccU', 'pass', 0);

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
-- Indexes for table `program_time`
--
ALTER TABLE `program_time`
  ADD PRIMARY KEY (`program_time_id`);

--
-- Indexes for table `swim_levels`
--
ALTER TABLE `swim_levels`
  ADD PRIMARY KEY (`swim_level_id`);

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
  MODIFY `account_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1000003;

--
-- AUTO_INCREMENT for table `employees`
--
ALTER TABLE `employees`
  MODIFY `employee_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1000003;

--
-- AUTO_INCREMENT for table `programs`
--
ALTER TABLE `programs`
  MODIFY `program_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `program_time`
--
ALTER TABLE `program_time`
  MODIFY `program_time_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `swim_levels`
--
ALTER TABLE `swim_levels`
  MODIFY `swim_level_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
