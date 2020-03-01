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
	WID     bigint unsigned not null,
	`Usage` text not null,
	primary key (UID),
	foreign key (WID) references Words(WID)
) ENGINE=InnoDB Default Charset=utf8;

-- ARTICLE
create table Article (
	AID     serial,
	Content text not null,
	primary key (AID)
) ENGINE=InnoDB Default Charset=utf8;

-- REFERENCE
create table Reference (
	RID serial,
	WID bigint unsigned not null,
	AID bigint unsigned not null,
	primary key (RID),
	foreign key (WID) references Words(WID),
	foreign key (AID) references Article(AID)
) ENGINE=InnoDB Default Charset=utf8;