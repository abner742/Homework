/*
 Navicat Premium Data Transfer

 Source Server         : 01
 Source Server Type    : MySQL
 Source Server Version : 80023
 Source Host           : localhost:3306
 Source Schema         : imu_py

 Target Server Type    : MySQL
 Target Server Version : 80023
 File Encoding         : 65001

 Date: 20/06/2021 15:43:40
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `user_name` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_password` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  `user_nickname` varchar(30) CHARACTER SET utf8 COLLATE utf8_general_ci NOT NULL,
  PRIMARY KEY (`user_id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 10 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (5, 'user1', '111111', 'itcast1');
INSERT INTO `users` VALUES (6, 'user2', '111111', 'itcast2');
INSERT INTO `users` VALUES (8, 'user3', '111111', 'itcast3');
INSERT INTO `users` VALUES (9, 'user4', '111111', 'itcast4');

SET FOREIGN_KEY_CHECKS = 1;
