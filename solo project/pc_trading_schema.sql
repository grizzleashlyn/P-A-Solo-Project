-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema pc_trading_schema
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema pc_trading_schema
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `pc_trading_schema` DEFAULT CHARACTER SET utf8 ;
USE `pc_trading_schema` ;

-- -----------------------------------------------------
-- Table `pc_trading_schema`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pc_trading_schema`.`users` (
  `id` INT NOT NULL,
  `first_name` VARCHAR(45) NULL,
  `last_name` VARCHAR(45) NULL,
  `email` MEDIUMTEXT NULL,
  `password` LONGTEXT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `pc_trading_schema`.`photocards`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `pc_trading_schema`.`photocards` (
  `id` INT NOT NULL,
  `member` VARCHAR(45) NULL,
  `group` VARCHAR(45) NULL,
  `album_version` MEDIUMTEXT NULL,
  `details` LONGTEXT NULL,
  `user_id` INT NOT NULL,
  PRIMARY KEY (`id`, `user_id`),
  INDEX `fk_photocards_users_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_photocards_users`
    FOREIGN KEY (`user_id`)
    REFERENCES `pc_trading_schema`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
