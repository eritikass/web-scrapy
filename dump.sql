CREATE TABLE `exploits` (
  `id` INT UNSIGNED NOT NULL AUTO_INCREMENT,
  `provider` VARCHAR(45) NOT NULL,
  `provider_id` VARCHAR(250) NOT NULL,
  `module` VARCHAR(250) NULL,
  `exploit` VARCHAR(250) NULL,
  `version` VARCHAR(45) NULL,
  `link` VARCHAR(250) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE INDEX `unq` (`provider`, `provider_id`)
);