-- 创建数据库并切换
CREATE DATABASE IF NOT EXISTS app_db;
USE app_db;

-- 创建用户并授权（确保主机名一致）
CREATE USER 'app_user'@'%' IDENTIFIED BY 'app_password';
GRANT SELECT, INSERT, UPDATE, DELETE ON app_db.* TO 'app_user'@'%';