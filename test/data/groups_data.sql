--
-- Dumping data for table `groups`
--
SET unique_checks = 0;
SET foreign_key_checks = 0;
LOCK TABLES `groups` WRITE;
INSERT INTO `groups` VALUES (1, 'Feature', '2012-03-21 18:26:03', '2012-03-21 18:26:03'),
  (2, 'New Bin', '2012-03-21 18:26:26', '2012-03-21 18:26:26'),
  (3, 'Library', '2012-03-21 18:26:37', '2012-03-21 18:26:37'),
  (4, 'Recurrent', '2012-03-21 18:26:48', '2012-03-21 18:26:48'),
  (5, 'Specialty Show', '2012-03-21 18:27:08', '2012-03-21 18:27:08');
SET foreign_key_checks = 1;
SET unique_checks = 1;
UNLOCK TABLES;
