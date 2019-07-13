PRAGMA encoding="UTF-8";


DROP TABLE IF EXISTS admins;
CREATE TABLE admins (
	email        TEXT PRIMARY KEY,
	created      DATETIME default current_timestamp,
	active       BOOL default 'Y',
	name         TEXT NOT NULL,
	surname      TEXT,
	screen_name  TEXT,
	bio          TEXT,
	A_NOTES      TEXT,
	last_acc     DATETIME,
	last_mail    DATETIME
);

DROP TABLE IF EXISTS users;
CREATE TABLE users (
	email        TEXT PRIMARY KEY,
	created      DATETIME default current_timestamp,
	active       BOOL default 'N',
	name         TEXT NOT NULL,
	surname      TEXT,
	screen_name  TEXT,
	bio          TEXT,
	A_NOTES      TEXT,
	last_acc     DATETIME,
	last_mail    DATETIME
);


DROP TABLE IF EXISTS devices;
CREATE TABLE devices (
	uuid         TEXT PRIMARY KEY,
	created      DATETIME default current_timestamp,
	user	       TEXT,
	active       BOOL default 'Y',
	last_acc     DATETIME,
	is_online    BOOL default 'N',
	is_heating   BOOL default 'N',
	A_NOTES      TEXT
);

DROP TABLE IF EXISTS reqs;
CREATE TABLE reqs (
	user         TEXT,
	device       TEXT,
	created      DATETIME default current_timestamp,
	reqtype      TEXT CHECK( reqtype IN ('Q','I','O') ) NOT NULL DEFAULT 'Q',
	ip           TEXT
);

DROP TABLE IF EXISTS temp;
CREATE TABLE temp (
	device			TEXT,
	temp				FLOAT,
	created     DATETIME default current_timestamp,
	rec_date		DATE,
	rec_time		TIME,
	ip					TEXT,

);
