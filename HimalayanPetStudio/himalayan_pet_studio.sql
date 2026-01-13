-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Dec 15, 2025 at 12:35 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.0.30

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `himalayan_pet_studio`
--

-- --------------------------------------------------------

--
-- Table structure for table `accounts_contact`
--

CREATE TABLE `accounts_contact` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `email` varchar(254) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `subject` varchar(200) NOT NULL,
  `message` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `is_read` tinyint(1) NOT NULL,
  `admin_reply` longtext DEFAULT NULL,
  `replied_at` datetime(6) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `accounts_contact`
--

INSERT INTO `accounts_contact` (`id`, `name`, `email`, `phone`, `subject`, `message`, `created_at`, `is_read`, `admin_reply`, `replied_at`) VALUES
(1, 'User 2', 'user2@gmail.com', '12345', 'sunday open or not', 'is studio open in sunday', '2025-11-25 10:48:16.454461', 1, NULL, NULL),
(2, 'User User', 'user@gmail.com', '1234567890', 'emergency', 'have an emergency at lakeside', '2025-11-30 08:24:23.172529', 0, NULL, NULL),
(3, 'test user2', 'testuser2@gmail.com', '654321', 'help please', 'dog have an accident', '2025-12-03 04:37:07.194797', 1, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` bigint(20) NOT NULL,
  `pet_name` varchar(100) NOT NULL,
  `pet_type` varchar(50) NOT NULL,
  `service` varchar(20) NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time(6) NOT NULL,
  `status` varchar(20) NOT NULL,
  `notes` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `appointments`
--

INSERT INTO `appointments` (`id`, `pet_name`, `pet_type`, `service`, `appointment_date`, `appointment_time`, `status`, `notes`, `created_at`, `updated_at`, `user_id`) VALUES
(1, 'Tommy', 'Dog', 'haircut', '2025-11-26', '10:26:00.000000', 'confirmed', '', '2025-11-25 12:41:51.915630', '2025-11-25 12:55:48.292581', 4),
(2, 'Leo', 'Dog', 'bath', '2025-11-28', '15:00:00.000000', 'confirmed', 'best', '2025-11-26 09:15:00.675060', '2025-11-26 09:48:35.835596', 2),
(3, 'belly', 'dog', 'bath', '2025-11-28', '12:39:00.000000', 'pending', '', '2025-11-26 09:54:41.788158', '2025-11-26 09:54:41.788251', 5),
(4, 'Laika', 'Dog', 'full', '2025-11-29', '10:44:00.000000', 'confirmed', '', '2025-11-26 09:59:07.891546', '2025-11-26 09:59:41.259197', 5),
(5, 'Bikky', 'Dog', 'full', '2025-12-01', '13:10:00.000000', 'confirmed', '', '2025-11-30 08:25:25.959048', '2025-11-30 08:28:37.517785', 2),
(6, 'Sandy', 'Cat', 'full', '2025-12-07', '10:20:00.000000', 'confirmed', 'zjvnsdk fgsdjh', '2025-12-03 04:35:51.901658', '2025-12-03 04:37:51.243345', 5),
(7, 'lolo', 'Dog', 'bath', '2025-12-13', '10:34:00.000000', 'pending', 'notjing', '2025-12-03 04:49:45.879509', '2025-12-03 04:49:45.879533', 4);

-- --------------------------------------------------------

--
-- Table structure for table `auth_group`
--

CREATE TABLE `auth_group` (
  `id` int(11) NOT NULL,
  `name` varchar(150) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_group_permissions`
--

CREATE TABLE `auth_group_permissions` (
  `id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `auth_permission`
--

CREATE TABLE `auth_permission` (
  `id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `content_type_id` int(11) NOT NULL,
  `codename` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `auth_permission`
--

INSERT INTO `auth_permission` (`id`, `name`, `content_type_id`, `codename`) VALUES
(1, 'Can add log entry', 1, 'add_logentry'),
(2, 'Can change log entry', 1, 'change_logentry'),
(3, 'Can delete log entry', 1, 'delete_logentry'),
(4, 'Can view log entry', 1, 'view_logentry'),
(5, 'Can add permission', 2, 'add_permission'),
(6, 'Can change permission', 2, 'change_permission'),
(7, 'Can delete permission', 2, 'delete_permission'),
(8, 'Can view permission', 2, 'view_permission'),
(9, 'Can add group', 3, 'add_group'),
(10, 'Can change group', 3, 'change_group'),
(11, 'Can delete group', 3, 'delete_group'),
(12, 'Can view group', 3, 'view_group'),
(13, 'Can add content type', 4, 'add_contenttype'),
(14, 'Can change content type', 4, 'change_contenttype'),
(15, 'Can delete content type', 4, 'delete_contenttype'),
(16, 'Can view content type', 4, 'view_contenttype'),
(17, 'Can add session', 5, 'add_session'),
(18, 'Can change session', 5, 'change_session'),
(19, 'Can delete session', 5, 'delete_session'),
(20, 'Can view session', 5, 'view_session'),
(21, 'Can add User', 6, 'add_user'),
(22, 'Can change User', 6, 'change_user'),
(23, 'Can delete User', 6, 'delete_user'),
(24, 'Can view User', 6, 'view_user'),
(25, 'Can add Appointment', 7, 'add_appointment'),
(26, 'Can change Appointment', 7, 'change_appointment'),
(27, 'Can delete Appointment', 7, 'delete_appointment'),
(28, 'Can view Appointment', 7, 'view_appointment'),
(29, 'Can add product', 8, 'add_product'),
(30, 'Can change product', 8, 'change_product'),
(31, 'Can delete product', 8, 'delete_product'),
(32, 'Can view product', 8, 'view_product'),
(33, 'Can add product category', 9, 'add_productcategory'),
(34, 'Can change product category', 9, 'change_productcategory'),
(35, 'Can delete product category', 9, 'delete_productcategory'),
(36, 'Can view product category', 9, 'view_productcategory'),
(37, 'Can add sale', 10, 'add_sale'),
(38, 'Can change sale', 10, 'change_sale'),
(39, 'Can delete sale', 10, 'delete_sale'),
(40, 'Can view sale', 10, 'view_sale'),
(41, 'Can add contact', 11, 'add_contact'),
(42, 'Can change contact', 11, 'change_contact'),
(43, 'Can delete contact', 11, 'delete_contact'),
(44, 'Can view contact', 11, 'view_contact'),
(45, 'Can add cart', 12, 'add_cart'),
(46, 'Can change cart', 12, 'change_cart'),
(47, 'Can delete cart', 12, 'delete_cart'),
(48, 'Can view cart', 12, 'view_cart'),
(49, 'Can add review', 13, 'add_review'),
(50, 'Can change review', 13, 'change_review'),
(51, 'Can delete review', 13, 'delete_review'),
(52, 'Can view review', 13, 'view_review'),
(53, 'Can add order item', 14, 'add_orderitem'),
(54, 'Can change order item', 14, 'change_orderitem'),
(55, 'Can delete order item', 14, 'delete_orderitem'),
(56, 'Can view order item', 14, 'view_orderitem'),
(57, 'Can add order', 15, 'add_order'),
(58, 'Can change order', 15, 'change_order'),
(59, 'Can delete order', 15, 'delete_order'),
(60, 'Can view order', 15, 'view_order');

-- --------------------------------------------------------

--
-- Table structure for table `django_admin_log`
--

CREATE TABLE `django_admin_log` (
  `id` int(11) NOT NULL,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext DEFAULT NULL,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint(5) UNSIGNED NOT NULL CHECK (`action_flag` >= 0),
  `change_message` longtext NOT NULL,
  `content_type_id` int(11) DEFAULT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `django_content_type`
--

CREATE TABLE `django_content_type` (
  `id` int(11) NOT NULL,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(11, 'accounts', 'contact'),
(6, 'accounts', 'user'),
(1, 'admin', 'logentry'),
(7, 'appointments', 'appointment'),
(3, 'auth', 'group'),
(2, 'auth', 'permission'),
(4, 'contenttypes', 'contenttype'),
(12, 'products', 'cart'),
(15, 'products', 'order'),
(14, 'products', 'orderitem'),
(8, 'products', 'product'),
(9, 'products', 'productcategory'),
(13, 'products', 'review'),
(10, 'products', 'sale'),
(5, 'sessions', 'session');

-- --------------------------------------------------------

--
-- Table structure for table `django_migrations`
--

CREATE TABLE `django_migrations` (
  `id` bigint(20) NOT NULL,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-11-25 03:51:56.111238'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-11-25 03:51:56.167438'),
(3, 'auth', '0001_initial', '2025-11-25 03:51:56.372213'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-11-25 03:51:56.425190'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-11-25 03:51:56.432424'),
(6, 'auth', '0004_alter_user_username_opts', '2025-11-25 03:51:56.439200'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-11-25 03:51:56.446209'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-11-25 03:51:56.449607'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-11-25 03:51:56.461276'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-11-25 03:51:56.468157'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-11-25 03:51:56.475496'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-11-25 03:51:56.488139'),
(13, 'auth', '0011_update_proxy_permissions', '2025-11-25 03:51:56.496695'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-11-25 03:51:56.505185'),
(15, 'accounts', '0001_initial', '2025-11-25 03:51:56.743147'),
(16, 'admin', '0001_initial', '2025-11-25 03:51:56.854912'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-11-25 03:51:56.864824'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-11-25 03:51:56.873192'),
(19, 'appointments', '0001_initial', '2025-11-25 03:51:56.937154'),
(20, 'sessions', '0001_initial', '2025-11-25 03:51:56.977815'),
(21, 'accounts', '0002_alter_user_phone', '2025-11-25 09:32:40.980585'),
(22, 'products', '0001_initial', '2025-11-25 09:59:02.988892'),
(23, 'products', '0002_sale', '2025-11-25 10:27:39.855530'),
(24, 'accounts', '0003_contact', '2025-11-25 10:42:48.934795'),
(25, 'products', '0003_cart', '2025-11-25 11:03:36.878817'),
(26, 'accounts', '0004_user_profile_picture', '2025-11-26 03:43:32.276421'),
(27, 'products', '0004_review', '2025-11-26 04:44:50.674253'),
(28, 'products', '0005_order_orderitem', '2025-11-26 05:59:59.734125'),
(29, 'accounts', '0005_contact_admin_reply_contact_replied_at', '2025-12-15 11:20:56.591152');

-- --------------------------------------------------------

--
-- Table structure for table `django_session`
--

CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('818vrtvwizxfvxqdlk576tkpwlufxk8v', '.eJxVj8sOwiAURP-FdUNoeZUu3fsNhMfFogYMtInG-O-Wpgvd3ZyZO5N5I23WZdZrhaKjRxPiqPtl1rgbpCb4q0mXjF1OS4kWNws-1IrP2cP9dHj_AmZT5-2bMScpp8EJrwZjgQinSKAjkX0I4Ohgac-ZdaCkl3LsqQgbY4JI66ga9tAKtcacNDwfsbzQRDq0V5R8h62i3ehAbQr_fAHIX0ku:1vQfKR:WF0ODOdPgfZBZTdpcNPyecvem4Q3H4VQMGpaQvkxvCI', '2025-12-04 05:23:03.006484'),
('ddqr5d4dzqi09a1toq1k1zon4jrivkh6', '.eJxVjsEOwiAQRP-FsyGALZUevfsNZIHFog0YaBON8d8FUxNN9rCZmX2zT6JhXSa9Fsw6ODISSXa_mgF7xdgMd4F4TtSmuORgaIvQzS30lBzOxy37B5igTPUalcEBhO17ZZhEy-3B90yAQy8EgvKCS94p3HeScTS2jhMM_VDDnvsG_eBymrHi2v6V2tuydhYsJaSo8X4L-UHGg-wYe70BUnxLcg:1vPcrW:vTR2Ix2KntzvOMYA8fjjUv-DmK4kNKkXJVHS1V3HWVo', '2025-12-01 08:32:54.356686'),
('j4m0875t9plnd89hgxnrlc97iher7g48', '.eJxVT0sOwiAUvAvrhtACpXTp3jMQPg-LNmCgTTTGu1sMC91N5pt5IaX3bVF7gayCQzNiqPvljLY3iFVwVx0vCdsUtxwMrhbc1ILPycF6at6_gkWX5UgbP7hxNK6XggD01kxysJJSEBZ0b6n3kgMFA4QSB4L5iTouvLCTHhjlvJYWKCWkqOBxD_mJZtKh70ROKxwTFaNG1Svs_QEk50on:1vS9nE:n8YyNVHYlMJ1AC_yHJQpjOierobZaqTRk7lpu52jcXE', '2025-12-08 08:06:56.235653'),
('rpv51jb5chuqxafqf0nx08mwi6fij1d7', '.eJxVT0sOwiAUvAvrhtACpXTp3jMQPg-LNmCgTTTGu1sMC91N5pt5IaX3bVF7gayCQzNiqPvljLY3iFVwVx0vCdsUtxwMrhbc1ILPycF6at6_gkWX5UgbP7hxNK6XggD01kxysJJSEBZ0b6n3kgMFA4QSB4L5iTouvLCTHhjlvJYWKCWkqOBxD_mJZtKh70ROKxwTFaNG1Svs_QEk50on:1vV6hr:owmBQOUKxoc1Nvdd_gYHn2kOTakBxQgvP0sKdhdjeSI', '2025-12-16 11:25:35.186780'),
('rvutw9cefjzkjdx39o10t7hmj6qiqtb8', '.eJxVT0sOgyAQvQtrY3AERJfd9wxkgGmlH2hAkzZN7141Ltrt-783MzhPo5kLZRM8Gxiw6hez6K4UV8JfMJ5T7VKccrD1Kql3ttTH5Ol22LV_ASOWcXELAKFReGicEh1ZRVJZkJoaDaiFbzWXvOvkCfvWut5TYwGVdNz3rXRqW1WolJCioecj5BcbeMW2ipxutFSgv4fIdmz9Ap8v3iZJDQ:1vOCMz:xP5T7CxE4PB1Z_KeVl5qwJ_bQM897YBhmkZNQ5W-vuo', '2025-11-27 10:03:29.671972');

-- --------------------------------------------------------

--
-- Table structure for table `products_cart`
--

CREATE TABLE `products_cart` (
  `id` bigint(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `added_at` datetime(6) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `products_order`
--

CREATE TABLE `products_order` (
  `id` bigint(20) NOT NULL,
  `order_number` varchar(100) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `status` varchar(20) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `payment_status` varchar(20) NOT NULL,
  `stripe_payment_intent_id` varchar(255) DEFAULT NULL,
  `shipping_address` longtext NOT NULL,
  `phone_number` varchar(15) NOT NULL,
  `notes` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_order`
--

INSERT INTO `products_order` (`id`, `order_number`, `total_amount`, `status`, `payment_method`, `payment_status`, `stripe_payment_intent_id`, `shipping_address`, `phone_number`, `notes`, `created_at`, `updated_at`, `user_id`) VALUES
(1, 'NNPPVZ90XW', 1000.00, 'pending', 'cod', 'pending', NULL, 'dfklnsdklvn', '1234567', 'nzsfkndskln', '2025-11-26 06:01:18.964816', '2025-11-26 06:01:18.980939', 4),
(2, 'LOBQYJQ21O', 3000.00, 'cancelled', 'cod', 'pending', NULL, 'hvjhgv', '1234567', '', '2025-11-26 06:02:24.422899', '2025-12-03 04:39:26.931024', 4),
(3, 'Y0YMHBRMTH', 7200.00, 'processing', 'cod', 'pending', NULL, 'abcd', '1234567', '', '2025-12-03 04:41:18.753602', '2025-12-03 04:48:32.582251', 4),
(4, 'DE5P1F5YUL', 2750.00, 'pending', 'cod', 'pending', NULL, 'knvzdklvnzl', '1234567', '', '2025-12-03 04:50:19.740661', '2025-12-03 04:50:19.764521', 4),
(5, '4T9B52LLBA', 700.00, 'pending', 'cod', 'pending', NULL, 'jhzvbsdzhb', '654321', '', '2025-12-03 04:51:33.607178', '2025-12-03 04:51:33.624497', 5),
(6, 'Z8J5G4ZM1S', 2100.00, 'pending', 'cod', 'pending', NULL, 'hv', '1234567', '', '2025-12-07 08:06:56.192073', '2025-12-07 08:06:56.203107', 4);

-- --------------------------------------------------------

--
-- Table structure for table `products_orderitem`
--

CREATE TABLE `products_orderitem` (
  `id` bigint(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `order_id` bigint(20) NOT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_orderitem`
--

INSERT INTO `products_orderitem` (`id`, `quantity`, `unit_price`, `subtotal`, `order_id`, `product_id`) VALUES
(1, 1, 1000.00, 1000.00, 1, 2),
(2, 1, 2000.00, 2000.00, 2, 1),
(3, 1, 1000.00, 1000.00, 2, 3),
(4, 1, 6500.00, 6500.00, 3, 8),
(5, 2, 350.00, 700.00, 3, 12),
(6, 1, 350.00, 350.00, 4, 12),
(7, 2, 1200.00, 2400.00, 4, 9),
(8, 2, 350.00, 700.00, 5, 12),
(9, 1, 2100.00, 2100.00, 6, 11);

-- --------------------------------------------------------

--
-- Table structure for table `products_product`
--

CREATE TABLE `products_product` (
  `id` bigint(20) NOT NULL,
  `name` varchar(200) NOT NULL,
  `description` longtext NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `stock_quantity` int(11) NOT NULL,
  `image` varchar(100) DEFAULT NULL,
  `is_active` tinyint(1) NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `category_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_product`
--

INSERT INTO `products_product` (`id`, `name`, `description`, `price`, `stock_quantity`, `image`, `is_active`, `created_at`, `updated_at`, `category_id`) VALUES
(1, 'Dog Food 1', 'Best food', 2000.00, 2, 'products/xpulse_back.jpg', 1, '2025-11-25 10:09:02.112265', '2025-11-26 06:02:24.429151', 1),
(2, 'Belt', 'nvjkdvnj', 1000.00, 9, 'products/xpulse_back_BvPzT94.jpg', 1, '2025-11-25 10:12:56.953240', '2025-11-26 06:01:18.971406', 3),
(3, 'Dog Cloths', 'njdsifbkjdfsbnj', 1000.00, 3, 'products/xpulse_back_QPLcbfT.jpg', 1, '2025-11-26 04:59:44.581283', '2025-11-26 06:02:24.437287', 2),
(4, 'Fake Bone', 'same as bone which provide energy in pet', 1500.00, 7, 'products/xpulse_right_facing.webp', 1, '2025-11-26 06:42:56.092902', '2025-11-26 06:42:56.896412', 3),
(5, 'sfnsj', 'zfvnsdjkvbdsjkbasjkdbFAS FOWHDFQWUIG FUYUYGF UY', 1000.00, 0, 'products/xpulse_front.jpg.webp', 1, '2025-11-26 06:43:23.069164', '2025-11-26 06:55:10.734881', 2),
(6, 'ZJVBNDJZ', 'BEST PET FOOD', 1000.00, 3, 'products/xpulse_back_xcQSE0b.jpg', 1, '2025-11-26 06:43:49.730195', '2025-11-26 06:43:49.736553', 1),
(7, 'Sofa for pet', 'dfnsdjn', 4500.00, 9, 'products/xpulse_left_facing.avif', 1, '2025-11-26 06:44:37.674608', '2025-11-26 06:44:37.682257', 3),
(8, 'kennel for dog', 'sdjkgnzjk fnf f fvJ HFV VHJFVZJHZGBV BFG SdBSV sjSHDVsjdhV sjV  a bfjhasfvb jh', 6500.00, 2, 'products/xpulse_left_facing_vhmrFJ0.avif', 1, '2025-11-26 06:45:20.104511', '2025-12-03 04:41:18.759365', 3),
(9, 'shoes for dog', 'zdjbnsdj gs gfhv hfjh fasvj', 1200.00, 4, 'products/xpulse_front.jpg_Sl2mTv4.webp', 1, '2025-11-26 06:45:54.047795', '2025-12-03 04:50:19.754586', 3),
(10, 'Name tag for pet', 'zvnadjkvbajkb', 1000.00, 14, 'products/xpulse_right_facing_h9YGjau.webp', 1, '2025-11-26 06:46:30.707030', '2025-11-26 06:46:30.715118', 3),
(11, 'healthy diet for cat', 'sdgfhsiughb n fweigfseiu igfsegfbshbh', 2100.00, 6, 'products/xpulse_front.jpg_NBig961.webp', 1, '2025-11-26 06:50:14.657771', '2025-12-07 08:06:56.197046', 1),
(12, 'Pet Biscuit', 'best and healthy food', 350.00, 5, 'products/xpulse_back_3rVJcxH.jpg', 1, '2025-12-03 04:38:56.896893', '2025-12-03 04:51:33.615538', 1);

-- --------------------------------------------------------

--
-- Table structure for table `products_productcategory`
--

CREATE TABLE `products_productcategory` (
  `id` bigint(20) NOT NULL,
  `name` varchar(100) NOT NULL,
  `description` longtext NOT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_productcategory`
--

INSERT INTO `products_productcategory` (`id`, `name`, `description`, `created_at`, `updated_at`) VALUES
(1, 'Food', 'Diet food', '2025-11-25 10:07:16.653683', '2025-11-25 10:07:16.655472'),
(2, 'Pet clothes', 'jvnkdjzvbndz', '2025-11-25 10:10:06.510599', '2025-11-25 10:10:06.512739'),
(3, 'Pet Accessories', 'nvdjsvbdsjkbj', '2025-11-25 10:12:25.638703', '2025-11-25 10:12:25.640555');

-- --------------------------------------------------------

--
-- Table structure for table `products_review`
--

CREATE TABLE `products_review` (
  `id` bigint(20) NOT NULL,
  `rating` int(11) NOT NULL,
  `comment` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `product_id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_review`
--

INSERT INTO `products_review` (`id`, `rating`, `comment`, `created_at`, `updated_at`, `product_id`, `user_id`) VALUES
(1, 2, 'this product is really awesome', '2025-11-26 06:05:45.838512', '2025-11-26 06:05:45.839666', 2, 4),
(2, 2, 'nice product', '2025-12-03 04:42:02.825392', '2025-12-03 04:42:02.826578', 12, 4),
(3, 5, 'really good', '2025-12-03 04:51:55.585254', '2025-12-03 04:51:55.586274', 12, 5);

-- --------------------------------------------------------

--
-- Table structure for table `products_sale`
--

CREATE TABLE `products_sale` (
  `id` bigint(20) NOT NULL,
  `quantity` int(11) NOT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `payment_method` varchar(20) NOT NULL,
  `sale_date` datetime(6) NOT NULL,
  `notes` longtext NOT NULL,
  `customer_id` bigint(20) DEFAULT NULL,
  `product_id` bigint(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `products_sale`
--

INSERT INTO `products_sale` (`id`, `quantity`, `unit_price`, `total_amount`, `payment_method`, `sale_date`, `notes`, `customer_id`, `product_id`) VALUES
(1, 1, 1000.00, 1000.00, 'cash', '2025-11-26 06:01:18.973936', '', 4, 2),
(2, 1, 2000.00, 2000.00, 'cash', '2025-11-26 06:02:24.431961', '', 4, 1),
(3, 1, 1000.00, 1000.00, 'cash', '2025-11-26 06:02:24.439685', '', 4, 3),
(4, 1, 6500.00, 6500.00, 'cash', '2025-12-03 04:41:18.761466', '', 4, 8),
(5, 2, 350.00, 700.00, 'cash', '2025-12-03 04:41:18.769394', '', 4, 12),
(6, 1, 350.00, 350.00, 'cash', '2025-12-03 04:50:19.750327', '', 4, 12),
(7, 2, 1200.00, 2400.00, 'cash', '2025-12-03 04:50:19.757635', '', 4, 9),
(8, 2, 350.00, 700.00, 'cash', '2025-12-03 04:51:33.617948', '', 5, 12),
(9, 1, 2100.00, 2100.00, 'cash', '2025-12-07 08:06:56.198941', '', 4, 11);

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` bigint(20) NOT NULL,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `role` varchar(10) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `address` longtext DEFAULT NULL,
  `created_at` datetime(6) NOT NULL,
  `updated_at` datetime(6) NOT NULL,
  `profile_picture` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`, `role`, `phone`, `address`, `created_at`, `updated_at`, `profile_picture`) VALUES
(1, 'pbkdf2_sha256$600000$o7ESO3aM1t7gKsGHHcwN3D$+YB2SHYZa/88gGno24k1W8Lqm/NhlNpebGDMRSkCLmY=', NULL, 1, 'admin', 'Admin', 'User', 'admin@himalayan.com', 1, 1, '2025-11-25 03:52:31.902202', 'admin', '0000000000', NULL, '2025-11-25 03:52:32.402538', '2025-11-25 03:52:32.402554', NULL),
(2, 'pbkdf2_sha256$600000$EyYXgkzpBwA8gj9hm6Ez8d$Fm01FUDl/L/umUmkMFv3HFES5C7Nhy+ALN0yK4/JS94=', '2025-12-07 07:50:05.110726', 0, 'User', 'User', 'User', 'user@gmail.com', 0, 1, '2025-11-25 09:34:52.786131', 'admin', '1234567890', NULL, '2025-11-25 09:34:53.334607', '2025-11-25 09:34:53.334625', NULL),
(3, 'pbkdf2_sha256$600000$oeFtsdalDY9X2Nj23xxToJ$oawoZX1P0M88VRW4UCSDsHTzD76luiQNE80SKcG+GFo=', '2025-11-25 10:34:54.228602', 0, 'user2', 'User', '2', 'user2@gmail.com', 0, 1, '2025-11-25 10:34:53.703667', 'admin', '12345', NULL, '2025-11-25 10:34:54.206038', '2025-11-25 10:34:54.206053', NULL),
(4, 'pbkdf2_sha256$600000$EAonIUfHf9uv8Q91egkIIp$WbHjzXDdeiiz4CBbmJkKTLwFRP2HBiHI5isa7QTFN/4=', '2025-12-15 10:57:09.535086', 0, 'testuser', 'User', 'Final', 'test@gmail.com', 0, 1, '2025-11-25 10:53:21.836110', 'user', '1234567', '', '2025-11-25 10:53:22.379991', '2025-11-26 05:07:14.986829', 'profile_pictures/xpulse_back.jpg'),
(5, 'pbkdf2_sha256$600000$SRVTZD4fSYTe5XfgKsTjmU$cTjNhjCsLRVAIyFB1YVhehDPsT3nM1X56ECvmNsMVn0=', '2025-12-03 04:51:02.356021', 0, 'testuser2', 'test', 'user2', 'testuser2@gmail.com', 0, 1, '2025-11-26 06:06:49.417291', 'user', '654321', NULL, '2025-11-26 06:06:50.107272', '2025-11-26 06:06:50.107290', ''),
(6, 'pbkdf2_sha256$600000$EM7uvvRJtKoEYscruuiiR0$o0VY6M5cu23GNBf8f0pOd9wnV27dz7UR+wjLnEfk3Ac=', '2025-11-30 08:32:54.209393', 0, 'iuygty', 'yui', 'hjb', 'uhgy@hg.com', 0, 1, '2025-11-30 08:32:53.632216', 'user', 'hgbiyvhbj7', NULL, '2025-11-30 08:32:54.182676', '2025-11-30 08:32:54.182694', '');

-- --------------------------------------------------------

--
-- Table structure for table `users_groups`
--

CREATE TABLE `users_groups` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `group_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Table structure for table `users_user_permissions`
--

CREATE TABLE `users_user_permissions` (
  `id` bigint(20) NOT NULL,
  `user_id` bigint(20) NOT NULL,
  `permission_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Indexes for dumped tables
--

--
-- Indexes for table `accounts_contact`
--
ALTER TABLE `accounts_contact`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `appointments_user_id_052f0814_fk_users_id` (`user_id`);

--
-- Indexes for table `auth_group`
--
ALTER TABLE `auth_group`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  ADD KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`);

--
-- Indexes for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`);

--
-- Indexes for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD PRIMARY KEY (`id`),
  ADD KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  ADD KEY `django_admin_log_user_id_c564eba6_fk_users_id` (`user_id`);

--
-- Indexes for table `django_content_type`
--
ALTER TABLE `django_content_type`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`);

--
-- Indexes for table `django_migrations`
--
ALTER TABLE `django_migrations`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `django_session`
--
ALTER TABLE `django_session`
  ADD PRIMARY KEY (`session_key`),
  ADD KEY `django_session_expire_date_a5c62663` (`expire_date`);

--
-- Indexes for table `products_cart`
--
ALTER TABLE `products_cart`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `products_cart_user_id_product_id_c2d7ed32_uniq` (`user_id`,`product_id`),
  ADD KEY `products_cart_product_id_52080291_fk_products_product_id` (`product_id`);

--
-- Indexes for table `products_order`
--
ALTER TABLE `products_order`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `order_number` (`order_number`),
  ADD KEY `products_order_user_id_dfb540d8_fk_users_id` (`user_id`);

--
-- Indexes for table `products_orderitem`
--
ALTER TABLE `products_orderitem`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_orderitem_order_id_09ecb3c7_fk_products_order_id` (`order_id`),
  ADD KEY `products_orderitem_product_id_60e2b174_fk_products_product_id` (`product_id`);

--
-- Indexes for table `products_product`
--
ALTER TABLE `products_product`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_product_category_id_9b594869_fk_products_` (`category_id`);

--
-- Indexes for table `products_productcategory`
--
ALTER TABLE `products_productcategory`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `products_review`
--
ALTER TABLE `products_review`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `products_review_product_id_user_id_6a28a89d_uniq` (`product_id`,`user_id`),
  ADD KEY `products_review_user_id_2e53b831_fk_users_id` (`user_id`);

--
-- Indexes for table `products_sale`
--
ALTER TABLE `products_sale`
  ADD PRIMARY KEY (`id`),
  ADD KEY `products_sale_customer_id_a2fb320b_fk_users_id` (`customer_id`),
  ADD KEY `products_sale_product_id_90b04df3_fk_products_product_id` (`product_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `users_phone_2b77170a_uniq` (`phone`);

--
-- Indexes for table `users_groups`
--
ALTER TABLE `users_groups`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_groups_user_id_group_id_fc7788e8_uniq` (`user_id`,`group_id`),
  ADD KEY `users_groups_group_id_2f3517aa_fk_auth_group_id` (`group_id`);

--
-- Indexes for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `users_user_permissions_user_id_permission_id_3b86cbdf_uniq` (`user_id`,`permission_id`),
  ADD KEY `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` (`permission_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `accounts_contact`
--
ALTER TABLE `accounts_contact`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `auth_group`
--
ALTER TABLE `auth_group`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `auth_permission`
--
ALTER TABLE `auth_permission`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- AUTO_INCREMENT for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `django_content_type`
--
ALTER TABLE `django_content_type`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `django_migrations`
--
ALTER TABLE `django_migrations`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `products_cart`
--
ALTER TABLE `products_cart`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `products_order`
--
ALTER TABLE `products_order`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `products_orderitem`
--
ALTER TABLE `products_orderitem`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `products_product`
--
ALTER TABLE `products_product`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `products_productcategory`
--
ALTER TABLE `products_productcategory`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products_review`
--
ALTER TABLE `products_review`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `products_sale`
--
ALTER TABLE `products_sale`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `users_groups`
--
ALTER TABLE `users_groups`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  MODIFY `id` bigint(20) NOT NULL AUTO_INCREMENT;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_user_id_052f0814_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `auth_group_permissions`
--
ALTER TABLE `auth_group_permissions`
  ADD CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`);

--
-- Constraints for table `auth_permission`
--
ALTER TABLE `auth_permission`
  ADD CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`);

--
-- Constraints for table `django_admin_log`
--
ALTER TABLE `django_admin_log`
  ADD CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  ADD CONSTRAINT `django_admin_log_user_id_c564eba6_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `products_cart`
--
ALTER TABLE `products_cart`
  ADD CONSTRAINT `products_cart_product_id_52080291_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  ADD CONSTRAINT `products_cart_user_id_d53bf7cf_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `products_order`
--
ALTER TABLE `products_order`
  ADD CONSTRAINT `products_order_user_id_dfb540d8_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `products_orderitem`
--
ALTER TABLE `products_orderitem`
  ADD CONSTRAINT `products_orderitem_order_id_09ecb3c7_fk_products_order_id` FOREIGN KEY (`order_id`) REFERENCES `products_order` (`id`),
  ADD CONSTRAINT `products_orderitem_product_id_60e2b174_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `products_product`
--
ALTER TABLE `products_product`
  ADD CONSTRAINT `products_product_category_id_9b594869_fk_products_` FOREIGN KEY (`category_id`) REFERENCES `products_productcategory` (`id`);

--
-- Constraints for table `products_review`
--
ALTER TABLE `products_review`
  ADD CONSTRAINT `products_review_product_id_d933ffa7_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`),
  ADD CONSTRAINT `products_review_user_id_2e53b831_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `products_sale`
--
ALTER TABLE `products_sale`
  ADD CONSTRAINT `products_sale_customer_id_a2fb320b_fk_users_id` FOREIGN KEY (`customer_id`) REFERENCES `users` (`id`),
  ADD CONSTRAINT `products_sale_product_id_90b04df3_fk_products_product_id` FOREIGN KEY (`product_id`) REFERENCES `products_product` (`id`);

--
-- Constraints for table `users_groups`
--
ALTER TABLE `users_groups`
  ADD CONSTRAINT `users_groups_group_id_2f3517aa_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`),
  ADD CONSTRAINT `users_groups_user_id_f500bee5_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);

--
-- Constraints for table `users_user_permissions`
--
ALTER TABLE `users_user_permissions`
  ADD CONSTRAINT `users_user_permissio_permission_id_6d08dcd2_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  ADD CONSTRAINT `users_user_permissions_user_id_92473840_fk_users_id` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
