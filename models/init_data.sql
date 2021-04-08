INSERT INTO users (id, firstname, lastname, email, password, verified) VALUES(1, "u1", "u1", "u1@u.com", "111111", 0),(2,"u2", "u2", "u2@u.com", "111111", 0),(3,"u3", "u3", "u3@u.com", "111111", 0),(4, "u4", "u4", "u4@u.com", "111111", 0),(5, "u5", "u5", "u5@u.com", "111111", 0);

INSERT INTO products (id, name, description) VALUES(1, "p1", "this is place one"),(2, "p2", "this is place two"),(3, "p3", "this is place three"),(4, "p4", "this is place four"),(5, "p5", "this is place five");

INSERT INTO favorites (id, uid, pid) VALUES(1, 1, 1), (2, 1, 2), (3, 1, 5),(4, 2, 2), (5, 2, 3),(6, 3, 4);

INSERT INTO comments (id, text, time, pid, uid) VALUES(1, "c1 p1 u1", "2020-01-01 01:10:12", 1, 1),(2, "c2 p1 u2", "2020-01-01 01:10:12", 1, 2),(3, "c3 p1 u3", "2020-01-01 01:10:12", 1, 3),(4, "c1 p2 u1", "2020-01-01 01:10:12", 2, 1),(5, "c2 p2 u2", "2020-01-01 01:10:12", 2, 2),(6, "c3 p2 u3", "2020-01-01 01:10:12", 2, 3),(7, "c1 p3 u1", "2020-01-01 01:10:12", 3, 1),(8, "c2 p3 u2", "2020-01-01 01:10:12", 3, 2),(9, "c3 p3 u3", "2020-01-01 01:10:12", 3, 3);

INSERT INTO ratings (id, rate, pid, uid) VALUES(1, 2, 1, 1),(2, 5, 1, 2),(3, 3, 1, 3),(4, 1, 2,1),(5, 3, 2, 2),(6, 2, 2, 3),(7, 5,3, 1),(8, 5, 3, 2),(9, 3, 3, 3);