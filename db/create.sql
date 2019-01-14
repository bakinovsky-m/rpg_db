GRANT ALL PRIVILEGES ON RPG_DB.* TO rpg_admin@localhost IDENTIFIED BY 'admin_pass';
GRANT SELECT, INSERT, UPDATE, DELETE ON RPG_DB.* to rpg_gamer@localhost IDENTIFIED BY 'gamer_pass';
GRANT SELECT ON RPG_DB.* TO rpg_viewer@locahost;

DROP DATABASE IF EXISTS RPG_DB;
CREATE DATABASE RPG_DB;
USE RPG_DB;

CREATE TABLE locations (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    x_coord INT NOT NULL,
    y_coord INT NOT NULL,
    hex_color VARCHAR(7)
);

INSERT INTO locations(name, x_coord, y_coord, hex_color) VALUES ('Skyrim', 0, 0, '#82b5e8');
INSERT INTO locations(name, x_coord, y_coord, hex_color) VALUES ('Morrowind', 1, 0, '#e8b792');
INSERT INTO locations(name, x_coord, y_coord, hex_color) VALUES ('Oblivion', 0, 1, '#0a672a');
INSERT INTO locations(name, x_coord, y_coord, hex_color) VALUES ('Los Santos', 1, 1, '#8d1c64');

CREATE TABLE inventories (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    capacity INT,
    size INT DEFAULT 0
);

INSERT INTO inventories(capacity) VALUES (3); -- for the DRAGONBORN

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

CREATE TABLE classes (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(50),
    base_health INT,
    base_dmg INT,
    item int,
    FOREIGN KEY (item) REFERENCES items(id)
);

INSERT INTO classes (name, base_health, base_dmg, item) values ('Warrior', 20, 2, 2);
INSERT INTO classes (name, base_health, base_dmg, item) values ('Archer', 15, 1, 4);
INSERT INTO classes (name, base_health, base_dmg, item) values ('Rogue', 10, 3, 1);

CREATE TABLE characters (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    lvl INT DEFAULT 1,
    curr_exp INT DEFAULT 0,
    base_health INT NOT NULL,
    base_damage INT NOT NULL,
    curr_location INT,
    inventory INT,
    class_ INT,
    FOREIGN KEY (curr_location) REFERENCES locations(id),
    FOREIGN KEY (inventory) REFERENCES inventories(id),
    FOREIGN KEY (class_) REFERENCES classes(id)
);

INSERT INTO characters (name, lvl, curr_exp, base_health, base_damage, curr_location, inventory, class_) values ('Dragonborn', 1, 0, 10, 10, 1, 1, 3);

CREATE TABLE monsters (
    id INT PRIMARY KEY AUTO_INCREMENT NOT NULL,
    name VARCHAR(25) NOT NULL,
    lvl INT NOT NULL,
    base_health INT NOT NULL,
    base_damage INT NOT NULL,
    curr_location INT,
    item INT,
    asset varchar(100),
    rarity INT,
    exp INT,
    FOREIGN KEY (curr_location) REFERENCES locations(id),
    FOREIGN KEY (item) REFERENCES items(id)
);

INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset, rarity, exp) values ('Rat', 1, 5, 2, 1, 1, 'assets/rat.png', 10, 1);
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset, rarity, exp) values ('Wolf', 1, 7, 5, 1, 2, 'assets/wolf.png', 20, 2);
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset, rarity, exp) values ('Zombie', 1, 10, 8, 1, 3, 'assets/zombie.png', 50, 5);
INSERT INTO monsters(name, lvl, base_health, base_damage, curr_location, item, asset, rarity, exp) values ('Dragon', 1, 15, 20, 1, 4, 'assets/dragon.png', 100, 10);

CREATE TABLE lvl_exp (
    lvl INT,
    exp INT
);

INSERT INTO lvl_exp (lvl, exp) values (1, 0);
INSERT INTO lvl_exp (lvl, exp) values (2, 10);
INSERT INTO lvl_exp (lvl, exp) values (3, 25);
INSERT INTO lvl_exp (lvl, exp) values (4, 40);
INSERT INTO lvl_exp (lvl, exp) values (5, 60);
INSERT INTO lvl_exp (lvl, exp) values (6, 85);
INSERT INTO lvl_exp (lvl, exp) values (7, 100);

CREATE TABLE items_in_inventory (
    inv int,
    item int,
    FOREIGN KEY (inv) REFERENCES inventories(id),
    FOREIGN KEY (item) REFERENCES items(id)
);