import pyodbc
import psutil
import time
from datetime import datetime
import platform
import mysql.connector
from mysql.connector import errorcode
import sys
import os
from multiprocessing import connection
from ast import Str
# Driver de instalação ODBC - Linux: https://docs.microsoft.com/pt-br/sql/connect/odbc/linux-mac/installing-the-microsoft-odbc-driver-for-sql-server?view=sql-server-ver15

# Importações de Bibliotecas:

def buscar_sistema_operacional():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = 'pip list | findstr /c:"{}"'
    elif "linux" in os_type:
        command = 'pip list | grep {}'
    return command


print("\U0001F916 O seu sistema operacional é",
      platform.uname().system, "\n--------")

bibliotecas = ['mysql-connector-python', 'pyodbc', 'psutil']


def validLibrary(bibliotecas):
    print("\U0001F916 Vou iniciar algumas validações de bibliotecas agora.", "\n--------")
    for i in bibliotecas:
        command = buscar_sistema_operacional().format(i)
        exibir = os.popen(command).read()

        if (exibir == ''):
            print("\U0001F916 Opa! identifiquei que a biblioteca",
                  i, "não esta instalada!", "\n--------")
            time.sleep(2)
            print("\U0001F916 Mas não se preocupe, vou instalar a biblioteca",
                  i, "para você.", "\n--------")
            ins = 'pip install {}'.format(i)
            os.system(ins)

        else:
            print("\U0001F916 Que ótimo, você ja tem a biblioteca",
                  exibir, "\n--------")


validLibrary(bibliotecas)



def buscar_serial():
    os_type = sys.platform.lower()
    if "win" in os_type:
        command = "wmic bios get serialnumber"
    elif "linux" in os_type:
        command = "hal-get-property --udi /org/freedesktop/Hal/devices/computer --key system.hardware.uuid"
    elif "darwin" in os_type:
        command = "ioreg -l | grep IOPlatformSerialNumber"
    return os.popen(command).read().replace("\n", "").replace(" ", "").replace(" ", "")


def captura(conn, cursor, conx, cursorMySQL):
    print("Seja bem-vindo ao sistema de captura de dados do seu Hardware \U0001F604")
    tempo = 2
    numero = 10

    if (tempo > 0):
        print("\U0001F750 Iniciando captura dos dados...", "\n--------")
        meu_sistema = platform.uname()
        sistema = meu_sistema.system
        arqmaquina = meu_sistema.machine
        nomeMaquina = meu_sistema.node
        modelo = meu_sistema.processor
        numero_serial = buscar_serial()

        codigosEquip = [sistema, arqmaquina,
                        nomeMaquina, modelo, numero_serial]

        numeros_serial = [codigosEquip[4],
                          "SerialNumberF2A3913", "SerialNumberB1M2932"]
        processadores = [codigosEquip[3], "Intel Core i7-8650 CPU @ 1.90GHz",
                         "Intel Xeon Silver 4114 2.2GHz, 10C/20T, 9.6GT/s"]
        nomemaquinas = [codigosEquip[2], "Ubuntu", "Monterey"]
        arquiteturas = [codigosEquip[1], "Intel86", "Intel86"]
        sistemas = [sistema[0], "Linux", "MacOS"]

        cursor.execute(
            "SELECT COUNT(idEquipamento) FROM Equipamento")
        row = cursor.fetchone()
        Equip = int(''.join(map(str, row)))
        print("\U0001F916 Equipamentos detectados:", Equip, "\n--------")
        cursor.execute(
            "SELECT COUNT(idParametro) FROM Parametro")
        rowPam = cursor.fetchone()
        Parametros = int(''.join(map(str, rowPam)))
        print("\U0001F916 Parametros detectados:", Parametros, "\n--------")

        if Equip < 1:
            cursor.execute(
                "SELECT COUNT(idLocal) FROM Local")
            rowLocal = cursor.fetchone()
            Locais = int(''.join(map(str, rowLocal)))
            print("\U0001F916 Locais detectados:", Locais)
            for i in range(Locais):
                i = i + 1
                a = i - 1
                cursor.execute("INSERT INTO Equipamento (fkFilial, fkLocal, serialNumber, nome,modelo,arqMaquina, sistemaOp) VALUES (?,?,?, ?,?, ?,?);",
                               (1000, i, numeros_serial[a], nomemaquinas[a], processadores[a], arquiteturas[a], sistemas[a]))
                print("\U0001F916 Inserção de dados de Equipamento:", i)
                conn.commit()

        if Parametros < 1:
            codigosHardware = [
                "psutil.cpu_percent(interval=None", "percpu=False)','psutil.disk_usage('/').percent", "psutil.virtual_memory().percent"]

            cursor.execute(
                "SELECT COUNT(idComponente) FROM Componente")
            rowComp = cursor.fetchone()
            Componentes = int(''.join(map(str, rowComp)))
            validacao = 0

            for p in range(Equip):
                p = p + 1
                for i in range(Componentes):
                    valor = codigosHardware[i]
                    i = i + 1
                    cursor.execute("INSERT INTO Parametro (fkEquipamento, fkComponente, codigo, valid) VALUES (?,?,?,?);",
                                   (p, i, valor, validacao))

            leitura(cursor, numero, tempo, conx,  cursorMySQL)
        else:
            leitura(cursor, numero, tempo, conx,  cursorMySQL)


def capturaMysql(conx, cursorMySQL):
    print("NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNN")
    print("Seja bem-vindo ao sistema de captura de dados do seu Hardware \U0001F604")
    tempo = 2
    numero = 10

    if (tempo > 0):
        print("\U0001F750 Iniciando captura dos dados...", "\n--------")
        meu_sistema = platform.uname()
        sistema = meu_sistema.system
        arqmaquina = meu_sistema.machine
        nomeMaquina = meu_sistema.node
        modelo = meu_sistema.processor
        numero_serial = buscar_serial()

        codigosEquip = [sistema, arqmaquina,
                        nomeMaquina, modelo, numero_serial]

        numeros_serial = [codigosEquip[4],
                          "SerialNumberF2A3913", "SerialNumberB1M2932"]
        processadores = [codigosEquip[3], "Intel Core i7-8650 CPU @ 1.90GHz",
                         "Intel Xeon Silver 4114 2.2GHz, 10C/20T, 9.6GT/s"]
        nomemaquinas = [codigosEquip[2], "Ubuntu", "Monterey"]
        arquiteturas = [codigosEquip[1], "Intel86", "Intel86"]
        sistemas = [sistema[0], "Linux", "MacOS"]

        cursorMySQL.execute(
            "SELECT COUNT(idEquipamento) FROM Equipamento")
        row = cursorMySQL.fetchone()
        Equip = int(''.join(map(str, row)))
        print("\U0001F916 Equipamentos detectados:", Equip, "\n--------")
        cursorMySQL.execute(
            "SELECT COUNT(idParametro) FROM Parametro")
        rowPam = cursorMySQL.fetchone()
        Parametros = int(''.join(map(str, rowPam)))
        print("\U0001F916 Parametros detectados:", Parametros, "\n--------")

        if Equip < 1:
            cursorMySQL.execute("SELECT COUNT(idLocal) FROM Local")
            rowLocal = cursorMySQL.fetchone()
            Locais = int(''.join(map(str, rowLocal)))
            print("\U0001F916 Locais detectados:", Locais)
            for i in range(Locais):
                i = i + 1
                a = i - 1
                cursorMySQL.execute("INSERT INTO Equipamento (fkFilial, fkLocal, serialNumber, nome,modelo,arqMaquina, sistemaOp) VALUES (%s,%s,%s, %s,%s, %s,%s);",
                                    (1000, i, numeros_serial[a], nomemaquinas[a], processadores[a], arquiteturas[a], sistemas[a]))

                print("\U0001F916 Inserção de dados de Equipamento:", i)
                print("test 1 realizado")
                conx.commit()

        if Parametros < 1:
            codigosHardware = [
                "psutil.cpu_percent(interval=None", "percpu=False)','psutil.disk_usage('/').percent", "psutil.virtual_memory().percent"]

            cursorMySQL.execute(
                "SELECT COUNT(idComponente) FROM Componente")
            rowComp = cursorMySQL.fetchone()
            Componentes = int(''.join(map(str, rowComp)))

            validacao = 0

            for p in range(Equip):
                p = p + 1
                for i in range(Componentes):
                    valor = codigosHardware[i]
                    i = i + 1

                    cursorMySQL.execute("INSERT INTO Parametro (fkEquipamento, fkComponente, codigo, valid) VALUES (%s,%s,%s,%s);",
                                        (p, i, valor, validacao))

            leituraMysql(cursorMySQL, numero, tempo)
        else:
            leituraMysql(cursorMySQL, numero, tempo)


def leitura(cursor, numero, tempo, conx, cursorMySQL):
    Quantidade = range(numero)
    for x in Quantidade:
        dataHora = datetime.now()
        dataHoraFormat = dataHora.strftime('%Y/%m/%d %H:%M:%S')

        percentualCPU = psutil.cpu_percent(interval=None, percpu=False)
        percentualDisco = psutil.disk_usage('/').percent
        percentualMemoria = psutil.virtual_memory().percent

        # Simulação de valores dos componentes de equipamentos

        percentualCPU3 = percentualCPU * 1.15
        percentualCPU2 = percentualCPU3 - (percentualCPU3 * 0.05)

        percentualMemoria3 = percentualMemoria * 1.10
        percentualMemoria2 = percentualMemoria * 1.15

        percentualDisco2 = percentualDisco - (percentualDisco * 0.05)
        percentualDisco3 = percentualDisco2 * 3

        # Simulação de Equipamentos:

        vetorHardware = [percentualCPU, percentualMemoria, percentualDisco]
        vetorHardware2 = [percentualCPU2, percentualMemoria2, percentualDisco2]
        vetorHardware3 = [percentualCPU3, percentualMemoria3, percentualDisco3]
        vetorEquip = [vetorHardware, vetorHardware2, vetorHardware3]

        cursor.execute(
            "SELECT COUNT(idEquipamento) FROM Equipamento")
        rowEquip = cursor.fetchone()
        Equipamentos = int(''.join(map(str, rowEquip)))
        print(
            "\U0001F916 Quantidade de Equipamentos detectados: ", Equipamentos)

        cursor.execute(
            "SELECT COUNT(idComponente) FROM Componente")
        rowComp = cursor.fetchone()
        Componentes = int(''.join(map(str, rowComp)))
        print(
            "\U0001F916 Quantidade de Componentes de Hardware detectados: ", Componentes, "\n--------")

        valor = 0
        for i in range(Equipamentos):
            i = i + 1
            for a in range(Componentes):
                valor = vetorEquip[i-1][a]
                a = a + 1
                cursor.execute("INSERT INTO Leitura (fkEquipamento, fkComponente, valor, momento) VALUES (?,?, ?, ?);",
                               (i, a, valor, dataHoraFormat))
                conn.commit()

            print("\U0001F4BB - Porcentagem de Utilização da CPU: {:.1f}%".format(percentualCPU),
                  "\n\U0001F4BB - Porcentagem de Utilização do Disco:", percentualDisco, '%',
                  "\n\U0001F4BB - Porcentagem de Utilização da Memoria:", percentualMemoria, '%',
                  "\n\U0001F55B - Data e Hora:", dataHoraFormat, "\n--------")

            conn.commit()
            cursorMySQL = conx.cursor()
            capturaMysql(conx, cursorMySQL)
            time.sleep(tempo)
    print("SQL Server - Captura de dados finalizada!")
    capturaMysql(conx, cursorMySQL)
    escolha = 0

def leituraMysql(cursorMySQL, numero, tempo):
    Quantidade = range(numero)
    for x in Quantidade:
        dataHora = datetime.now()
        dataHoraFormat = dataHora.strftime('%Y/%m/%d %H:%M:%S')

        percentualCPU = psutil.cpu_percent(interval=None, percpu=False)
        percentualDisco = psutil.disk_usage('/').percent
        percentualMemoria = psutil.virtual_memory().percent

        # Simulação de valores dos componentes de equipamentos

        percentualCPU3 = percentualCPU * 1.15
        percentualCPU2 = percentualCPU3 - (percentualCPU3 * 0.05)

        percentualMemoria3 = percentualMemoria * 1.10
        percentualMemoria2 = percentualMemoria * 1.15

        percentualDisco2 = percentualDisco - (percentualDisco * 0.05)
        percentualDisco3 = percentualDisco2 * 3

        # Simulação de Equipamentos:

        vetorHardware = [percentualCPU, percentualMemoria, percentualDisco]
        vetorHardware2 = [percentualCPU2, percentualMemoria2, percentualDisco2]
        vetorHardware3 = [percentualCPU3, percentualMemoria3, percentualDisco3]
        vetorEquip = [vetorHardware, vetorHardware2, vetorHardware3]

        cursorMySQL.execute(
            "SELECT COUNT(idEquipamento) FROM Equipamento")
        rowEquip = cursorMySQL.fetchone()
        Equipamentos = int(''.join(map(str, rowEquip)))
        print(
            "\U0001F916 Quantidade de Equipamentos detectados: ", Equipamentos)

        cursorMySQL.execute(
            "SELECT COUNT(idComponente) FROM Componente")
        rowComp = cursorMySQL.fetchone()
        Componentes = int(''.join(map(str, rowComp)))
        print(
            "\U0001F916 Quantidade de Componentes de Hardware detectados: ", Componentes, "\n--------")

        valor = 0
        for i in range(Equipamentos):
            i = i + 1
            for a in range(Componentes):
                valor = vetorEquip[i-1][a]
                a = a + 1

                cursorMySQL.execute("INSERT INTO Leitura (fkEquipamento, fkComponente, valor, momento) VALUES (%s,%s, %s, %s);",
                                    (i, a, valor, dataHoraFormat))
                conx.commit()

            print("\U0001F4BB - Porcentagem de Utilização da CPU: {:.1f}%".format(percentualCPU),
                  "\n\U0001F4BB - Porcentagem de Utilização do Disco:", percentualDisco, '%',
                  "\n\U0001F4BB - Porcentagem de Utilização da Memoria:", percentualMemoria, '%',
                  "\n\U0001F55B - Data e Hora:", dataHoraFormat, "\n--------")
            conx.commit()
            time.sleep(tempo)
    print("Captura de dados finalizada!")
    exit()
    escolha = 0


# Validações banco local e nuvem:

def validacaoMysql(conn, conx):
    print("Iniciando validações...")

    cursor = conn.cursor()
    cursorMySQL = conx.cursor()

    cursorMySQL.execute("CREATE DATABASE IF NOT EXISTS `healthsystem`;")

    cursorMySQL.execute("USE `healthsystem`;")

    cursorMySQL.execute("""
    CREATE TABLE IF NOT EXISTS `healthsystem`.`Empresa` (
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
);""")

    cursorMySQL.execute(
        "SELECT COUNT(idEmpresa) FROM `healthsystem`.`Empresa`")
    rowEmp = cursorMySQL.fetchone()
    empresa = int(''.join(map(str, rowEmp)))

    if empresa < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Empresa` VALUES (NULL,'PHILIPS DO BRASIL LTDA',61086336000103,'Avenida Marcos Penteado de Ulhoa Rodrigues',939,'Tambore','Barueri','SP','06460040');")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Credencial` (
    `idCredencial` INT NOT NULL,
    `tipoCredencial` VARCHAR(45) NOT NULL,
    `nivelPermissao` ENUM('1', '2', '3') NOT NULL,
    PRIMARY KEY (`idCredencial`)
);""")

    cursorMySQL.execute(
        "SELECT COUNT(idCredencial) FROM `healthsystem`.`Credencial`")
    rowCre = cursorMySQL.fetchone()
    credencial = int(''.join(map(str, rowCre)))

    if credencial < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Credencial` VALUES (323145,'Tecnico',1), (543221,'Analista',2), (386531,'Gerente',3);")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Usuario` (`fkEmpresa` INT NOT NULL,
  `idUsuario` INT NOT NULL AUTO_INCREMENT,
  `nome` VARCHAR(45) NOT NULL,
  `email` VARCHAR(45) NOT NULL,
  `senha` VARCHAR(45) NOT NULL,
  `fkcredencial` INT NOT NULL,
  PRIMARY KEY(`idUsuario`),
    FOREIGN KEY(`fkEmpresa`)
    REFERENCES `healthsystem`.`Empresa` (`idEmpresa`),
    FOREIGN KEY(`fkcredencial`)
    REFERENCES `healthsystem`.`Credencial` (`idCredencial`)
    );""")

    cursorMySQL.execute(
        "SELECT COUNT(idUsuario) FROM `healthsystem`.`Usuario`")
    rowUser = cursorMySQL.fetchone()
    usuario = int(''.join(map(str, rowUser)))

    if usuario < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Usuario` VALUES (1,NULL,'fernandoBrandao','fernando.brandao@sptech.school','1234',323145);")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Componente` (
    `idComponente` INT NOT NULL AUTO_INCREMENT,
    `nomeComponente` VARCHAR(45) NOT NULL,
    PRIMARY KEY(`idComponente`)
);
""")
    cursorMySQL.execute(
        "SELECT COUNT(idComponente) FROM `healthsystem`.`Componente`")
    rowComp = cursorMySQL.fetchone()
    componente = int(''.join(map(str, rowComp)))

    if componente < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Componente` (`nomeComponente`) VALUES ('CPU'), ('Memoria'), ('Disco');")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Filial` (
    `idFilial` INT NOT NULL AUTO_INCREMENT,
    `fkEmpresa` INT NOT NULL,
    `nomeFantasia` VARCHAR(45) NOT NULL,
    `logradouro` VARCHAR(45) NOT NULL,
    `numero` INT NOT NULL,
    `bairro` VARCHAR(45) NOT NULL,
    `cidade` VARCHAR(45) NOT NULL,
    `estado` CHAR(2) NOT NULL,
    `cep` CHAR(8) NOT NULL,
    PRIMARY KEY(`idFilial`),
    FOREIGN KEY(`fkEmpresa`)
    REFERENCES `healthsystem`.`Empresa` (`idEmpresa`))
    AUTO_INCREMENT = 1000;""")

    cursorMySQL.execute("SELECT COUNT(idFilial) FROM `healthsystem`.`Filial`")
    rowFil = cursorMySQL.fetchone()
    filial = int(''.join(map(str, rowFil)))

    if filial < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Filial` VALUES (NULL,1,'HOSPITAL SAO LUIZ GONZAGA','R MICHEL OUCHANA',94,'JACANA','SÃO PAULO','SP','02276140');")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Local` (
    `idLocal` INT NOT NULL AUTO_INCREMENT,
    `identificacao` VARCHAR(45) NOT NULL,
    PRIMARY KEY(`idLocal`)
);""")

    cursorMySQL.execute("SELECT COUNT(idLocal) FROM `healthsystem`.`Local`")
    rowLoc = cursorMySQL.fetchone()
    local = int(''.join(map(str, rowLoc)))

    if local < 1:
        cursorMySQL.execute(
            "INSERT INTO `healthsystem`.`Local` (`identificacao`) VALUES ('Sala de Ultrassom'),('Enfermaria'),('Sala de Manutenção');")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Equipamento` (
  `idEquipamento` INT NOT NULL AUTO_INCREMENT,
  `fkFilial` INT NOT NULL,
  `fkLocal` INT NOT NULL,
  `serialNumber` VARCHAR(45) NOT NULL,
  `nome` VARCHAR(45) NOT NULL,
  `modelo` VARCHAR(100) NOT NULL,
  `arqMaquina` VARCHAR(45) NOT NULL,
  `sistemaOp` VARCHAR(45) NOT NULL,
  PRIMARY KEY (`idEquipamento`),
    FOREIGN KEY (`fkLocal`)
    REFERENCES `healthsystem`.`Local` (`idLocal`),
  CONSTRAINT `fk_Equipamento_Filial1`
    FOREIGN KEY (`fkFilial`)
    REFERENCES `healthsystem`.`Filial` (`idFilial`)
    );
    """)

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Parametro` (
  `fkEquipamento` INT NOT NULL,
  `fkComponente` INT NOT NULL,
  `idParametro` INT NOT NULL AUTO_INCREMENT,
  `codigo` VARCHAR(100) NOT NULL,
  `valid` TINYINT NOT NULL,
  PRIMARY KEY (`idParametro`,`fkEquipamento`, `fkComponente`),
    FOREIGN KEY (`fkEquipamento`)
    REFERENCES `healthsystem`.`Equipamento` (`idEquipamento`),
    FOREIGN KEY (`fkComponente`)
    REFERENCES `healthsystem`.`Componente` (`idComponente`)
    );""")

    cursorMySQL.execute("""CREATE TABLE IF NOT EXISTS `healthsystem`.`Leitura` (
  `fkEquipamento` INT NOT NULL,
  `fkComponente` INT NOT NULL,
  `idLeitura` INT NOT NULL AUTO_INCREMENT,
  `valor` FLOAT NOT NULL,
  `momento` DATETIME NOT NULL,
  PRIMARY KEY (`idLeitura`,`fkEquipamento`, `fkComponente`),
    FOREIGN KEY (`fkEquipamento`)
    REFERENCES `healthsystem`.`Equipamento` (`idEquipamento`),
    FOREIGN KEY (`fkComponente`)
    REFERENCES `healthsystem`.`Componente` (`idComponente`)
    );""")

    print("Validações de tabelas finalizada com sucesso.")
    captura(conn, cursor, conx, cursorMySQL)

try:
    conx = mysql.connector.connect(
        host='172.17.0.2',
        user='root',
        password='urubu100',
        port=3306
    )
    print("Conexão com o Banco de Dados MySQL efetuada com sucesso.")

    server = 'healthsystem.database.windows.net'
    database = 'healthsystem'
    username = 'grupo01sis'
    password = '#GfHealthSystem01'
    conn = pyodbc.connect('DRIVER={ODBC Driver 18 for SQL Server};SERVER=' +
                          server+';DATABASE='+database+';ENCRYPT=yes;UID='+username+';PWD='+password)

    print("Conexão com o Banco de Dados SQL Server Azure efetuada com sucesso.")
    validacaoMysql(conn, conx)

    # Validações de Erro:
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Algo está errado com o Usuário do Banco ou a Senha.")
        time.sleep(10)
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("O banco de dados direcionado não existe.")
        time.sleep(10)
    else:
        print(err)
        time.sleep(10)
else:
    cursor = conn.cursor()
    cursorMySQL = conx.cursorMySQL()

# DBCC CHECKIDENT('Nome da tabela', RESEED, -1)
