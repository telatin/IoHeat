PRAGMA encoding="UTF-8";



DROP TABLE IF EXISTS temp;
CREATE TABLE temp (
	device			TEXT,
	temp				FLOAT,
	created     DATETIME default current_timestamp,
	rec_date		DATE,
	rec_time		TIME,
	ip					TEXT,
);

CREATE TABLE actions (
	request			TEXT CHECK( reqtype IN ('ON','OFF','STATUS', '?') ) NOT NULL DEFAULT '?',
	created     DATETIME default current_timestamp,
	start_temp	FLOAT,
	start_date	DATE,
	start_time	TIME,
	
);
