INSERT INTO Users (FullName, Email, Password) VALUES
('Иван Иванов', 'ivan@example.com', 'password123'),
('Анна Смирнова', 'anna@example.com', 'password123'),
('Петр Петров', 'petr@example.com', 'password123');

INSERT INTO Breeds (BreedName, Description) VALUES
('Лабрадор', 'Крупная, дружелюбная порода, отличная для семей.'),
('Чихуахуа', 'Маленькая порода с большим характером.'),
('Бигль', 'Среднего размера порода, известна своим обонянием.');

INSERT INTO Dogs (OwnerID, BreedID, DogName, Size, ActivityLevel) VALUES
(1, 1, 'Барсик', 'large', 'high'),
(2, 2, 'Лаки', 'small', 'medium'),
(3, 3, 'Рекс', 'medium', 'low');

INSERT INTO Parks (ParkName, Location, Description, Popularity) VALUES
('Парк Победы', 'Санкт-Петербург', 'Большой парк с озером и зелеными зонами.', 5),
('Центральный парк', 'Москва', 'Огромный парк в центре города.', 10),
('Городской парк', 'Казань', 'Компактный парк для коротких прогулок.', 7);

INSERT INTO Meetings (OrganizerID, ParkID, StartDateTime, Duration, Status) VALUES
(1, 1, '2024-05-21 15:00:00', '1 hour', 'scheduled'),
(2, 2, '2024-05-22 10:00:00', '45 minutes', 'scheduled');

INSERT INTO MeetingDogs (MeetingID, DogID) VALUES
(1, 1),
(1, 2),
(2, 3);

INSERT INTO Moderators (FullName, Email, Password) VALUES
('Мария Сидорова', 'maria@example.com', 'adminpassword123');
