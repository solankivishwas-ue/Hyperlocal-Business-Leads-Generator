"""Geography data for cascading Country → State → City → Area dropdowns.

Data structure per country:
    {
        "has_states": bool,
        "states": {          # present when has_states is True
            "StateName": {
                "CityName": ["Area1", "Area2", ...]
            }
        },
        "cities": {          # present when has_states is False
            "CityName": ["Area1", "Area2", ...]
        }
    }
"""

GEO_DATA: dict = {

    # ==================================================================
    # INDIA  — 28 states + UTs
    # ==================================================================
    "India": {
        "has_states": True,
        "states": {
            "Andhra Pradesh": {
                "Visakhapatnam": ["MVP Colony", "Dwaraka Nagar", "Gajuwaka", "Steel Plant Area", "Rushikonda", "Seethammadhara"],
                "Vijayawada": ["Benz Circle", "Governorpet", "MG Road", "Kanuru", "Patamata", "Labbipet"],
                "Guntur": ["Brodipet", "Nagarampalem", "Arundelpet", "Kothapet"],
                "Tirupati": ["Balaji Colony", "Tiruchanur Road", "Renigunta Road", "Srinivasa Nagar"],
                "Nellore": ["Grand Trunk Road", "Vedayapalem", "Autonagar"],
                "Kurnool": ["Old Town", "New Town", "Srinivasa Nagar"],
            },
            "Assam": {
                "Guwahati": ["Pan Bazaar", "Silpukhuri", "Dispur", "Paltan Bazaar", "GS Road", "Six Mile", "Noonmati", "Bhangagarh"],
                "Silchar": ["Tarapur", "Ward Road", "Ambikapatty", "Premtola"],
                "Jorhat": ["AT Road", "Gar Ali", "Tarajan"],
                "Dibrugarh": ["Shantipara", "Lahowal", "Mancotta Road"],
            },
            "Bihar": {
                "Patna": ["Boring Road", "Ashok Rajpath", "Bailey Road", "Kankarbagh", "Rajendra Nagar", "Gandhi Maidan", "Danapur"],
                "Gaya": ["Civil Lines", "Station Road", "Bodh Gaya"],
                "Bhagalpur": ["Adampur", "TN Ganguly Road", "Maidan"],
                "Muzaffarpur": ["Mithanpura", "Brahmpura", "Company Bagh"],
            },
            "Chhattisgarh": {
                "Raipur": ["Shankar Nagar", "Pandri", "Telibandha", "VIP Road", "Devendra Nagar", "Pachpedi Naka"],
                "Bhilai": ["Sector 1", "Sector 6", "Sector 9", "Supela", "Charoda"],
                "Bilaspur": ["Vyapaar Vihar", "Sadar Bazar", "Torwa", "Mangla"],
                "Durg": ["Nehru Nagar", "Padmanabhapur", "Transport Nagar"],
            },
            "Delhi": {
                "New Delhi": [
                    "Connaught Place", "Karol Bagh", "Lajpat Nagar", "Saket",
                    "Dwarka", "Rohini", "Janakpuri", "Vasant Kunj",
                    "Nehru Place", "Pitampura", "Rajouri Garden", "Preet Vihar",
                    "Malviya Nagar", "Greater Kailash", "Hauz Khas", "Mayur Vihar",
                    "Shahdara", "Tilak Nagar", "Uttam Nagar", "Vikaspuri",
                ],
            },
            "Goa": {
                "Panaji": ["Altinho", "Fontainhas", "Miramar", "Dona Paula", "Caranzalem"],
                "Margao": ["Aquem", "Fatorda", "Monte Hill", "Comba"],
                "Vasco da Gama": ["Baina", "Bogda", "Headland Sada"],
                "Mapusa": ["Mapusa Market", "Calangute", "Anjuna"],
                "Calangute": ["Calangute Beach", "Baga", "Candolim"],
            },
            "Gujarat": {
                "Ahmedabad": [
                    "Ranip", "Satellite", "Navrangpura", "Bodakdev", "Prahlad Nagar",
                    "Vastrapur", "Maninagar", "Thaltej", "Gota", "Chandkheda",
                    "Bopal", "Ambawadi", "Paldi", "Ellisbridge", "Memnagar",
                    "Sarkhej", "Naranpura", "Vejalpur", "Nikol", "Vastral",
                    "Shahibaug", "Naroda", "Odhav", "Vatva", "Isanpur",
                ],
                "Surat": [
                    "Adajan", "Varachha", "Katargam", "Udhna", "Piplod",
                    "Vesu", "Althan", "Pal", "Rander", "City Light",
                    "Dumas", "Palanpur", "Bhatar", "Chalthan",
                ],
                "Vadodara": [
                    "Alkapuri", "Gotri", "Manjalpur", "Waghodia Road",
                    "Fatehganj", "Akota", "Sama", "Karelibaug",
                    "Sayajigunj", "Racecourse", "Harni Road",
                ],
                "Rajkot": [
                    "Kalawad Road", "150 Feet Ring Road", "Raiya Road",
                    "Kotecha Chowk", "Gondal Road", "University Road",
                    "Mavdi", "Yagnik Road",
                ],
                "Anand": ["Anand Town", "Vallabh Vidyanagar", "Karamsad", "Borsad"],
                "Gandhinagar": ["Sector 11", "Sector 16", "Sector 21", "Sector 28", "Infocity"],
                "Bhavnagar": ["Waghawadi Road", "Crescent Circle", "Atabhai Chowk", "Ghogha Circle"],
                "Jamnagar": ["Bedi Gate", "Chandi Bazaar", "Digvijay Plot", "Park Colony"],
            },
            "Haryana": {
                "Gurgaon": [
                    "DLF Phase 1", "DLF Phase 2", "DLF Phase 3", "Sector 29",
                    "Cyber City", "Sohna Road", "Golf Course Road", "MG Road",
                    "Udyog Vihar", "Palam Vihar", "Sector 56", "Manesar",
                ],
                "Faridabad": ["Sector 14", "Sector 21", "NIT", "Old Faridabad", "Palwal Road"],
                "Hisar": ["Urban Estate", "Model Town", "Janta Colony", "Red Square Market"],
                "Panipat": ["Model Town", "Sector 12", "IFFCO Chowk"],
                "Karnal": ["Sector 12", "Ansal Sushant City", "Model Town"],
                "Rohtak": ["Civil Lines", "Model Town", "Sector 1"],
                "Ambala": ["Ambala City", "Ambala Cantt", "Model Town"],
            },
            "Himachal Pradesh": {
                "Shimla": ["The Mall", "Lakkar Bazaar", "Chhota Shimla", "Khalini", "Sanjauli"],
                "Manali": ["Old Manali", "Mall Road", "Vashisht", "Naggar"],
                "Dharamsala": ["McLeod Ganj", "Bhagsu", "Dharamsala Main Town", "Palampur"],
                "Solan": ["The Mall", "Subzi Mandi", "Rajgarh Road"],
                "Kullu": ["Dhalpur", "Bhuntar", "Mohal"],
            },
            "Jharkhand": {
                "Ranchi": ["Main Road", "Ashok Nagar", "Harmu", "Kanke Road", "Bariatu", "Lalpur"],
                "Jamshedpur": ["Bistupur", "Sakchi", "Telco Colony", "Kadma", "Adityapur"],
                "Dhanbad": ["Hirapur", "Bank More", "Saraidhela", "Jharia"],
                "Bokaro": ["Sector 4", "Sector 9", "City Centre"],
            },
            "Karnataka": {
                "Bengaluru": [
                    "Koramangala", "Indiranagar", "HSR Layout", "Whitefield",
                    "Electronic City", "Jayanagar", "Malleshwaram", "BTM Layout",
                    "Bannerghatta Road", "Sarjapur Road", "Yelahanka", "JP Nagar",
                    "Rajajinagar", "Hebbal", "Marathahalli", "Bellandur",
                    "Brookefield", "CV Raman Nagar", "Banaswadi", "Hennur",
                    "Kengeri", "Vijayanagar", "Basavanagudi", "Ulsoor",
                ],
                "Mysuru": [
                    "VV Mohalla", "Jayalakshmipuram", "Kuvempunagar", "Vijayanagar",
                    "Saraswathipuram", "Gokulam", "Lakshmipuram",
                ],
                "Hubli": ["Deshpande Nagar", "Vidyanagar", "Gokul Road", "Navanagar", "Keshwapur"],
                "Mangaluru": ["Hampankatta", "Kodialbail", "Kadri", "Bejai", "Kankanady", "Attavar"],
                "Belagavi": ["Camp", "Shahpur", "Tilakwadi", "Shivaji Nagar"],
                "Davangere": ["MCC B Block", "P J Extension", "Azad Nagar"],
            },
            "Kerala": {
                "Kochi": [
                    "Ernakulam", "MG Road", "Kakkanad", "Edapally", "Aluva",
                    "Tripunithura", "Panampilly Nagar", "Vyttila", "Kadavanthra",
                    "Fort Kochi", "Palarivattom",
                ],
                "Thiruvananthapuram": [
                    "Kowdiar", "Pattom", "Vanchiyoor", "Vazhuthacaud",
                    "Medical College", "Ulloor", "Sreekaryam", "Technopark",
                ],
                "Kozhikode": ["Calicut Beach", "Palayam", "Mavoor Road", "Nadakkavu", "Westhill"],
                "Thrissur": ["Round South", "Shoranur Road", "Ayyanthole", "Ollur"],
                "Kollam": ["Chinnakada", "Asramam", "Sakthikulangara"],
                "Palakkad": ["Town Hall", "Sulthanpet", "Chandranagar"],
                "Kannur": ["SM Street", "Thavakkara", "Fort Road"],
            },
            "Madhya Pradesh": {
                "Indore": [
                    "Vijay Nagar", "Palasia", "MG Road", "AB Road",
                    "Scheme 54", "LIG Colony", "South Tukoganj",
                    "Geeta Bhawan", "Sapna Sangeeta", "Rajwada", "Bhanwarkuan",
                ],
                "Bhopal": [
                    "MP Nagar", "New Market", "Arera Colony", "Kolar Road",
                    "Habibganj", "Shyamla Hills", "Jahangirabad", "Bairagarh",
                ],
                "Jabalpur": ["Napier Town", "Wright Town", "Sadar", "Civil Lines", "Adhartal"],
                "Gwalior": ["Lashkar", "Morar", "Gwalior Fort Area", "Hazira"],
                "Ujjain": ["Freeganj", "Nanakheda", "Mahakaleshwar Road"],
            },
            "Maharashtra": {
                "Mumbai": [
                    "Andheri", "Bandra", "Powai", "Juhu", "Dadar",
                    "Kurla", "Borivali", "Malad", "Goregaon", "Kandivali",
                    "Thane", "Mulund", "Ghatkopar", "Chembur", "Vikhroli",
                    "Versova", "Lokhandwala", "Lower Parel", "Worli", "Colaba",
                    "Churchgate", "Fort", "Nariman Point",
                ],
                "Pune": [
                    "Koregaon Park", "Kothrud", "Baner", "Viman Nagar",
                    "Hadapsar", "Wakad", "Aundh", "Deccan", "Shivajinagar",
                    "Hinjewadi", "Pimpri", "Chinchwad", "Kalyani Nagar",
                    "Camp", "MG Road", "Nibm Road", "Kondhwa", "Kharadi",
                ],
                "Nagpur": [
                    "Dharampeth", "Sadar", "Civil Lines", "Sitabuldi", "Wardha Road",
                    "Pratap Nagar", "Hingna Road", "Manish Nagar", "Trimurti Nagar",
                ],
                "Nashik": ["College Road", "Gangapur Road", "Panchavati", "Cidco", "Dwarka", "Indira Nagar"],
                "Aurangabad": ["Cidco", "Garkheda", "Osmanpura", "Beed Bypass", "Cantonment"],
                "Solapur": ["Hotgi Road", "Vijapur Road", "Akkalkot Road", "Station Road"],
                "Kolhapur": ["Rajarampuri", "Shahupuri", "New Shahupuri"],
                "Navi Mumbai": ["Vashi", "Belapur", "Airoli", "Ghansoli", "Panvel", "Kharghar"],
            },
            "Manipur": {
                "Imphal": ["Thangal Bazaar", "Paona Bazaar", "BT Road", "Kakwa", "Kiyamgei"],
            },
            "Meghalaya": {
                "Shillong": ["Police Bazaar", "Laitumkhrah", "Mawlai", "Rynjah", "Nongthymmai"],
            },
            "Odisha": {
                "Bhubaneswar": [
                    "Saheed Nagar", "Nayapalli", "Chandrasekharpur", "Patia",
                    "Kharavel Nagar", "Unit 4", "Jaydev Vihar",
                ],
                "Cuttack": ["Buxi Bazaar", "Bidanasi", "CDA", "Mangalabag"],
                "Rourkela": ["Steel Township", "Udit Nagar", "Shaktinagar"],
                "Berhampur": ["Town", "Ambapua", "Golebazar"],
            },
            "Punjab": {
                "Chandigarh": ["Sector 17", "Sector 22", "Sector 35", "Sector 43", "Sector 9", "Sector 8"],
                "Ludhiana": ["Model Town", "Sarabha Nagar", "Civil Lines", "BRS Nagar", "Pakhowal Road", "Gill Road", "Dugri"],
                "Amritsar": ["Lawrence Road", "Ranjit Avenue", "Green Avenue", "Mall Road", "Majitha Road", "GT Road"],
                "Jalandhar": ["Model Town", "Guru Nanak Mission Chowk", "Nakodar Road", "Lajpat Nagar"],
                "Patiala": ["Model Town", "Leela Bhawan", "New Lal Bagh", "Tripuri"],
                "Mohali": ["Phase 5", "Phase 7", "Phase 9", "Aerocity", "IT City"],
                "Pathankot": ["Defence Colony", "Dhar Road", "Khalsa Colony"],
            },
            "Rajasthan": {
                "Jaipur": [
                    "Malviya Nagar", "Vaishali Nagar", "C Scheme", "Tonk Road",
                    "Mansarovar", "Banipark", "Civil Lines", "Sindhi Camp",
                    "Jagatpura", "Pratap Nagar", "Raja Park", "Bani Park",
                ],
                "Jodhpur": ["Sardarpura", "Paota", "Ratanada", "Shastri Nagar", "Chopasni Housing Board", "Basni"],
                "Udaipur": ["Ashok Nagar", "Chetak Circle", "Residency Road", "Suraj Pol", "Hiran Magri"],
                "Kota": ["Talwandi", "Vigyan Nagar", "DC Colony", "Nayapura", "Rangbari"],
                "Bikaner": ["Rani Bazaar", "Ganga Shahar", "Karni Nagar", "Shastri Nagar"],
                "Ajmer": ["Civil Lines", "Naya Bazaar", "Vaishali Nagar", "Pushkar Road"],
                "Bhilwara": ["Sewa Mandir", "RC Vyas Colony", "Sanjay Nagar"],
                "Alwar": ["Civil Lines", "Aravali Vihar", "Shastri Nagar"],
            },
            "Tamil Nadu": {
                "Chennai": [
                    "T Nagar", "Adyar", "Anna Nagar", "Velachery",
                    "Nungambakkam", "Mylapore", "Perambur", "Tambaram",
                    "Chrompet", "Porur", "Sholinganallur", "OMR",
                    "ECR", "Thiruvanmiyur", "Besant Nagar", "Guindy",
                    "Vadapalani", "Kodambakkam", "Ashok Nagar", "KK Nagar",
                ],
                "Coimbatore": [
                    "RS Puram", "Gandhipuram", "Peelamedu", "Saibaba Colony",
                    "Singanallur", "Avinashi Road", "Race Course", "Ukkadam",
                ],
                "Madurai": ["Anna Nagar", "KK Nagar", "Thiruppalai", "Bypass Road", "Goripalayam", "Alagar Kovil Road"],
                "Salem": ["Fairlands", "Suramangalam", "Shevapet", "Four Roads", "Hasthampatti"],
                "Tiruchirappalli": ["Thillai Nagar", "KK Nagar", "Tennur", "Srirangam"],
                "Tirunelveli": ["Palayamkottai", "Melapalayam", "Pettai"],
                "Vellore": ["Sathuvachari", "Gandhinagar", "Town", "CMC Area"],
            },
            "Telangana": {
                "Hyderabad": [
                    "Banjara Hills", "Jubilee Hills", "Gachibowli", "Madhapur",
                    "Hitech City", "Secunderabad", "Ameerpet", "Kukatpally",
                    "LB Nagar", "Miyapur", "Kondapur", "Begumpet",
                    "Mehdipatnam", "Dilsukhnagar", "Uppal", "Alwal",
                    "Bachupally", "Kompally", "Manikonda",
                ],
                "Warangal": ["Hanamkonda", "Kazipet", "Hunter Road", "NIT Area", "Nakkalagutta"],
                "Karimnagar": ["Collectorate Road", "Kothirampur", "RTC Complex"],
                "Nizamabad": ["Subhash Road", "Indira Nagar", "Beside Jagtial Road"],
            },
            "Uttarakhand": {
                "Dehradun": ["Rajpur Road", "Rajendra Nagar", "Dalanwala", "Patel Nagar", "Vasant Vihar", "Clock Tower"],
                "Haridwar": ["Har Ki Pauri", "Jwalapur", "Roorkee Road", "Ranipur More"],
                "Nainital": ["Mall Road", "Tallital", "Mallital", "Bhowali"],
                "Rishikesh": ["Ram Jhula", "Laxman Jhula", "Tapovan", "Muni Ki Reti"],
            },
            "Uttar Pradesh": {
                "Lucknow": [
                    "Hazratganj", "Gomti Nagar", "Aliganj", "Indira Nagar",
                    "Rajajipuram", "Mahanagar", "Vikas Nagar", "Alambagh",
                    "Chinhat", "Sushant Golf City",
                ],
                "Agra": ["Sadar Bazaar", "Civil Lines", "Tajganj", "Sikandra", "Kamla Nagar", "Fatehabad Road"],
                "Varanasi": ["Lanka", "Sigra", "Assi", "Cantonment", "Godowlia", "BHU Area", "Orderly Bazaar"],
                "Noida": ["Sector 18", "Sector 62", "Greater Noida", "Sector 50", "Sector 76", "Sector 137"],
                "Gurgaon": ["DLF Phase 1", "Sector 29", "Cyber City", "Sohna Road", "Golf Course Road", "MG Road"],
                "Kanpur": ["Civil Lines", "Kakadeo", "Swaroop Nagar", "Kidwai Nagar", "Arya Nagar"],
                "Allahabad": ["Civil Lines", "George Town", "Kydganj", "Naini", "Mumfordganj"],
                "Meerut": ["Shastri Nagar", "Garh Road", "Hapur Road", "Sadar"],
                "Ghaziabad": ["Indirapuram", "Vaishali", "Kaushambi", "Raj Nagar", "Shalimar Garden"],
                "Mathura": ["Vrindavan", "Govardhan Road", "Civil Lines", "Dampier Nagar"],
            },
            "West Bengal": {
                "Kolkata": [
                    "Park Street", "Salt Lake", "New Town", "Ballygunge",
                    "Behala", "Gariahat", "Jadavpur", "Esplanade",
                    "Howrah", "Dum Dum", "Alipore", "Tollygunge",
                    "Lake Town", "Dhakuria", "Kasba", "Rashbehari",
                ],
                "Siliguri": ["Sevoke Road", "Hill Cart Road", "Pradhan Nagar", "Bagdogra", "Matigara"],
                "Durgapur": ["Benachity", "City Centre", "NIT Township", "Bidhannagar"],
                "Asansol": ["GT Road", "Burnpur", "Raniganj", "Kulti"],
            },
        },
    },

    # ==================================================================
    # USA  — 50 states (major ones with full city/area data)
    # ==================================================================
    "USA": {
        "has_states": True,
        "states": {
            "Alabama": {
                "Birmingham": ["Downtown", "Southside", "Homewood", "Mountain Brook", "Hoover", "Vestavia Hills"],
                "Montgomery": ["Downtown", "Midtown", "Cloverdale", "East Montgomery"],
                "Huntsville": ["Downtown", "Madison", "Research Park", "Jones Valley"],
            },
            "Alaska": {
                "Anchorage": ["Downtown", "Midtown", "South Anchorage", "Eagle River"],
                "Fairbanks": ["Downtown", "College", "Badger Road"],
            },
            "Arizona": {
                "Phoenix": ["Downtown Phoenix", "Scottsdale", "Tempe", "Chandler", "Mesa", "Gilbert", "Ahwatukee", "North Phoenix", "Glendale"],
                "Tucson": ["Downtown", "Midtown", "Foothills", "Sam Hughes", "4th Avenue", "Oro Valley"],
                "Mesa": ["Downtown Mesa", "North Mesa", "East Mesa", "Mesa Arts District"],
                "Scottsdale": ["Old Town", "North Scottsdale", "South Scottsdale", "Kierland"],
                "Tempe": ["Downtown Tempe", "Arizona State University", "Tempe Marketplace"],
            },
            "Arkansas": {
                "Little Rock": ["Downtown", "Hillcrest", "Heights", "Chenal", "West Little Rock"],
                "Fayetteville": ["Downtown", "Dickson Street", "University District"],
            },
            "California": {
                "Los Angeles": [
                    "Hollywood", "Santa Monica", "Beverly Hills", "Venice",
                    "Silver Lake", "Downtown LA", "Culver City", "West Hollywood",
                    "Koreatown", "Echo Park", "Burbank", "Pasadena",
                    "Long Beach", "Inglewood", "Compton", "Glendale",
                ],
                "San Francisco": [
                    "SoMa", "Mission District", "Castro", "Nob Hill",
                    "Marina District", "Haight-Ashbury", "Financial District",
                    "North Beach", "Tenderloin", "Chinatown", "SOMA",
                    "Outer Sunset", "Inner Richmond", "Potrero Hill",
                ],
                "San Diego": ["Gaslamp Quarter", "La Jolla", "Mission Valley", "Hillcrest", "North Park", "Pacific Beach", "Little Italy", "Ocean Beach"],
                "San Jose": ["Downtown", "Willow Glen", "Almaden Valley", "Evergreen", "Santana Row", "Berryessa", "Campbell"],
                "Sacramento": ["Downtown", "Midtown", "Land Park", "East Sacramento", "Natomas", "Oak Park", "Curtis Park"],
                "Oakland": ["Downtown", "Temescal", "Rockridge", "Fruitvale", "Jack London Square", "Piedmont"],
                "Fresno": ["Downtown", "Tower District", "Old Fig Garden", "Northwest Fresno"],
                "Long Beach": ["Downtown", "Belmont Shore", "Bixby Knolls", "Signal Hill"],
            },
            "Colorado": {
                "Denver": ["LoDo", "RiNo", "Cherry Creek", "Capitol Hill", "Stapleton", "Highland", "Wash Park", "Cheesman Park", "Platt Park"],
                "Boulder": ["Pearl Street", "Hill District", "Downtown", "NoBo", "East Boulder"],
                "Colorado Springs": ["Downtown", "Old Colorado City", "Briargate", "Broadmoor", "Manitou Springs"],
                "Fort Collins": ["Old Town", "Midtown", "CSU Area", "South Fort Collins"],
                "Aurora": ["Downtown Aurora", "Southlands", "Fitzsimons", "Stapleton"],
            },
            "Connecticut": {
                "Hartford": ["Downtown", "West End", "Blue Hills", "South End"],
                "New Haven": ["Downtown", "East Rock", "Westville", "Wooster Square", "Yale Area"],
                "Stamford": ["Downtown", "North Stamford", "Shippan Point"],
                "Bridgeport": ["Downtown", "Black Rock", "Brooklawn"],
            },
            "Florida": {
                "Miami": ["Brickell", "Wynwood", "South Beach", "Coral Gables", "Little Havana", "Coconut Grove", "Midtown", "Design District", "Hialeah"],
                "Orlando": ["Downtown", "Lake Nona", "Dr Phillips", "Kissimmee", "Winter Park", "Sand Lake", "International Drive"],
                "Tampa": ["Ybor City", "Hyde Park", "Seminole Heights", "Downtown", "South Tampa", "Channelside", "Carrollwood"],
                "Jacksonville": ["Downtown", "San Marco", "Riverside", "Avondale", "Ponte Vedra", "Mandarin"],
                "Fort Lauderdale": ["Las Olas", "Victoria Park", "Flagler Village", "Rio Vista"],
                "St. Petersburg": ["Downtown", "Old Northeast", "Kenwood", "Grand Central"],
                "Sarasota": ["Downtown", "Burns Court", "Siesta Key", "Lakewood Ranch"],
            },
            "Georgia": {
                "Atlanta": ["Buckhead", "Midtown", "East Atlanta", "Little Five Points", "Decatur", "Inman Park", "Virginia-Highland", "Old Fourth Ward", "West End", "Ponce City Market"],
                "Savannah": ["Downtown", "Historic District", "Midtown", "Ardsley Park", "Victorian District"],
                "Augusta": ["Downtown", "Summerville", "Martinez", "Evans"],
                "Athens": ["Downtown", "Five Points", "Normaltown", "Boulevard"],
            },
            "Hawaii": {
                "Honolulu": ["Downtown", "Waikiki", "Manoa", "Kaimuki", "Kakaako", "Pearl City"],
                "Kailua": ["Downtown Kailua", "Lanikai", "Enchanted Lake"],
                "Hilo": ["Downtown", "Keaukaha", "Waiakea"],
            },
            "Idaho": {
                "Boise": ["Downtown", "Hyde Park", "North End", "East End", "Bench", "Eagle"],
                "Nampa": ["Downtown", "Central", "South Nampa"],
            },
            "Illinois": {
                "Chicago": ["The Loop", "River North", "Wicker Park", "Lincoln Park", "Hyde Park", "Pilsen", "Bucktown", "Gold Coast", "Wrigleyville", "Logan Square", "Andersonville", "Ravenswood"],
                "Naperville": ["Downtown", "Route 59 Corridor", "Nichols Library Area"],
                "Rockford": ["Downtown", "Midtown", "East Side", "Kishwaukee Corridor"],
                "Peoria": ["Downtown", "East Bluff", "West Bluff", "North Peoria"],
            },
            "Indiana": {
                "Indianapolis": ["Downtown", "Fountain Square", "Broad Ripple", "Mass Ave", "Irvington", "Carmel", "Fishers"],
                "Fort Wayne": ["Downtown", "Aboite", "Waynedale", "North Fort Wayne"],
                "Bloomington": ["Downtown", "IU Campus", "Elm Heights", "Bryan Park"],
            },
            "Iowa": {
                "Des Moines": ["Downtown", "East Village", "Beaverdale", "Ankeny", "West Des Moines"],
                "Cedar Rapids": ["Downtown", "Czech Village", "Kingston Village", "Marion"],
                "Iowa City": ["Downtown", "University District", "Coralville"],
            },
            "Kansas": {
                "Wichita": ["Downtown", "Delano", "College Hill", "East Wichita", "Andover"],
                "Kansas City": ["Downtown", "Westwood", "Mission", "Overland Park"],
                "Overland Park": ["Downtown Overland Park", "Blue Valley", "South OP"],
            },
            "Kentucky": {
                "Louisville": ["Downtown", "NuLu", "Highlands", "Germantown", "Crescent Hill", "St. Matthews"],
                "Lexington": ["Downtown", "Chevy Chase", "Beaumont", "Hamburg", "Nicholasville Road"],
            },
            "Louisiana": {
                "New Orleans": ["French Quarter", "Garden District", "Mid-City", "Uptown", "Marigny", "Bywater", "Lakeview"],
                "Baton Rouge": ["Downtown", "Mid-City", "Garden District", "LSU Area", "Perkins Road"],
                "Shreveport": ["Downtown", "Broadmoor", "Cross Lake", "Bossier City"],
            },
            "Maine": {
                "Portland": ["Old Port", "West End", "Munjoy Hill", "Bayside"],
                "Bangor": ["Downtown", "Orono", "Brewer"],
            },
            "Maryland": {
                "Baltimore": ["Inner Harbor", "Fells Point", "Canton", "Roland Park", "Charles Village", "Federal Hill", "Hampden"],
                "Bethesda": ["Downtown", "Chevy Chase", "Friendship Heights"],
                "Silver Spring": ["Downtown", "Sligo Creek", "Long Branch"],
                "Annapolis": ["Downtown", "West Annapolis", "Parole"],
            },
            "Massachusetts": {
                "Boston": ["Back Bay", "South End", "Beacon Hill", "Fenway", "Allston", "Cambridge", "Somerville", "North End", "South Boston", "Dorchester", "Jamaica Plain"],
                "Worcester": ["Downtown", "Main South", "Tatnuck Square", "Clark University Area"],
                "Springfield": ["Downtown", "Forest Park", "East Springfield", "Longmeadow"],
                "Cambridge": ["Harvard Square", "Central Square", "Inman Square", "Kendall Square"],
            },
            "Michigan": {
                "Detroit": ["Downtown", "Midtown", "Corktown", "Greektown", "New Center", "Eastern Market", "Rivertown"],
                "Grand Rapids": ["Downtown", "Eastown", "Heritage Hill", "East Hills", "Heartside"],
                "Ann Arbor": ["Downtown", "Burns Park", "Kerrytown", "North Side", "University Area"],
                "Lansing": ["Downtown", "Old Town", "REO Town", "East Lansing"],
            },
            "Minnesota": {
                "Minneapolis": ["Downtown", "Northeast", "Uptown", "North Loop", "Dinkytown", "Longfellow", "Seward"],
                "St. Paul": ["Downtown", "Summit Hill", "Cathedral Hill", "Hamline-Midway", "Lowertown"],
                "Rochester": ["Downtown", "Eastside", "Cascade", "Hawthorne"],
                "Duluth": ["Downtown", "Hillside", "East Hillside", "Canal Park"],
            },
            "Mississippi": {
                "Jackson": ["Downtown", "Fondren", "Belhaven", "Northside"],
                "Gulfport": ["Downtown", "Long Beach", "Ocean Springs"],
            },
            "Missouri": {
                "Kansas City": ["Power and Light District", "Westport", "Plaza", "Crossroads", "Brookside", "Midtown"],
                "St. Louis": ["Downtown", "Soulard", "Lafayette Square", "The Hill", "Central West End", "Clayton"],
                "Springfield": ["Downtown", "C-Street", "Battlefield", "South Side"],
            },
            "Montana": {
                "Billings": ["Downtown", "Heights", "West End", "Rimrock"],
                "Missoula": ["Downtown", "Rattlesnake", "University District"],
            },
            "Nebraska": {
                "Omaha": ["Downtown", "Dundee", "Benson", "Midtown", "Aksarben"],
                "Lincoln": ["Downtown", "Haymarket", "University Place", "South Lincoln"],
            },
            "Nevada": {
                "Las Vegas": ["The Strip", "Downtown", "Henderson", "Summerlin", "North Las Vegas", "Centennial Hills"],
                "Reno": ["Downtown", "Midtown", "Sparks", "South Reno"],
                "Henderson": ["Green Valley", "Anthem", "Downtown Henderson"],
            },
            "New Hampshire": {
                "Manchester": ["Downtown", "South Elm", "West Side", "North End"],
                "Nashua": ["Downtown", "South Nashua", "Mine Falls"],
                "Concord": ["Downtown", "West Concord", "East Concord"],
            },
            "New Jersey": {
                "Newark": ["Downtown", "Ironbound", "North Newark", "Weequahic"],
                "Jersey City": ["Downtown", "Journal Square", "The Heights", "Bergen-Lafayette", "Newport"],
                "Hoboken": ["Uptown", "Midtown Hoboken", "Downtown Hoboken"],
                "Princeton": ["Nassau Street", "Palmer Square", "Princeton Junction"],
                "Atlantic City": ["The Boardwalk", "Chelsea", "Ventnor", "Margate"],
            },
            "New Mexico": {
                "Albuquerque": ["Old Town", "Nob Hill", "Downtown", "Northeast Heights", "Corrales"],
                "Santa Fe": ["Downtown", "Museum Hill", "Railyard District"],
            },
            "New York": {
                "New York City": ["Manhattan", "Brooklyn", "Queens", "Bronx", "Staten Island", "Midtown", "SoHo", "Harlem", "Upper East Side", "Lower East Side", "Astoria", "Williamsburg", "Bushwick", "Park Slope", "DUMBO"],
                "Buffalo": ["Elmwood Village", "Downtown", "Allentown", "North Buffalo", "South Buffalo", "Kenmore"],
                "Albany": ["Center Square", "Downtown", "Pine Hills", "Delmar", "Colonie"],
                "Rochester": ["Downtown", "Park Avenue", "South Wedge", "Corn Hill", "Pittsford"],
                "Syracuse": ["Downtown", "Armory Square", "Eastwood", "Tipperary Hill"],
            },
            "North Carolina": {
                "Charlotte": ["Uptown", "South End", "NoDa", "Myers Park", "Dilworth", "Plaza Midwood", "University City"],
                "Raleigh": ["Downtown", "Glenwood South", "Five Points", "North Hills", "Brier Creek"],
                "Durham": ["Downtown", "Brightleaf Square", "American Village", "South Square"],
                "Greensboro": ["Downtown", "Fisher Park", "Irving Park", "Friendly"],
                "Winston-Salem": ["Downtown", "Arts District", "West End", "Ardmore"],
                "Chapel Hill": ["Downtown", "University Area", "Southern Village"],
            },
            "Ohio": {
                "Columbus": ["Downtown", "Short North", "German Village", "Victorian Village", "Clintonville", "Bexley", "Westerville"],
                "Cleveland": ["Downtown", "Ohio City", "Tremont", "Little Italy", "University Circle", "Lakewood"],
                "Cincinnati": ["Downtown", "Over-the-Rhine", "Hyde Park", "Mount Adams", "Covington"],
                "Dayton": ["Downtown", "Oregon District", "South Park", "Wright-Patterson Area"],
                "Toledo": ["Downtown", "Old West End", "Ottawa Hills", "Sylvania"],
            },
            "Oklahoma": {
                "Oklahoma City": ["Bricktown", "Midtown", "Paseo Arts District", "Capitol Hill", "Edmond"],
                "Tulsa": ["Blue Dome District", "Cherry Street", "Brookside", "Midtown", "Jenks"],
            },
            "Oregon": {
                "Portland": ["Pearl District", "Division Street", "Mississippi Avenue", "Hawthorne", "Alberta Arts District", "Sellwood", "St. Johns"],
                "Eugene": ["Downtown", "Whiteaker", "University District", "South Eugene"],
                "Salem": ["Downtown", "South Salem", "West Salem", "Pringle Creek"],
                "Bend": ["Old Town Bend", "Northwest Crossing", "River West"],
            },
            "Pennsylvania": {
                "Philadelphia": ["Center City", "Old City", "South Philly", "Fishtown", "Northern Liberties", "Rittenhouse Square", "Manayunk", "Chestnut Hill"],
                "Pittsburgh": ["Downtown", "Strip District", "Oakland", "Lawrenceville", "Squirrel Hill", "Shadyside", "Bloomfield"],
                "Allentown": ["Downtown", "South Side", "West End", "Center City"],
                "Erie": ["Downtown", "Little Italy", "West Erie", "Millcreek"],
                "Scranton": ["Downtown", "Green Ridge", "South Side"],
            },
            "Rhode Island": {
                "Providence": ["Downtown", "College Hill", "Federal Hill", "Wayland Square", "Fox Point"],
                "Newport": ["Downtown", "Thames Street", "Bellevue Avenue"],
            },
            "South Carolina": {
                "Charleston": ["Downtown", "Mount Pleasant", "West Ashley", "North Charleston", "James Island"],
                "Columbia": ["Downtown", "Five Points", "Forest Acres", "Shandon"],
                "Greenville": ["Downtown", "Augusta Road", "Overbrook"],
            },
            "Tennessee": {
                "Nashville": ["Downtown", "East Nashville", "12 South", "The Gulch", "Germantown", "Belmont-Hillsboro", "Sylvan Park"],
                "Memphis": ["Downtown", "Cooper-Young", "Midtown", "Overton Square", "East Memphis"],
                "Knoxville": ["Downtown", "Market Square", "Old City", "North Knoxville"],
                "Chattanooga": ["Downtown", "Northshore", "St. Elmo", "Brainerd"],
            },
            "Texas": {
                "Austin": ["Downtown", "South Congress", "East Austin", "Mueller", "Domain", "Cedar Park", "Round Rock", "Barton Creek", "South Lamar"],
                "Houston": ["Midtown", "Montrose", "The Woodlands", "Sugar Land", "Katy", "River Oaks", "Galleria", "Heights", "Pearland"],
                "Dallas": ["Uptown", "Deep Ellum", "Oak Lawn", "Plano", "Frisco", "McKinney", "Addison", "Highland Park", "Bishop Arts"],
                "San Antonio": ["Downtown", "Alamo Heights", "Stone Oak", "Medical Center", "Pearl District", "King William", "Southtown"],
                "Fort Worth": ["Sundance Square", "Near Southside", "Cultural District", "West 7th", "Camp Bowie"],
                "El Paso": ["Downtown", "Kern Place", "Mission Hills", "West Side"],
                "Arlington": ["Downtown", "Entertainment District", "Pantego", "Dalworthington Gardens"],
            },
            "Utah": {
                "Salt Lake City": ["Downtown", "Sugar House", "9th & 9th", "The Avenues", "Millcreek", "Cottonwood Heights"],
                "Provo": ["Downtown", "BYU Area", "Orem", "American Fork"],
                "Ogden": ["Downtown", "Historic 25th Street", "East Bench", "South Ogden"],
            },
            "Vermont": {
                "Burlington": ["Downtown", "Church Street", "Old North End", "South End", "New North End"],
                "Montpelier": ["Downtown", "Berlin", "East Montpelier"],
            },
            "Virginia": {
                "Virginia Beach": ["Oceanfront", "Town Center", "Chesapeake", "Norfolk"],
                "Richmond": ["Downtown", "Carytown", "Museum District", "Fan District", "Scott's Addition", "Church Hill"],
                "Norfolk": ["Downtown", "Ghent", "Ocean View", "Wards Corner"],
                "Arlington": ["Rosslyn", "Ballston", "Clarendon", "Pentagon City", "Crystal City"],
                "Alexandria": ["Old Town", "Del Ray", "Arlandria", "West End"],
                "Roanoke": ["Downtown", "South Roanoke", "Old Southwest", "Grandin Road"],
            },
            "Washington": {
                "Seattle": ["Capitol Hill", "Fremont", "Ballard", "SoDo", "Belltown", "South Lake Union", "Queen Anne", "Beacon Hill", "Pioneer Square", "Columbia City"],
                "Spokane": ["Downtown", "South Hill", "North Side", "East Central", "Browne's Addition"],
                "Bellevue": ["Downtown", "Crossroads", "Wilburton", "Redmond", "Kirkland"],
                "Tacoma": ["Downtown", "Proctor District", "Hilltop", "South Tacoma", "Fircrest"],
            },
            "West Virginia": {
                "Charleston": ["Downtown", "South Hills", "St. Albans", "Dunbar"],
                "Morgantown": ["Downtown", "WVU Area", "Suncrest", "Evansdale"],
            },
            "Wisconsin": {
                "Milwaukee": ["Downtown", "Brady Street", "Bay View", "Walker's Point", "Riverwest", "East Side"],
                "Madison": ["Downtown", "Isthmus", "Willy Street", "Monroe Street", "University Avenue"],
                "Green Bay": ["Downtown", "Ashwaubenon", "Allouez", "De Pere"],
                "Kenosha": ["Downtown", "Uptown", "Lakeshore"],
            },
            "Wyoming": {
                "Cheyenne": ["Downtown", "South Greeley", "Lions Park"],
                "Casper": ["Downtown", "East Side", "Bar Nunn"],
            },
        },
    },

    # ==================================================================
    # UK  — England, Scotland, Wales, Northern Ireland
    # ==================================================================
    "UK": {
        "has_states": True,
        "states": {
            "England": {
                "London": [
                    "Shoreditch", "Soho", "Canary Wharf", "Hackney", "Islington",
                    "Chelsea", "Notting Hill", "Brixton", "Camden", "Greenwich",
                    "Fulham", "Clapham", "Bermondsey", "Dalston", "Stratford",
                    "Elephant & Castle", "Bethnal Green", "Whitechapel", "Waterloo",
                    "Mayfair", "Kensington", "Chiswick", "Richmond",
                ],
                "Manchester": [
                    "Northern Quarter", "Deansgate", "Salford", "Didsbury",
                    "Chorlton", "Ancoats", "Spinningfields", "Castlefield",
                    "Fallowfield", "Withington", "Whalley Range",
                ],
                "Birmingham": [
                    "Digbeth", "Jewellery Quarter", "Sutton Coldfield",
                    "Solihull", "Edgbaston", "Moseley", "Harborne",
                    "Erdington", "Bournville", "Selly Oak",
                ],
                "Bristol": [
                    "Clifton", "Stokes Croft", "Harbourside",
                    "Fishponds", "Bedminster", "Montpelier", "Southville",
                    "Hotwells", "Easton", "St Werburghs",
                ],
                "Leeds": ["City Centre", "Headingley", "Chapel Allerton", "Roundhay", "Hyde Park", "Meanwood", "Kirkstall"],
                "Liverpool": ["City Centre", "Baltic Triangle", "Ropewalks", "Aigburth", "Toxteth", "Anfield", "Allerton"],
                "Newcastle": ["City Centre", "Jesmond", "Gosforth", "Byker", "Ouseburn", "Heaton"],
                "Sheffield": ["City Centre", "Kelham Island", "Ecclesall Road", "Sharrow", "Broomhill", "Crookes"],
                "Nottingham": ["City Centre", "Hockley", "Lace Market", "The Park", "Mapperley", "West Bridgford"],
                "Leicester": ["City Centre", "Clarendon Park", "Stoneygate", "Evington", "Braunstone"],
                "Coventry": ["City Centre", "Earlsdon", "Coundon", "Binley", "Canley"],
                "Southampton": ["City Centre", "Shirley", "Portswood", "Bitterne", "Hedge End"],
                "Portsmouth": ["Southsea", "Old Portsmouth", "Fratton", "Cosham"],
                "Brighton": ["The Lanes", "North Laine", "Hove", "Kemptown", "Fiveways"],
                "Oxford": ["City Centre", "Headington", "Cowley", "Summertown", "Jericho"],
                "Cambridge": ["City Centre", "Chesterton", "Newnham", "Romsey", "Arbury"],
                "York": ["City Centre", "Micklegate", "Gillygate", "Holgate", "Acomb"],
                "Plymouth": ["City Centre", "Mutley Plain", "Stonehouse", "Plymstock"],
                "Exeter": ["City Centre", "St Thomas", "Pennsylvania", "Heavitree"],
                "Derby": ["City Centre", "Spondon", "Allestree", "Littleover"],
                "Reading": ["City Centre", "Caversham", "Earley", "Whitley"],
                "Sunderland": ["City Centre", "Roker", "Millfield", "Houghton-le-Spring"],
                "Wolverhampton": ["City Centre", "Penn", "Tettenhall", "Finchfield"],
            },
            "Scotland": {
                "Glasgow": ["West End", "Merchant City", "Southside", "East End", "Finnieston", "Partick", "Shawlands", "Dennistoun"],
                "Edinburgh": ["Old Town", "New Town", "Leith", "Morningside", "Stockbridge", "Bruntsfield", "Newington", "Portobello"],
                "Aberdeen": ["City Centre", "West End", "Rosemount", "Old Aberdeen", "Torry", "Duthie Park"],
                "Dundee": ["City Centre", "Broughty Ferry", "West End", "Lochee", "Stobswell"],
                "Inverness": ["City Centre", "Crown", "Inshes", "Dalneigh"],
                "Stirling": ["City Centre", "Bridge of Allan", "Cambusbarron"],
            },
            "Wales": {
                "Cardiff": ["City Centre", "Pontcanna", "Roath", "Canton", "Bay", "Cathays", "Llandaff", "Splott"],
                "Swansea": ["City Centre", "Mumbles", "Uplands", "Marina", "Gorseinon"],
                "Newport": ["City Centre", "Maindee", "Rogerstone", "Caerleon"],
                "Wrexham": ["City Centre", "Rhosddu", "Erddig"],
            },
            "Northern Ireland": {
                "Belfast": ["City Centre", "Cathedral Quarter", "East Belfast", "South Belfast", "Titanic Quarter", "Queens Quarter", "Botanic"],
                "Derry": ["City Centre", "Waterside", "Cityside", "Foyleside", "Bogside"],
                "Lisburn": ["City Centre", "Sprucefield", "Hillsborough"],
                "Bangor": ["City Centre", "Groomsport", "Donaghadee"],
            },
        },
    },

    # ==================================================================
    # GERMANY  — all 16 federal states
    # ==================================================================
    "Germany": {
        "has_states": True,
        "states": {
            "Baden-Württemberg": {
                "Stuttgart": ["Mitte", "Stuttgarter West", "Bad Cannstatt", "Degerloch", "Vaihingen", "Feuerbach", "Zuffenhausen"],
                "Heidelberg": ["Old Town", "Neuenheim", "Handschuhsheim", "Kirchheim", "Rohrbach"],
                "Freiburg": ["Altstadt", "Stühlinger", "Wiehre", "Herdern", "Vauban", "Haslach"],
                "Mannheim": ["Innenstadt", "Jungbusch", "Schwetzingerstadt", "Neustadt", "Käfertal"],
                "Karlsruhe": ["Innenstadt", "Weststadt", "Südstadt", "Mühlburg", "Durlach"],
                "Ulm": ["Innenstadt", "Söflingen", "Wiblingen", "Gögglingen"],
            },
            "Bavaria": {
                "Munich": ["Maxvorstadt", "Schwabing", "Haidhausen", "Glockenbach", "Bogenhausen", "Neuhausen", "Schwabing-West", "Sendling", "Pasing"],
                "Nuremberg": ["Old Town", "Gostenhof", "Langwasser", "Südstadt", "St. Leonhard", "Gibitzenhof"],
                "Augsburg": ["City Centre", "Pfersee", "Hochzoll", "Innenstadt", "Oberhausen"],
                "Regensburg": ["Old Town", "Stadtamhof", "Kumpfmühl", "Westenviertel"],
                "Würzburg": ["Altstadt", "Zellerau", "Sanderau", "Frauenland"],
                "Ingolstadt": ["Innenstadt", "Südost", "Nordost", "Piusviertel"],
                "Erlangen": ["Altstadt", "Innenstadt", "Büchenbach", "Tennenlohe"],
            },
            "Berlin": {
                "Berlin": [
                    "Mitte", "Prenzlauer Berg", "Kreuzberg", "Friedrichshain",
                    "Charlottenburg", "Neukölln", "Pankow", "Lichtenberg",
                    "Tempelhof", "Schöneberg", "Spandau", "Reinickendorf",
                    "Wedding", "Moabit", "Steglitz", "Zehlendorf",
                    "Treptow", "Köpenick", "Hellersdorf", "Marzahn",
                ],
            },
            "Brandenburg": {
                "Potsdam": ["Innenstadt", "Babelsberg", "Sacrow", "Nauener Vorstadt", "Drewitz"],
                "Cottbus": ["Innenstadt", "Sandow", "Branitz", "Sachsendorf"],
                "Brandenburg an der Havel": ["Innenstadt", "Görden", "Plaue"],
            },
            "Bremen": {
                "Bremen": ["Innenstadt", "Neustadt", "Schwachhausen", "Findorff", "Walle", "Hemelingen"],
                "Bremerhaven": ["Geestemünde", "Lehe", "Mitte"],
            },
            "Hamburg": {
                "Hamburg": ["Altona", "Eimsbüttel", "HafenCity", "Blankenese", "Eppendorf", "Barmbek", "Wandsbek", "Harburg", "Bergedorf", "Wilhelmsburg"],
            },
            "Hesse": {
                "Frankfurt": ["Sachsenhausen", "Bornheim", "Westend", "Nordend", "Bockenheim", "Gallus", "Bahnhofsviertel"],
                "Wiesbaden": ["Innenstadt", "Südost", "Sonnenberg", "Biebrich"],
                "Kassel": ["Innenstadt", "Wesertor", "Nord-Holland", "Vorderer Westen"],
                "Darmstadt": ["Innenstadt", "Bessungen", "Eberstadt", "Arheilgen"],
                "Offenbach": ["Innenstadt", "Lauterborn", "Bieber", "Bürgel"],
            },
            "Lower Saxony": {
                "Hanover": ["Mitte", "Vahrenwald", "Linden", "List", "Misburg", "Ricklingen"],
                "Brunswick": ["Innenstadt", "Weststadt", "Östliches Ringgebiet", "Heidberg"],
                "Oldenburg": ["Innenstadt", "Kreyenbrück", "Nadorst", "Ohmstede"],
                "Osnabrück": ["Innenstadt", "Schinkel", "Wüste", "Atter"],
                "Wolfsburg": ["Innenstadt", "Fallersleben", "Detmerode", "Nordsteimke"],
            },
            "Mecklenburg-Vorpommern": {
                "Rostock": ["Innenstadt", "Kröpeliner-Tor-Vorstadt", "Dierkow", "Evershagen"],
                "Schwerin": ["Innenstadt", "Paulsstadt", "Weststadt", "Lankow"],
                "Greifswald": ["Innenstadt", "Schönwalde I", "Fettenvorstadt"],
            },
            "North Rhine-Westphalia": {
                "Cologne": ["Ehrenfeld", "Nippes", "Mülheim", "Deutz", "Sülz", "Innenstadt", "Lindenthal", "Kalk", "Porz", "Rodenkirchen"],
                "Düsseldorf": ["Altstadt", "Oberkassel", "Friedrichstadt", "Derendorf", "Pempelfort", "Bilk", "Flingern"],
                "Dortmund": ["City Centre", "Hörde", "Aplerbeck", "Mengede", "Huckarde", "Innenstadt-West"],
                "Essen": ["City Centre", "Rüttenscheid", "Kettwig", "Werden", "Stadtwald", "Steele"],
                "Duisburg": ["Innenstadt", "Duissern", "Rumeln", "Homberg"],
                "Bochum": ["Innenstadt", "Wattenscheid", "Langendreer", "Riemke"],
                "Wuppertal": ["Elberfeld", "Barmen", "Cronenberg", "Vohwinkel"],
                "Bonn": ["Bad Godesberg", "Beuel", "Godesberg", "Innenstadt", "Kessenich", "Poppelsdorf"],
                "Münster": ["Innenstadt", "Gievenbeck", "Mauritz", "Handorf"],
                "Aachen": ["Innenstadt", "Burtscheid", "Haaren", "Laurensberg"],
            },
            "Rhineland-Palatinate": {
                "Mainz": ["Altstadt", "Neustadt", "Lerchenberg", "Bretzenheim"],
                "Ludwigshafen": ["Innenstadt", "Süd", "West", "Oggersheim"],
                "Koblenz": ["Innenstadt", "Lützel", "Güls", "Metternich"],
                "Trier": ["Innenstadt", "Petrisberg", "Pallien", "Feyen"],
            },
            "Saarland": {
                "Saarbrücken": ["Innenstadt", "St. Johann", "Malstatt", "Dudweiler"],
                "Neunkirchen": ["Innenstadt", "Wiebelskirchen", "Kohlhof"],
            },
            "Saxony": {
                "Dresden": ["Altstadt", "Neustadt", "Loschwitz", "Prohlis", "Plauen", "Striesen"],
                "Leipzig": ["City Centre", "Connewitz", "Lindenau", "Gohlis", "Schleußig", "Plagwitz", "Grunau"],
                "Chemnitz": ["Innenstadt", "Kaßberg", "Schlosschemnitz", "Hilbersdorf"],
                "Zwickau": ["Innenstadt", "Eckersbach", "Marienthal"],
            },
            "Saxony-Anhalt": {
                "Magdeburg": ["Innenstadt", "Neue Neustadt", "Stadtfeld", "Sudenburg"],
                "Halle": ["Innenstadt", "Neustadt", "Kröllwitz", "Giebichenstein"],
                "Dessau": ["Innenstadt", "Mitte", "Törten", "Ziebigk"],
            },
            "Schleswig-Holstein": {
                "Kiel": ["Innenstadt", "Gaarden", "Hassee", "Ellerbek"],
                "Lübeck": ["Innenstadt", "St. Lorenz", "Buntekuh", "Marli"],
                "Flensburg": ["Innenstadt", "Jürgensby", "Mürwik", "Friesischer Berg"],
            },
            "Thuringia": {
                "Erfurt": ["Altstadt", "Löbervorstadt", "Andreasvorstadt", "Daberstedt"],
                "Jena": ["Zentrum", "Lobeda", "Winzerla", "Wenigenjena"],
                "Gera": ["Innenstadt", "Bieblach", "Debschwitz", "Zwötzen"],
            },
        },
    },

    # ==================================================================
    # FRANCE  — major regions
    # ==================================================================
    "France": {
        "has_states": True,
        "states": {
            "Île-de-France": {
                "Paris": [
                    "Le Marais", "Montmartre", "Saint-Germain-des-Prés", "Bastille",
                    "Opéra", "Châtelet", "République", "Belleville",
                    "Pigalle", "Oberkampf", "Nation", "Père Lachaise",
                    "Montparnasse", "Latin Quarter", "Champs-Élysées",
                ],
                "Versailles": ["Old Town", "Saint-Louis Quarter", "Porchefontaine"],
                "Boulogne-Billancourt": ["City Centre", "Parc de Saint-Cloud", "Billancourt"],
                "Saint-Denis": ["Centre-ville", "Franc-Moisin", "La Plaine"],
            },
            "Auvergne-Rhône-Alpes": {
                "Lyon": ["Presqu'île", "Croix-Rousse", "Confluence", "Villeurbanne", "Vieux-Lyon", "Part-Dieu", "Monplaisir"],
                "Grenoble": ["City Centre", "Championnet", "Teisseire", "Berriat", "Europole"],
                "Annecy": ["City Centre", "Old Town", "Cran-Gevrier", "Seynod"],
                "Clermont-Ferrand": ["City Centre", "Montferrand", "Les Vergnes", "Jaude"],
                "Saint-Étienne": ["City Centre", "Crêt de Roc", "Montplaisir"],
                "Chambéry": ["City Centre", "Biollay", "Les Hauts de Chambéry"],
            },
            "Bourgogne-Franche-Comté": {
                "Dijon": ["City Centre", "Clemenceau", "Montchapet", "Les Grésilles"],
                "Besançon": ["City Centre", "Battant", "Planoise", "Châteaufarine"],
            },
            "Bretagne": {
                "Rennes": ["City Centre", "Thabor", "Villejean", "Beaulieu"],
                "Brest": ["City Centre", "Recouvrance", "Saint-Marc", "Kerinou"],
                "Quimper": ["City Centre", "Ergué-Gabéric", "Kerfeunteun"],
            },
            "Centre-Val de Loire": {
                "Tours": ["City Centre", "Prébendes", "Les Halles", "Saint-Symphorien"],
                "Orléans": ["City Centre", "Argonne", "La Source", "Chécy"],
            },
            "Grand Est": {
                "Strasbourg": ["Petite France", "Krutenau", "Neustadt", "Robertsau", "Cronenbourg"],
                "Reims": ["City Centre", "Clairmarais", "Courlancy", "Murigny"],
                "Metz": ["City Centre", "Sablon", "Queuleu", "Borny"],
                "Mulhouse": ["City Centre", "Rebberg", "Dornach", "Daguerre"],
                "Nancy": ["City Centre", "Haussonville", "Boudonville", "Rives de Meurthe"],
            },
            "Hauts-de-France": {
                "Lille": ["City Centre", "Vieux-Lille", "Wazemmes", "Euralille", "Moulins"],
                "Amiens": ["City Centre", "Saint-Leu", "Saint-Germain", "Henriville"],
                "Roubaix": ["City Centre", "Union", "Beaulieu"],
                "Valenciennes": ["City Centre", "Mont-Houy", "Anzin"],
            },
            "Normandie": {
                "Rouen": ["City Centre", "Saint-Sever", "Rive Droite", "Maromme"],
                "Le Havre": ["City Centre", "Sanvic", "Caucriauville"],
                "Caen": ["City Centre", "Venoix", "La Folie"],
            },
            "Nouvelle-Aquitaine": {
                "Bordeaux": ["Saint-Pierre", "Chartrons", "Caudéran", "Bacalan", "Capucins", "Saint-Michel", "Nansouty"],
                "Biarritz": ["City Centre", "La Négresse", "Mouriscot"],
                "La Rochelle": ["Vieux-Port", "Centre-ville", "Minimes"],
                "Pau": ["City Centre", "Hédas", "Berlioz"],
                "Limoges": ["Centre-ville", "Carnot", "Val de l'Aurence"],
            },
            "Occitanie": {
                "Toulouse": ["Capitole", "Saint-Étienne", "Côte Pavée", "Saint-Sernin", "Wilson", "Compans-Cafarelli"],
                "Montpellier": ["Comédie", "Antigone", "Port Marianne", "Écusson", "Près d'Arènes"],
                "Nîmes": ["City Centre", "Pissevin", "Valdegour"],
                "Perpignan": ["City Centre", "Saint-Martin", "Moyen Vernet"],
            },
            "Pays de la Loire": {
                "Nantes": ["City Centre", "Île de Nantes", "Erdre", "Doulon", "Chantenay"],
                "Le Mans": ["City Centre", "Cité Plantagenêt", "Bollée"],
                "Angers": ["City Centre", "Belle-Beille", "Monplaisir"],
            },
            "Provence-Alpes-Côte d'Azur": {
                "Marseille": ["Old Port", "Cours Julien", "La Plaine", "Castellane", "Endoume", "Joliette", "Panier"],
                "Nice": ["Old Town", "Carré d'Or", "Libération", "Cimiez", "Riquier", "Promenade des Anglais"],
                "Aix-en-Provence": ["Old Town", "Mazarin Quarter", "Jas de Bouffan", "Pays d'Aix"],
                "Toulon": ["City Centre", "Le Mourillon", "Haute Ville", "Claret"],
                "Cannes": ["La Croisette", "Le Suquet", "Mougins", "Ranguin"],
                "Antibes": ["Old Town", "Juan-les-Pins", "Sophia Antipolis"],
            },
        },
    },

    # ==================================================================
    # AUSTRALIA  — all states and territories
    # ==================================================================
    "Australia": {
        "has_states": True,
        "states": {
            "Australian Capital Territory": {
                "Canberra": ["City", "Braddon", "Kingston", "Dickson", "Belconnen", "Woden", "Tuggeranong"],
            },
            "New South Wales": {
                "Sydney": ["CBD", "Surry Hills", "Newtown", "Bondi", "Glebe", "Manly", "Parramatta", "Ultimo", "Chippendale", "Pyrmont", "Darlinghurst", "Paddington", "Leichhardt", "Balmain"],
                "Newcastle": ["City Centre", "Cooks Hill", "Hamilton", "Bar Beach", "Islington", "Adamstown"],
                "Wollongong": ["City Centre", "Fairy Meadow", "Figtree", "Thirroul", "Corrimal"],
                "Albury": ["City Centre", "East Albury", "Table Top"],
                "Lismore": ["City Centre", "Goonellabah", "East Lismore"],
                "Coffs Harbour": ["City Centre", "Sawtell", "Toormina"],
            },
            "Northern Territory": {
                "Darwin": ["City Centre", "Fannie Bay", "Parap", "Nightcliff", "Coconut Grove"],
                "Alice Springs": ["City Centre", "The Gap", "Eastside"],
            },
            "Queensland": {
                "Brisbane": ["CBD", "Fortitude Valley", "West End", "Paddington", "South Brisbane", "New Farm", "Teneriffe", "Spring Hill", "Woolloongabba"],
                "Gold Coast": ["Surfers Paradise", "Broadbeach", "Burleigh Heads", "Robina", "Coolangatta", "Currumbin"],
                "Cairns": ["City Centre", "Cairns North", "Earlville", "Whitfield", "Mooroobool"],
                "Townsville": ["City Centre", "North Ward", "Kirwan", "Aitkenvale", "Hyde Park"],
                "Sunshine Coast": ["Maroochydore", "Noosa Heads", "Caloundra", "Buderim"],
                "Ipswich": ["City Centre", "Springfield", "Redbank Plains"],
                "Toowoomba": ["City Centre", "Rangeville", "East Toowoomba"],
            },
            "South Australia": {
                "Adelaide": ["CBD", "North Adelaide", "Norwood", "Unley", "Glenelg", "Burnside", "Prospect", "Hindmarsh", "Kensington"],
                "Mount Gambier": ["City Centre", "Moorak", "Suttontown"],
                "Whyalla": ["City Centre", "Hincks Ave", "Norrie Avenue"],
                "Port Augusta": ["City Centre", "Stirling North", "Commissariat Point"],
            },
            "Tasmania": {
                "Hobart": ["City Centre", "Sandy Bay", "Battery Point", "North Hobart", "West Hobart", "South Hobart"],
                "Launceston": ["City Centre", "Trevallyn", "Mowbray", "Invermay", "Newstead"],
                "Devonport": ["City Centre", "Latrobe", "East Devonport"],
                "Burnie": ["City Centre", "Shorewell Park", "Upper Burnie"],
            },
            "Victoria": {
                "Melbourne": ["CBD", "Fitzroy", "Collingwood", "South Yarra", "St Kilda", "Richmond", "Carlton", "Prahran", "Brunswick", "Northcote", "Hawthorn", "Footscray", "Williamstown", "Docklands"],
                "Geelong": ["City Centre", "Belmont", "Newtown", "Corio", "Geelong West", "Highton"],
                "Ballarat": ["City Centre", "Sebastopol", "Wendouree", "Alfredton", "Lake Gardens"],
                "Bendigo": ["City Centre", "Golden Square", "Strathdale", "Eaglehawk"],
                "Shepparton": ["City Centre", "Mooroopna", "Kialla"],
            },
            "Western Australia": {
                "Perth": ["CBD", "Fremantle", "Subiaco", "Mount Lawley", "Leederville", "Northbridge", "Claremont", "Cottesloe", "Scarborough"],
                "Bunbury": ["City Centre", "South Bunbury", "East Bunbury", "College Grove"],
                "Geraldton": ["City Centre", "Rangeway", "Utakarra"],
                "Kalgoorlie": ["City Centre", "Hannans", "Broad Arrow"],
            },
        },
    },

    # ==================================================================
    # CANADA  — all provinces and territories
    # ==================================================================
    "Canada": {
        "has_states": True,
        "states": {
            "Alberta": {
                "Calgary": ["Inglewood", "Kensington", "Beltline", "Mission", "East Village", "Marda Loop", "Bridgeland", "Hillhurst", "Sunridge", "Saddleridge"],
                "Edmonton": ["Downtown", "Whyte Avenue", "Glenora", "Oliver", "Mill Woods", "Strathcona", "Windermere", "St. Albert"],
                "Red Deer": ["City Centre", "Gaetz Avenue", "Anders", "Clearview Ridge"],
                "Lethbridge": ["Downtown", "North Lethbridge", "West Lethbridge", "Henderson"],
                "Medicine Hat": ["Downtown", "Crescent Heights", "Southlands"],
            },
            "British Columbia": {
                "Vancouver": ["Downtown", "Gastown", "Kitsilano", "Commercial Drive", "Yaletown", "Mount Pleasant", "Fairview", "East Van", "Granville Island", "West End", "Chinatown"],
                "Victoria": ["Downtown", "Fernwood", "James Bay", "Oak Bay", "Saanich", "Fairfield", "Esquimalt"],
                "Kelowna": ["Downtown", "Pandosy", "North Glenmore", "Rutland", "Lake Country"],
                "Surrey": ["City Centre", "Newton", "Guildford", "Cloverdale", "Fleetwood"],
                "Burnaby": ["Metrotown", "Brentwood", "Lougheed", "Edmonds"],
                "Abbotsford": ["Downtown", "West Abbotsford", "East Abbotsford"],
                "Nanaimo": ["Downtown", "South Nanaimo", "Brechin Hill"],
                "Kamloops": ["Downtown", "North Shore", "Sahali", "Westsyde"],
                "Prince George": ["Downtown", "Millar Addition", "Spruceland"],
            },
            "Manitoba": {
                "Winnipeg": ["Exchange District", "Osborne Village", "River Heights", "Downtown", "St. Boniface", "Wolseley", "West Broadway", "North End"],
                "Brandon": ["Downtown", "East End", "University Area"],
                "Steinbach": ["City Centre", "North End"],
            },
            "New Brunswick": {
                "Moncton": ["Downtown", "Dieppe", "Riverview", "Highfield"],
                "Fredericton": ["Downtown", "North Side", "Silverwood", "Barker's Point"],
                "Saint John": ["Uptown", "South End", "North End", "Millidgeville"],
            },
            "Newfoundland and Labrador": {
                "St. John's": ["Downtown", "Duckworth Street", "Quidi Vidi", "Mount Pearl"],
                "Corner Brook": ["City Centre", "Humber Village", "Massey Drive"],
            },
            "Northwest Territories": {
                "Yellowknife": ["Downtown", "Old Town", "Frame Lake"],
            },
            "Nova Scotia": {
                "Halifax": ["Downtown", "South End", "North End", "Dartmouth", "Bedford", "Spring Garden", "West End"],
                "Truro": ["City Centre", "Willow Street", "Prince Street"],
                "Sydney": ["Downtown", "Whitney Pier", "New Waterford"],
            },
            "Nunavut": {
                "Iqaluit": ["Downtown", "Apex", "Tundra"],
            },
            "Ontario": {
                "Toronto": ["Downtown", "Kensington Market", "Annex", "Leslieville", "Distillery District", "North York", "Scarborough", "Etobicoke", "Little Italy", "Roncesvalles", "Davisville", "Bloor West Village"],
                "Ottawa": ["ByWard Market", "Glebe", "Westboro", "Centretown", "Kanata", "Barrhaven", "Orleans"],
                "Mississauga": ["Port Credit", "City Centre", "Streetsville", "Cooksville", "Erin Mills", "Square One"],
                "Hamilton": ["Downtown", "Westdale", "Locke Street", "Dundas", "Ancaster"],
                "Brampton": ["Downtown", "Bramalea", "Heart Lake", "Castlemore", "Springdale"],
                "London": ["Downtown", "Old North", "Old South", "Byron", "Wortley Village"],
                "Kitchener": ["Downtown", "Victoria Hills", "Cherry Park"],
                "Windsor": ["Downtown", "Walkerville", "South Windsor", "East Windsor"],
                "Sudbury": ["Downtown", "New Sudbury", "Minnow Lake"],
                "Kingston": ["Downtown", "Princess Street", "Sydenham Ward"],
                "Guelph": ["Downtown", "Kortright Hills", "Clairfields"],
                "Thunder Bay": ["Downtown", "Current River", "Lakehead"],
                "Markham": ["Unionville", "Markham Village", "Milliken Mills"],
                "Vaughan": ["Maple", "Woodbridge", "Thornhill", "Concord"],
                "Barrie": ["Downtown", "South Barrie", "Allandale"],
            },
            "Prince Edward Island": {
                "Charlottetown": ["Downtown", "Parkdale", "Sherwood"],
                "Summerside": ["Downtown", "Slemon Park"],
            },
            "Quebec": {
                "Montreal": ["Plateau-Mont-Royal", "Old Montreal", "Mile End", "Rosemont", "Westmount", "Mile Ex", "NDG", "Verdun", "Outremont", "Little Italy", "Griffintown", "Hochelaga"],
                "Quebec City": ["Old Quebec", "Montcalm", "Limoilou", "Sainte-Foy", "Charlesbourg"],
                "Laval": ["Chomedey", "Sainte-Rose", "Vimont", "Duvernay"],
                "Sherbrooke": ["Downtown", "Fleurimont", "Rock Forest", "Brompton"],
                "Saguenay": ["Chicoutimi", "Jonquière", "La Baie"],
                "Trois-Rivières": ["Downtown", "Cap-de-la-Madeleine", "Pointe-du-Lac"],
            },
            "Saskatchewan": {
                "Regina": ["Downtown", "Cathedral", "Lakeview", "University Park", "Wascana"],
                "Saskatoon": ["Downtown", "Broadway", "Riversdale", "City Park", "Nutana"],
                "Prince Albert": ["Downtown", "East Flat", "West Hill"],
            },
            "Yukon": {
                "Whitehorse": ["Downtown", "Riverdale", "Porter Creek"],
            },
        },
    },

    # ==================================================================
    # NETHERLANDS  — flat (no states)
    # ==================================================================
    "Netherlands": {
        "has_states": False,
        "cities": {
            "Amsterdam": ["Centrum", "Jordaan", "De Pijp", "Oud-West", "Noord", "Oost", "Buitenveldert", "Westerpark", "De Baarsjes", "Watergraafsmeer", "Zuideramstel", "IJburg", "Zeeburg"],
            "Rotterdam": ["City Centre", "Delfshaven", "Kralingen", "Hillegersberg", "Katendrecht", "Feijenoord", "Charlois", "Overschie", "Capelle aan den IJssel"],
            "The Hague": ["City Centre", "Scheveningen", "Voorburg", "Rijswijk", "Ypenburg", "Bezuidenhout", "Laak", "Escamp"],
            "Utrecht": ["City Centre", "Lombok", "Transwijk", "Leidsche Rijn", "Overvecht", "Zuilen", "Lunetten", "Oog in Al", "Hoograven"],
            "Eindhoven": ["City Centre", "Woensel", "Stratum", "Gestel", "Strijp-S", "Tongelre", "Woensel-Noord"],
            "Groningen": ["City Centre", "Schilderswijk", "Oosterpoort", "Paddepoel", "Ulgersmaborg", "Corpus den Hoorn"],
            "Tilburg": ["City Centre", "Tilburg Noord", "Udenhout", "Wandelbos", "Reeshof", "Oud-Noord"],
            "Breda": ["City Centre", "Bavel", "Ulvenhout", "Westerpark", "Haagse Beemden", "Prinsenbeek"],
            "Nijmegen": ["City Centre", "Bottendaal", "Hunnerpark", "Nijmegen Oost", "Neerbosch", "Dukenburg"],
            "Leiden": ["City Centre", "Leiden Noord", "Mors", "Stevenshof", "Merenwijk", "Bockhorst"],
            "Delft": ["City Centre", "Delft Noord", "TU Delft Campus", "Tanthof"],
            "Haarlem": ["City Centre", "Schalkwijk", "Heemstede", "Kleverpark"],
            "Maastricht": ["City Centre", "Wyck", "Céramique", "Caberg"],
            "Enschede": ["City Centre", "Roombeek", "Pathmos", "Glanerbrug"],
            "Apeldoorn": ["City Centre", "Zevenhuizen", "Ugchelen"],
            "Arnhem": ["City Centre", "Presikhaaf", "Malburgen", "Kronenburg"],
            "Amersfoort": ["City Centre", "Kattenbroek", "Vathorst", "Schothorst"],
            "Dordrecht": ["City Centre", "Wielwijk", "Dubbeldam"],
            "Zwolle": ["City Centre", "Holtenbroek", "Berkum"],
            "Venlo": ["City Centre", "Belfeld", "Tegelen"],
        },
    },

    # ==================================================================
    # IRELAND  — flat (no states)
    # ==================================================================
    "Ireland": {
        "has_states": False,
        "cities": {
            "Dublin": ["City Centre", "Southside", "Northside", "Docklands", "Ranelagh", "Rathmines", "Ballsbridge", "Clontarf", "Sandyford", "Dundrum", "Blackrock", "Glasnevin", "Finglas", "Tallaght", "Lucan"],
            "Cork": ["City Centre", "Douglas", "Blackrock", "Sunday's Well", "Ballincollig", "Bishopstown", "Mahon", "Togher"],
            "Galway": ["City Centre", "Salthill", "Knocknacarra", "Westside", "Renmore", "Doughiska", "Oranmore"],
            "Limerick": ["City Centre", "Castletroy", "Dooradoyle", "Raheen", "Ballinacurra", "Annacotty", "Mungret"],
            "Waterford": ["City Centre", "Ferrybank", "Gracedieu", "Tramore Road", "Ballybeg", "Kilbarry"],
            "Kilkenny": ["City Centre", "Freshford Road", "Callan Road", "Loughboy", "Hebron Road"],
            "Drogheda": ["City Centre", "Moneymore", "Donore Road", "Rathmullan Road", "Ballsgrove"],
            "Athlone": ["City Centre", "Westside", "Clonbrusk", "Monksland", "Coosan"],
            "Sligo": ["City Centre", "Strandhill", "Calry", "Carrowroe"],
            "Dundalk": ["City Centre", "Muirhevnamore", "Dowdallshill", "Cox's Demesne"],
            "Bray": ["City Centre", "Vevay Road", "Killruddery", "Ravenswell"],
            "Navan": ["City Centre", "Johnstown", "Clonmagadden"],
            "Ennis": ["City Centre", "Clarecastle", "Lifford"],
            "Tralee": ["City Centre", "Manor", "Monavalley"],
            "Naas": ["City Centre", "Monread", "Oldtown"],
        },
    },

    # ==================================================================
    # UAE  — Emirates act as states
    # ==================================================================
    "UAE": {
        "has_states": True,
        "states": {
            "Dubai": {
                "Dubai": [
                    "Downtown Dubai", "Dubai Marina", "Jumeirah", "Business Bay",
                    "DIFC", "Deira", "Bur Dubai", "JLT", "Palm Jumeirah",
                    "JBR", "Motor City", "Sports City", "Dubai Hills",
                    "Al Quoz", "Mirdif", "Jumeirah Village Circle",
                    "Al Barsha", "International City", "Silicon Oasis",
                    "The Springs", "The Lakes", "Meadows", "Arabian Ranches",
                    "Dubai Land", "Al Nahda", "Hor Al Anz",
                ],
            },
            "Abu Dhabi": {
                "Abu Dhabi": [
                    "Downtown", "Khalidiyah", "Al Reem Island", "Yas Island",
                    "Saadiyat Island", "Corniche", "Al Zahiyah", "Khalifa City",
                    "Mohammed Bin Zayed City", "Al Mushrif", "Al Reef",
                    "Masdar City", "Al Ain Road",
                ],
                "Al Ain": ["Al Jimi", "Al Muwaiji", "Al Ain Centre", "Al Murabba"],
            },
            "Sharjah": {
                "Sharjah": ["Al Majaz", "Al Khan", "Al Qasimia", "Industrial Area", "Muwailih", "Al Nahda", "Halwan", "Abu Shagara"],
            },
            "Ras Al Khaimah": {
                "Ras Al Khaimah": ["Al Nakheel", "Khuzam", "Al Dhait", "Al Hamra", "Mina Al Arab", "Al Azra"],
            },
            "Ajman": {
                "Ajman": ["Ajman City Centre", "Al Rashidiya", "Al Nuaimia", "Al Jurf", "Corniche", "Al Jerf"],
            },
            "Fujairah": {
                "Fujairah": ["City Centre", "Dibba", "Khor Fakkan", "Fujairah Free Zone", "Al Faseel"],
            },
            "Umm Al Quwain": {
                "Umm Al Quwain": ["City Centre", "New UAQ", "Al Raqaib"],
            },
        },
    },
}
