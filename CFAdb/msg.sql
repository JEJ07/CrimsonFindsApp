-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 03, 2024 at 07:04 AM
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
-- Database: `msg`
--

-- --------------------------------------------------------

--
-- Table structure for table `items`
--

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL,
  `image` varchar(255) DEFAULT NULL,
  `title` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `location` varchar(100) DEFAULT NULL,
  `date` date DEFAULT NULL,
  `item_type` enum('LOST','FOUND','CLAIMED') NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `claimed_by` int(11) DEFAULT NULL,
  `status` enum('available','already claimed') DEFAULT 'available',
  `claimed_date` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `items`
--

INSERT INTO `items` (`item_id`, `image`, `title`, `description`, `location`, `date`, `item_type`, `user_id`, `claimed_by`, `status`, `claimed_date`) VALUES
(2, 'C:\\Users\\MSi\\OneDrive\\Desktop\\onedrive desktop\\APPDEVPROJECT\\loweffort\\img\\raviel.jpg', 'missing wife', 'nawala last yr', 'earth', '2024-02-15', 'LOST', NULL, NULL, 'available', NULL),
(3, 'C:\\Users\\MSi\\OneDrive\\Desktop\\onedrive desktop\\APPDEVPROJECT\\loweffort\\img\\kaorukosmol.jpg', 'MISSING GF', 'kaoruko where r u', 'zamboanga', '2024-01-05', 'LOST', 5, NULL, 'available', NULL),
(4, 'C:/Users/MSi/OneDrive/Desktop/Crimsonfindsappmsgdb/products\\FzqwqioaEAEg6Hk.jpg', 'Fami', 'nawawala', 'chainsawman', '2024-01-07', 'LOST', 5, NULL, 'available', NULL),
(5, 'C:/Users/MSi/OneDrive/Desktop/Crimsonfindsappmsgdb/products\\guard_by_wlop_d9kmnxu-pre.jpg', 'Knight in shining armor', 'wala lang trip ko lang na pic', 'venus', '2024-02-11', 'FOUND', 2, 1, 'already claimed', '2024-11-02 00:29:17'),
(6, 'C:/Users/MSi/OneDrive/Desktop/Crimsonfindsappmsgdb/products\\sk.png', 'Shorekeeper', 'WUWA SHOREKEEPER', 'Wuthering WAVES', '2024-05-14', 'FOUND', 2, NULL, 'available', NULL),
(7, 'C:/Users/MSi/OneDrive/Desktop/Crimsonfindsappmsgdb/products\\lost-items.png', 'Box', 'big mystery box', 'field', '2024-07-25', 'LOST', 2, 3, 'already claimed', '2024-11-02 00:24:36'),
(8, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\raviel.jpg', 'Raviel MISSING', 'bat to wala', 'earth', '2024-02-05', 'LOST', 3, 2, 'already claimed', '2024-11-02 00:15:54'),
(9, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\bag.jpg', 'Bag', 'Pink color', 'CR', '2024-11-02', 'LOST', 2, 6, 'already claimed', '2024-11-02 01:39:55'),
(10, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\laptop.jpg', 'Laptop', 'color black', 'CCS', '2024-05-05', 'LOST', 2, NULL, 'available', NULL),
(11, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\susi.jpg', 'Keys', 'Nahulog sa canteen', 'bulsa ko', '2024-01-15', 'LOST', 6, 7, 'already claimed', '2024-11-02 00:35:14'),
(12, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\iphone.jpg', 'Iphone', 'color pink', 'gym', '2024-11-20', 'LOST', 7, 6, 'already claimed', '2024-11-02 01:33:42'),
(14, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\ccslogo.jpg', 'CCS LOGO', 'missing logo', 'campus b', '2024-10-05', 'LOST', 7, 6, 'already claimed', '2024-11-02 01:43:16'),
(15, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\F1SBfrwaYAAZ6hv.jpg', 'Wawi', 'haaalaaa', 'earth', '2024-11-09', 'LOST', 3, NULL, 'available', NULL),
(16, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\minifan.jpg', 'Minifan', 'minifan found', 'canteen', '2024-11-06', 'FOUND', 3, NULL, 'available', NULL),
(17, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\gtech.jpg', 'GTech', 'mamahaling ballpen', 'CLA', '2024-11-20', 'LOST', 8, 7, 'already claimed', '2024-11-03 02:30:41'),
(18, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\toblerone.jpg', 'Toblerone', 'paexpired na', 'CLA', '2024-11-27', 'FOUND', 8, NULL, 'available', NULL),
(19, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\coke.jpg', 'Coke', 'penge', 'gate', '2024-11-19', 'FOUND', 3, NULL, 'available', NULL),
(20, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\piattos.jpg', 'Piattos', 'kakabili ko lang nawala agad', 'canteen', '2024-11-11', 'LOST', 3, NULL, 'available', NULL),
(21, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\earphones.jpg', 'earphones', 'brandnew', 'CR', '2024-11-27', 'FOUND', 8, NULL, 'available', NULL),
(22, 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/products\\eyeee.png', 'eyeglasses', 'pakibalik po ty', 'opencourt', '2024-11-25', 'LOST', 8, NULL, 'available', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `messages`
--

CREATE TABLE `messages` (
  `message_id` int(11) NOT NULL,
  `sender_id` int(11) NOT NULL,
  `receiver_id` int(11) NOT NULL,
  `message` text NOT NULL,
  `timestamp` datetime DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `messages`
--

INSERT INTO `messages` (`message_id`, `sender_id`, `receiver_id`, `message`, `timestamp`) VALUES
(1, 2, 1, 'hey', '2024-10-26 22:24:18'),
(2, 1, 2, 'anoo', '2024-10-26 22:24:41'),
(3, 1, 2, 'pakyu', '2024-10-26 22:26:31'),
(4, 2, 1, 'ediwow', '2024-10-26 22:26:44'),
(5, 3, 1, 'halo', '2024-10-26 22:41:48'),
(6, 3, 2, 'hoy', '2024-10-26 22:53:31'),
(7, 1, 2, 'tanginamo', '2024-10-26 23:28:50'),
(8, 2, 1, 'hh', '2024-10-27 00:25:06'),
(9, 2, 5, 'aaaaaaaa', '2024-10-27 01:43:04'),
(10, 7, 3, 'hoy saken yan magnanakaw', '2024-11-02 00:34:23'),
(11, 7, 6, 'nakita ko to', '2024-11-02 00:34:45'),
(12, 6, 7, 'ulol', '2024-11-02 00:35:50'),
(13, 3, 7, 'ulol', '2024-11-02 22:37:33'),
(14, 8, 1, 'wawuririi', '2024-11-03 00:07:47'),
(15, 7, 8, 'hey sakin yang gtech', '2024-11-03 02:29:17');

-- --------------------------------------------------------

--
-- Table structure for table `notifications`
--

CREATE TABLE `notifications` (
  `notification_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `message` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `item_id` int(11) DEFAULT NULL,
  `is_read` tinyint(1) DEFAULT 0,
  `notification_type` enum('claim','message','post') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `notifications`
--

INSERT INTO `notifications` (`notification_id`, `user_id`, `message`, `created_at`, `item_id`, `is_read`, `notification_type`) VALUES
(1, 8, 'Item \'GTech\' was posted successfully.', '2024-11-02 18:01:25', 17, 1, 'claim'),
(2, 8, 'Item \'Toblerone\' was posted successfully.', '2024-11-02 18:37:43', 18, 0, 'claim'),
(3, 3, 'Item \'Coke\' was posted successfully.', '2024-11-02 18:45:45', 19, 0, 'claim'),
(4, 3, 'Item \'Piattos\' was posted successfully.', '2024-11-02 18:48:47', 20, 0, 'claim'),
(5, 8, 'Item \'earphones\' was posted successfully.', '2024-11-02 18:56:55', 21, 0, 'claim'),
(6, 8, 'Item \'eyeglasses\' was posted successfully.', '2024-11-02 19:01:21', 22, 0, 'claim');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_name` varchar(255) NOT NULL,
  `password` varchar(100) NOT NULL,
  `email` varchar(255) NOT NULL,
  `college` varchar(100) DEFAULT NULL,
  `birthday` date DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `profile_pic` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `user_name`, `password`, `email`, `college`, `birthday`, `name`, `profile_pic`) VALUES
(1, 'emz', 'emz', 'jjohnemman@gmail.com', 'college of computing studies', '2004-01-03', 'john emman l juaquera', NULL),
(2, 'ria', 'ria', 'ria@gmail.com', 'CCS', NULL, 'Ria Dagalea', NULL),
(3, 'a', 'b', 'gagi@gmail.com', 'CCSCJE', '2017-08-10', 'sawakas', 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/profilepics\\F0UGZHqaUAEdR-V.jpg'),
(4, 'test', 'test', 'try@gmail.com', NULL, NULL, NULL, NULL),
(5, 'emman07', 'wakera', 'jjohnemman@gmail.com', NULL, NULL, NULL, NULL),
(6, 'wax', 'emz', 'emz@gmail.com', NULL, NULL, NULL, NULL),
(7, 'riri123', 'ria', 'ria@gmail.com', 'ccs', '2002-05-17', 'ria jeanel', 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/profilepics\\Fzqpa77aYAEZYng.jpg'),
(8, 'kaoruko', 'a', 'kaoruko@gmail.com', 'ils', '2004-01-03', 'waguribest', 'C:/Users/MSi/OneDrive/Desktop/CFAexternal/profilepics\\kaoruko.jpg');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `fk_user` (`user_id`),
  ADD KEY `claimed_by` (`claimed_by`);

--
-- Indexes for table `messages`
--
ALTER TABLE `messages`
  ADD PRIMARY KEY (`message_id`),
  ADD KEY `sender_id` (`sender_id`),
  ADD KEY `receiver_id` (`receiver_id`);

--
-- Indexes for table `notifications`
--
ALTER TABLE `notifications`
  ADD PRIMARY KEY (`notification_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `item_id` (`item_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_name` (`user_name`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=23;

--
-- AUTO_INCREMENT for table `messages`
--
ALTER TABLE `messages`
  MODIFY `message_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `notifications`
--
ALTER TABLE `notifications`
  MODIFY `notification_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `fk_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE,
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`claimed_by`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `messages`
--
ALTER TABLE `messages`
  ADD CONSTRAINT `messages_ibfk_1` FOREIGN KEY (`sender_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `messages_ibfk_2` FOREIGN KEY (`receiver_id`) REFERENCES `users` (`user_id`);

--
-- Constraints for table `notifications`
--
ALTER TABLE `notifications`
  ADD CONSTRAINT `notifications_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `notifications_ibfk_2` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
