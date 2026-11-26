"""Guess the country: hand-written clues (Phase 3).

Each entry: (name as in docs/data/countries.json, extra aliases, four clues hardest first,
capital clue or None). None = "Its capital is <capital from countries.json>."
Clue 2 is always where it is and some neighbours ("include" = not a full list unless stated).
Rules: no clue before the last names the country or uses its demonym; facts only where
sure; nothing about disputed borders, recognition, religion rankings or wars' blame.
"""

C = [
    # ---------------------------------------------------------------- Europe
    ("France", [], [
        "Thanks to its overseas territories it has more time zones than any other country.",
        "It is in western Europe. Its neighbours include Belgium, Germany, Switzerland and Spain.",
        "The Cannes Film Festival is held here every year.",
        "The Eiffel Tower and the Louvre are here."], None),
    ("Germany", [], [
        "It shares land borders with nine countries.",
        "It is in central Europe. Its neighbours include Poland, Austria, Denmark and the Netherlands.",
        "Volkswagen, BMW and Mercedes-Benz are all based here.",
        "The Brandenburg Gate stands in its capital, a city divided by a wall until 1989."], None),
    ("Italy", [], [
        "Two independent countries, San Marino and Vatican City, lie entirely inside it.",
        "It is in southern Europe. Its neighbours include France, Switzerland, Austria and Slovenia.",
        "Mount Etna and Mount Vesuvius are both here.",
        "The Leaning Tower of Pisa and the canals of Venice are here."], None),
    ("Spain", [], [
        "Its Canary Islands lie in the Atlantic off the coast of north-west Africa.",
        "It is in south-west Europe. Its neighbours include Portugal, France and Andorra.",
        "Gaudí's Sagrada Família, still being finished, is in its city of Barcelona.",
        "Flamenco and paella come from here."], None),
    ("Portugal", [], [
        "The Azores and Madeira, far out in the Atlantic, belong to it.",
        "It is in south-west Europe and has only one land neighbour, Spain.",
        "Its explorer Vasco da Gama was the first European to reach India by sailing around Africa.",
        "Port wine is named after its second city, Porto."], None),
    ("United Kingdom", ["The United Kingdom", "U.K.", "United Kingdom of Great Britain and Northern Ireland"], [
        "Its parliament has an elected House of Commons and an unelected House of Lords.",
        "It is in north-west Europe, and its only land border is with Ireland.",
        "Stonehenge is here.",
        "It is made up of England, Scotland, Wales and Northern Ireland."], None),
    ("Ireland", ["Republic of Ireland", "Eire", "Éire"], [
        "Its first official language is Irish, though most people speak English.",
        "It is in north-west Europe, and its only land neighbour is the United Kingdom.",
        "The Cliffs of Moher face the Atlantic on its west coast.",
        "Its national symbol is the shamrock, and its patron saint's day is 17 March."], None),
    ("Netherlands", ["The Netherlands"], [
        "About a quarter of its land lies below sea level.",
        "It is in north-west Europe. Its European neighbours are Germany and Belgium.",
        "Rotterdam, the biggest port in Europe, is here.",
        "It is famous for tulips, windmills and clogs."],
        "Its capital is Amsterdam, though the government sits in The Hague."),
    ("Belgium", [], [
        "It has three official languages: Dutch, French and German.",
        "It is in western Europe. Its neighbours are France, Luxembourg, Germany and the Netherlands.",
        "The Battle of Waterloo was fought here in 1815.",
        "It is famous for waffles, chocolate and the Atomium."],
        "Its capital, Brussels, is home to the main European Union institutions."),
    ("Luxembourg", [], [
        "It is the only grand duchy left in the world.",
        "It is in western Europe. Its neighbours are Belgium, France and Germany.",
        "It was one of the six founding members of what became the European Union.",
        "It is one of Europe's smallest countries, with fewer than a million people."],
        "Its capital has the same name as the country."),
    ("Switzerland", [], [
        "It has four national languages: German, French, Italian and Romansh.",
        "It is in central Europe. Its neighbours are Germany, France, Italy, Austria and Liechtenstein.",
        "The Red Cross was founded in its city of Geneva.",
        "It is famous for the Matterhorn, watches and cheese with holes."],
        "Its capital, officially the 'federal city', is Bern."),
    ("Austria", [], [
        "It has been officially neutral since 1955.",
        "It is in central Europe. Its neighbours include Germany, Switzerland, Italy and Hungary.",
        "Mozart was born in its city of Salzburg.",
        "The Sound of Music is set here."], None),
    ("Greece", [], [
        "It has about 6,000 islands and islets.",
        "It is in south-east Europe. Its neighbours include Albania, North Macedonia, Bulgaria and Turkey.",
        "Mount Olympus, home of the gods in ancient myth, is its highest mountain.",
        "The first modern Olympic Games were held here in 1896."], None),
    ("Norway", [], [
        "About nine in ten new cars sold here are fully electric (as of 2024).",
        "It is in northern Europe. Its neighbours are Sweden, Finland and Russia.",
        "Roald Amundsen, first to reach the South Pole, came from here.",
        "Its coast is famous for deep fjords and the midnight sun."], None),
    ("Sweden", [], [
        "Alfred Nobel, who founded the Nobel Prizes, was born here.",
        "It is in northern Europe. Its land neighbours are Norway and Finland, and a long bridge links it to Denmark.",
        "IKEA and Volvo were founded here.",
        "The pop group ABBA came from here."], None),
    ("Finland", [], [
        "It is nicknamed the land of a thousand lakes, though it has far more than that.",
        "It is in northern Europe. Its neighbours are Sweden, Norway and Russia.",
        "Nokia started out here, in a town of the same name.",
        "Santa Claus Village is in its northern region of Lapland."], None),
    ("Denmark", [], [
        "Greenland, the world's largest island, is part of its kingdom.",
        "It is in northern Europe, and its only land neighbour is Germany.",
        "LEGO was invented here.",
        "The Little Mermaid statue sits on its capital's waterfront."], None),
    ("Iceland", [], [
        "Its parliament, the Althing, was founded in 930, one of the oldest in the world.",
        "It is an island in the North Atlantic, between Norway and Greenland.",
        "It sits on the Mid-Atlantic Ridge and has many active volcanoes.",
        "The Blue Lagoon, a geothermal spa, is one of its best-known sights."], None),
    ("Poland", [], [
        "Copernicus, who said the Earth goes round the Sun, was born here.",
        "It is in central Europe. Its neighbours include Germany, Czechia, Ukraine and Lithuania.",
        "Marie Curie was born here.",
        "Its flag is white over red."], None),
    ("Czechia", ["Czech Republic", "The Czech Republic", "Czech"], [
        "Its people drink more beer per person than any other country's.",
        "It is in central Europe. Its neighbours are Germany, Poland, Slovakia and Austria.",
        "It split peacefully from Slovakia in 1993.",
        "Its capital, with the Charles Bridge, is nicknamed the City of a Hundred Spires."], None),
    ("Hungary", [], [
        "Its language is not related to its neighbours' but is distantly related to Finnish and Estonian.",
        "It is in central Europe. Its neighbours include Austria, Slovakia, Romania and Serbia.",
        "The Rubik's Cube was invented here.",
        "Its capital was formed in 1873 by uniting towns on both banks of the Danube."], None),
    ("Croatia", [], [
        "The necktie, or cravat, is named after its soldiers.",
        "It is in south-east Europe. Its neighbours include Slovenia, Hungary, Serbia and Bosnia and Herzegovina.",
        "It has more than a thousand islands along the Adriatic.",
        "Its walled city of Dubrovnik was a filming location for Game of Thrones."], None),
    ("Russia", ["Russian Federation"], [
        "It spans eleven time zones.",
        "It stretches across eastern Europe and northern Asia. Its neighbours include Finland, China, Mongolia and Kazakhstan.",
        "Lake Baikal, the world's deepest lake, is here.",
        "It is the largest country in the world by area."], None),
    ("Ukraine", [], [
        "It is the largest country lying entirely in Europe.",
        "It is in eastern Europe. Its neighbours include Poland, Romania, Moldova and Belarus.",
        "The 1986 Chernobyl nuclear disaster happened here.",
        "Its flag is blue over yellow."], None),
    ("Romania", [], [
        "Its Palace of the Parliament is one of the heaviest buildings in the world.",
        "It is in south-east Europe. Its neighbours include Hungary, Ukraine, Moldova and Bulgaria.",
        "The Danube reaches the Black Sea through a huge delta here.",
        "Bran Castle in Transylvania is sold to tourists as Dracula's castle."], None),
    ("Bulgaria", [], [
        "Its Rose Valley is famous for rose oil used in perfume.",
        "It is in south-east Europe. Its neighbours include Romania, Serbia, Greece and Turkey.",
        "Here, shaking your head traditionally means yes and nodding means no.",
        "Its Black Sea resorts include Sunny Beach."], None),
    ("Serbia", [], [
        "The Sava and the Danube meet in its capital.",
        "It is in south-east Europe. Its neighbours include Hungary, Romania, Bulgaria and Croatia.",
        "The EXIT music festival is held in a fortress in its city of Novi Sad.",
        "Tennis great Novak Djokovic was born here."], None),
    ("Slovenia", [], [
        "More than half of it is covered in forest.",
        "It is in central Europe. Its neighbours are Italy, Austria, Hungary and Croatia.",
        "Its flag shows Mount Triglav, its highest peak.",
        "Lake Bled, with a little church on an island, is here."], None),
    ("Slovakia", [], [
        "Its capital is the only one in the world that borders two other countries.",
        "It is in central Europe. Its neighbours are Czechia, Poland, Ukraine, Hungary and Austria.",
        "It makes more cars per person than any other country.",
        "It split peacefully from Czechia in 1993."], None),
    ("Estonia", [], [
        "Skype was developed here.",
        "It is in northern Europe on the Baltic Sea. Its neighbours are Latvia and Russia.",
        "Its language is closely related to Finnish.",
        "It is the northernmost of the three Baltic states."], None),
    ("Latvia", [], [
        "Its language is one of only two living Baltic languages; the other is Lithuanian.",
        "It is in northern Europe. Its neighbours are Estonia, Lithuania, Russia and Belarus.",
        "Its capital has one of the world's finest collections of Art Nouveau buildings.",
        "It is the middle one of the three Baltic states."], None),
    ("Lithuania", [], [
        "It was the first Soviet republic to declare independence, in March 1990.",
        "It is in northern Europe. Its neighbours are Latvia, Belarus, Poland and Russia's Kaliningrad region.",
        "Basketball is by far its most popular sport.",
        "It is the largest and southernmost of the three Baltic states."], None),
    ("Albania", [], [
        "Its language forms its own branch of the Indo-European family.",
        "It is in south-east Europe. Its neighbours include Greece, North Macedonia and Montenegro.",
        "Hundreds of thousands of concrete bunkers were built here under communist rule.",
        "Its flag shows a black double-headed eagle on red."], None),
    ("Bosnia and Herzegovina", ["Bosnia", "Bosnia-Herzegovina", "BiH"], [
        "Its coastline is only about 20 km long, around the town of Neum.",
        "It is in south-east Europe. Its neighbours are Croatia, Serbia and Montenegro.",
        "The assassination that set off the First World War happened in its capital in 1914.",
        "The rebuilt Old Bridge of Mostar is its most famous landmark."], None),
    ("Malta", [], [
        "King George VI awarded its whole population the George Cross in 1942.",
        "It is a small island country in the Mediterranean, south of Sicily.",
        "Its language is the only Semitic language that is official in the European Union.",
        "Its capital is a fortified city built by the Knights of St John."], None),
    ("Monaco", [], [
        "It is the most densely populated country in the world.",
        "It sits on the Mediterranean coast and is surrounded on land by France.",
        "It has been ruled by the Grimaldi family for centuries.",
        "Its streets host a famous Formula One Grand Prix, and it is home to the Monte Carlo casino."],
        "Its capital has the same name as the country."),
    ("Vatican City", ["Vatican", "The Vatican", "Vatican City State"], [
        "It is guarded by the Swiss Guard.",
        "It is a walled enclave entirely surrounded by one city.",
        "It is the smallest country in the world, by both area and population.",
        "St Peter's Basilica and the Sistine Chapel are here."],
        "It is where the Pope lives, in the middle of Rome."),
    ("San Marino", [], [
        "It claims to be the world's oldest surviving republic, founded in 301.",
        "It is one of only three countries entirely surrounded by a single other country.",
        "The three towers on its flag stand on Mount Titano.",
        "It lies entirely inside Italy, near Rimini."],
        "Its capital has the same name as the country."),
    ("Liechtenstein", [], [
        "It is one of only two doubly landlocked countries in the world.",
        "It is a tiny country in central Europe, between Switzerland and Austria.",
        "It is one of the world's leading makers of false teeth.",
        "It is ruled by a prince."], None),
    ("Andorra", [], [
        "Its two co-princes are the President of France and a Spanish bishop.",
        "It is a tiny country high in the Pyrenees, between France and Spain.",
        "Its only official language is Catalan.",
        "It is famous for its ski resorts and tax-free shopping."], None),
    ("Georgia", ["Sakartvelo"], [
        "Archaeologists have found traces of winemaking here from about 8,000 years ago.",
        "It is where Europe meets Asia. Its neighbours include Turkey, Armenia, Azerbaijan and Russia.",
        "It has its own alphabet, used for no other national language.",
        "It shares its name with a US state."], None),
    ("Armenia", [], [
        "Its alphabet was created by Mesrop Mashtots around the year 405.",
        "It is a landlocked country in the South Caucasus. Its neighbours include Georgia and Iran.",
        "Mount Ararat, a national symbol, can be seen from its capital.",
        "Its flag is red, blue and orange."], None),
    ("Azerbaijan", [], [
        "Its capital lies below sea level, the lowest national capital in the world.",
        "It is on the Caspian Sea. Its neighbours include Russia, Georgia and Iran.",
        "It is nicknamed the Land of Fire, after natural gas flames that never go out.",
        "Its capital hosts a Formula One race on a street circuit."], None),
    ("Turkey", ["Türkiye", "Turkiye"], [
        "The ancient cities of Troy and Ephesus were in what is now this country.",
        "It spans Europe and Asia. Its neighbours include Greece, Bulgaria, Georgia and Iran.",
        "Cappadocia is famous for hot-air balloons over its rock 'fairy chimneys'.",
        "Its largest city, Istanbul, straddles Europe and Asia."], None),

    # ---------------------------------------------------------------- Asia
    ("China", ["People's Republic of China", "PRC"], [
        "It uses a single time zone, even though it is wide enough for about five.",
        "It is in East Asia. Its neighbours include Mongolia, Russia, India and Vietnam.",
        "The Terracotta Army was found near its city of Xi'an.",
        "The Great Wall is here."], None),
    ("Japan", ["Nippon", "Nihon"], [
        "Its national parliament is called the Diet.",
        "It is an island country in East Asia, east of the Korean Peninsula.",
        "Its high-speed bullet trains are called Shinkansen.",
        "Mount Fuji is its highest mountain."], None),
    ("South Korea", ["Korea", "Republic of Korea", "ROK"], [
        "Its alphabet, Hangul, was created in the 15th century.",
        "It is in East Asia, on the southern half of a peninsula, with just one land neighbour to its north.",
        "Samsung and Hyundai are based here.",
        "K-pop group BTS comes from here."], None),
    ("India", ["Bharat"], [
        "Its flag has a navy-blue wheel with 24 spokes.",
        "It is in South Asia. Its neighbours include Pakistan, China, Nepal and Bangladesh.",
        "The Ganges flows through it to the Bay of Bengal.",
        "The Taj Mahal is in its city of Agra."], None),
    ("Pakistan", [], [
        "Its founder, Muhammad Ali Jinnah, is known as the Quaid-e-Azam, the Great Leader.",
        "It is in South Asia. Its neighbours include India, Iran, Afghanistan and China.",
        "The ruins of the ancient city of Mohenjo-daro are here.",
        "It became independent in 1947, when British India was partitioned."], None),
    ("Bangladesh", [], [
        "It is one of the most densely populated large countries in the world.",
        "It is in South Asia. It is almost surrounded by India and also borders Myanmar.",
        "Part of the Sundarbans, a mangrove forest home to Bengal tigers, is here.",
        "It became independent from Pakistan in 1971."], None),
    ("Nepal", [], [
        "Its flag is the only national flag that isn't a rectangle.",
        "It is a landlocked country in South Asia, between India and China.",
        "Lumbini, the birthplace of the Buddha, is here.",
        "Mount Everest stands on its border with China."], None),
    ("Bhutan", [], [
        "It measures its progress by Gross National Happiness.",
        "It is a small landlocked kingdom in the Himalayas, between India and China.",
        "The Tiger's Nest monastery clings to a cliff here.",
        "Its flag shows a white dragon."], None),
    ("Sri Lanka", ["Ceylon"], [
        "In 1960 it elected the world's first female prime minister.",
        "It is an island in the Indian Ocean, just off the south-east tip of India.",
        "Sigiriya, an ancient fortress on top of a huge rock, is here.",
        "It is one of the world's biggest tea exporters."],
        "Its biggest city is Colombo; the official capital is Sri Jayawardenepura Kotte."),
    ("Maldives", ["The Maldives"], [
        "It is the lowest-lying country in the world.",
        "It is a chain of coral atolls in the Indian Ocean, south-west of India.",
        "It is the smallest country in Asia by both area and population.",
        "It is famous for luxury overwater bungalows."], None),
    ("Thailand", [], [
        "It is the only country in South-East Asia never colonised by a European power.",
        "It is in South-East Asia. Its neighbours are Myanmar, Laos, Cambodia and Malaysia.",
        "The full ceremonial name of its capital is one of the longest place names in the world.",
        "It was known as Siam until 1939."], None),
    ("Vietnam", ["Viet Nam"], [
        "It is the world's second-biggest coffee exporter, after Brazil.",
        "It is in South-East Asia. Its neighbours are China, Laos and Cambodia.",
        "Ha Long Bay, with thousands of limestone islands, is here.",
        "Pho, a noodle soup, is its best-known dish."], None),
    ("Cambodia", [], [
        "Its flag is one of the very few to show a building.",
        "It is in South-East Asia. Its neighbours are Thailand, Laos and Vietnam.",
        "The Khmer Empire ruled much of South-East Asia from here.",
        "Angkor Wat is here."], None),
    ("Laos", ["Lao PDR"], [
        "It is the only landlocked country in South-East Asia.",
        "Its neighbours are China, Myanmar, Thailand, Cambodia and Vietnam.",
        "The Mekong forms much of its border with Thailand.",
        "The old royal city of Luang Prabang, with its temples and saffron-robed monks, is here."], None),
    ("Myanmar", ["Burma"], [
        "Its capital was moved to a brand-new purpose-built city in 2005-2006.",
        "It is in South-East Asia. Its neighbours include Thailand, India, Bangladesh and China.",
        "Thousands of ancient temples cover the plain of Bagan.",
        "The golden Shwedagon Pagoda stands in its biggest city, Yangon."], None),
    ("Malaysia", [], [
        "Its king is chosen every five years from among nine hereditary state rulers.",
        "It is split between a peninsula and the north of Borneo. Its neighbours include Thailand, Indonesia and Brunei.",
        "Proton is its national car maker.",
        "The Petronas Twin Towers are here."],
        "Its capital is Kuala Lumpur, though the government is based in Putrajaya."),
    ("Singapore", [], [
        "It became independent in 1965 after leaving Malaysia.",
        "It is a small island city-state at the southern tip of the Malay Peninsula.",
        "The sale of chewing gum is restricted here.",
        "The Marina Bay Sands hotel, with its rooftop pool, is here."],
        "Its capital has the same name as the country."),
    ("Indonesia", [], [
        "It is made up of more than 17,000 islands.",
        "It is in South-East Asia. Its land neighbours are Malaysia, Papua New Guinea and Timor-Leste.",
        "Komodo dragons live in the wild only here.",
        "Bali is one of its islands."],
        "Its biggest city, Jakarta, has long been its capital."),
    ("Philippines", ["The Philippines"], [
        "It is made up of more than 7,000 islands.",
        "It is an island country in South-East Asia, between the South China Sea and the Pacific.",
        "It is named after a Spanish king, Philip II.",
        "Colourful jeepneys are a famous form of public transport here."], None),
    ("Mongolia", [], [
        "It is the most sparsely populated country in the world.",
        "It is a landlocked country between Russia and China.",
        "Genghis Khan built his empire from here.",
        "Many people still live in round felt tents called gers."], None),
    ("Kazakhstan", [], [
        "It is the world's largest landlocked country.",
        "It is in Central Asia. Its neighbours include Russia, China, Uzbekistan and Kyrgyzstan.",
        "Yuri Gagarin, the first person in space, was launched from the Baikonur Cosmodrome here.",
        "It is the largest of the Central Asian countries whose names end in 'stan'."], None),
    ("Uzbekistan", [], [
        "It is one of only two doubly landlocked countries in the world.",
        "It is in Central Asia. Its neighbours include Kazakhstan, Turkmenistan, Tajikistan and Kyrgyzstan.",
        "The old Silk Road cities of Bukhara and Khiva are here.",
        "Samarkand's Registan square, with its tiled madrasas, is here."], None),
    ("Saudi Arabia", ["KSA"], [
        "It has no permanent rivers.",
        "It covers most of the Arabian Peninsula. Its neighbours include Jordan, Iraq, Kuwait and Yemen.",
        "Its flag carries an Arabic inscription above a sword.",
        "It is one of the world's biggest oil producers."], None),
    ("United Arab Emirates", ["UAE", "The UAE", "Emirates", "The Emirates"], [
        "A branch of the Louvre museum opened here in 2017.",
        "It is on the Arabian Peninsula. Its neighbours are Saudi Arabia and Oman.",
        "It is a federation of seven states, each with its own hereditary ruler.",
        "The Burj Khalifa, the world's tallest building, is in its city of Dubai."], None),
    ("Qatar", [], [
        "Thanks to natural gas, it has one of the highest incomes per person in the world.",
        "It is a small peninsula in the Gulf, and its only land border is with Saudi Arabia.",
        "The Al Jazeera news network is based here.",
        "It hosted the 2022 FIFA World Cup."], None),
    ("Iran", [], [
        "Its new year, Nowruz, begins at the spring equinox.",
        "It is in western Asia. Its neighbours include Iraq, Turkey, Pakistan and Afghanistan.",
        "The ruins of ancient Persepolis are here.",
        "It was known in the West as Persia until 1935."], None),
    ("Iraq", [], [
        "The ruins of ancient Babylon are here.",
        "It is in western Asia. Its neighbours include Iran, Turkey, Syria and Saudi Arabia.",
        "Much of ancient Mesopotamia, the 'land between the rivers', lay here.",
        "The Tigris and the Euphrates both flow through it."], None),
    ("Jordan", [], [
        "Its only coastline is a short stretch on the Gulf of Aqaba.",
        "It is in western Asia. Its neighbours include Saudi Arabia, Iraq and Syria.",
        "The Dead Sea, the lowest point on land, lies on its western border.",
        "Petra, a city carved into rose-red rock, is here."], None),
    ("Lebanon", [], [
        "The ruins of great Roman temples stand at Baalbek here.",
        "It is on the eastern shore of the Mediterranean. Its neighbours are Syria and Israel.",
        "Its capital was once nicknamed the Paris of the Middle East.",
        "Its flag shows a green cedar tree."], None),

    # ---------------------------------------------------------------- Africa
    ("Egypt", [], [
        "The Suez Canal runs through it.",
        "It is in north-east Africa. Its neighbours include Libya and Sudan.",
        "Its ancient writing was deciphered with the help of the Rosetta Stone.",
        "The Great Pyramid of Giza is here."], None),
    ("Morocco", [], [
        "Its city of Fez has one of the oldest universities still running, founded in 859.",
        "It is in north-west Africa, just across the Strait of Gibraltar from Spain.",
        "The Atlas Mountains run across it.",
        "Marrakesh and Casablanca are two of its best-known cities."], None),
    ("Algeria", [], [
        "It became independent from France in 1962.",
        "It is in North Africa. Its neighbours include Tunisia, Libya, Mali and Niger.",
        "Most of it lies in the Sahara.",
        "It is the largest country in Africa by area."], None),
    ("Tunisia", [], [
        "The Arab Spring protests began here in December 2010.",
        "It is in North Africa, between Algeria and Libya.",
        "The ruins of ancient Carthage are here.",
        "Star Wars desert scenes were filmed here, and Tatooine is named after its town Tataouine."], None),
    ("Nigeria", [], [
        "Its capital was moved from Lagos to a new city in 1991.",
        "It is in West Africa. Its neighbours are Benin, Niger, Chad and Cameroon.",
        "Its huge film industry is nicknamed Nollywood.",
        "It has the largest population in Africa."], None),
    ("Ghana", [], [
        "It became independent from Britain in 1957, led by Kwame Nkrumah.",
        "It is in West Africa. Its neighbours are Côte d'Ivoire, Burkina Faso and Togo.",
        "Lake Volta, one of the largest man-made lakes in the world, is here.",
        "It used to be called the Gold Coast."], None),
    ("Senegal", [], [
        "Gorée Island, a memorial to the Atlantic slave trade, lies off its coast.",
        "It is in West Africa. Its neighbours include Mauritania, Mali and Guinea, and it almost surrounds the Gambia.",
        "Its Cap-Vert peninsula is the westernmost point of mainland Africa.",
        "Its national football team are nicknamed the Lions of Teranga."], None),
    ("Kenya", [], [
        "Fossils found around Lake Turkana make it a key place in the story of human origins.",
        "It is in East Africa. Its neighbours include Tanzania, Uganda, Ethiopia and Somalia.",
        "The Maasai Mara reserve sees the great wildebeest migration every year.",
        "Marathon great Eliud Kipchoge comes from here."], None),
    ("Tanzania", [], [
        "It was formed in 1964 by uniting Tanganyika and Zanzibar.",
        "It is in East Africa. Its neighbours include Kenya, Uganda, Mozambique and Zambia.",
        "Serengeti National Park is here.",
        "Kilimanjaro, Africa's highest mountain, is here."],
        "Its capital is Dodoma, though its biggest city is Dar es Salaam."),
    ("Uganda", [], [
        "The White Nile begins here, flowing out of Lake Victoria.",
        "It is a landlocked country in East Africa. Its neighbours are Kenya, Tanzania, Rwanda, DR Congo and South Sudan.",
        "About half of the world's mountain gorillas live here.",
        "Winston Churchill called it the Pearl of Africa."], None),
    ("Ethiopia", [], [
        "Its calendar runs about seven to eight years behind the one used in Europe.",
        "It is a landlocked country in the Horn of Africa. Its neighbours include Kenya, Sudan, Somalia and Eritrea.",
        "Churches carved down into solid rock stand at Lalibela.",
        "Legend says coffee was first discovered here."], None),
    ("Rwanda", [], [
        "It banned plastic bags in 2008.",
        "It is a small landlocked country in East Africa. Its neighbours are Uganda, Tanzania, Burundi and DR Congo.",
        "It is called the land of a thousand hills.",
        "Visitors trek to see mountain gorillas in its Volcanoes National Park."], None),
    ("South Africa", ["RSA"], [
        "The world's first human heart transplant was performed here in 1967.",
        "It is at the southern tip of Africa. Its neighbours include Namibia, Botswana and Zimbabwe, and it surrounds Lesotho.",
        "Nelson Mandela became its president in 1994.",
        "Table Mountain overlooks its city of Cape Town."],
        "It has three capitals: Pretoria, Cape Town and Bloemfontein."),
    ("Namibia", [], [
        "Its coastal desert is thought to be the oldest desert in the world.",
        "It is in south-west Africa. Its neighbours are Angola, Botswana, South Africa and Zambia.",
        "The giant red dunes of Sossusvlei are here.",
        "Its Skeleton Coast is littered with shipwrecks."], None),
    ("Botswana", [], [
        "It has more elephants than any other country.",
        "It is a landlocked country in southern Africa. Its neighbours include South Africa, Namibia and Zimbabwe.",
        "The Okavango Delta floods part of the Kalahari here.",
        "It is one of the world's biggest diamond producers."], None),
    ("Zimbabwe", [], [
        "It is named after a medieval stone city whose ruins are here.",
        "It is a landlocked country in southern Africa. Its neighbours are South Africa, Botswana, Zambia and Mozambique.",
        "It used to be called Rhodesia.",
        "It shares Victoria Falls with Zambia."], None),
    ("Zambia", [], [
        "Copper is by far its biggest export.",
        "It is a landlocked country in southern Africa. Its neighbours include DR Congo, Tanzania, Malawi and Zimbabwe.",
        "It used to be called Northern Rhodesia.",
        "It shares Victoria Falls with Zimbabwe."], None),
    ("Madagascar", [], [
        "It is the fourth-largest island in the world.",
        "It is an island in the Indian Ocean, off the south-east coast of Africa.",
        "Its Avenue of the Baobabs is lined with giant trees.",
        "Lemurs live in the wild only here."], None),
    ("Mozambique", [], [
        "Its flag is the only national flag that shows a modern rifle.",
        "It is in south-east Africa. Its neighbours include Tanzania, Malawi, Zimbabwe and South Africa.",
        "It was a Portuguese colony, and Portuguese is its official language.",
        "Its long Indian Ocean coast faces Madagascar."], None),
    ("Angola", [], [
        "Its province of Cabinda is cut off from the rest of the country.",
        "It is in south-west Africa. Its neighbours include Namibia, Zambia and DR Congo.",
        "It is one of Africa's biggest oil producers.",
        "It was a Portuguese colony, and Portuguese is its official language."], None),
    ("DR Congo", ["DRC", "Democratic Republic of Congo", "Congo Kinshasa"], [
        "It is the most populous country where French is an official language.",
        "It is in central Africa. Its neighbours include Angola, Zambia, Uganda and the Republic of the Congo.",
        "It used to be called Zaire.",
        "It is the second-largest country in Africa by area."], None),
    ("Cameroon", [], [
        "It is called 'Africa in miniature' for its varied landscapes.",
        "It is in central Africa. Its neighbours include Nigeria, Chad, Gabon and the Central African Republic.",
        "Both French and English are official languages here.",
        "Its national football team are the Indomitable Lions."], None),
    ("Mali", [], [
        "Mansa Musa, often called the richest person in history, ruled an empire from here.",
        "It is a landlocked country in West Africa. Its neighbours include Algeria, Niger, Burkina Faso and Senegal.",
        "The Great Mosque of Djenné is the largest mud-brick building in the world.",
        "The legendary desert city of Timbuktu is here."], None),
    ("Côte d'Ivoire", ["Ivory Coast", "The Ivory Coast"], [
        "It is the world's largest producer of cocoa beans.",
        "It is in West Africa. Its neighbours include Ghana, Liberia, Guinea and Burkina Faso.",
        "Its official capital has a giant basilica modelled on St Peter's in Rome.",
        "Footballer Didier Drogba comes from here."],
        "Its biggest city is Abidjan; the official capital is Yamoussoukro."),
    ("Liberia", [], [
        "It was founded by freed slaves from the United States.",
        "It is in West Africa. Its neighbours are Sierra Leone, Guinea and Côte d'Ivoire.",
        "Its capital is named after US President James Monroe.",
        "Ellen Johnson Sirleaf, Africa's first elected female head of state, led it."], None),
    ("Lesotho", [], [
        "Its lowest point, about 1,400 m above sea level, is the highest low point of any country.",
        "It is completely surrounded by South Africa.",
        "It is called the Kingdom in the Sky.",
        "Its flag shows a traditional Basotho hat."], None),
    ("Mauritius", [], [
        "Its 1847 'Blue' stamp is one of the rarest stamps in the world.",
        "It is an island country in the Indian Ocean, east of Madagascar.",
        "The dodo lived only here before it was wiped out.",
        "Its beaches and lagoons make it a favourite honeymoon spot."], None),

    # ---------------------------------------------------------------- Americas
    ("United States", ["USA", "US", "U.S.", "U.S.A.", "America", "United States of America",
                       "The United States", "The US", "The USA"], [
        "Its flag has 13 stripes for its original colonies.",
        "Its only land neighbours are Canada, to the north, and Mexico, to the south.",
        "The Grand Canyon is here.",
        "The Statue of Liberty stands in New York Harbor."],
        "Its capital is Washington, D.C."),
    ("Canada", [], [
        "It has the longest coastline of any country.",
        "It is in North America, and its only land neighbour is the United States.",
        "Its two official languages are English and French.",
        "A red maple leaf is on its flag."], None),
    ("Mexico", [], [
        "Chichén Itzá, a great Maya city, is here.",
        "It is in North America. Its neighbours are the United States, Guatemala and Belize.",
        "It has more Spanish speakers than any other country.",
        "Its flag shows an eagle eating a snake on a cactus."], None),
    ("Cuba", [], [
        "A failed invasion landed at its Bay of Pigs in 1961.",
        "It is the largest island in the Caribbean, just south of Florida.",
        "Its streets are famous for 1950s American cars still in use.",
        "Its cigars are world famous."], None),
    ("Jamaica", [], [
        "Its Blue Mountains grow some of the world's most famous coffee.",
        "It is a Caribbean island, south of Cuba.",
        "Reggae began here, made famous by Bob Marley.",
        "Sprinter Usain Bolt comes from here."], None),
    ("Haiti", [], [
        "In 1804 it became the first country formed by a successful slave revolt.",
        "It shares the island of Hispaniola with the Dominican Republic.",
        "The Citadelle Laferrière here is the largest fortress in the Americas.",
        "Its official languages are French and Creole."], None),
    ("Dominican Republic", ["The Dominican Republic"], [
        "Baseball is its favourite sport, and it sends many players to the US major leagues.",
        "It shares the island of Hispaniola with Haiti.",
        "Merengue and bachata music come from here.",
        "Punta Cana is its best-known beach resort."], None),
    ("Costa Rica", [], [
        "It abolished its army in 1948.",
        "It is in Central America. Its neighbours are Nicaragua and Panama.",
        "About a quarter of its land is protected in national parks and reserves.",
        "Its 'pura vida' motto and cloud forests draw eco-tourists."], None),
    ("Panama", [], [
        "US dollar notes are used here alongside its own currency, the balboa.",
        "It is in Central America. Its neighbours are Costa Rica and Colombia.",
        "It is the narrow land bridge where Central America meets South America.",
        "Its famous canal links the Atlantic and Pacific oceans."], None),
    ("Guatemala", [], [
        "Its flag shows a quetzal, the bird its currency is named after.",
        "It is in Central America. Its neighbours are Mexico, Belize, Honduras and El Salvador.",
        "Lake Atitlán, ringed by volcanoes, is here.",
        "The great Maya city of Tikal is here."], None),
    ("Trinidad and Tobago", ["Trinidad", "Trinidad & Tobago", "T&T"], [
        "The steelpan, or steel drum, was invented here.",
        "It is a two-island country in the Caribbean, just off the coast of Venezuela.",
        "Its Pitch Lake is the largest natural lake of asphalt in the world.",
        "Its carnival and calypso music are world famous."], None),
    ("Bahamas", ["The Bahamas"], [
        "Columbus is thought to have first landed in the Americas on one of its islands in 1492.",
        "It is a chain of islands in the Atlantic, south-east of Florida.",
        "Swimming pigs are a tourist attraction on its Exuma islands.",
        "It is made up of about 700 islands and many more cays."], None),
    ("Argentina", [], [
        "Its name comes from the Latin word for silver.",
        "It is in South America. Its neighbours include Chile, Brazil, Uruguay and Bolivia.",
        "Aconcagua, the highest mountain outside Asia, is here.",
        "Footballers Diego Maradona and Lionel Messi come from here."], None),
    ("Brazil", ["Brasil"], [
        "Its official language is Portuguese.",
        "It borders every other South American country except Chile and Ecuador.",
        "Its capital was moved inland to a brand-new city in 1960.",
        "Rio de Janeiro and the Christ the Redeemer statue are here."], None),
    ("Chile", [], [
        "Its Atacama Desert is one of the driest places on Earth.",
        "It is in South America. Its neighbours are Argentina, Bolivia and Peru.",
        "Easter Island, with its giant moai statues, belongs to it.",
        "It is a very long, thin country running down the Pacific coast."], None),
    ("Peru", [], [
        "Lake Titicaca lies on its border with Bolivia.",
        "It is in South America. Its neighbours are Ecuador, Colombia, Brazil, Bolivia and Chile.",
        "The giant Nazca Lines are drawn in its desert.",
        "Machu Picchu is here."], None),
    ("Colombia", [], [
        "It is the only South American country with coasts on both the Pacific and the Caribbean.",
        "Its neighbours are Venezuela, Brazil, Peru, Ecuador and Panama.",
        "Novelist Gabriel García Márquez came from here.",
        "It is famous for its coffee and for singer Shakira."], None),
    ("Venezuela", [], [
        "Its name means 'little Venice'.",
        "It is in northern South America. Its neighbours are Colombia, Brazil and Guyana.",
        "It has the largest proven oil reserves in the world.",
        "Angel Falls, the world's highest uninterrupted waterfall, is here."], None),
    ("Ecuador", [], [
        "Its currency is the US dollar.",
        "It is in South America. Its neighbours are Colombia and Peru.",
        "The straw 'Panama hat' is actually made here.",
        "The Galápagos Islands belong to it."], None),
    ("Bolivia", [], [
        "Salar de Uyuni, the largest salt flat in the world, is here.",
        "It is a landlocked country in South America. Its neighbours are Brazil, Paraguay, Argentina, Chile and Peru.",
        "It shares Lake Titicaca with Peru.",
        "It is named after the liberator Simón Bolívar."],
        "Its seat of government is La Paz; the constitutional capital is Sucre."),
    ("Paraguay", [], [
        "Its flag has a different emblem on each side.",
        "It is a landlocked country in South America. Its neighbours are Argentina, Brazil and Bolivia.",
        "Guaraní, an indigenous language, is official here alongside Spanish.",
        "The Itaipu Dam, one of the world's largest, is on its border with Brazil."], None),
    ("Uruguay", [], [
        "In 2013 it became the first country to legalise the cannabis trade nationwide.",
        "It is in South America. Its neighbours are Argentina and Brazil.",
        "Its flag shows a 'Sun of May' with a face.",
        "It hosted and won the first FIFA World Cup, in 1930."], None),

    # ---------------------------------------------------------------- Oceania
    ("Australia", [], [
        "Its capital was purpose-built as a compromise between its two biggest cities.",
        "It is the only country that covers a whole continent.",
        "The Great Barrier Reef lies off its north-east coast.",
        "Sydney Opera House is its most famous building."], None),
    ("New Zealand", ["NZ", "Aotearoa"], [
        "In 1893 it became the first self-governing country to give women the vote.",
        "It is an island country in the south-west Pacific, south-east of Australia.",
        "Its native people are the Māori.",
        "The Lord of the Rings films were shot here."], None),
    ("Fiji", [], [
        "It is made up of more than 300 islands.",
        "It is an island country in the South Pacific, north of New Zealand.",
        "Its men's rugby sevens team won Olympic gold in 2016 and 2021.",
        "Its main island is Viti Levu."], None),
    ("Papua New Guinea", ["PNG"], [
        "More than 800 languages are spoken here.",
        "It shares the island of New Guinea with Indonesia.",
        "A bird of paradise is on its flag.",
        "It lies just north of Australia."], None),
]

# Never fuzzy-matched to an answer (real places that aren't answers or countries.json entries).
EXTRA_DECOYS = ["England", "Scotland", "Wales", "Northern Ireland", "Greenland", "Taiwan", "Hong Kong",
                "Macau", "Kosovo", "Palestine", "Tibet", "Puerto Rico", "Siam", "Persia", "Zaire", "Rhodesia",
                "Abyssinia", "Formosa", "Borneo", "Hispaniola", "Tasmania", "Sicily", "Sardinia", "Corsica"]
