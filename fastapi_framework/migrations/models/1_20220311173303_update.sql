-- upgrade --
ALTER TABLE `user` RENAME TO `users`;
ALTER TABLE `users` ADD UNIQUE INDEX `uid_users_name_6aafa3` (`name`);
-- downgrade --
ALTER TABLE `users` DROP INDEX `idx_users_name_6aafa3`;
ALTER TABLE `users` RENAME TO `user`;
