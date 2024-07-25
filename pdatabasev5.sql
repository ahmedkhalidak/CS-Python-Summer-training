-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jul 25, 2024 at 08:27 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `pdatabasev5`
--

-- --------------------------------------------------------

--
-- Table structure for table `add_stuff`
--

CREATE TABLE `add_stuff` (
  `SName` varchar(30) NOT NULL,
  `role` varchar(4) NOT NULL,
  `SEmail` varchar(30) NOT NULL,
  `SID` int(11) NOT NULL,
  `section` int(2) NOT NULL,
  `level` int(2) NOT NULL,
  `subject` varchar(10) NOT NULL,
  `department` varchar(15) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `add_stuff`
--

INSERT INTO `add_stuff` (`SName`, `role`, `SEmail`, `SID`, `section`, `level`, `subject`, `department`) VALUES
('Osama', 'Dr', 'osama34@gmail.com', 5, 2, 3, 'OOP', 'CS'),
('Mohammed', 'TA', 'mohammed326@mail.ru', 10, 3, 1, 'python', 'IS'),
('gg', 'TA', 'gg', 12, 0, 0, '', '');

-- --------------------------------------------------------

--
-- Table structure for table `load_data`
--

CREATE TABLE `load_data` (
  `name` varchar(20) NOT NULL,
  `type` varchar(5) NOT NULL,
  `section` int(2) NOT NULL,
  `level` int(2) NOT NULL,
  `subject` varchar(20) NOT NULL,
  `Department` varchar(30) NOT NULL,
  `id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `load_data`
--

INSERT INTO `load_data` (`name`, `type`, `section`, `level`, `subject`, `Department`, `id`) VALUES
('mohammed', 'TA', 1, 1, '1', '1', 24),
('mohammed', 'TA', 1, 1, '1', '1', 25),
('mohammed', 'TA', 1, 1, '1', '1', 26),
('ahmed', 'DR', 1, 1, '1', '1', 29);

-- --------------------------------------------------------

--
-- Table structure for table `location`
--

CREATE TABLE `location` (
  `ID` int(11) NOT NULL,
  `type` varchar(10) NOT NULL,
  `number` int(11) NOT NULL,
  `capacity` int(11) NOT NULL,
  `building` varchar(1) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `location`
--

INSERT INTO `location` (`ID`, `type`, `number`, `capacity`, `building`) VALUES
(9, 'Room', 1, 50, 'B'),
(10, 'Room', 3, 3, 'A');

-- --------------------------------------------------------

--
-- Table structure for table `login`
--

CREATE TABLE `login` (
  `ID` int(11) NOT NULL,
  `UName` varchar(30) NOT NULL,
  `Pass` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `login`
--

INSERT INTO `login` (`ID`, `UName`, `Pass`) VALUES
(1, 'Ahmed', 123456),
(2, 'khalid', 123456);

-- --------------------------------------------------------

--
-- Table structure for table `staff_info`
--

CREATE TABLE `staff_info` (
  `position` varchar(3) NOT NULL,
  `name` varchar(50) NOT NULL,
  `department` varchar(30) NOT NULL,
  `level` int(5) NOT NULL,
  `subject` varchar(50) NOT NULL,
  `sections` int(15) NOT NULL,
  `email` varchar(50) NOT NULL,
  `id` int(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `staff_info`
--

INSERT INTO `staff_info` (`position`, `name`, `department`, `level`, `subject`, `sections`, `email`, `id`) VALUES
('DR', 'Ahmed', 'CS', 1, 'OOP', 2, 'ahmed987@gmail.com', 1),
('TA', 'Mohammed', 'IS', 3, 'python', 1, 'mohammed434@mail.ru', 2),
('TA', 'Osama', 'SWE', 4, 'algorithm', 5, 'Osama33@edu.eg', 3),
('DR', 'Omar', 'AI', 3, 'math1', 7, 'Omar.55@yandex.com', 4),
('DR', 'Omar', 'CS', 2, 'math2', 4, '', 24);

-- --------------------------------------------------------

--
-- Table structure for table `subject`
--

CREATE TABLE `subject` (
  `Name` varchar(30) NOT NULL,
  `Code` varchar(30) NOT NULL,
  `Level` int(30) NOT NULL,
  `Department` varchar(30) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `add_stuff`
--
ALTER TABLE `add_stuff`
  ADD PRIMARY KEY (`SID`);

--
-- Indexes for table `load_data`
--
ALTER TABLE `load_data`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `location`
--
ALTER TABLE `location`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `login`
--
ALTER TABLE `login`
  ADD PRIMARY KEY (`ID`);

--
-- Indexes for table `staff_info`
--
ALTER TABLE `staff_info`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `subject`
--
ALTER TABLE `subject`
  ADD PRIMARY KEY (`Code`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `add_stuff`
--
ALTER TABLE `add_stuff`
  MODIFY `SID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `load_data`
--
ALTER TABLE `load_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- AUTO_INCREMENT for table `location`
--
ALTER TABLE `location`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `login`
--
ALTER TABLE `login`
  MODIFY `ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `staff_info`
--
ALTER TABLE `staff_info`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
