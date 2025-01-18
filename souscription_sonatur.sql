-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : jeu. 16 jan. 2025 à 18:43
-- Version du serveur : 8.3.0
-- Version de PHP : 8.2.18

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `souscription_sonatur`
--

-- --------------------------------------------------------

--
-- Structure de la table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
CREATE TABLE IF NOT EXISTS `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
CREATE TABLE IF NOT EXISTS `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissions_group_id_b120cbf9` (`group_id`),
  KEY `auth_group_permissions_permission_id_84c5c92e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
CREATE TABLE IF NOT EXISTS `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  KEY `auth_permission_content_type_id_2f476e4b` (`content_type_id`)
) ENGINE=MyISAM AUTO_INCREMENT=97 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `auth_permission`
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
(21, 'Can add Rôle', 6, 'add_role'),
(22, 'Can change Rôle', 6, 'change_role'),
(23, 'Can delete Rôle', 6, 'delete_role'),
(24, 'Can view Rôle', 6, 'view_role'),
(25, 'Can add Utilisateur', 7, 'add_utilisateur'),
(26, 'Can change Utilisateur', 7, 'change_utilisateur'),
(27, 'Can delete Utilisateur', 7, 'delete_utilisateur'),
(28, 'Can view Utilisateur', 7, 'view_utilisateur'),
(29, 'Can add Condition', 8, 'add_condition'),
(30, 'Can change Condition', 8, 'change_condition'),
(31, 'Can delete Condition', 8, 'delete_condition'),
(32, 'Can view Condition', 8, 'view_condition'),
(33, 'Can add Liste des Parcelles', 9, 'add_listesparcelles'),
(34, 'Can change Liste des Parcelles', 9, 'change_listesparcelles'),
(35, 'Can delete Liste des Parcelles', 9, 'delete_listesparcelles'),
(36, 'Can view Liste des Parcelles', 9, 'view_listesparcelles'),
(37, 'Can add Localité', 10, 'add_localite'),
(38, 'Can change Localité', 10, 'change_localite'),
(39, 'Can delete Localité', 10, 'delete_localite'),
(40, 'Can view Localité', 10, 'view_localite'),
(41, 'Can add Opération', 11, 'add_operations'),
(42, 'Can change Opération', 11, 'change_operations'),
(43, 'Can delete Opération', 11, 'delete_operations'),
(44, 'Can view Opération', 11, 'view_operations'),
(45, 'Can add parcelle', 12, 'add_parcelle'),
(46, 'Can change parcelle', 12, 'change_parcelle'),
(47, 'Can delete parcelle', 12, 'delete_parcelle'),
(48, 'Can view parcelle', 12, 'view_parcelle'),
(49, 'Can add Position de parcelle', 13, 'add_positionparcelle'),
(50, 'Can change Position de parcelle', 13, 'change_positionparcelle'),
(51, 'Can delete Position de parcelle', 13, 'delete_positionparcelle'),
(52, 'Can view Position de parcelle', 13, 'view_positionparcelle'),
(53, 'Can add Processus d\'attribution', 14, 'add_processusattribution'),
(54, 'Can change Processus d\'attribution', 14, 'change_processusattribution'),
(55, 'Can delete Processus d\'attribution', 14, 'delete_processusattribution'),
(56, 'Can view Processus d\'attribution', 14, 'view_processusattribution'),
(57, 'Can add projet', 15, 'add_projet'),
(58, 'Can change projet', 15, 'change_projet'),
(59, 'Can delete projet', 15, 'delete_projet'),
(60, 'Can view projet', 15, 'view_projet'),
(61, 'Can add Type de parcelle', 16, 'add_typeparcelle'),
(62, 'Can change Type de parcelle', 16, 'change_typeparcelle'),
(63, 'Can delete Type de parcelle', 16, 'delete_typeparcelle'),
(64, 'Can view Type de parcelle', 16, 'view_typeparcelle'),
(65, 'Can add Compte Bancaire', 17, 'add_comptebancaire'),
(66, 'Can change Compte Bancaire', 17, 'change_comptebancaire'),
(67, 'Can delete Compte Bancaire', 17, 'delete_comptebancaire'),
(68, 'Can view Compte Bancaire', 17, 'view_comptebancaire'),
(69, 'Can add Mode de Paiement', 18, 'add_modepaiement'),
(70, 'Can change Mode de Paiement', 18, 'change_modepaiement'),
(71, 'Can delete Mode de Paiement', 18, 'delete_modepaiement'),
(72, 'Can view Mode de Paiement', 18, 'view_modepaiement'),
(73, 'Can add Quittance', 19, 'add_quittance'),
(74, 'Can change Quittance', 19, 'change_quittance'),
(75, 'Can delete Quittance', 19, 'delete_quittance'),
(76, 'Can view Quittance', 19, 'view_quittance'),
(77, 'Can add Paiement', 20, 'add_paiement'),
(78, 'Can change Paiement', 20, 'change_paiement'),
(79, 'Can delete Paiement', 20, 'delete_paiement'),
(80, 'Can view Paiement', 20, 'view_paiement'),
(81, 'Can add Type de Souscripteur', 21, 'add_typesouscripteur'),
(82, 'Can change Type de Souscripteur', 21, 'change_typesouscripteur'),
(83, 'Can delete Type de Souscripteur', 21, 'delete_typesouscripteur'),
(84, 'Can view Type de Souscripteur', 21, 'view_typesouscripteur'),
(85, 'Can add Souscription Effectuée', 22, 'add_souscriptioneffectuee'),
(86, 'Can change Souscription Effectuée', 22, 'change_souscriptioneffectuee'),
(87, 'Can delete Souscription Effectuée', 22, 'delete_souscriptioneffectuee'),
(88, 'Can view Souscription Effectuée', 22, 'view_souscriptioneffectuee'),
(89, 'Can add Souscripteur Physique', 23, 'add_souscripteurphysique'),
(90, 'Can change Souscripteur Physique', 23, 'change_souscripteurphysique'),
(91, 'Can delete Souscripteur Physique', 23, 'delete_souscripteurphysique'),
(92, 'Can view Souscripteur Physique', 23, 'view_souscripteurphysique'),
(93, 'Can add Souscripteur Moral', 24, 'add_souscripteurmorale'),
(94, 'Can change Souscripteur Moral', 24, 'change_souscripteurmorale'),
(95, 'Can delete Souscripteur Moral', 24, 'delete_souscripteurmorale'),
(96, 'Can view Souscripteur Moral', 24, 'view_souscripteurmorale');

-- --------------------------------------------------------

--
-- Structure de la table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
CREATE TABLE IF NOT EXISTS `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext COLLATE utf8mb4_unicode_ci,
  `object_repr` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `action_flag` smallint UNSIGNED NOT NULL,
  `change_message` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6` (`user_id`)
) ;

--
-- Déchargement des données de la table `django_admin_log`
--

INSERT INTO `django_admin_log` (`id`, `action_time`, `object_id`, `object_repr`, `action_flag`, `change_message`, `content_type_id`, `user_id`) VALUES
(1, '2025-01-11 11:47:00.040496', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(2, '2025-01-11 11:47:16.520378', '29', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Actif\"]}}]', 9, 1),
(3, '2025-01-11 11:47:19.758206', '28', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(4, '2025-01-11 11:47:22.648656', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(5, '2025-01-11 11:47:25.418049', '26', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(6, '2025-01-11 11:47:28.011851', '20', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(7, '2025-01-11 11:47:30.614600', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(8, '2025-01-11 11:47:34.268598', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(9, '2025-01-11 11:47:38.159063', '41', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(10, '2025-01-11 11:47:41.050082', '33', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(11, '2025-01-11 11:47:45.174886', '32', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(12, '2025-01-11 11:47:49.141414', '31', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Actif\"]}}]', 9, 1),
(13, '2025-01-11 11:47:52.952383', '30', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(14, '2025-01-11 11:47:56.117427', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(15, '2025-01-11 11:50:06.071737', '2', '', 3, '', 24, 1),
(16, '2025-01-11 11:50:06.071737', '1', '', 3, '', 24, 1),
(17, '2025-01-11 11:50:12.500824', '1', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(18, '2025-01-11 11:54:13.817825', '3', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736595896780', 3, '', 22, 1),
(19, '2025-01-11 11:54:13.817825', '2', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736595857789', 3, '', 22, 1),
(20, '2025-01-11 11:54:13.817825', '1', 'Souscription de OUEDRAOGO Moussa - TX-1736595589836', 3, '', 22, 1),
(21, '2025-01-11 12:02:21.518431', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(22, '2025-01-11 12:06:06.989047', '3', '', 3, '', 24, 1),
(23, '2025-01-11 12:06:13.375916', '2', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(24, '2025-01-11 12:06:21.109459', '5', 'Souscription de OUEDRAOGO Moussa - TX-1736596960739', 3, '', 22, 1),
(25, '2025-01-11 12:06:21.109459', '4', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736596506124', 3, '', 22, 1),
(26, '2025-01-11 13:22:02.942336', '29', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(27, '2025-01-11 13:22:06.622519', '27', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(28, '2025-01-11 13:22:10.051702', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(29, '2025-01-11 13:22:13.250940', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(30, '2025-01-11 13:22:16.158718', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(31, '2025-01-11 13:22:20.212653', '41', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(32, '2025-01-11 13:22:23.137698', '40', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(33, '2025-01-11 13:22:26.556423', '39', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(34, '2025-01-11 13:22:29.322726', '38', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(35, '2025-01-11 13:22:32.861376', '31', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(36, '2025-01-11 13:22:36.795984', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(37, '2025-01-11 13:22:41.014210', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(38, '2025-01-11 13:23:01.266908', '11', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(39, '2025-01-11 13:23:01.266908', '10', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(40, '2025-01-11 13:23:01.266908', '9', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(41, '2025-01-11 13:23:01.266908', '8', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(42, '2025-01-11 13:23:01.266908', '7', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(43, '2025-01-11 13:23:01.266908', '6', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(44, '2025-01-11 13:23:01.266908', '5', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(45, '2025-01-11 13:23:01.266908', '4', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(46, '2025-01-11 13:23:05.699387', '4', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(47, '2025-01-11 13:23:05.699387', '3', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(48, '2025-01-11 13:23:11.263449', '15', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736601689387', 3, '', 22, 1),
(49, '2025-01-11 13:23:11.263449', '14', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736601288379', 3, '', 22, 1),
(50, '2025-01-11 13:23:11.263449', '13', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736600917259', 3, '', 22, 1),
(51, '2025-01-11 13:23:11.263449', '12', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736600567715', 3, '', 22, 1),
(52, '2025-01-11 13:23:11.263449', '11', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736600305195', 3, '', 22, 1),
(53, '2025-01-11 13:23:11.263449', '10', 'Souscription de OUEDRAOGO Moussa - TX-1736600163236', 3, '', 22, 1),
(54, '2025-01-11 13:23:11.263449', '9', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736599119011', 3, '', 22, 1),
(55, '2025-01-11 13:23:11.263449', '8', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736597634580', 3, '', 22, 1),
(56, '2025-01-11 13:23:11.263449', '7', 'Souscription de OUEDRAOGO Moussa - TX-1736597372436', 3, '', 22, 1),
(57, '2025-01-11 13:23:11.263449', '6', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736597351716', 3, '', 22, 1),
(58, '2025-01-11 15:22:14.809760', '19', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736608912738', 3, '', 22, 1),
(59, '2025-01-11 15:22:14.809760', '18', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736603593707', 3, '', 22, 1),
(60, '2025-01-11 15:22:14.809760', '17', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736602769027', 3, '', 22, 1),
(61, '2025-01-11 15:22:14.809760', '16', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736602445468', 3, '', 22, 1),
(62, '2025-01-11 15:22:22.527294', '15', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(63, '2025-01-11 15:22:22.527294', '14', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(64, '2025-01-11 15:22:22.527294', '13', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(65, '2025-01-11 15:22:22.527294', '12', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(66, '2025-01-11 15:27:21.240852', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(67, '2025-01-11 15:27:24.563680', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(68, '2025-01-11 15:27:27.773708', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(69, '2025-01-11 15:27:30.457863', '31', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(70, '2025-01-11 15:27:33.084246', '25', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(71, '2025-01-11 15:27:36.093842', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(72, '2025-01-11 15:27:38.861249', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(73, '2025-01-11 15:28:03.817823', '17', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(74, '2025-01-11 15:28:03.817823', '16', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(75, '2025-01-11 15:28:08.288115', '5', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(76, '2025-01-11 15:28:13.075113', '22', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736609205210', 3, '', 22, 1),
(77, '2025-01-11 15:28:13.075113', '21', 'Souscription de OUEDRAOGO Moussa - TX-1736609166345', 3, '', 22, 1),
(78, '2025-01-11 15:28:13.075113', '20', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736608953801', 3, '', 22, 1),
(79, '2025-01-11 22:51:54.769828', '1', 'Ecobank (146708)', 2, '[{\"changed\": {\"fields\": [\"Num\\u00e9ro de compte\"]}}]', 17, 1),
(80, '2025-01-12 23:43:36.357069', '7', 'Paiement de ENTREPRISE FASO SERVICES SARL - TX-1736701409078', 2, '[{\"changed\": {\"fields\": [\"Statut du Paiement\"]}}]', 20, 1),
(81, '2025-01-15 10:03:30.209326', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Code\", \"Intitul\\u00e9\"]}}]', 11, 1),
(82, '2025-01-15 10:03:45.617308', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(83, '2025-01-15 10:03:56.639607', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Date de fin de l\'op\\u00e9ration\"]}}]', 11, 1),
(84, '2025-01-15 10:05:44.499947', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(85, '2025-01-15 10:39:08.453021', '29', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(86, '2025-01-15 10:39:15.187008', '28', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(87, '2025-01-15 10:39:18.847145', '27', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(88, '2025-01-15 10:39:22.344023', '26', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(89, '2025-01-15 10:39:26.518040', '20', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(90, '2025-01-15 10:39:29.834510', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(91, '2025-01-15 10:39:32.995750', '41', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(92, '2025-01-15 10:39:37.222960', '31', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(93, '2025-01-15 10:39:41.891621', '24', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(94, '2025-01-15 10:39:45.533864', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(95, '2025-01-15 10:39:59.509303', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(96, '2025-01-15 10:40:04.962113', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(97, '2025-01-15 14:48:52.038992', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(98, '2025-01-15 14:48:55.313060', '26', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(99, '2025-01-15 14:48:58.735877', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(100, '2025-01-15 14:49:01.472963', '20', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(101, '2025-01-15 14:49:04.092337', '24', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(102, '2025-01-15 14:49:06.673858', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(103, '2025-01-15 14:49:10.311251', '38', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(104, '2025-01-15 14:49:14.136128', '25', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(105, '2025-01-15 14:49:17.179043', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(106, '2025-01-15 14:49:19.800608', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(107, '2025-01-15 15:12:09.889231', '8', 'Paiement de OUEDRAOGO Moussa - TX-1736900493112', 3, '', 20, 1),
(108, '2025-01-15 15:12:09.889231', '7', 'Paiement de ENTREPRISE FASO SERVICES SARL - TX-1736701409078', 3, '', 20, 1),
(109, '2025-01-15 15:12:09.889231', '6', 'Paiement de OUEDRAOGO Moussa - TX-1736700754325', 3, '', 20, 1),
(110, '2025-01-15 15:12:09.889231', '5', 'Paiement de OUEDRAOGO Moussa - TX-1736699168108', 3, '', 20, 1),
(111, '2025-01-15 15:12:09.889231', '4', 'Paiement de OUEDRAOGO Moussa - TX-1736630992125', 3, '', 20, 1),
(112, '2025-01-15 15:12:09.889231', '3', 'Paiement de OUEDRAOGO Moussa - TX-1736630712573', 3, '', 20, 1),
(113, '2025-01-15 15:12:09.889231', '2', 'Paiement de OUEDRAOGO Moussa - TX-1736611625353', 3, '', 20, 1),
(114, '2025-01-15 15:12:37.442866', '37', 'Souscription de OUE SERGE GEDEON - TX-1736953149195', 3, '', 22, 1),
(115, '2025-01-15 15:12:37.443871', '36', 'Souscription de OUE SERGE GEDEON - TX-1736952567668', 3, '', 22, 1),
(116, '2025-01-15 15:12:37.443871', '35', 'Souscription de OUE SERGE GEDEON - TX-1736940380517', 3, '', 22, 1),
(117, '2025-01-15 15:12:37.443871', '34', 'Souscription de OUE SERGE GEDEON - TX-1736940202997', 3, '', 22, 1),
(118, '2025-01-15 15:12:37.443871', '33', 'Souscription de OUEDRAOGO Moussa - TX-1736900493112', 3, '', 22, 1),
(119, '2025-01-15 15:12:37.443871', '32', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736701409078', 3, '', 22, 1),
(120, '2025-01-15 15:12:37.443871', '31', 'Souscription de OUEDRAOGO Moussa - TX-1736700754325', 3, '', 22, 1),
(121, '2025-01-15 15:12:37.443871', '30', 'Souscription de OUEDRAOGO Moussa - TX-1736699168108', 3, '', 22, 1),
(122, '2025-01-15 15:12:37.443871', '29', 'Souscription de OUEDRAOGO Moussa - TX-1736630992125', 3, '', 22, 1),
(123, '2025-01-15 15:12:37.443871', '28', 'Souscription de OUEDRAOGO Moussa - TX-1736630712573', 3, '', 22, 1),
(124, '2025-01-15 15:12:37.443871', '27', 'Souscription de OUEDRAOGO Moussa - TX-1736611625353', 3, '', 22, 1),
(125, '2025-01-15 15:12:37.443871', '26', 'Souscription de OUEDRAOGO Moussa - TX-1736611528049', 3, '', 22, 1),
(126, '2025-01-15 15:12:37.443871', '25', 'Souscription de OUEDRAOGO Moussa - TX-1736611473041', 3, '', 22, 1),
(127, '2025-01-15 15:12:37.443871', '24', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736610924957', 3, '', 22, 1),
(128, '2025-01-15 15:12:37.443871', '23', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736610874721', 3, '', 22, 1),
(129, '2025-01-15 15:12:53.237606', '13', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(130, '2025-01-15 15:12:53.237606', '12', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(131, '2025-01-15 15:12:53.237606', '11', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(132, '2025-01-15 15:12:53.237606', '10', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(133, '2025-01-15 15:12:53.237606', '9', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(134, '2025-01-15 15:12:53.237606', '8', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(135, '2025-01-15 15:12:53.237606', '7', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(136, '2025-01-15 15:12:53.237606', '6', 'OUEDRAOGO Moussa', 3, '', 23, 1),
(137, '2025-01-15 15:12:58.165122', '20', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(138, '2025-01-15 15:12:58.165122', '19', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(139, '2025-01-15 15:12:58.165122', '18', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(140, '2025-01-15 15:31:28.171754', '9', 'Paiement de OUE SERGE GEDEON - TX-1736954867276', 3, '', 20, 1),
(141, '2025-01-15 15:31:35.141317', '39', 'Souscription de OUE SERGE GEDEON - TX-1736954867276', 3, '', 22, 1),
(142, '2025-01-15 15:31:35.141317', '38', 'Souscription de OUE SERGE GEDEON - TX-1736954298710', 3, '', 22, 1),
(143, '2025-01-15 16:00:23.746287', '21', 'ENTREPRISE FASO SERVICES SARL', 3, '', 24, 1),
(144, '2025-01-15 16:00:29.780571', '40', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736955612468', 3, '', 22, 1),
(145, '2025-01-15 16:00:59.507676', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(146, '2025-01-15 16:01:05.093416', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(147, '2025-01-15 16:01:08.138673', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(148, '2025-01-15 16:01:11.058675', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(149, '2025-01-15 16:01:13.651213', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(150, '2025-01-15 16:04:01.242278', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(151, '2025-01-15 16:04:14.831029', '14', 'OUE SERGE GEDEON', 3, '', 23, 1),
(152, '2025-01-15 16:39:30.349626', '11', 'Paiement de OUE SERGE GEDEON - TX-1736958050053', 3, '', 20, 1),
(153, '2025-01-15 16:39:37.161998', '41', 'Souscription de OUE SERGE GEDEON - TX-1736958050053', 3, '', 22, 1),
(154, '2025-01-15 16:47:35.740440', '12', 'Paiement de OUE SERGE GEDEON - TX-1736959204935', 3, '', 20, 1),
(155, '2025-01-15 16:47:41.523626', '42', 'Souscription de OUE SERGE GEDEON - TX-1736959204935', 3, '', 22, 1),
(156, '2025-01-15 16:54:51.914547', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(157, '2025-01-15 16:54:57.517425', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(158, '2025-01-15 16:55:04.093428', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(159, '2025-01-15 17:41:41.463281', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(160, '2025-01-15 17:41:45.652539', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(161, '2025-01-15 17:41:49.559344', '25', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(162, '2025-01-15 17:41:55.060493', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(163, '2025-01-15 17:42:00.104280', '18', 'Paiement de 11111111 - TX-1736962289199', 3, '', 20, 1),
(164, '2025-01-15 17:42:00.104280', '17', 'Paiement de NADRE NADRE - TX-1736961451087', 3, '', 20, 1),
(165, '2025-01-15 17:42:00.104280', '16', 'Paiement de OUEDRAOGO Moussa - TX-1736960977551', 3, '', 20, 1),
(166, '2025-01-15 17:42:00.105279', '15', 'Paiement de SERGE SERGE  - TX-1736960494142', 3, '', 20, 1),
(167, '2025-01-15 17:42:00.105279', '14', 'Paiement de OUE SERGE - TX-1736960150398', 3, '', 20, 1),
(168, '2025-01-15 17:42:00.105279', '13', 'Paiement de OUE SERGE - TX-1736959682814', 3, '', 20, 1),
(169, '2025-01-15 17:42:06.079581', '48', 'Souscription de 11111111 - TX-1736962289199', 3, '', 22, 1),
(170, '2025-01-15 17:42:06.079581', '47', 'Souscription de NADRE NADRE - TX-1736961451087', 3, '', 22, 1),
(171, '2025-01-15 17:42:06.079581', '46', 'Souscription de OUEDRAOGO Moussa - TX-1736960977551', 3, '', 22, 1),
(172, '2025-01-15 17:42:06.079581', '45', 'Souscription de SERGE SERGE  - TX-1736960494142', 3, '', 22, 1),
(173, '2025-01-15 17:42:06.079581', '44', 'Souscription de OUE SERGE - TX-1736960150398', 3, '', 22, 1),
(174, '2025-01-15 17:42:06.079581', '43', 'Souscription de OUE SERGE - TX-1736959682814', 3, '', 22, 1),
(175, '2025-01-15 17:42:35.647012', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(176, '2025-01-15 21:37:54.939526', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(177, '2025-01-15 21:37:57.837320', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(178, '2025-01-15 21:38:00.889422', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(179, '2025-01-15 21:38:04.163722', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(180, '2025-01-15 22:25:23.696093', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(181, '2025-01-15 22:25:32.735668', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(182, '2025-01-15 23:08:12.168295', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(183, '2025-01-15 23:08:16.983275', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(184, '2025-01-15 23:08:25.649086', '22', 'Paiement de OUEDRAOGO Moussa - TX-1736981868760', 3, '', 20, 1),
(185, '2025-01-15 23:08:25.649086', '21', 'Paiement de OUEDRAOGO Moussa - TX-1736981657281', 3, '', 20, 1),
(186, '2025-01-15 23:08:25.649086', '20', 'Paiement de OUEDRAOGO Moussa - TX-1736980745648', 3, '', 20, 1),
(187, '2025-01-15 23:08:25.649086', '19', 'Paiement de OUEDRAOGO Moussa - TX-1736980724343', 3, '', 20, 1),
(188, '2025-01-15 23:08:31.301785', '52', 'Souscription de OUEDRAOGO Moussa - TX-1736981868760', 3, '', 22, 1),
(189, '2025-01-15 23:08:31.301785', '51', 'Souscription de OUEDRAOGO Moussa - TX-1736981657281', 3, '', 22, 1),
(190, '2025-01-15 23:08:31.301785', '50', 'Souscription de OUEDRAOGO Moussa - TX-1736980745648', 3, '', 22, 1),
(191, '2025-01-15 23:08:31.301785', '49', 'Souscription de OUEDRAOGO Moussa - TX-1736980724343', 3, '', 22, 1),
(192, '2025-01-15 23:19:15.179027', '54', 'Souscription de OUEDRAOGO Moussa - TX-1736983133945', 3, '', 22, 1),
(193, '2025-01-15 23:19:15.179027', '53', 'Souscription de OUEDRAOGO Moussa - TX-1736982962369', 3, '', 22, 1),
(194, '2025-01-15 23:19:20.727897', '24', 'Paiement de OUEDRAOGO Moussa - TX-1736983133945', 3, '', 20, 1),
(195, '2025-01-15 23:19:20.727897', '23', 'Paiement de OUEDRAOGO Moussa - TX-1736982962369', 3, '', 20, 1),
(196, '2025-01-15 23:36:29.884395', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(197, '2025-01-15 23:36:33.505239', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(198, '2025-01-15 23:36:37.481486', '24', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(199, '2025-01-15 23:36:40.646972', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(200, '2025-01-15 23:43:24.702422', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(201, '2025-01-15 23:43:30.307831', '25', 'Paiement de OUEDRAOGO Moussa - TX-1736984477209', 3, '', 20, 1),
(202, '2025-01-15 23:43:36.406291', '55', 'Souscription de OUEDRAOGO Moussa - TX-1736984477209', 3, '', 22, 1),
(203, '2025-01-15 23:45:51.280009', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(204, '2025-01-15 23:45:55.984845', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(205, '2025-01-15 23:45:59.907793', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(206, '2025-01-16 00:23:16.335643', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(207, '2025-01-16 00:23:19.058922', '20', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(208, '2025-01-16 00:23:22.172604', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(209, '2025-01-16 00:23:25.321772', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(210, '2025-01-16 00:23:37.274524', '26', 'Paiement de ENTREPRISE FASO SERVICES SARL - TX-1736986128917', 3, '', 20, 1),
(211, '2025-01-16 00:23:43.432582', '56', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736986128917', 3, '', 22, 1),
(212, '2025-01-16 17:02:26.051332', '58', 'Souscription de ENTREPRISE FASO SERVICES SARL - TX-1736987518491', 3, '', 22, 1),
(213, '2025-01-16 17:02:26.051332', '57', 'Souscription de OUEDRAOGO Moussa - TX-1736987040267', 3, '', 22, 1),
(214, '2025-01-16 17:02:38.661819', '28', 'Paiement de ENTREPRISE FASO SERVICES SARL - TX-1736987518491', 3, '', 20, 1),
(215, '2025-01-16 17:02:38.661819', '27', 'Paiement de OUEDRAOGO Moussa - TX-1736987040267', 3, '', 20, 1),
(216, '2025-01-16 17:02:52.020133', '27', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(217, '2025-01-16 17:02:56.292360', '21', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\", \"Bloqu\\u00e9\"]}}]', 9, 1),
(218, '2025-01-16 17:03:00.009804', '20', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(219, '2025-01-16 17:03:02.903066', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(220, '2025-01-16 17:03:06.035506', '25', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(221, '2025-01-16 17:03:09.090042', '24', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(222, '2025-01-16 17:03:11.767123', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(223, '2025-01-16 17:03:14.375800', '22', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(224, '2025-01-16 17:03:45.250890', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(225, '2025-01-16 17:03:57.121264', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(226, '2025-01-16 17:04:04.809081', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(227, '2025-01-16 17:10:27.391951', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(228, '2025-01-16 17:10:30.422004', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(229, '2025-01-16 17:10:33.691634', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(230, '2025-01-16 17:11:38.488861', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(231, '2025-01-16 17:11:43.564691', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(232, '2025-01-16 17:11:47.715054', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(233, '2025-01-16 17:11:54.785384', '19', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(234, '2025-01-16 17:11:57.692013', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(235, '2025-01-16 17:12:35.490779', '18', 'SI - C1 - 300', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(236, '2025-01-16 17:12:38.888091', '39', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Pay\\u00e9\"]}}]', 9, 1),
(237, '2025-01-16 17:14:46.683512', '23', 'SI - C2 - 600', 2, '[{\"changed\": {\"fields\": [\"Bloqu\\u00e9\"]}}]', 9, 1),
(238, '2025-01-16 17:14:59.888348', '5', 'Vente des parcelle Yopougon Sideci (YOP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(239, '2025-01-16 17:15:04.739512', '4', 'Vente des parcelle site Yopougon (OP2)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1),
(240, '2025-01-16 17:15:09.355826', '2', 'Vente site de Tougan (OP1)', 2, '[{\"changed\": {\"fields\": [\"Montant de la souscription (FCFA)\"]}}]', 11, 1);

-- --------------------------------------------------------

--
-- Structure de la table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
CREATE TABLE IF NOT EXISTS `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `model` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=MyISAM AUTO_INCREMENT=25 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_content_type`
--

INSERT INTO `django_content_type` (`id`, `app_label`, `model`) VALUES
(1, 'admin', 'logentry'),
(2, 'auth', 'permission'),
(3, 'auth', 'group'),
(4, 'contenttypes', 'contenttype'),
(5, 'sessions', 'session'),
(6, 'utilisateurs', 'role'),
(7, 'utilisateurs', 'utilisateur'),
(8, 'operations', 'condition'),
(9, 'operations', 'listesparcelles'),
(10, 'operations', 'localite'),
(11, 'operations', 'operations'),
(12, 'operations', 'parcelle'),
(13, 'operations', 'positionparcelle'),
(14, 'operations', 'processusattribution'),
(15, 'operations', 'projet'),
(16, 'operations', 'typeparcelle'),
(17, 'paiements', 'comptebancaire'),
(18, 'paiements', 'modepaiement'),
(19, 'paiements', 'quittance'),
(20, 'paiements', 'paiement'),
(21, 'souscriptions', 'typesouscripteur'),
(22, 'souscriptions', 'souscriptioneffectuee'),
(23, 'souscriptions', 'souscripteurphysique'),
(24, 'souscriptions', 'souscripteurmorale');

-- --------------------------------------------------------

--
-- Structure de la table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
CREATE TABLE IF NOT EXISTS `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `name` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=35 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_migrations`
--

INSERT INTO `django_migrations` (`id`, `app`, `name`, `applied`) VALUES
(1, 'contenttypes', '0001_initial', '2025-01-11 11:33:39.103964'),
(2, 'contenttypes', '0002_remove_content_type_name', '2025-01-11 11:33:39.164965'),
(3, 'auth', '0001_initial', '2025-01-11 11:33:39.412965'),
(4, 'auth', '0002_alter_permission_name_max_length', '2025-01-11 11:33:39.444965'),
(5, 'auth', '0003_alter_user_email_max_length', '2025-01-11 11:33:39.450965'),
(6, 'auth', '0004_alter_user_username_opts', '2025-01-11 11:33:39.454964'),
(7, 'auth', '0005_alter_user_last_login_null', '2025-01-11 11:33:39.461965'),
(8, 'auth', '0006_require_contenttypes_0002', '2025-01-11 11:33:39.463969'),
(9, 'auth', '0007_alter_validators_add_error_messages', '2025-01-11 11:33:39.467962'),
(10, 'auth', '0008_alter_user_username_max_length', '2025-01-11 11:33:39.471963'),
(11, 'auth', '0009_alter_user_last_name_max_length', '2025-01-11 11:33:39.476970'),
(12, 'auth', '0010_alter_group_name_max_length', '2025-01-11 11:33:39.509969'),
(13, 'auth', '0011_update_proxy_permissions', '2025-01-11 11:33:39.517963'),
(14, 'auth', '0012_alter_user_first_name_max_length', '2025-01-11 11:33:39.523966'),
(15, 'utilisateurs', '0001_initial', '2025-01-11 11:33:39.929965'),
(16, 'admin', '0001_initial', '2025-01-11 11:33:40.139966'),
(17, 'admin', '0002_logentry_remove_auto_add', '2025-01-11 11:33:40.148965'),
(18, 'admin', '0003_logentry_add_action_flag_choices', '2025-01-11 11:33:40.156964'),
(19, 'operations', '0001_initial', '2025-01-11 11:33:40.282964'),
(20, 'souscriptions', '0001_initial', '2025-01-11 11:33:41.209969'),
(21, 'paiements', '0001_initial', '2025-01-11 11:33:41.518962'),
(22, 'operations', '0002_initial', '2025-01-11 11:33:43.147964'),
(23, 'paiements', '0002_initial', '2025-01-11 11:33:43.315965'),
(24, 'sessions', '0001_initial', '2025-01-11 11:33:43.358965'),
(25, 'paiements', '0003_delete_quittance_and_more', '2025-01-11 16:01:56.461015'),
(26, 'paiements', '0004_remove_paiement_date_confirmation', '2025-01-11 16:20:47.322596'),
(27, 'paiements', '0005_remove_paiement_numero_paiement', '2025-01-11 20:44:41.429538'),
(28, 'souscriptions', '0002_souscriptioneffectuee_compte_bancaire_and_more', '2025-01-11 21:18:51.582857'),
(29, 'souscriptions', '0003_remove_souscriptioneffectuee_compte_bancaire_and_more', '2025-01-11 21:24:25.893261'),
(30, 'souscriptions', '0004_souscriptioneffectuee_statut', '2025-01-16 17:55:15.680721'),
(31, 'paiements', '0006_alter_paiement_date_paiement', '2025-01-16 18:01:09.330423'),
(32, 'souscriptions', '0005_alter_souscripteurmorale_date_creation_and_more', '2025-01-16 18:01:09.415584'),
(33, 'operations', '0003_alter_projet_date_debut_alter_projet_date_fin', '2025-01-16 18:11:43.956522'),
(34, 'operations', '0004_alter_operations_date_debut_operation_and_more', '2025-01-16 18:17:51.739049');

-- --------------------------------------------------------

--
-- Structure de la table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
CREATE TABLE IF NOT EXISTS `django_session` (
  `session_key` varchar(40) COLLATE utf8mb4_unicode_ci NOT NULL,
  `session_data` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `django_session`
--

INSERT INTO `django_session` (`session_key`, `session_data`, `expire_date`) VALUES
('wq2txu0qqmjad01bsshwwxpgr0zio54i', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tWZqa:7EvfuPHTScqLy_0VVxetRsBq-D2TT4GJwakt78PGoUM', '2025-01-25 11:40:08.262849'),
('5ffcewcmlynyq5j2ddo2hmgrdsy6xu4x', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tWbPQ:kOzq-KEcMiquj8VT7SNHc64NHdT8-1OnRmO2ZghLkE4', '2025-01-25 13:20:12.736274'),
('rt1svm8tyogc4vc7sbprfy8wlzovn54g', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tWd2c:O6YdI25G5JFyHn99Hd488HBlAApgtghlMpSFXNOZMHU', '2025-01-25 15:04:46.420393'),
('ovqi1l38qceo159j9i5tvbfxv3vfe7jx', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tWd6S:SZeNamVbeFJfFhJKgE8S5kr-rBaRfZX8E_QKUylAkDY', '2025-01-25 15:08:44.830747'),
('ezy6yvjng4e3ap0fhcdzypkcc453tpro', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tWdyo:NiUsVugKlFoPh3Em5rtnDWQ9dPw8zBeR6e7ado16ZpI', '2025-01-25 16:04:54.711249'),
('898hlm5dnp3uri0c02hroktvi62o9io3', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tX0ki:iixAFzO1C61qaJrYRA4WxKkpvhNXQxu_OWjbqxLIfU8', '2025-01-26 16:23:52.391354'),
('su4i3d3u59cwrjoj1lxr02yozkldajjn', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tX0rE:DNDylIoKLIjEzVRjPqd1YcsBBTbHEm3CJi7lWDt8LX0', '2025-01-26 16:30:36.357619'),
('g99h5jocrql2rovw9v7tlvofec0hmfo2', '.eJxVkc1uqzAUhN-F9S2yweYnO257g0hrUEKSJtlEtjHBqYNRoC1Q9d1r2uqqXZ4z38zR0bxZR_rcVcfnVlyPsrBmFrT-_Nwxyp9EPQnFmdYnbXNdd1fJ7Amxv9XWJroQ6u83-yugom1l3LTk2BVYhIFHMS5LwUqAyhBDJwiQR32PCcYd4RUUwxAFPgh44LJAIBxAyqhvQpU8FZKbuGN3pXVLeSd1bc3erE6bs-aGGBZA7CKZycX9Fi7lw-2iYjGf5mQzJjCVi9A2UHOYhw2rDy_0MVXJWcv0nCAy7t1sHU2msYjnQzEPn_a71adOztGQ5uCV5KBP86jP7vRrttaA5EmbXLaIx2oQ2_98n47EJXdLl4ynvlzacHN_iflqF0dF93jo96qiHYucE6kHqW8UazRUnJcQu__Mmz-e-2okz9JovVndQN_1Qg9hOFV0MTXQurNmEADjEUo0la6FwR3H85GDgYOR4Rp65UIp8RXlQOv9_QOHGqRc:1tY7oe:vb1Qlq2FUouKVlSXAmAyUrc1ogDn47TdXJ4F7-yLPck', '2025-01-29 18:08:32.370849'),
('p4jeui6x3z6zuo1v21i7t7p5urnxp87g', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tY4FW:nugkuPWYHfhWSRm7aDR18pheSRCbXS6Up8kQkKYOSoA', '2025-01-29 14:20:02.165050'),
('8tox720y69qgwi4jov029hpxvy5m0qqb', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tY4Ft:cmJjoFLwrsOFDTB91A0S55PAXoUgFy2eFumy8gY9xjE', '2025-01-29 14:20:25.203405'),
('wmds4vkcrsuf4ffnf8wvtgbvhpduv7vq', '.eJxVjEEOwiAQRe_C2pDSMjC4dO8ZyAwMUjVtUtqV8e7apAvd_vfef6lI21rj1mSJY1ZnZdTpd2NKD5l2kO803Wad5mldRta7og_a9HXO8rwc7t9BpVa_NZUEg4AEdARQinDpbAlgekTryDsWTr24TGCCRd9hwoFRLKAhJq_eH_72OE4:1tYTBm:cwcTIe5TCVY7eKfI9Dn9tVsxLh30A2l6mA9n6KA3NmQ', '2025-01-30 16:57:50.461689');

-- --------------------------------------------------------

--
-- Structure de la table `operations_condition`
--

DROP TABLE IF EXISTS `operations_condition`;
CREATE TABLE IF NOT EXISTS `operations_condition` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `intitule` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `condition_souscription` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `methode_attribution` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `documents_requis` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `date_modification` datetime(6) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `operation_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  KEY `operations_condition_operation_id_b498b46c` (`operation_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_condition`
--

INSERT INTO `operations_condition` (`id`, `code`, `intitule`, `condition_souscription`, `methode_attribution`, `documents_requis`, `date_creation`, `date_modification`, `actif`, `operation_id`) VALUES
(1, 'C1', 'Condition site TOUGAN', 'Pour prétendre à l’attribution d’un terrain au Burkina Faso, le demandeur doit remplir certaines conditions. Tout d’abord, il doit être de nationalité burkinabè ou justifier d’un investissement économique significatif dans le pays pour les étrangers. Les entreprises, quant à elles, doivent être légalement enregistrées et exercer des activités conformes à la législation en vigueur. Les demandeurs doivent également prouver leur capacité à mettre en valeur le terrain, que ce soit pour des projets résidentiels, agricoles, industriels ou commerciaux.', 'Les terrains sont classés selon leur vocation : urbains, ruraux, agricoles, industriels ou à usage mixte. Les terrains urbains sont généralement destinés à la construction de logements, d’infrastructures publiques ou de projets immobiliers. Les terrains ruraux et agricoles sont attribués pour soutenir le développement de l’agriculture, de l’élevage ou de l’agro-industrie. Les terrains industriels, quant à eux, sont réservés aux projets de production, de transformation ou de services à grande échelle.', 'Au Burkina Faso, l’attribution de terrains est régie par des règles et des procédures bien définies, visant à garantir une gestion transparente et équitable des ressources foncières. Ces conditions sont encadrées par des textes législatifs et réglementaires, notamment le Code général des collectivités territoriales, la Loi portant réorganisation agraire et foncière (RAF), ainsi que les décrets d’application relatifs à la gestion du domaine foncier national. L’objectif est de répondre aux besoins en logement, en développement économique et en infrastructures tout en préservant les droits des populations locales.', '2025-01-06 14:50:27.641850', '2025-01-09 17:20:10.734839', 1, 2),
(3, 'CD2', 'conditon site de yoppougon', '3. Prix de vente\r\nMontant total : [Montant en chiffres et en lettres].\r\n\r\nModalités de paiement :\r\n\r\nAcompte de [X%] à la signature du contrat.\r\n\r\nSolde à payer dans un délai de [X jours/mois] après [événement spécifique, par exemple l\'obtention du permis de construire].\r\n\r\nMoyens de paiement acceptés : [chèque, virement bancaire, etc.].\r\n\r\n4. Frais et taxes\r\nFrais de notaire : À la charge de [l\'acheteur/le vendeur/les deux parties selon accord].\r\n\r\nTaxes foncières : Le vendeur s\'engage à régler les taxes foncières jusqu\'au [date], après quoi elles seront à la charge de l\'acheteur.', 'dans ajouter une operation quand on importe les parcelle il ya un cahmps POSITION et ce champs POSITIONest le code de la posiiton de parcelel qui se trouve dans positionparcelle  donc quan don importe des parcelle faut que les position des parcelle s\'ajoute en meme temps dans l\'opertation aussi directement via le code de la position , la position de la parcelle s\'ajoute et se selectione en meme temps sur l\'operation ', '5. Obligations du vendeur\r\nGarantir que la parcelle est libre de tout droit, hypothèque ou servitude non mentionnée.\r\n\r\nFournir tous les documents nécessaires (titre de propriété, plan cadastral, etc.).\r\n\r\nSignaler toute restriction d\'usage ou servitude existante.\r\n\r\n6. Obligations de l\'acheteur\r\nRespecter les modalités de paiement convenues.\r\n\r\nPrendre connaissance des règles d\'urbanisme et des restrictions applicables à la parcelle.\r\n\r\nS\'acquitter des frais de notaire et taxes à sa charge.\r\n\r\n7. Acte de vente', '2025-01-09 14:42:38.504261', '2025-01-09 19:50:41.908207', 1, 4),
(4, 'AAAA', 'aaaaaa', 'aaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaa', 'aaaaaaaaaaaaaaaaaaaaaaaaaa', '2025-01-09 19:31:39.728658', '2025-01-09 19:31:47.320108', 1, 5);

-- --------------------------------------------------------

--
-- Structure de la table `operations_listesparcelles`
--

DROP TABLE IF EXISTS `operations_listesparcelles`;
CREATE TABLE IF NOT EXISTS `operations_listesparcelles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `site` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `zone` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `section` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `parcelle` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `surface` int NOT NULL,
  `cout_m2` int NOT NULL,
  `acompte` int NOT NULL,
  `reste_a_payer` int NOT NULL,
  `cout_total` int NOT NULL,
  `paye` tinyint(1) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `bloquer` tinyint(1) NOT NULL,
  `date_ajout` datetime(6) NOT NULL,
  `operation_id` bigint DEFAULT NULL,
  `position_id` bigint DEFAULT NULL,
  `usage_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `operations_listesparcelles_operation_id_a69bd386` (`operation_id`),
  KEY `operations_listesparcelles_position_id_a84ffb50` (`position_id`),
  KEY `operations_listesparcelles_usage_id_ff481fd2` (`usage_id`)
) ENGINE=MyISAM AUTO_INCREMENT=42 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_listesparcelles`
--

INSERT INTO `operations_listesparcelles` (`id`, `code`, `site`, `zone`, `section`, `lot`, `parcelle`, `surface`, `cout_m2`, `acompte`, `reste_a_payer`, `cout_total`, `paye`, `actif`, `bloquer`, `date_ajout`, `operation_id`, `position_id`, `usage_id`) VALUES
(29, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.540259', 4, 4, 2),
(30, 'SI', 'SI', 'C2', 'SE', '5', '600', 600, 40000, 10000000, 14000000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.542267', 4, 1, 1),
(31, 'SI', 'SI', 'C2', 'SE', '6', '600', 600, 40000, 12000000, 12000000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.544260', 4, 1, 1),
(32, 'SI', 'SI', 'C2', 'SE', '7', '600', 600, 40000, 15000000, 9000000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.546259', 4, 2, 1),
(28, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.538260', 4, 4, 2),
(27, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 7800000, 0, 1, 0, '2025-01-09 14:42:38.535262', 4, 3, 2),
(26, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 7800000, 0, 1, 0, '2025-01-09 14:42:38.531277', 4, 3, 2),
(18, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 7800000, 0, 1, 0, '2025-01-06 14:50:27.663844', 2, 3, 2),
(19, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 7800000, 1, 1, 1, '2025-01-06 14:50:27.666845', 2, 3, 2),
(20, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 24000000, 1, 1, 1, '2025-01-06 14:50:27.669843', 2, 4, 2),
(21, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 24000000, 1, 1, 1, '2025-01-06 14:50:27.671842', 2, 4, 2),
(22, 'SI', 'SI', 'C2', 'SE', '5', '600', 600, 40000, 10000000, 14000000, 24000000, 0, 1, 0, '2025-01-06 14:50:27.676846', 2, 1, 1),
(23, 'SI', 'SI', 'C2', 'SE', '6', '600', 600, 40000, 12000000, 12000000, 24000000, 0, 1, 0, '2025-01-06 14:50:27.678842', 2, 1, 1),
(24, 'SI', 'SI', 'C2', 'SE', '7', '600', 600, 40000, 15000000, 9000000, 24000000, 0, 1, 0, '2025-01-06 14:50:27.681846', 2, 2, 1),
(25, 'SI', 'SI', 'C2', 'SE', '3', '600', 600, 40000, 20000000, 4000000, 24000000, 0, 1, 0, '2025-01-06 14:50:27.684880', 2, 2, 1),
(33, 'SI', 'SI', 'C2', 'SE', '3', '600', 600, 40000, 20000000, 4000000, 24000000, 0, 1, 0, '2025-01-09 14:42:38.549260', 4, 2, 1),
(34, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 7800000, 0, 1, 0, '2025-01-09 19:31:39.753654', 5, 3, 2),
(35, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 7800000, 0, 1, 0, '2025-01-09 19:31:39.756650', 5, 3, 2),
(36, 'SI', 'SI', 'C1', 'SE', '17', '300', 300, 26000, 2000000, 5800000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.759652', 5, 4, 2),
(37, 'SI', 'SI', 'C1', 'SE', '22', '300', 300, 26000, 2500000, 5300000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.762653', 5, 4, 2),
(38, 'SI', 'SI', 'C2', 'SE', '5', '600', 600, 40000, 10000000, 14000000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.764693', 5, 1, 1),
(39, 'SI', 'SI', 'C2', 'SE', '6', '600', 600, 40000, 12000000, 12000000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.767650', 5, 1, 1),
(40, 'SI', 'SI', 'C2', 'SE', '7', '600', 600, 40000, 15000000, 9000000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.769653', 5, 2, 1),
(41, 'SI', 'SI', 'C2', 'SE', '3', '600', 600, 40000, 20000000, 4000000, 24000000, 0, 1, 0, '2025-01-09 19:31:39.772658', 5, 2, 1);

-- --------------------------------------------------------

--
-- Structure de la table `operations_localite`
--

DROP TABLE IF EXISTS `operations_localite`;
CREATE TABLE IF NOT EXISTS `operations_localite` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_localite`
--

INSERT INTO `operations_localite` (`id`, `code`, `nom`, `description`, `actif`) VALUES
(1, 'Tougan', 'Tougan', 'Tougan', 1),
(2, 'Ouaga 2000', 'Ouaga 2000', 'Ouaga 2000', 1),
(3, 'yop', 'Yopougon', 'yopougon', 1);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations`
--

DROP TABLE IF EXISTS `operations_operations`;
CREATE TABLE IF NOT EXISTS `operations_operations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `intitule` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `date_debut_operation` datetime(6) NOT NULL,
  `date_fin_operation` datetime(6) DEFAULT NULL,
  `duree_depot_physique` int UNSIGNED NOT NULL,
  `duree_souscription` int UNSIGNED NOT NULL,
  `montant_souscription` int UNSIGNED NOT NULL,
  `visuel` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `disponible` tinyint(1) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `condition_id` bigint DEFAULT NULL,
  `projet_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `operations_operations_condition_id_cc9555ec` (`condition_id`),
  KEY `operations_operations_projet_id_cc57ff6e` (`projet_id`)
) ;

--
-- Déchargement des données de la table `operations_operations`
--

INSERT INTO `operations_operations` (`id`, `code`, `intitule`, `description`, `date_debut_operation`, `date_fin_operation`, `duree_depot_physique`, `duree_souscription`, `montant_souscription`, `visuel`, `disponible`, `actif`, `condition_id`, `projet_id`) VALUES
(2, 'OP1', 'Vente site de Tougan', 'Un site premium situé dans un quartier calme et verdoyant de Ziniaré.', '2025-01-06 00:00:00.000000', '2025-01-26 00:00:00.000000', 12, 12, 10, 'operations/visuels/parcelle1_D3nSzaj.jpg', 1, 1, 1, 1),
(4, 'OP2', 'Vente des parcelle site Yopougon', 'Ventes des tres  beau site de yopougon sideci akadjoba', '2025-01-09 00:00:00.000000', '2025-01-26 00:00:00.000000', 11, 1, 10, 'operations/visuels/Image1_lHkwrIb.jpg', 1, 1, 3, 2),
(5, 'YOP2', 'Vente des parcelle Yopougon Sideci', 'aaaaaaaa', '2025-01-09 00:00:00.000000', '2025-01-31 00:00:00.000000', 11, 11, 10, '', 1, 1, 4, 2);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_comptes_bancaires`
--

DROP TABLE IF EXISTS `operations_operations_comptes_bancaires`;
CREATE TABLE IF NOT EXISTS `operations_operations_comptes_bancaires` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `comptebancaire_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_co_operations_id_comptebanc_b74c68c1_uniq` (`operations_id`,`comptebancaire_id`),
  KEY `operations_operations_comptes_bancaires_operations_id_cc601d20` (`operations_id`),
  KEY `operations_operations_compt_comptebancaire_id_6f6505cf` (`comptebancaire_id`)
) ENGINE=MyISAM AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_comptes_bancaires`
--

INSERT INTO `operations_operations_comptes_bancaires` (`id`, `operations_id`, `comptebancaire_id`) VALUES
(2, 2, 1),
(4, 4, 1),
(5, 5, 1);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_parcelles`
--

DROP TABLE IF EXISTS `operations_operations_parcelles`;
CREATE TABLE IF NOT EXISTS `operations_operations_parcelles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `listesparcelles_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_pa_operations_id_listesparc_3378ed27_uniq` (`operations_id`,`listesparcelles_id`),
  KEY `operations_operations_parcelles_operations_id_90e73a9e` (`operations_id`),
  KEY `operations_operations_parcelles_listesparcelles_id_29365bfb` (`listesparcelles_id`)
) ENGINE=MyISAM AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_parcelles`
--

INSERT INTO `operations_operations_parcelles` (`id`, `operations_id`, `listesparcelles_id`) VALUES
(1, 2, 18),
(2, 2, 19),
(3, 2, 20),
(4, 2, 21),
(5, 2, 22),
(6, 2, 23),
(7, 2, 24),
(8, 2, 25),
(24, 4, 31),
(23, 4, 30),
(22, 4, 29),
(21, 4, 28),
(20, 4, 27),
(19, 4, 26),
(18, 4, 33),
(17, 4, 32),
(25, 5, 34),
(26, 5, 35),
(27, 5, 36),
(28, 5, 37),
(29, 5, 38),
(30, 5, 39),
(31, 5, 40),
(32, 5, 41);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_positions_parcelles`
--

DROP TABLE IF EXISTS `operations_operations_positions_parcelles`;
CREATE TABLE IF NOT EXISTS `operations_operations_positions_parcelles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `positionparcelle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_po_operations_id_positionpa_ee4441e1_uniq` (`operations_id`,`positionparcelle_id`),
  KEY `operations_operations_positions_parcelles_operations_id_4bdf6f88` (`operations_id`),
  KEY `operations_operations_posit_positionparcelle_id_d319cdab` (`positionparcelle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_positions_parcelles`
--

INSERT INTO `operations_operations_positions_parcelles` (`id`, `operations_id`, `positionparcelle_id`) VALUES
(1, 2, 1),
(2, 2, 2),
(3, 2, 3),
(4, 2, 4),
(12, 4, 4),
(11, 4, 3),
(10, 4, 2),
(9, 4, 1),
(13, 5, 1),
(14, 5, 2),
(15, 5, 3),
(16, 5, 4);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_processus_attributions`
--

DROP TABLE IF EXISTS `operations_operations_processus_attributions`;
CREATE TABLE IF NOT EXISTS `operations_operations_processus_attributions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `processusattribution_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_pr_operations_id_processusa_634450df_uniq` (`operations_id`,`processusattribution_id`),
  KEY `operations_operations_proce_operations_id_466d420a` (`operations_id`),
  KEY `operations_operations_proce_processusattribution_id_6c2c2d47` (`processusattribution_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_processus_attributions`
--

INSERT INTO `operations_operations_processus_attributions` (`id`, `operations_id`, `processusattribution_id`) VALUES
(2, 2, 2),
(8, 4, 3),
(7, 4, 2),
(6, 4, 1),
(9, 5, 2);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_types_parcelles`
--

DROP TABLE IF EXISTS `operations_operations_types_parcelles`;
CREATE TABLE IF NOT EXISTS `operations_operations_types_parcelles` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `typeparcelle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_ty_operations_id_typeparcel_c755c392_uniq` (`operations_id`,`typeparcelle_id`),
  KEY `operations_operations_types_parcelles_operations_id_304781e3` (`operations_id`),
  KEY `operations_operations_types_parcelles_typeparcelle_id_4c6ab79d` (`typeparcelle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_types_parcelles`
--

INSERT INTO `operations_operations_types_parcelles` (`id`, `operations_id`, `typeparcelle_id`) VALUES
(4, 2, 2),
(3, 2, 1),
(8, 4, 2),
(7, 4, 1),
(9, 5, 1);

-- --------------------------------------------------------

--
-- Structure de la table `operations_operations_types_souscripteurs`
--

DROP TABLE IF EXISTS `operations_operations_types_souscripteurs`;
CREATE TABLE IF NOT EXISTS `operations_operations_types_souscripteurs` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `operations_id` bigint NOT NULL,
  `typesouscripteur_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `operations_operations_ty_operations_id_typesouscr_df528855_uniq` (`operations_id`,`typesouscripteur_id`),
  KEY `operations_operations_types_souscripteurs_operations_id_b55ab146` (`operations_id`),
  KEY `operations_operations_types_typesouscripteur_id_38527891` (`typesouscripteur_id`)
) ENGINE=MyISAM AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_operations_types_souscripteurs`
--

INSERT INTO `operations_operations_types_souscripteurs` (`id`, `operations_id`, `typesouscripteur_id`) VALUES
(4, 2, 4),
(3, 2, 3),
(9, 5, 3),
(7, 4, 3),
(10, 4, 4);

-- --------------------------------------------------------

--
-- Structure de la table `operations_parcelle`
--

DROP TABLE IF EXISTS `operations_parcelle`;
CREATE TABLE IF NOT EXISTS `operations_parcelle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `cout_m2` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `operations_positionparcelle`
--

DROP TABLE IF EXISTS `operations_positionparcelle`;
CREATE TABLE IF NOT EXISTS `operations_positionparcelle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `actif` tinyint(1) NOT NULL,
  `type_parcelle_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  KEY `operations_positionparcelle_type_parcelle_id_0b0e35f9` (`type_parcelle_id`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_positionparcelle`
--

INSERT INTO `operations_positionparcelle` (`id`, `code`, `nom`, `description`, `actif`, `type_parcelle_id`) VALUES
(1, 'CM1', 'Commerce Et Service À L\'Angle D\'Une Non Voie Bitumée', 'Commerce Et Service À L\'Angle D\'Une Non Voie Bitumée', 1, 1),
(2, 'CM2', 'Commerce Et Service A L\'Angle D\'Une Voie Bitumée', 'Commerce Et Service A L\'Angle D\'Une Voie Bitumée', 1, 1),
(3, 'HB1', 'Habitation A L\'Angle D\'Une Voie Bitumée', 'Habitation A L\'Angle D\'Une Voie Bitumée', 1, 2),
(4, 'HB2', 'Habitation À L\'Angle D\'Une Voie Non Bitumée', 'Habitation À L\'Angle D\'Une Voie Non Bitumée', 1, 2);

-- --------------------------------------------------------

--
-- Structure de la table `operations_processusattribution`
--

DROP TABLE IF EXISTS `operations_processusattribution`;
CREATE TABLE IF NOT EXISTS `operations_processusattribution` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `date_creation` datetime(6) NOT NULL,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_processusattribution`
--

INSERT INTO `operations_processusattribution` (`id`, `code`, `nom`, `description`, `date_creation`, `actif`) VALUES
(1, 'GG', 'Gré a gré', 'Gré a gré', '2024-12-29 16:28:30.748029', 1),
(2, 'Au Premier Souscripteur', 'Au Premier Souscripteur', 'Au Premier Souscripteur', '2024-12-29 16:28:39.589994', 1),
(3, 'Au plus offrant', 'Au plus offrant', 'Au plus offrant', '2024-12-29 16:29:26.003420', 1);

-- --------------------------------------------------------

--
-- Structure de la table `operations_projet`
--

DROP TABLE IF EXISTS `operations_projet`;
CREATE TABLE IF NOT EXISTS `operations_projet` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `libelle` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `date_debut` datetime(6) DEFAULT NULL,
  `date_fin` datetime(6) DEFAULT NULL,
  `date_creation` datetime(6) NOT NULL,
  `superficie_origine` double NOT NULL,
  `superficie_viabilisee` double NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `date_archivage` datetime(6) DEFAULT NULL,
  `archive` tinyint(1) NOT NULL,
  `localite_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`),
  UNIQUE KEY `libelle` (`libelle`),
  KEY `operations_projet_localite_id_71b4c8bf` (`localite_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_projet`
--

INSERT INTO `operations_projet` (`id`, `code`, `libelle`, `description`, `date_debut`, `date_fin`, `date_creation`, `superficie_origine`, `superficie_viabilisee`, `actif`, `date_archivage`, `archive`, `localite_id`) VALUES
(1, 'Vente des parcelle site Tongan', 'Vente des parcelle site Tongan', 'Vente des parcelle site Tongan', '2024-12-31 00:00:00.000000', '2024-12-31 00:00:00.000000', '2024-12-29 16:31:53.206710', 12, 13, 1, NULL, 0, 1),
(2, 'PR2', 'Site de Yopougon', 'ventes des site de yopougon', '2025-01-09 00:00:00.000000', '2025-01-15 00:00:00.000000', '2025-01-09 14:30:00.012472', 2000, 1800, 1, NULL, 0, 3);

-- --------------------------------------------------------

--
-- Structure de la table `operations_typeparcelle`
--

DROP TABLE IF EXISTS `operations_typeparcelle`;
CREATE TABLE IF NOT EXISTS `operations_typeparcelle` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `operations_typeparcelle`
--

INSERT INTO `operations_typeparcelle` (`id`, `code`, `nom`, `description`, `actif`) VALUES
(1, 'CM', 'Commercial', 'Commercial', 1),
(2, 'HB', 'Habitation', 'Habitation', 1);

-- --------------------------------------------------------

--
-- Structure de la table `paiements_comptebancaire`
--

DROP TABLE IF EXISTS `paiements_comptebancaire`;
CREATE TABLE IF NOT EXISTS `paiements_comptebancaire` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `code_banque` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `code_guichet` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_compte` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rib` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `image` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `paiements_comptebancaire`
--

INSERT INTO `paiements_comptebancaire` (`id`, `code`, `nom`, `description`, `code_banque`, `code_guichet`, `numero_compte`, `rib`, `image`, `actif`) VALUES
(1, '146708', 'Ecobank', 'aaaaaaaaaaaaa', 'BF148', '12112', '121985485001', '12112121121211212112', '', 1);

-- --------------------------------------------------------

--
-- Structure de la table `paiements_modepaiement`
--

DROP TABLE IF EXISTS `paiements_modepaiement`;
CREATE TABLE IF NOT EXISTS `paiements_modepaiement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `paiements_modepaiement`
--

INSERT INTO `paiements_modepaiement` (`id`, `code`, `nom`, `actif`) VALUES
(1, 'MM', 'Mobile Money', 1),
(2, 'Carte Bancaire', 'Carte Bancaire', 1),
(3, 'Mobile Money', 'Mobile Money', 1);

-- --------------------------------------------------------

--
-- Structure de la table `paiements_paiement`
--

DROP TABLE IF EXISTS `paiements_paiement`;
CREATE TABLE IF NOT EXISTS `paiements_paiement` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `date_paiement` datetime(6) NOT NULL,
  `numero_transaction` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant_souscription` decimal(15,2) NOT NULL,
  `statut` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `mode_paiement_id` bigint NOT NULL,
  `souscripteur_morale_id` bigint DEFAULT NULL,
  `souscripteur_physique_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `paiements_paiement_mode_paiement_id_f2fb8bc8` (`mode_paiement_id`),
  KEY `paiements_paiement_souscripteur_morale_id_be876bf0` (`souscripteur_morale_id`),
  KEY `paiements_paiement_souscripteur_physique_id_b69e4aeb` (`souscripteur_physique_id`)
) ;

--
-- Déchargement des données de la table `paiements_paiement`
--

INSERT INTO `paiements_paiement` (`id`, `date_paiement`, `numero_transaction`, `montant_souscription`, `statut`, `mode_paiement_id`, `souscripteur_morale_id`, `souscripteur_physique_id`) VALUES
(31, '2025-01-16 17:37:48.666741', 'TX-1737049042284', 10.00, 'confirme', 3, NULL, 33),
(29, '2025-01-16 17:18:50.409911', 'TX-1737047750828', 10.00, 'confirme', 3, NULL, 31),
(30, '2025-01-16 17:23:11.595216', 'TX-1737048165892', 10.00, 'confirme', 3, NULL, 32);

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_souscripteurmorale`
--

DROP TABLE IF EXISTS `souscriptions_souscripteurmorale`;
CREATE TABLE IF NOT EXISTS `souscriptions_souscripteurmorale` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `raison_sociale` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `forme_juridique` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `rccm` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ifu` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `siege_social` varchar(200) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom_representant` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `prenom_representant` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `fonction_representant` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `type_souscripteur_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `souscriptions_souscripteurmorale_type_souscripteur_id_240f25b1` (`type_souscripteur_id`)
) ENGINE=MyISAM AUTO_INCREMENT=24 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `souscriptions_souscripteurmorale`
--

INSERT INTO `souscriptions_souscripteurmorale` (`id`, `raison_sociale`, `forme_juridique`, `rccm`, `ifu`, `siege_social`, `nom_representant`, `prenom_representant`, `fonction_representant`, `telephone`, `email`, `pays`, `region`, `ville`, `adresse`, `actif`, `date_creation`, `type_souscripteur_id`) VALUES
(22, 'ENTREPRISE FASO SERVICES SARL', 'SARL', 'BFOUA2023B1234', '00123456A', 'Avenue Kwame N\'Krumah, Ouagadougou', 'KABORE', 'Issouf', 'Directeur Général', '70123456', 'moussa.ouedraogo@example.com', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 00:08:48.926822', 3),
(23, 'ENTREPRISE FASO SERVICES SARL', 'SARL', 'BFOUA2023B1234', '00123456A', 'Avenue Kwame N\'Krumah, Ouagadougou', 'KABORE', 'Issouf', 'Directeur Général', '70123456', 'moussa.ouedraogo@example.com', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 00:31:58.521836', 3);

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_souscripteurphysique`
--

DROP TABLE IF EXISTS `souscriptions_souscripteurphysique`;
CREATE TABLE IF NOT EXISTS `souscriptions_souscripteurphysique` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom_complet` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_naissance` date NOT NULL,
  `lieu_naissance` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `profession` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `genre` varchar(10) COLLATE utf8mb4_unicode_ci NOT NULL,
  `document` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `numero_piece` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_expiration` date NOT NULL,
  `lieu_etablissement` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_etablissement` date NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `type_souscripteur_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `souscriptions_souscripteurphysique_type_souscripteur_id_e540e74b` (`type_souscripteur_id`)
) ENGINE=MyISAM AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `souscriptions_souscripteurphysique`
--

INSERT INTO `souscriptions_souscripteurphysique` (`id`, `nom_complet`, `email`, `telephone`, `date_naissance`, `lieu_naissance`, `profession`, `genre`, `document`, `numero_piece`, `date_expiration`, `lieu_etablissement`, `date_etablissement`, `pays`, `region`, `ville`, `adresse`, `actif`, `date_creation`, `type_souscripteur_id`) VALUES
(22, '11111111', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 17:31:29.208325', 4),
(21, 'NADRE NADRE', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 17:17:31.095529', 4),
(20, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 17:09:37.559956', 4),
(19, 'SERGE SERGE ', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 17:01:34.151397', 4),
(18, 'OUE SERGE', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 16:55:50.407442', 4),
(17, 'OUE SERGE', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 16:48:02.825229', 4),
(16, 'OUE SERGE GEDEON', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 16:40:04.943539', 4),
(15, 'OUE SERGE GEDEON', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 16:20:50.062979', 4),
(23, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 22:38:44.352678', 4),
(24, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 22:39:05.659899', 4),
(25, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 22:54:17.293515', 4),
(26, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 22:57:48.771429', 4),
(27, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 23:16:02.379248', 4),
(28, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 23:18:53.966358', 4),
(29, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-15 23:41:17.218979', 4),
(30, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 00:24:00.275869', 4),
(31, 'OUEDRAOGO Moussa', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 17:18:50.382294', 4),
(32, 'OUE SERGE GEDEON', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 17:23:11.567219', 4),
(33, 'LE GRAND MARTN', 'moussa.ouedraogo@example.com', '70123456', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 1, '2025-01-16 17:37:48.641748', 4);

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_souscriptioneffectuee`
--

DROP TABLE IF EXISTS `souscriptions_souscriptioneffectuee`;
CREATE TABLE IF NOT EXISTS `souscriptions_souscriptioneffectuee` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `numero_transaction` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_souscription` datetime(6) NOT NULL,
  `nom_complet` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `lieu_naissance` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `profession` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `genre` varchar(10) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `document` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `numero_piece` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_expiration` date DEFAULT NULL,
  `lieu_etablissement` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `date_etablissement` date DEFAULT NULL,
  `raison_sociale` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `forme_juridique` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `rccm` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `ifu` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `siege_social` varchar(200) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `nom_representant` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `prenom_representant` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `fonction_representant` varchar(100) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `telephone` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(254) COLLATE utf8mb4_unicode_ci NOT NULL,
  `pays` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `region` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `ville` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `adresse` longtext COLLATE utf8mb4_unicode_ci NOT NULL,
  `surface` decimal(15,2) NOT NULL,
  `cout_unitaire` decimal(15,0) NOT NULL,
  `prix_total` decimal(15,0) NOT NULL,
  `acompte` decimal(15,0) NOT NULL,
  `reste_a_payer` decimal(15,0) NOT NULL,
  `section` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `lot` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `montant_souscription` decimal(15,0) NOT NULL,
  `methode_paiement` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `date_paiement` datetime(6) NOT NULL,
  `operation_id` bigint NOT NULL,
  `parcelle_id` bigint NOT NULL,
  `position_id` bigint NOT NULL,
  `type_parcelle_id` bigint NOT NULL,
  `type_souscripteur_id` bigint NOT NULL,
  `duree_depot_physique` int UNSIGNED DEFAULT NULL,
  `statut` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `numero_transaction` (`numero_transaction`),
  KEY `souscriptions_souscriptioneffectuee_operation_id_389126fc` (`operation_id`),
  KEY `souscriptions_souscriptioneffectuee_parcelle_id_d455544b` (`parcelle_id`),
  KEY `souscriptions_souscriptioneffectuee_position_id_2ecb146e` (`position_id`),
  KEY `souscriptions_souscriptioneffectuee_type_parcelle_id_93d1e4dd` (`type_parcelle_id`),
  KEY `souscriptions_souscriptione_type_souscripteur_id_8f755356` (`type_souscripteur_id`)
) ;

--
-- Déchargement des données de la table `souscriptions_souscriptioneffectuee`
--

INSERT INTO `souscriptions_souscriptioneffectuee` (`id`, `numero_transaction`, `date_souscription`, `nom_complet`, `date_naissance`, `lieu_naissance`, `profession`, `genre`, `document`, `numero_piece`, `date_expiration`, `lieu_etablissement`, `date_etablissement`, `raison_sociale`, `forme_juridique`, `rccm`, `ifu`, `siege_social`, `nom_representant`, `prenom_representant`, `fonction_representant`, `telephone`, `email`, `pays`, `region`, `ville`, `adresse`, `surface`, `cout_unitaire`, `prix_total`, `acompte`, `reste_a_payer`, `section`, `lot`, `montant_souscription`, `methode_paiement`, `date_paiement`, `operation_id`, `parcelle_id`, `position_id`, `type_parcelle_id`, `type_souscripteur_id`, `duree_depot_physique`, `statut`) VALUES
(59, 'TX-1737047750828', '2025-01-16 17:18:50.391897', 'OUEDRAOGO Moussa', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '70123456', 'moussa.ouedraogo@example.com', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 300.00, 26000, 24000000, 2000000, 5800000, 'SE', '17', 10, 'Mobile Money', '2025-01-16 17:18:50.391897', 2, 20, 4, 2, 4, 12, 'en_attente'),
(60, 'TX-1737048165892', '2025-01-16 17:23:11.576221', 'OUE SERGE GEDEON', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '70123456', 'moussa.ouedraogo@example.com', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 300.00, 26000, 24000000, 2500000, 5300000, 'SE', '22', 10, 'Mobile Money', '2025-01-16 17:23:11.576221', 2, 21, 4, 2, 4, 12, 'en_attente'),
(61, 'TX-1737049042284', '2025-01-16 17:37:48.649732', 'LE GRAND MARTN', '1990-05-15', 'Ouagadougou', 'Commerçant', 'M', 'CNIB', 'B123456789', '2025-12-31', 'Ouagadougou', '2020-01-15', NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, '70123456', 'moussa.ouedraogo@example.com', 'Burkina Faso', 'Centre', 'Ouagadougou', 'Secteur 15, Rue 15.25', 300.00, 26000, 7800000, 2500000, 5300000, 'SE', '22', 10, 'Mobile Money', '2025-01-16 17:37:48.650735', 2, 19, 3, 2, 4, 12, 'en_attente');

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_souscriptioneffectuee_comptes_bancaires`
--

DROP TABLE IF EXISTS `souscriptions_souscriptioneffectuee_comptes_bancaires`;
CREATE TABLE IF NOT EXISTS `souscriptions_souscriptioneffectuee_comptes_bancaires` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `souscriptioneffectuee_id` bigint NOT NULL,
  `comptebancaire_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `souscriptions_souscripti_souscriptioneffectuee_id_9193c5b7_uniq` (`souscriptioneffectuee_id`,`comptebancaire_id`),
  KEY `souscriptions_souscriptione_souscriptioneffectuee_id_44a324db` (`souscriptioneffectuee_id`),
  KEY `souscriptions_souscriptione_comptebancaire_id_c6862663` (`comptebancaire_id`)
) ENGINE=MyISAM AUTO_INCREMENT=30 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `souscriptions_souscriptioneffectuee_comptes_bancaires`
--

INSERT INTO `souscriptions_souscriptioneffectuee_comptes_bancaires` (`id`, `souscriptioneffectuee_id`, `comptebancaire_id`) VALUES
(27, 59, 1),
(28, 60, 1),
(29, 61, 1);

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_souscriptioneffectuee_processus_attributions`
--

DROP TABLE IF EXISTS `souscriptions_souscriptioneffectuee_processus_attributions`;
CREATE TABLE IF NOT EXISTS `souscriptions_souscriptioneffectuee_processus_attributions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `souscriptioneffectuee_id` bigint NOT NULL,
  `processusattribution_id` bigint NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `souscriptions_souscripti_souscriptioneffectuee_id_bb1270a3_uniq` (`souscriptioneffectuee_id`,`processusattribution_id`),
  KEY `souscriptions_souscriptione_souscriptioneffectuee_id_0c7e6909` (`souscriptioneffectuee_id`),
  KEY `souscriptions_souscriptione_processusattribution_id_41a4c790` (`processusattribution_id`)
) ENGINE=MyISAM AUTO_INCREMENT=36 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `souscriptions_souscriptioneffectuee_processus_attributions`
--

INSERT INTO `souscriptions_souscriptioneffectuee_processus_attributions` (`id`, `souscriptioneffectuee_id`, `processusattribution_id`) VALUES
(35, 61, 2),
(34, 60, 2),
(33, 59, 2);

-- --------------------------------------------------------

--
-- Structure de la table `souscriptions_typesouscripteur`
--

DROP TABLE IF EXISTS `souscriptions_typesouscripteur`;
CREATE TABLE IF NOT EXISTS `souscriptions_typesouscripteur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `code` varchar(50) COLLATE utf8mb4_unicode_ci NOT NULL,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `actif` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `code` (`code`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `souscriptions_typesouscripteur`
--

INSERT INTO `souscriptions_typesouscripteur` (`id`, `code`, `nom`, `description`, `actif`, `date_creation`) VALUES
(3, 'MORALE', 'Personne Morale', 'Type pour les personnes morales', 1, '2025-01-04 11:06:11.351685'),
(4, 'PHYSIQUE', 'Personne Physique', 'Type pour les personnes physiques', 1, '2025-01-04 17:10:43.704958');

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs_role`
--

DROP TABLE IF EXISTS `utilisateurs_role`;
CREATE TABLE IF NOT EXISTS `utilisateurs_role` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `nom` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` longtext COLLATE utf8mb4_unicode_ci,
  `actif` tinyint(1) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `utilisateurs_role`
--

INSERT INTO `utilisateurs_role` (`id`, `nom`, `description`, `actif`) VALUES
(1, 'Administrateur', 'Administrateur', 1),
(2, 'Moderateur', 'Moderateur', 1);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs_utilisateur`
--

DROP TABLE IF EXISTS `utilisateurs_utilisateur`;
CREATE TABLE IF NOT EXISTS `utilisateurs_utilisateur` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `password` varchar(128) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `first_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `last_name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  `nom_complet` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `actif` tinyint(1) NOT NULL,
  `date_creation` datetime(6) NOT NULL,
  `role_id` bigint DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `email` (`email`),
  KEY `utilisateurs_utilisateur_role_id_ea16d41b` (`role_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

--
-- Déchargement des données de la table `utilisateurs_utilisateur`
--

INSERT INTO `utilisateurs_utilisateur` (`id`, `password`, `last_login`, `is_superuser`, `first_name`, `last_name`, `is_staff`, `is_active`, `date_joined`, `nom_complet`, `email`, `actif`, `date_creation`, `role_id`) VALUES
(1, 'pbkdf2_sha256$870000$GzeRSTjFqjjIjzk4ZNBnfB$/BBoaXRKEVRp6NgG9pyVuN7bmoYE56DCl7E8gxLajdY=', '2025-01-16 16:57:50.453691', 1, '', '', 1, 1, '2024-12-24 00:22:54.982404', 'Administrateur Sonatur', 'admin@admin.com', 1, '2024-12-24 00:22:55.809694', 1),
(2, 'pbkdf2_sha256$870000$NNTWGpdFse9ZurRfPVPzoL$c35Pg+ETkRarlZJCUVNYk0jtn9wX/LwR/1RmduSGpRs=', NULL, 0, '', '', 0, 1, '2024-12-28 13:45:58.902165', 'gedeon', 'admin@bkctransport.com', 1, '2024-12-28 13:45:59.951451', 1);

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs_utilisateur_groups`
--

DROP TABLE IF EXISTS `utilisateurs_utilisateur_groups`;
CREATE TABLE IF NOT EXISTS `utilisateurs_utilisateur_groups` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint NOT NULL,
  `group_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utilisateurs_utilisateur_utilisateur_id_group_id_954b1d5c_uniq` (`utilisateur_id`,`group_id`),
  KEY `utilisateurs_utilisateur_groups_utilisateur_id_3264257e` (`utilisateur_id`),
  KEY `utilisateurs_utilisateur_groups_group_id_9cd3c896` (`group_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- --------------------------------------------------------

--
-- Structure de la table `utilisateurs_utilisateur_user_permissions`
--

DROP TABLE IF EXISTS `utilisateurs_utilisateur_user_permissions`;
CREATE TABLE IF NOT EXISTS `utilisateurs_utilisateur_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `utilisateur_id` bigint NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `utilisateurs_utilisateur_utilisateur_id_permissio_a16db5bb_uniq` (`utilisateur_id`,`permission_id`),
  KEY `utilisateurs_utilisateur_us_utilisateur_id_604dcf80` (`utilisateur_id`),
  KEY `utilisateurs_utilisateur_user_permissions_permission_id_42b32d4e` (`permission_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
