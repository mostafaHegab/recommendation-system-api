
INSERT INTO users (id, firstname, lastname, email, password, verified, image) VALUES("1", "u1", "u1", "u1@u.com", "111111", 0, "u1.png"),("2","u2", "u2", "u2@u.com", "111111", 0, "u2.png"),("3","u3", "u3", "u3@u.com", "111111", 0, "u3.png"),("4", "u4", "u4", "u4@u.com", "111111", 0, "u4.png"),("5", "u5", "u5", "u5@u.com", "111111", 0, "u5.png");

INSERT INTO places (name, country, city, lat, lng) VALUES("p1", "cn1", "c1", 0, 0),("p2", "cn1", "c2", 0, 0),("p3", "cn2", "c1", 0, 0),("p4", "cn2", "c2", 0, 0),("p5", "cn3", "c1", 0, 0);

INSERT INTO images (name, pid) VALUES("img11.png", 1), ("img12.png", 1), ("img13.png", 1),("img21.png", 2), ("img22.png", 2),("img31.png", 3);

INSERT INTO favorites (uid, pid) VALUES("1", 1), ("1", 2), ("1", 5),("2", 2), ("2", 3),("3", 4);

INSERT INTO comments (text, time, pid, uid) VALUES("c1 p1 u1", "2020-01-01 01:10:12", 1, "1"),("c2 p1 u2", "2020-01-01 01:10:12", 1, "2"),("c3 p1 u3", "2020-01-01 01:10:12", 1, "3"),("c1 p2 u1", "2020-01-01 01:10:12", 2, "1"),("c2 p2 u2", "2020-01-01 01:10:12", 2, "2"),("c3 p2 u3", "2020-01-01 01:10:12", 2, "3"),("c1 p3 u1", "2020-01-01 01:10:12", 3, "1"),("c2 p3 u2", "2020-01-01 01:10:12", 3, "2"),("c3 p3 u3", "2020-01-01 01:10:12", 3, "3");

INSERT INTO ratings (rate, pid, uid) VALUES(2, 1, "1"),(5, 1, "2"),(3, 1, "3"),(1, 2,"1"),(3, 2, "2"),(2, 2, "3"),(5,3, "1"),(5, 3, "2"),(3, 3, "3");





