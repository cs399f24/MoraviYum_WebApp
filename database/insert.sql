-- Insert food options
INSERT INTO foods (vendor, food_name, food_id, price, calories, avg_rating) VALUES
('Cru5h', 'Crispy Chicken Tenders', 1, '$7.29/9.79', 380, NULL),
('Cru5h', 'Crispy Incogmeato Tenders', 2, '$6.99', 550, NULL),
('Cru5h', 'French Fried Potatoes', 3, '$2.99', 360, NULL),
('Cru5h', 'French Fried Tater Tots', 4, '$2.99', 440, NULL),
('Cru5h', 'Mozzarella Sticks', 5, '$7.29', 580, NULL),
('Cru5h', 'Burrito Bowl', 6, '$9.49', NULL, NULL),
('Cru5h', 'Quesadilla', 7, '$9.49', NULL, NULL),
('Cru5h', 'FUN Burger On Brioche Bun', 8, '$7.19', 540, NULL),
('Cru5h', 'FUN Double Burger On Brioche Bun', 9, '$9.29', 840, NULL),
('Cru5h', 'FUN Impossible Burger On Brioche Bun', 10, '$7.59', 380, NULL),
('Garbanzos', 'Bowl', 11, '$8.69', 160, NULL),
('Garbanzos', 'Flatbread', 12, '$8.69', 440, NULL),
('Garbanzos', 'Pita', 13, '$1.99', 440, NULL),
('Garbanzos', 'Plate', 14, '$8.69', 160, NULL),
('Garbanzos', 'Salad', 15, '$8.69', 160, NULL),
('Garbanzos', 'Laffa Wrap', 16, '$7.19', 490, NULL),
('Garbanzos', 'Baklava', 17, '$2.99', 230, NULL),
('Garbanzos', 'Falafel', 18, '$3.39', 60, NULL),
('Garbanzos', 'House Made Chips', 19, '$2.59', 530, NULL),
('Garbanzos', 'House Made Fries', 20, '$2.59', 530, NULL),
('Garbanzos', 'Hummus', 21, '$0.79', 190, NULL),
('Garbanzos', 'Pita, Side', 22, '$1.99', 440, NULL),
('Garbanzos', 'Seasoned Rice', 23, '$0.99', 110, NULL),
('Garbanzos', 'Tabbouleh', 24, '$0.99', 50, NULL),
('Hissho Sushi', 'Pork Gyoza Dumpling', 25, '$5.49', 310, NULL),
('Hissho Sushi', 'California Roll', 26, '$7.99', 330, NULL),
('Hissho Sushi', 'Krispy Krab Roll', 27, '$9.49', 410, NULL),
('Hissho Sushi', 'Nagano Special', 28, '$14.99', 730, NULL),
('Hissho Sushi', 'Outer Banks Roll', 29, '$13.99', 670, NULL),
('Hissho Sushi', 'Rainbow Roll', 30, '$12.99', 340, NULL),
('Hissho Sushi', 'Southern Charm Roll', 31, '$10.99', 410, NULL),
('Hissho Sushi', 'Spicy Roll', 32, '$8.99', 300, NULL),
('Hissho Sushi', 'Tempura Shrimp Roll', 33, '$10.99', 520, NULL),
('Hissho Sushi', 'Veggie Roll', 34, '$6.99', 320, NULL),
('Hissho Sushi', 'Special Cooked Combo', 35, '$12.99', 620, NULL),
('Natural', 'Acai Berry Bowl', 36, '$9.99', 470, NULL),
('Natural', 'Acai Peanut Butter & Banana Bowl', 37, '$9.99', 580, NULL),
('Natural', 'Chocolate Almond Smoothie', 38, '$4.79', 280, NULL),
('Natural', 'Honey Almond Smoothie', 39, '$4.79', 350, NULL),
('Natural', 'Pineapple Peach Almond Smoothie', 40, '$4.79', 220, NULL),
('Natural', 'Mango Banana Smoothie', 41, '$4.79', 200, NULL),
('Natural', 'Mango Mint Smoothie', 42, '$4.79', 210, NULL),
('Natural', 'Strawberry Banana Smoothie', 43, '$4.79', 170, NULL),
('Natural', 'Strawberry Mango Smoothie', 44, '$4.79', 160, NULL),
('Natural', 'Pineapple Coconut Smoothie', 45, '$4.79', 320, NULL),
('Natural', 'Pink Lemonade Smoothie', 46, '$4.79', 110, NULL),
('Natural', 'Tropical Fruit Smoothie', 47, '$4.79', 150, NULL),
('Zime', 'Artisan Blueberry Scone', 48, '$2.99', 360, NULL),
('Zime', 'Artisan Cinnamon Scone', 49, '$2.99', 410, NULL),
('Zime', 'Blueberry Crumb Muffin', 50, '$2.99', 400, NULL),
('Zime', 'Butter Croissant', 51, '$2.69', 300, NULL),
('Zime', 'Baked Croissant', 52, '$2.69', 240, NULL),
('Zime', 'Antipasto Entree Salad', 53, '$7.79', 520, NULL),
('Starbucks', 'Caffé Americano', 54, '$3.49/3.79/4.29', 15, NULL),
('Starbucks', 'Caffé Latte', 55, '$4.49/4.99/5.29', 190, NULL),
('Starbucks', 'Iced Caffé Latte', 56, '$4.99/5.49', 130, NULL),
('Starbucks', 'Caffé Mocha', 57, '$5.29/5.49/5.99', 370, NULL),
('Starbucks', 'Iced Caffé Mocha', 58, '$5.49/5.99', 350, NULL),
('Starbucks', 'Caramel Macchiato', 59, '$5.49/5.79/6.29', 250, NULL),
('Starbucks', 'Iced Caramel Macchiato', 60, '$5.79/6.29', 250, NULL),
('Starbucks', 'White Chocolate Mocha', 61, '$5.49/5.79/6.29', 390, NULL),
('Starbucks', 'Iced White Chocolate Mocha', 62, '$5.79/6.29', 390, NULL),
('Starbucks', 'Starbucks® Cold Brew Coffee', 63, '$2.79/2.99/3.29', 5, NULL),
('Starbucks', 'Chai Latte', 64, '$4.29/4.79/4.99', 240, NULL),
('Starbucks', 'Hot Chocolate', 65, '$3.79/4.29/4.79', 370, NULL),
('Starbucks', 'White Hot Chocolate', 66, '$3.79/4.29/4.79', 400, NULL),
('Starbucks', 'Iced Matcha Latte', 67, '$5.69', 190, NULL),
('Starbucks', 'Iced Matcha Lemonade', 68, '$5.59/5.99', 120, NULL),
('Starbucks', 'Strawberry Acai Lemonade Starbucks Refreshers® Beverage', 69, '$5.59/5.99', 140, NULL),
('Starbucks', 'Mango Dragonfruit Lemonade Starbucks Refreshers® Beverage', 70, '$5.59/5.99', 140, NULL),
('Starbucks', 'Pink Drink Starbucks Refreshers® Beverage', 71, '$5.59/5.99', 140, NULL),
('Starbucks', 'Dragon Drink Starbucks Refreshers® Beverage', 72, '$5.59/5.99', 130, NULL),
('Starbucks', 'Strawberry Acai Starbucks Refreshers® Beverage', 73, '$5.59/5.99', 100, NULL),
('Starbucks', 'Mango Dragonfruit Starbucks Refreshers® Beverage', 74, '$5.59/5.99', 90, NULL),
('Starbucks', 'Iced Pumpkin Spice Latte', 75, '$4.99', 370, NULL),
('Starbucks', 'Iced Caramel Apple Cream Latte', 76, '$4.99', 390, NULL);

-- Insert food images
INSERT INTO images (food_id, image_url) VALUES
(1, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_CrispyChickenTenders6Piece.png'),
(2, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_CrispyIncogmeatoTenders.png'),
(3, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_FrenchFriedPotatoes.png'),
(4, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_FrenchFriedTaterTots.png'),
(5, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_MozzarellaSticks5.png'),
(6, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_BurritoBowl.png'),
(7, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_Quesadilla.png'),
(8, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_FUNBurgerOnBriocheBun.png'),
(9, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_FUNDoubleBurgerOnBriocheBun.png'),
(10, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Crush_FUNImpossibleBurgerOnBriocheBun.png'),
(11, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Bowl.png'),
(12, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Flatbread.png'),
(13, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Pita.png'),
(14, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Plate.png'),
(15, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Salad.png'),
(16, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_LaffaWrap.png'),
(17, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Baklava.png'),
(18, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Falafel.png'),
(19, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_HouseMadeChips.png'),
(20, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_HouseMadeFries.png'),
(21, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Hummus.png'),
(22, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_PitaSide.png'),
(23, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_SeasonedRice.png'),
(24, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Garbanzo_Tabbouleh.png'),
(25, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_PorkGyozaDumpling.png'),
(26, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_CaliforniaRoll.png'),
(27, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_KrispyKrabRoll_SouthernCharmRoll.png'),
(28, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_NaganoSpecial.png'),
(29, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_OuterBanksRoll.png'),
(30, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_RainbowRoll.png'),
(31, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_KrispyKrabRoll_SouthernCharmRoll.png'),
(32, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_SpicyRoll.png'),
(33, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_TempuraShrimpRoll.png'),
(34, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_VeggieRoll.png'),
(35, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/HisshoSushi_SpecialCookedCombo.png'),
(36, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Natural_AcaiBerryBowl.png'),
(37, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Natural_AcaiPeanutButterAndBananaBowl.png'),
(38, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_ChocolateAlmondSmoothie.png'),
(39, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_HoneyAlmondSmoothie.png'),
(40, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_PineapplePeachAlmondSmoothie.png'),
(41, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_MangoBananaSmoothie.png'),
(42, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_MangoMintSmoothie.png'),
(43, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_StrawberryBananaSmoothie.png'),
(44, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_StrawberryMangoSmoothie.png'),
(45, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_PineappleCoconutSmoothie.png'),
(46, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_PinkLemonadeSmoothie.png'),
(47, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_TropicalFruitSmoothie.png'),
(48, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_ArtisanBlueberryScone.png'),
(49, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_ArtisanCinnamonScone.png'),
(50, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_BlueberryCrumbMuffin.png'),
(51, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_ButterCroissant.png'),
(52, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_BakedCroissant.png'),
(53, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Zime_AntipastoEntreeSalad.png'),
(54, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_CaffeAmericano.png'),
(55, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_CaffeLatte.png'),
(56, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedCaffeLatte.png'),
(57, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_CaffeMocha.png'),
(58, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedCaffeMocha.png'),
(59, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_CaramelMacchiato.png'),
(60, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedCaramelMacchiato.png'),
(61, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_WhiteChocolateMocha.png'),
(62, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedWhiteChocolateMocha.png'),
(63, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_Starbucks%C2%AEColdBrewCoffee.png'),
(64, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_ChaiLatte.png'),
(65, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_HotChocolate.png'),
(66, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_WhiteHotChocolate.png'),
(67, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedMatchaLatte.png'),
(68, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedMatchaLemonade.png'),
(69, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_StrawberryAcaiLemonadeStarbucksRefreshersStarbucks_Starbucks%C2%AEBeverage.png'),
(70, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_MangoDragonfruitLemonadeStarbucksRefreshersStarbucks_Starbucks%C2%AEBeverage.png'),
(71, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_PinkDrinkStarbucksRefreshers%C2%AEBeverage.png'),
(72, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_DragonDrink%C2%AEStarbucksRefreshers%C2%AEBeverage.png'),
(73, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_StrawberryAcaiStarbucksRefreshers%C2%AEBeverage.png'),
(74, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_MangoDragonfruitStarbucksRefreshers%C2%AEBeverage.png'),
(75, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedPumpkinSpice.png'),
(76, 'https://temp-bucket-2024-11-20.s3.amazonaws.com/Starbucks_IcedCaramelAppleCreamLatte.png');
