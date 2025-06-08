create table Contact(
    name varchar(50) PRIMARY KEY,
    address varchar(50),
    phoneNumber varchar(12) NOT NULL,
    check (phoneNumber like '9725%' and len(phoneNumber) = 12)
);

create table Situationship(
    contact1 varchar(50),
    contact2 varchar(50),
    check (contact1 <> contact2),
    foreign key (contact1) references Contact(Name) on delete cascade,
    foreign key (contact2) references Contact(Name), -- on delete cascade
    primary key (contact1,contact2)
    --previous line is commented out, because having two "ON DELETE CASCADE" in one table (both foreign keys depend on the same column in the primary table)
    -- leads to cyclic constraint
);

create table ZoomMeeting(
    startTime timestamp primary key,
    topic varchar(50),
    --foreign key (startTime) references Attends(startTime) on delete cascade
    --previous line is commented out, bc this constraint can not be implemented in SQL
);

create table Attends(
    startTime timestamp,
    attendee varchar(50),
    foreign key (attendee) references Contact(Name) on delete cascade,
    foreign key (startTime) references ZoomMeeting(startTime) , --on delete cascade
--we can't use timestamp as a foreign key, so "on delete cascade" is commented out
    primary key (startTime, attendee)
);

create table BeingLate(
    startTime timestamp,
    attendee varchar(50),
    reason varchar(50) not null,
    delay int check (delay>0),
    foreign key (startTime, attendee) references Attends(startTime, attendee), --on delete cascade,
    --we can't use timestamp as a foreign key, so "on delete cascade" is commented out
    foreign key (reason) references Contact(Name) on delete cascade,
    primary key (attendee, startTime)
);

create table Folder(
    fID int primary key,
    folderName varchar(50) not null,
    folderDate date not null,
);

create table ContainsFolder(
    folder1 int primary key,
    folder2 int,
    check (folder1 <> folder2),
    foreign key (folder1) references Folder(fID) on delete cascade
    --foreign key (folder2) references Folder(fID) on delete cascade
    --previous line is commented out, because having two "ON DELETE CASCADE" in one table
    -- (both foreign keys depend on the same column in the primary table), leads to cyclic constraint
);

create table FileType(
    extension varchar(3) primary key,
    check (len(extension) = 3)
);

create table Files(
    folder int,
    extension varchar (3),
    fileName varchar (50),
    size int,
    check (size > 0),
    foreign key (folder) references Folder(fID) on delete cascade,
    foreign key (extension) references FileType(extension) on delete cascade,
    primary key (folder, fileName, extension)
);

create table courseFile(
    folder int,
    extension varchar (3),
    fileName varchar (50),
    correctName bit,
    foreign key (folder, fileName, extension) references Files(folder, fileName, extension) on delete cascade,
    primary key (folder, fileName, extension)
);

create table importantFile(
    folder int,
    extension varchar (3),
    fileName varchar (50),
    timeEditedInHours float,
    check (timeEditedInHours > 0),
    foreign key (folder, fileName, extension) references Files(folder, fileName, extension) on delete cascade,
    primary key (folder, fileName, extension),
);

create table EditedIn(
    meeting timestamp,
    folder int,
    fileName varchar (50),
    extension varchar (3),
    foreign key (folder, fileName, extension) references importantFile(folder, fileName, extension) on delete cascade,
    foreign key (meeting) references ZoomMeeting(startTime),
    primary key (folder, fileName, extension,meeting)
);

create table permissionDate(
    blindDate date primary key
    );

create table accessPermission(
    permissionDate date,
    extension varchar (3),
    contact varchar(50),
    permissionReason varchar(50),
    foreign key (extension) references FileType(extension) on delete cascade,
    foreign key (permissionDate) references permissionDate(blindDate) on delete cascade,
    foreign key (contact) references Contact(name) on delete cascade,
    primary key (permissionDate,extension,contact)
);

create table myException(
    exceptionID int primary key,
    hotnessLevel float,
    check (hotnessLevel >= 0 and hotnessLevel <= 10),
    permissionDate date,
    extension varchar (3),
    contact varchar(50),
    foreign key (permissionDate,extension,contact) references accessPermission(permissionDate,extension,contact)
    on delete cascade
);

