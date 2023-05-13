INSERT INTO hotels (name, location, services, rooms_quantity, image_id) VALUES 
('Happy Walley', 'Shanghai, Wanda street, 20', '["Wi-Fi", "Pool", "Parking lot", "Conditioner"]', 15, 1),
('Foreign Resort', 'Shanghai, Weining street 40а', '["Wi-Fi", "Parking lot"]', 23, 2),
('The Best', 'Shanghai, Hongqiao street, 44А', '["Parking lot"]', 30, 3),
('Grand Hotel', 'Shanghai, Jiting street, 67', '["Wi-Fi", "Parking lot", "Gym"]', 55, 4),
('Palace', 'Shanghai, Waitang street, 62', '["Wi-Fi", "Parking lot", "Conditioner"]', 22, 5),
('Bridge Resort', 'Shanghai, Baoling street, 45', '["Wi-Fi", "Parking lot", "Conditioner", "Gym"]', 45, 6);

INSERT INTO rooms (hotel_id, name, description, price, quantity, services, image_id) VALUES
(1, 'Upgraded room with terrace', 'Room with a mountain view', 24500, 5, '["Free Wi-Fi", "Conditioner"]', 7),
(1, 'Delux PLUS', 'Gorgeous room with a nice view', 22450, 10, '["Free Wi-Fi", "Conditioner"]', 8),
(2, 'Room for 2 people', 'Roow with an ocean view', 4570, 15, '[]', 9),
(2, 'Room for 3 people', 'Room with a beautiful view.', 4350, 8, '[]', 10),
(3, 'Half-luxary family room with a single bed', 'Good choice for a family.', 7080, 20, '["Fridge"]', 11),
(3, '2 rooms luxary comfort', 'Beautiful room for a couple of lovers.', 9815, 10, '[]', 12),
(4, 'Double standard', 'Standard room for a couple.', 4300, 20, '["Free Wi-Fi", "Fridge"]', 13),
(4, 'Upgraded standard PLUS', 'Room to have fun together.', 4700, 35, '["Free Wi-Fi", "Fridge", "Bathroom", "Conditioner"]', 14),
(5, 'Standard room with two single beds (breakfast included)', 'Delicious breakfast and soft bed is a good way to start a day.', 5000, 15, '[]', 15),
(5, 'Half-luxary room (with breakfast)', 'Half-luxary is a perfect choice for you.', 8000, 7, '[]', 16),
(6, 'Standard (top building)', 'Standard room.', 8125, 45, '[]', 17);

INSERT INTO users (email, hashed_password) VALUES 
('test_1@gmail.com', 'hashed_pwd_1'),
('test_2@gmail.com', 'hashed_pwd_2');

INSERT INTO bookings (room_id, user_id, date_from, date_to, price) VALUES
(1, 1, '2023-06-15', '2023-06-30', 24500),
(7, 2, '2023-06-25', '2023-07-10', 4300);
