DROP DATABASE IF EXISTS `zhihu`;
CREATE DATABASE `zhihu`;
use zhihu;
DROP TABLE IF EXISTS `user_info`;
create table `user_info` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`uid` varchar(100) NOT NULL DEFAULT '',
	`url_token` varchar(300) NOT NULL DEFAULT '',
	`name` varchar(100) NOT NULL DEFAULT '',
	`type` varchar(50) NOT NULL DEFAULT '',
	`headline` varchar(500) NOT NULL DEFAULT '',
	`gender` int(11) NOT NULL DEFAULT '-1',
	`follower_count` int(11) NOT NULL DEFAULT '0',
	`answer_count` int(11) NOT NULL DEFAULT '0',
	`article_count` int(11) NOT NULL DEFAULT '0',
	`company` varchar(100),
	`job` varchar(100),
	PRIMARY KEY(`id`),
	UNIQUE KEY (`uid`),
	UNIQUE KEY (`url_token`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `question`;
create table `question` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`qid` varchar(100) NOT NULL DEFAULT '',
	`uid` varchar(100) NOT NULL DEFAULT '',
	`url_token` varchar(300) NOT NULL DEFAULT '',
	`title` varchar(500) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`),
	UNIQUE KEY (`qid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `answer`;
create table `answer` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`aid` varchar(100) NOT NULL DEFAULT '',
	`uid` varchar(100) NOT NULL DEFAULT '',
	`url_token` varchar(300) NOT NULL DEFAULT '',
	`qid` varchar(100) NOT NULL DEFAULT '',
	`content` text,
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`),
	UNIQUE KEY (`aid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `article`;
create table `article` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`arid` varchar(100) NOT NULL DEFAULT '',
	`uid` varchar(100) NOT NULL DEFAULT '',
	`url_token` varchar(300) NOT NULL DEFAULT '',
	`title` varchar(500) NOT NULL DEFAULT '',
	`content` text,
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	`updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`),
	UNIQUE KEY (`arid`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `collect_answer`;
create table `collect_answer` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`aid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `agree_answer`;
create table `agree_answer` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`aid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `follow_question`;
create table `follow_question` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`qid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `collect_question`;
create table `collect_question` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`qid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `agree_article`;
create table `agree_article` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`arid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

DROP TABLE IF EXISTS `collect_article`;
create table `collect_article` (
	`id` int(11) NOT NULL AUTO_INCREMENT,
	`url_token` varchar(100) NOT NULL DEFAULT '',
	`arid` varchar(100) NOT NULL DEFAULT '',
	`created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY(`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

