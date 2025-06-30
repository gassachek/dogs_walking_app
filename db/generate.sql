CREATE TABLE Users (
    UserID SERIAL PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL
);

CREATE TABLE Breeds (
    BreedID SERIAL PRIMARY KEY,
    BreedName VARCHAR(50) UNIQUE NOT NULL,
    Description TEXT
);

CREATE TABLE Dogs (
    DogID SERIAL PRIMARY KEY,
    OwnerID INT REFERENCES Users(UserID) ON DELETE CASCADE,
    BreedID INT REFERENCES Breeds(BreedID) ON DELETE CASCADE,
    DogName VARCHAR(50) NOT NULL,
    Size VARCHAR(20) CHECK (Size IN ('small', 'medium', 'large')) NOT NULL,
    ActivityLevel VARCHAR(20) CHECK (ActivityLevel IN ('low', 'medium', 'high')) NOT NULL
);

CREATE TABLE Parks (
    ParkID SERIAL PRIMARY KEY,
    ParkName VARCHAR(100) NOT NULL,
    Location VARCHAR(100) NOT NULL,
    Description TEXT,
    Popularity INT CHECK (Popularity >= 0)
);

CREATE TABLE Meetings (
    MeetingID SERIAL PRIMARY KEY,
    OrganizerID INT REFERENCES Users(UserID) ON DELETE CASCADE,
    ParkID INT REFERENCES Parks(ParkID) ON DELETE CASCADE,
    StartDateTime TIMESTAMP NOT NULL,
    Duration INTERVAL NOT NULL,
    Status VARCHAR(20) CHECK (Status IN ('scheduled', 'ongoing', 'completed')) NOT NULL
);

CREATE TABLE MeetingDogs (
    MeetingDogID SERIAL PRIMARY KEY,
    MeetingID INT REFERENCES Meetings(MeetingID) ON DELETE CASCADE,
    DogID INT REFERENCES Dogs(DogID) ON DELETE CASCADE
);

CREATE TABLE Moderators (
    ModeratorID SERIAL PRIMARY KEY,
    FullName VARCHAR(100) NOT NULL,
    Email VARCHAR(100) UNIQUE NOT NULL,
    Password VARCHAR(100) NOT NULL
);
