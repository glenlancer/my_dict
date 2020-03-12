-- Tables used for my_dict program.
-- WORDS
create table Words (
	WID           serial,
	Word          varchar(50) not null unique,
	Meaning       varchar(250) not null,
	Pronunciation varchar(50),
	Exchange      varchar(100),
	`date`        datetime not null,
	primary key (Word)
) ENGINE=InnoDB Default Charset=utf8;

-- USAGE
create table `Usage` (
	UID     serial,
	Word    varchar(50) not null,
	`Usage` text not null,
	primary key (UID),
	foreign key (Word) references Words(Word)
) ENGINE=InnoDB Default Charset=utf8;

-- ARTICLE
create table Article (
	AID     serial,
	Title   varchar(100) not null unique,
	Content text not null,
	primary key (AID)
) ENGINE=InnoDB Default Charset=utf8;

-- REFERENCE
create table Reference (
	RID serial,
	Word varchar(50) not null,
	AID  bigint unsigned not null,
	primary key (RID),
	foreign key (Word) references Words(Word),
	foreign key (AID) references Article(AID)
) ENGINE=InnoDB Default Charset=utf8;

-- test data


-- alter Pronunciation not null attribute.
-- alter table Words change Pronunciation Pronunciation varchar(50);

-- add new column into Words table .
-- alter table Words add Exchange varchar(80);

-- alter Words `date` attribute.
-- alter table Words modify column `date` datetime not null;