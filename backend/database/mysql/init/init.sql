-- 创建数据库并切换
CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- 创建用户（如果不存在）
CREATE USER IF NOT EXISTS 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_user'@'%';
FLUSH PRIVILEGES;