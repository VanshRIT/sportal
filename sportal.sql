-- MySQL dump 10.13  Distrib 8.0.28, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: sportal
-- ------------------------------------------------------
-- Server version	8.0.28

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `counsellors`
--
drop database if exists sportal;
create database sportal;
DROP TABLE IF EXISTS `counsellors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `counsellors` (
  `counsellor_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `counsellor_name` varchar(100) NOT NULL,
  `user_id` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`counsellor_id`),
  UNIQUE KEY `counsellor_id` (`counsellor_id`),
  KEY `counsellors_users_user_id_fk` (`user_id`),
  CONSTRAINT `counsellors_users_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `counsellors`
--

LOCK TABLES `counsellors` WRITE;
/*!40000 ALTER TABLE `counsellors` DISABLE KEYS */;
INSERT INTO `counsellors` (`counsellor_id`, `counsellor_name`, `user_id`) VALUES (1,'test_counsellor_1',3),(2,'admin',2);
/*!40000 ALTER TABLE `counsellors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `grades`
--

DROP TABLE IF EXISTS `grades`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `grades` (
  `grade_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `student_id` bigint unsigned DEFAULT NULL,
  `teacher_id` bigint unsigned DEFAULT NULL,
  `item` varchar(100) NOT NULL,
  `score` char(1) NOT NULL,
  `date` date NOT NULL,
  `subject_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`grade_id`),
  UNIQUE KEY `grade_id` (`grade_id`),
  KEY `grades_students_student_id_fk` (`student_id`),
  KEY `grades_teachers_teacher_id_fk` (`teacher_id`),
  CONSTRAINT `grades_students_student_id_fk` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `grades_teachers_teacher_id_fk` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=10 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `grades`
--

LOCK TABLES `grades` WRITE;
/*!40000 ALTER TABLE `grades` DISABLE KEYS */;
INSERT INTO `grades` (`grade_id`, `student_id`, `teacher_id`, `item`, `score`, `date`, `subject_id`) VALUES (1,1,1,'Quiz 1','C','2023-10-01',1),(2,1,1,'Quiz 1','B','2023-11-06',3),(3,1,1,'Quiz 2','A','2023-10-13',3),(4,1,1,'Quiz 2','B','2023-10-18',1),(5,1,1,'Quiz 3','B','2023-11-02',1),(6,1,1,'Midterm','C','2023-11-06',1),(7,1,1,'Project','A','2023-12-02',1),(8,1,1,'Quiz 1','B','2023-12-10',2),(9,1,1,'Quiz 2','A','2023-12-10',2);
/*!40000 ALTER TABLE `grades` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `messages`
--

DROP TABLE IF EXISTS `messages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `messages` (
  `message_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `sender_id` int DEFAULT NULL,
  `receiver_id` int DEFAULT NULL,
  `message_text` text NOT NULL,
  `timestamp` timestamp NOT NULL,
  PRIMARY KEY (`message_id`),
  UNIQUE KEY `message_id` (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `messages`
--

LOCK TABLES `messages` WRITE;
/*!40000 ALTER TABLE `messages` DISABLE KEYS */;
/*!40000 ALTER TABLE `messages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `parents`
--

DROP TABLE IF EXISTS `parents`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `parents` (
  `parent_id` int NOT NULL AUTO_INCREMENT,
  `parent_name` varchar(100) DEFAULT NULL,
  `user_id` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`parent_id`),
  KEY `parents_users_user_id_fk` (`user_id`),
  CONSTRAINT `parents_users_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `parents`
--

LOCK TABLES `parents` WRITE;
/*!40000 ALTER TABLE `parents` DISABLE KEYS */;
INSERT INTO `parents` (`parent_id`, `parent_name`, `user_id`) VALUES (1,'test_parent_1',5),(2,'pap',2);
/*!40000 ALTER TABLE `parents` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `students`
--

DROP TABLE IF EXISTS `students`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `students` (
  `student_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `student_name` varchar(255) NOT NULL,
  `counsellor_id` bigint unsigned DEFAULT NULL,
  `parent_id` int DEFAULT NULL,
  `weak_subjects` varchar(100) NOT NULL,
  PRIMARY KEY (`student_id`),
  UNIQUE KEY `student_id` (`student_id`),
  KEY `students___fk` (`parent_id`),
  KEY `students_counsellors_counsellor_id_fk` (`counsellor_id`),
  CONSTRAINT `students___fk` FOREIGN KEY (`parent_id`) REFERENCES `parents` (`parent_id`),
  CONSTRAINT `students_counsellors_counsellor_id_fk` FOREIGN KEY (`counsellor_id`) REFERENCES `counsellors` (`counsellor_id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `students`
--

LOCK TABLES `students` WRITE;
/*!40000 ALTER TABLE `students` DISABLE KEYS */;
INSERT INTO `students` (`student_id`, `student_name`, `counsellor_id`, `parent_id`, `weak_subjects`) VALUES (1,'test_student_1',1,1,'1,2,3,4'),(2,'test_student_2',1,1,'2,3,4,5'),(3,'test_student_3',2,2,'1,4'),(18,'asdf',1,1,'4'),(19,'test_student_3',1,1,'3');
/*!40000 ALTER TABLE `students` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `subjects`
--

DROP TABLE IF EXISTS `subjects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `subjects` (
  `subject_id` int NOT NULL AUTO_INCREMENT,
  `subject_name` varchar(100) NOT NULL,
  `teacher_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`subject_id`),
  KEY `subjects_teachers_teacher_id_fk` (`teacher_id`),
  CONSTRAINT `subjects_teachers_teacher_id_fk` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `subjects`
--

LOCK TABLES `subjects` WRITE;
/*!40000 ALTER TABLE `subjects` DISABLE KEYS */;
INSERT INTO `subjects` (`subject_id`, `subject_name`, `teacher_id`) VALUES (1,'Math',1),(2,'Physics',1),(3,'GCIS',1),(4,'Chemistry',2),(5,'Biology',1),(6,'English',2);
/*!40000 ALTER TABLE `subjects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `tasks`
--

DROP TABLE IF EXISTS `tasks`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `tasks` (
  `task_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `student_id` bigint unsigned DEFAULT NULL,
  `teacher_id` bigint unsigned DEFAULT NULL,
  `counsellor_id` bigint unsigned DEFAULT NULL,
  `task_description` text NOT NULL,
  `status` varchar(20) NOT NULL,
  `deadline` date NOT NULL,
  `date_created` timestamp NOT NULL,
  `file_path_parent` varchar(1000) DEFAULT NULL,
  `file_path_counsellor_teacher` varchar(1000) DEFAULT NULL,
  `marks` int DEFAULT NULL,
  `feedback` varchar(10000) DEFAULT NULL,
  `subject_id` bigint unsigned NOT NULL,
  PRIMARY KEY (`task_id`),
  UNIQUE KEY `task_id` (`task_id`),
  KEY `tasks_students_student_id_fk` (`student_id`),
  KEY `tasks_teachers_teacher_id_fk` (`teacher_id`),
  KEY `tasks_counsellors_counsellor_id_fk` (`counsellor_id`),
  CONSTRAINT `tasks_counsellors_counsellor_id_fk` FOREIGN KEY (`counsellor_id`) REFERENCES `counsellors` (`counsellor_id`),
  CONSTRAINT `tasks_students_student_id_fk` FOREIGN KEY (`student_id`) REFERENCES `students` (`student_id`),
  CONSTRAINT `tasks_teachers_teacher_id_fk` FOREIGN KEY (`teacher_id`) REFERENCES `teachers` (`teacher_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `tasks`
--

LOCK TABLES `tasks` WRITE;
/*!40000 ALTER TABLE `tasks` DISABLE KEYS */;
INSERT INTO `tasks` (`task_id`, `student_id`, `teacher_id`, `counsellor_id`, `task_description`, `status`, `deadline`, `date_created`, `file_path_parent`, `file_path_counsellor_teacher`, `marks`, `feedback`, `subject_id`) VALUES (1,1,1,NULL,'Read 10 Pages in Chapter 2 English Textbook','D','2023-11-28','2023-11-23 14:15:12','C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\parent\\serverEcho.py',NULL,NULL,NULL,1),(2,1,NULL,1,'Make a flappy bird game form scratch purely in assembly','D','2023-12-11','2023-11-24 18:19:09','C:\\Users\\prana\\Documents\\GitHub\\sportal\\static\\files_uploaded\\parent\\clientEcho.py',NULL,NULL,NULL,1),(5,1,NULL,1,'Do question 1','D','2023-11-29','2023-11-26 20:00:00','C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\parent\\Picture1.png','C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\counsellor_teacher\\Picture1.png',10,'asdf',1),(6,1,NULL,1,'Do question 2-5','D','2023-11-27','2023-11-26 20:00:00','C:\\Users\\prana\\Documents\\GitHub\\sportal\\files_uploaded\\parent\\as.txt',NULL,5,'Decent Work!',1),(9,1,1,NULL,'Write down and memorize formulas','D','2023-12-09','2023-12-08 20:00:00','C:\\Users\\prana\\Documents\\GitHub\\sportal\\static\\files_uploaded\\parent\\HW.pdf','C:\\Users\\prana\\Documents\\GitHub\\sportal\\static\\files_uploaded\\counsellor_teacher\\asdf2.pdf',10,'12sfytrgefw',3),(10,1,1,NULL,'Test','D','2023-12-18','2023-12-09 20:00:00','C:\\Users\\prana\\Documents\\GitHub\\sportal\\static\\files_uploaded\\parent\\244-lab3-vCenter_and_ESXi.pdf',NULL,7,'Well done!',3);
/*!40000 ALTER TABLE `tasks` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `teachers`
--

DROP TABLE IF EXISTS `teachers`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `teachers` (
  `teacher_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `teacher_name` varchar(255) NOT NULL,
  `user_id` bigint unsigned DEFAULT NULL,
  PRIMARY KEY (`teacher_id`),
  UNIQUE KEY `teacher_id` (`teacher_id`),
  KEY `teachers_users_user_id_fk` (`user_id`),
  CONSTRAINT `teachers_users_user_id_fk` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `teachers`
--

LOCK TABLES `teachers` WRITE;
/*!40000 ALTER TABLE `teachers` DISABLE KEYS */;
INSERT INTO `teachers` (`teacher_id`, `teacher_name`, `user_id`) VALUES (1,'test_teacher_1',4),(2,'test_teacher_2',6);
/*!40000 ALTER TABLE `teachers` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` bigint unsigned NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `role_id` int DEFAULT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `user_id` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `role_id`) VALUES (1,'admin','admin','admin',2),(2,'pap','pap','pap5183@rit.edu',3),(3,'counsellor1_test','counsellor1','asdf',2),(4,'teacher1_test','teacher1','asdff',1),(5,'parent1_test','parent1','asdfff',3),(6,'teacher2_test','teacher2','asdffff',1);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2023-12-12  2:24:53
