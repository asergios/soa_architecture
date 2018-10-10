DROP TABLE IF EXISTS CHECKOUT;
DROP TABLE IF EXISTS MERCHANT;
DROP TABLE IF EXISTS USER;
DROP TABLE IF EXISTS CLIENT;

CREATE TABLE USER(
  id TEXT PRIMARY KEY,
  name TEXT NOT NULL,
  email TEXT NOT NULL
);

CREATE TABLE MERCHANT(
  id TEXT PRIMARY KEY,
  FOREIGN KEY (id) REFERENCES USER(id)
);

CREATE TABLE CLIENT(
  id TEXT PRIMARY KEY,
  FOREIGN KEY (id) REFERENCES USER(id)
);

CREATE TABLE CHECKOUT (
  id TEXT PRIMARY KEY,
  amount REAL NOT NULL,
  return_url TEXT NOT NULL,
  cancel_url TEXT NOT NULL,
  merchant TEXT NOT NULL,
  FOREIGN KEY (merchant) REFERENCES MERCHANT(id)
);

INSERT INTO USER (id, name, email) VALUES ("tokensample123", "STROAM", "geral@stroam.net");
INSERT INTO MERCHANT (id) VALUES ("tokensample123");