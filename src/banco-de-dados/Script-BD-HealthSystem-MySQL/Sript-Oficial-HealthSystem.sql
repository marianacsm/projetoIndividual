-----------------------------------------------------
-- Schema HealthSystem
-- -----------------------------------------------------
CREATE DATABASE `HealthSystem`;
-- -----------------------------------------------------
-- Schema healthsystem
-- -----------------------------------------------------
USE `HealthSystem` ;
-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Empresa`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Empresa` (
    `idEmpresa` INT NOT NULL AUTO_INCREMENT,
    `razaoSocial` VARCHAR(45) NOT NULL,
    `cnpj` CHAR(14) NOT NULL,
    `logradouro` VARCHAR(45) NOT NULL,
    `numero` INT NOT NULL,
    `bairro` VARCHAR(45) NOT NULL,
    `cidade` VARCHAR(45) NOT NULL,
    `estado` CHAR(2) NOT NULL,
    `cep` CHAR(8) NOT NULL,
    PRIMARY KEY (`idEmpresa`)
);
DESC `HealthSystem`.`Empresa`;
SELECT * FROM `HealthSystem`.`Empresa`;
INSERT INTO `HealthSystem`.`Empresa` VALUES (NULL,"PHILIPS DO BRASIL LTDA",61086336000103,"Avenida Marcos Penteado de Ulhoa Rodrigues",939,"Tambore","Barueri","SP","06460040");

-- -----------------------------------------------------
-- Table `HealthSystem`.`Credencial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Credencial` (
    `idCredencial` INT NOT NULL,
    `tipoCredencial` VARCHAR(45) NOT NULL,
    `nivelPermissao` ENUM('1', '2', '3') NOT NULL,
    PRIMARY KEY (`idCredencial`)
);
DESC `healthsystem`.`Credencial`;
SELECT * FROM `healthsystem`.`Credencial`;
INSERT INTO `healthsystem`.`Credencial` VALUES (323145,"Tecnico",1), (543221,"Analista",2), (386531,"Gerente",3);
-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Usuario`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Usuario` (
  `fkEmpresa` INT NOT NULL,
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `fkCredencial` INT NOT NULL,
  PRIMARY KEY (`idUsuario`),
  INDEX `fk_Usuario_Empresa1_idx` (`fkEmpresa` ASC) VISIBLE,
  INDEX `fk_Usuario_Credencial1_idx` (`fkCredencial` ASC) VISIBLE,
  CONSTRAINT `fk_Usuario_Empresa1`
    FOREIGN KEY (`fkEmpresa`)
    REFERENCES `HealthSystem`.`Empresa` (`idEmpresa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Usuario_Credencial1`
    FOREIGN KEY (`fkCredencial`)
    REFERENCES `HealthSystem`.`Credencial` (`idCredencial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
DESC `HealthSystem`.`Usuario`;
SELECT * FROM `HealthSystem`.`Usuario`;
INSERT INTO `healthsystem`.`Usuario` VALUES (1,NULL,"fernandoBrandao","fernando.brandao@sptech.school","1234",323145);

-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Componente`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Componente` (
    `idComponente` INT NOT NULL AUTO_INCREMENT,
    `nomeComponente` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`idComponente`)
);
DESC `HealthSystem`.`Componente`;
SELECT * FROM `HealthSystem`.`Componente`;
INSERT INTO `HealthSystem`.`Componente` (`nomeComponente`) VALUES ("CPU"), ("Memoria"), ("Disco");

-- -----------------------------------------------------
-- Table `HealthSystem`.`Filial`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Filial` (
  `idFilial` INT NOT NULL AUTO_INCREMENT,
  `fkEmpresa` INT NOT NULL,
  `nomeFantasia` VARCHAR(45) NOT NULL,
  `logradouro` VARCHAR(45) NOT NULL,
  `numero` INT NOT NULL,
  `bairro` VARCHAR(45) NOT NULL,
  `cidade` VARCHAR(45) NOT NULL,
  `estado` CHAR(2) NOT NULL,
  `cep` CHAR(8) NOT NULL,
  PRIMARY KEY (`idFilial`),
  INDEX `fk_Filial_Empresa1_idx` (`fkEmpresa` ASC) VISIBLE,
  CONSTRAINT `fk_Filial_Empresa1`
    FOREIGN KEY (`fkEmpresa`)
    REFERENCES `healthsystem`.`Empresa` (`idEmpresa`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION) 
    AUTO_INCREMENT = 1000;
DESC `healthsystem`.`filial`;
SELECT * FROM `healthsystem`.`filial`;
INSERT INTO `healthsystem`.`filial` VALUES (NULL,1,"HOSPITAL SAO LUIZ GONZAGA","R MICHEL OUCHANA",94,"JACANA","SÃO PAULO","SP","02276140");
-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Local`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Local` (
    `idLocal` INT NOT NULL AUTO_INCREMENT,
    `identificacao` VARCHAR(45) NOT NULL,
    PRIMARY KEY (`idLocal`)
);
DESC `healthsystem`.`Local`;
SELECT * FROM `HealthSystem`.`Local`;
INSERT INTO `healthsystem`.`Local` (`identificacao`) VALUES ("Sala de Ultrassom"),("Enfermaria"),("Sala de Manutenção");
SELECT COUNT(idLocal) FROM `healthsystem`.`local`;
-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Equipamento`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Equipamento` (
  `idEquipamento` INT NOT NULL AUTO_INCREMENT,
  `fkFilial` INT NOT NULL,
  `fkLocal` INT NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `arqMaquina` VARCHAR(45) NOT NULL,
  `sistemaOp` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEquipamento`),
  INDEX `fk_Equipamento_Local1_idx` (`fkLocal` ASC) VISIBLE,
  INDEX `fk_Equipamento_Filial1_idx` (`fkFilial` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_Sala1`
    FOREIGN KEY (`fkLocal`)
    REFERENCES `HealthSystem`.`Local` (`idLocal`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Equipamento_Filial1`
    FOREIGN KEY (`fkFilial`)
    REFERENCES `HealthSystem`.`Filial` (`idFilial`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION);
DESC `healthsystem`.`Equipamento`;
SELECT * FROM `healthsystem`.`Equipamento`;
SELECT COUNT(idEquipamento) FROM `healthsystem`.`Equipamento`;

-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Parametro`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Parametro` (
  `fkEquipamento` INT NOT NULL,
  `fkComponente` INT NOT NULL,
  `idParametro` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(100) NOT NULL,
  `valid` TINYINT NOT NULL,
  PRIMARY KEY (`idParametro`,`fkEquipamento`, `fkComponente`),
  INDEX `fk_Equipamento_has_Componente_Componente1_idx` (`fkComponente` ASC) VISIBLE,
  INDEX `fk_Equipamento_has_Componente_Equipamento1_idx` (`fkEquipamento` ASC) VISIBLE,
  CONSTRAINT `fk_Equipamento_has_Componente_Equipamento1`
    FOREIGN KEY (`fkEquipamento`)
    REFERENCES `HealthSystem`.`Equipamento` (`idEquipamento`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_Equipamento_has_Componente_Componente1`
    FOREIGN KEY (`fkComponente`)
    REFERENCES `HealthSystem`.`Componente` (`idComponente`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION
    );
    DESC `healthsystem`.`Parametro`;
    SELECT * FROM `healthsystem`.`Parametro`;

-- -----------------------------------------------------
-- Tabela `HealthSystem`.`Leitura`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `HealthSystem`.`Leitura` (
  `idLeitura` INT NOT NULL AUTO_INCREMENT,
  `temperatura` FLOAT,
  `ociosidade` FLOAT,
  `momento` DATETIME NOT NULL,
  PRIMARY KEY (`idLeitura`)
    );
	DESC `healthsystem`.`Leitura`;

    USE `healthsystem`;
    
    TRUNCATE TABLE `healthsystem`.`Leitura`;
	SELECT * FROM `healthsystem`.`leitura`;
    
    DROP DATABASE healthsystem;