-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 19-11-2025 a las 20:53:35
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `bd_cita_psico`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `appointments`
--

CREATE TABLE `appointments` (
  `ID_app` int(11) NOT NULL,
  `FK_stu` varchar(15) NOT NULL,
  `FK_psy` int(11) NOT NULL,
  `date` datetime DEFAULT NULL,
  `status` varchar(10) DEFAULT NULL,
  `num_app` int(11) DEFAULT NULL,
  `diag` varchar(100) DEFAULT NULL,
  `note` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `groups`
--

CREATE TABLE `groups` (
  `ID_group` int(11) NOT NULL,
  `carrer` varchar(50) NOT NULL,
  `period` int(11) NOT NULL,
  `group_code` varchar(2) NOT NULL,
  `modal` varchar(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `psychologists`
--

CREATE TABLE `psychologists` (
  `ID_psy` int(11) NOT NULL,
  `name_psy` varchar(100) DEFAULT NULL,
  `mail_psy` varchar(50) DEFAULT NULL,
  `phone_psy` varchar(15) DEFAULT NULL,
  `pass` text DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `students`
--

CREATE TABLE `students` (
  `control_num` varchar(15) NOT NULL,
  `FK_group` int(11) NOT NULL,
  `name_stu` varchar(100) DEFAULT NULL,
  `mail_stu` varchar(50) DEFAULT NULL,
  `phone_stu` varchar(15) DEFAULT NULL,
  `cont_app` int(11) DEFAULT NULL,
  `susp` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tutored`
--

CREATE TABLE `tutored` (
  `ID_tutor` int(11) NOT NULL,
  `FK_group` int(11) NOT NULL,
  `name_tea` varchar(100) DEFAULT NULL,
  `mail_tea` varchar(50) DEFAULT NULL,
  `phone_tea` varchar(15) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`ID_app`),
  ADD KEY `student_app` (`FK_stu`),
  ADD KEY `psychologist_app` (`FK_psy`);

--
-- Indices de la tabla `groups`
--
ALTER TABLE `groups`
  ADD PRIMARY KEY (`ID_group`);

--
-- Indices de la tabla `psychologists`
--
ALTER TABLE `psychologists`
  ADD PRIMARY KEY (`ID_psy`);

--
-- Indices de la tabla `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`control_num`),
  ADD KEY `group_stu` (`FK_group`);

--
-- Indices de la tabla `tutored`
--
ALTER TABLE `tutored`
  ADD PRIMARY KEY (`ID_tutor`),
  ADD KEY `group_tea` (`FK_group`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `appointments`
--
ALTER TABLE `appointments`
  MODIFY `ID_app` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `groups`
--
ALTER TABLE `groups`
  MODIFY `ID_group` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `psychologists`
--
ALTER TABLE `psychologists`
  MODIFY `ID_psy` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `students`
--
ALTER TABLE `students`
  MODIFY `control_num` varchar(15) NOT NULL;

--
-- AUTO_INCREMENT de la tabla `tutored`
--
ALTER TABLE `tutored`
  MODIFY `ID_tutor` int(11) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `psychologist_app` FOREIGN KEY (`FK_psy`) REFERENCES `psychologists` (`ID_psy`) ON UPDATE CASCADE,
  ADD CONSTRAINT `student_app` FOREIGN KEY (`FK_stu`) REFERENCES `students` (`control_num`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `students`
--
ALTER TABLE `students`
  ADD CONSTRAINT `group_stu` FOREIGN KEY (`FK_group`) REFERENCES `groups` (`ID_group`) ON UPDATE CASCADE;

--
-- Filtros para la tabla `tutored`
--
ALTER TABLE `tutored`
  ADD CONSTRAINT `group_tea` FOREIGN KEY (`FK_group`) REFERENCES `groups` (`ID_group`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
