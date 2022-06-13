CREATE TABLE usergroups(
    group_id INT(6) PRIMARY KEY AUTO_INCREMENT,
    description VARCHAR(255) NOT NULL
);

CREATE TABLE seniors(
    senior_id INT(6) PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(40) NOT NULL,
    family_name VARCHAR(40) NOT NULL,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(100) NOT NULL,
    address VARCHAR(255) NOT NULL,
    phone_number VARCHAR(30),
    group_id INT(6),
    FOREIGN KEY (group_id) REFERENCES usergroups(group_id)
);

CREATE TABLE juniors(
    junior_id INT(6) PRIMARY KEY AUTO_INCREMENT,
    first_name VARCHAR(40) NOT NULL,
    family_name VARCHAR(40) NOT NULL,
    senior_id INT(6),
    FOREIGN KEY (senior_id) REFERENCES seniors(senior_id),
    is_developmental BIT(1) DEFAULT 0
);

CREATE TABLE subscriptions(
    subscription_id INT(6) PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(40) NOT NULL,
    description TEXT
);

CREATE TABLE orders(
    order_id INT(6) PRIMARY KEY AUTO_INCREMENT,
    senior_id INT(6),
    subscription_id INT(6),
    order_date DATETIME NOT NULL,
    total_price DECIMAL(5, 2) NOT NULL,
    FOREIGN KEY (senior_id) REFERENCES seniors(senior_id),
    FOREIGN KEY (subscription_id) REFERENCES subscriptions(subscription_id)
);
