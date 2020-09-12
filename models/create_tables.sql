CREATE TABLE IF NOT EXISTS users (id BIGINT PRIMARY KEY NOT NULL, firstname CHAR(255) NOT NULL, lastname CHAR(255) NOT NULL, email CHAR(255) UNIQUE KEY NOT NULL, password CHAR(255) NOT NULL, verified INT NOT NULL, reset_code INT NOT NULL DEFAULT 0, image CHAR(255) NOT NULL DEFAULT "user.png");

CREATE TABLE IF NOT EXISTS places (id BIGINT PRIMARY KEY NOT NULL, name CHAR(255) NOT NULL, country CHAR(255) NOT NULL, city CHAR(255) NOT NULL, lat FLOAT NOT NULL, lng FLOAT NOT NULL);

CREATE TABLE IF NOT EXISTS images (id BIGINT PRIMARY KEY NOT NULL, name CHAR(255) NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id));

CREATE TABLE IF NOT EXISTS visits (id BIGINT PRIMARY KEY NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id), uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id));

CREATE TABLE IF NOT EXISTS favorites (id BIGINT PRIMARY KEY NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id), uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id));

CREATE TABLE IF NOT EXISTS plans (id BIGINT PRIMARY KEY NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id), uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id), date DATETIME NOT NULL);

CREATE TABLE IF NOT EXISTS comments (id BIGINT PRIMARY KEY NOT NULL, text CHAR(255) NOT NULL, time DATETIME NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id), uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id));

CREATE TABLE IF NOT EXISTS ratings (id BIGINT PRIMARY KEY NOT NULL, rate TINYINT NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id), uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id));

CREATE TABLE IF NOT EXISTS tags (id BIGINT PRIMARY KEY NOT NULL, name CHAR(255) NOT NULL);

CREATE TABLE IF NOT EXISTS place_tags (id BIGINT PRIMARY KEY NOT NULL, pid BIGINT NOT NULL, FOREIGN KEY (pid) REFERENCES places (id));

CREATE TABLE IF NOT EXISTS user_tags (id BIGINT PRIMARY KEY NOT NULL, uid BIGINT NOT NULL, FOREIGN KEY (uid) REFERENCES users (id));