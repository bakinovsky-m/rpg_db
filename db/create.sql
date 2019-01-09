GRANT ALL PRIVILEGES ON RPG_DB.* TO admin@localhost IDENTIFIED BY 'admin_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON RPG_DB.* to gamer@localhost;
GRANT SELECT ON RPG_DB.* TO viewer@locahost;

DROP DATABASE IF EXISTS RPG_DB;
CREATE DATABASE RPG_DB;
USE RPG_DB;

CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    x_coord INT NOT NULL,
    y_coord INT NOT NULL
);

INSERT INTO locations(name, x_coord, y_coord) VALUES ('Skyrim', 0, 0);
INSERT INTO locations(name, x_coord, y_coord) VALUES ('Morrowind', 1, 0);
INSERT INTO locations(name, x_coord, y_coord) VALUES ('Oblivion', 0, 1);
INSERT INTO locations(name, x_coord, y_coord) VALUES ('Los Santos', 1, 1);

CREATE TABLE inventories (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    capacity INT,
    size INT DEFAULT 0
);

INSERT INTO inventories(capacity) VALUES (3);
INSERT INTO inventories(capacity) VALUES (3);
INSERT INTO inventories(capacity) VALUES (3);
INSERT INTO inventories(capacity) VALUES (3);

CREATE TABLE characters (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    lvl INT NOT NULL,
    curr_exp INT NOT NULL,
    base_health INT NOT NULL,
    base_damage INT NOT NULL,
    curr_location INT,
    inventory INT,
    FOREIGN KEY (curr_location) REFERENCES locations(id),
    FOREIGN KEY (inventory) REFERENCES inventories(id)
);

INSERT INTO characters (name, lvl, curr_exp, base_health, base_damage, curr_location, inventory) values ('Dragonborn', 1, 0, 10, 10, 1, 1);
INSERT INTO characters (name, lvl, curr_exp, base_health, base_damage, curr_location, inventory) values ('Lydia', 1, 0, 10, 1, 1, 2);
INSERT INTO characters (name, lvl, curr_exp, base_health, base_damage, curr_location, inventory) values ('The Choosen One', 1, 0, 10, 1, 1, 3);
INSERT INTO characters (name, lvl, curr_exp, base_health, base_damage, curr_location, inventory) values ('Anton', 1, 0, 10, 1, 1, 4);

CREATE TABLE items (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50) NOT NULL,
    dmg INT,
    hp INT,
    block INT,
    asset VARCHAR(150)
);

INSERT INTO items(name, dmg, hp, block, asset) values ('Iron dagger', 2, 0, 0, 'assets/dagger.png');
INSERT INTO items(name, dmg, hp, block, asset) values ('Wooden shield', 0, 0, 1, 'assets/wooden_shield.png');
INSERT INTO items(name, dmg, hp, block, asset) values ('Sladkiy rulet', 0, 3, 0, 'assets/sl_rulet.png');
INSERT INTO items(name, dmg, hp, block, asset) values ('ArrowInAKnee', 3, 0, 0, 'assets/arrowinaknee.png');

CREATE TABLE monsters (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    lvl INT NOT NULL,
    base_health INT NOT NULL,
    base_damage INT NOT NULL,
    curr_location INT,
    item INT,
    asset varchar(100),
    FOREIGN KEY (curr_location) REFERENCES locations(id),
    FOREIGN KEY (item) REFERENCES items(id)
);

INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset) values ('Rat', 1, 5, 2, 1, 1, 'assets/rat.png');
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset) values ('Wolf', 1, 5, 2, 1, 2, 'assets/wolf.png');
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset) values ('Draugr', 1, 5, 2, 1, 3, 'assets/rat.png');
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset) values ('Dragon', 1, 5, 3, 1, 4, 'assets/rat.png');

CREATE TABLE items_in_inventory (
    inv int,
    item int,
    FOREIGN KEY (inv) REFERENCES inventories(id),
    FOREIGN KEY (item) REFERENCES items(id)
);