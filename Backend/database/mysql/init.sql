-- 创建数据库并切换
CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- 创建示例表
CREATE TABLE IF NOT EXISTS users (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  email VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS invite (
  id INT AUTO_INCREMENT PRIMARY KEY,
  creater VARCHAR(50) NOT NULL,
  invite_code VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS auther (
  id INT AUTO_INCREMENT PRIMARY KEY,
  editor VARCHAR(50) NOT NULL,
  cent INT NOT NULL
);

CREATE TABLE IF NOT EXISTS sqli_bypass (
  id INT AUTO_INCREMENT PRIMARY KEY,
  username VARCHAR(50) NOT NULL,
  password VARCHAR(50) NOT NULL,
  security_key  VARCHAR(50) NOT NULL
);

-- 插入测试数据
INSERT INTO users (username, email) VALUES
('alice', 'alice@example.com'),
('bb', 'bob@example.com');

INSERT INTO invite (creater, invite_code) VALUES
('alice', '481f6cc0511143ccdd7e2d1b1b94faf0a700a8b49cd13922a70b5ae28acaa8c5'),
('bob', '52f1476494897c64f417deb7ef7cd690f1cea9edce638746c420f1240d3d39dc');

INSERT INTO auther (editor, cent) VALUES
('admin', 100000),
('LaoWang', 50);

INSERT INTO sqli_bypass (username, password,security_key) VALUES
('admin', 'qwudasjqwwiue83g2h2g312h3gj123','asiudoaisudusyaihjhad'),
('LaoWang', 'asduoijczkxcaiuwoeqpwoieasjdka','asudoiausdoiausdxcxzxczq7');

-- 创建用户并授权（确保主机名一致）
CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_user'@'%';