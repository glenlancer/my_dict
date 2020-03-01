-- Tables used for my_dict program.
-- WORDS
create table Words (
	WID           serial,
	Word          varchar(50) not null unique,
	Meaning       varchar(250) not null,
	Pronunciation varchar(50) not null,
	`date`        date,
	primary key (Word)
) ENGINE=InnoDB Default Charset=utf8;

-- USAGE
create table `Usage` (
	UID     serial,
	-- WID     bigint unsigned not null,
	Word    varchar(50) not null unique,
	`Usage` text not null,
	primary key (UID),
	foreign key (Word) references Words(Word)
) ENGINE=InnoDB Default Charset=utf8;

-- ARTICLE
create table Article (
	AID     serial,
	Title   varchar(100) not null,
	Content text not null,
	primary key (AID)
) ENGINE=InnoDB Default Charset=utf8;

-- REFERENCE
create table Reference (
	RID serial,
	-- WID bigint unsigned not null,
	Word varchar(50) not null unique,
	AID  bigint unsigned not null,
	primary key (RID),
	foreign key (Word) references Words(Word),
	foreign key (AID) references Article(AID)
) ENGINE=InnoDB Default Charset=utf8;
