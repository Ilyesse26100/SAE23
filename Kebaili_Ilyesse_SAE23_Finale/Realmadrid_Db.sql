-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Hôte : 127.0.0.1:3306
-- Généré le : dim. 05 mai 2024 à 17:24
-- Version du serveur : 8.2.0
-- Version de PHP : 8.2.13

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de données : `realmadriddb`
--

-- --------------------------------------------------------

--
-- Structure de la table `equipes`
--

DROP TABLE IF EXISTS `equipes`;
CREATE TABLE IF NOT EXISTS `equipes` (
  `equipe_id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `stade` varchar(255) DEFAULT NULL,
  `entraineur` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`equipe_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `joueurs`
--

DROP TABLE IF EXISTS `joueurs`;
CREATE TABLE IF NOT EXISTS `joueurs` (
  `joueur_id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  `age` int DEFAULT NULL,
  `date_naissance` date DEFAULT NULL,
  `poste` varchar(255) DEFAULT NULL,
  `prix_achat` decimal(10,2) DEFAULT NULL,
  `equipe_id` int DEFAULT NULL,
  PRIMARY KEY (`joueur_id`),
  KEY `equipe_id` (`equipe_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `matches`
--

DROP TABLE IF EXISTS `matches`;
CREATE TABLE IF NOT EXISTS `matches` (
  `match_id` int NOT NULL AUTO_INCREMENT,
  `date` date NOT NULL,
  `equipe_domicile_id` int DEFAULT NULL,
  `equipe_exterieur_id` int DEFAULT NULL,
  `Resultat` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`match_id`),
  KEY `equipe_domicile_id` (`equipe_domicile_id`),
  KEY `equipe_exterieur_id` (`equipe_exterieur_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `paris`
--

DROP TABLE IF EXISTS `paris`;
CREATE TABLE IF NOT EXISTS `paris` (
  `paris_id` int NOT NULL AUTO_INCREMENT,
  `match_id` int DEFAULT NULL,
  `supporteur_id` int DEFAULT NULL,
  `mise` decimal(10,2) DEFAULT NULL,
  `Resultat_Prédit` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`paris_id`),
  KEY `match_id` (`match_id`),
  KEY `supporteur_id` (`supporteur_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `performances`
--

DROP TABLE IF EXISTS `performances`;
CREATE TABLE IF NOT EXISTS `performances` (
  `performances_id` int NOT NULL AUTO_INCREMENT,
  `joueur_id` int DEFAULT NULL,
  `match_id` int DEFAULT NULL,
  `buts` int DEFAULT '0',
  `passes_decisives` int DEFAULT '0',
  PRIMARY KEY (`performances_id`),
  KEY `joueur_id` (`joueur_id`),
  KEY `match_id` (`match_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- --------------------------------------------------------

--
-- Structure de la table `supporteurs`
--

DROP TABLE IF EXISTS `supporteurs`;
CREATE TABLE IF NOT EXISTS `supporteurs` (
  `supporteur_id` int NOT NULL AUTO_INCREMENT,
  `nom` varchar(255) NOT NULL,
  `prenom` varchar(255) NOT NULL,
  PRIMARY KEY (`supporteur_id`)
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
