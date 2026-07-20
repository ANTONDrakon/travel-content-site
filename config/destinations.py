"""
TravelHub Destinations — Information Architecture v2.0

Hierarchy: Country → Region → City → Article

Each country contains regions, each region contains cities.
Main page shows only countries. Country page shows regions.
Region page shows cities. City page shows articles.
"""

DESTINATIONS = {
    # ═══════════════════════════════════════════════════════════════
    # RUSSIA
    # ═══════════════════════════════════════════════════════════════
    "russia": {
        "name_ru": "Россия",
        "name_ru_prepositional": "России",
        "name_en": "Russia",
        "slug": "russia",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "SVO",
        "regions": {
            "moscow-region": {
                "name_ru": "Москва и Московская область",
                "name_en": "Moscow & Moscow Region",
                "slug": "moscow-region",
                "cities": {
                    "moscow": {
                        "name_ru": "Москва",
                        "name_en": "Moscow",
                        "slug": "moscow",
                        "airport_codes": ["SVO", "DME", "VKO"],
                        "lat": 55.7558, "lon": 37.6173,
                    },
                },
            },
            "leningrad-region": {
                "name_ru": "Ленинградская область",
                "name_en": "Leningrad Oblast",
                "slug": "leningrad-region",
                "cities": {
                    "saint-petersburg": {
                        "name_ru": "Санкт-Петербург",
                        "name_en": "Saint Petersburg",
                        "slug": "saint-petersburg",
                        "airport_codes": ["LED"],
                        "lat": 59.9343, "lon": 30.3351,
                    },
                },
            },
            "krasnodar-krai": {
                "name_ru": "Краснодарский край",
                "name_en": "Krasnodar Krai",
                "slug": "krasnodar-krai",
                "cities": {
                    "sochi": {
                        "name_ru": "Сочи",
                        "name_en": "Sochi",
                        "slug": "sochi",
                        "airport_codes": ["AER"],
                        "lat": 43.6028, "lon": 39.7342,
                    },
                },
            },
            "republic-of-tatarstan": {
                "name_ru": "Республика Татарстан",
                "name_en": "Republic of Tatarstan",
                "slug": "republic-of-tatarstan",
                "cities": {
                    "kazan": {
                        "name_ru": "Казань",
                        "name_en": "Kazan",
                        "slug": "kazan",
                        "airport_codes": ["KZN"],
                        "lat": 55.7887, "lon": 49.1221,
                    },
                },
            },
            "kaliningrad-region": {
                "name_ru": "Калининградская область",
                "name_en": "Kaliningrad Oblast",
                "slug": "kaliningrad-region",
                "cities": {
                    "kaliningrad": {
                        "name_ru": "Калининград",
                        "name_en": "Kaliningrad",
                        "slug": "kaliningrad",
                        "airport_codes": ["KGD"],
                        "lat": 54.7104, "lon": 20.4522,
                    },
                },
            },
            "republic-of-karelia": {
                "name_ru": "Республика Карелия",
                "name_en": "Republic of Karelia",
                "slug": "republic-of-karelia",
                "cities": {
                    "petrozavodsk": {
                        "name_ru": "Петрозаводск",
                        "name_en": "Petrozavodsk",
                        "slug": "petrozavodsk",
                        "airport_codes": ["PES"],
                        "lat": 61.7850, "lon": 34.3469,
                    },
                    "sortavala": {
                        "name_ru": "Сортавала",
                        "name_en": "Sortavala",
                        "slug": "sortavala",
                        "airport_codes": ["PES"],
                        "lat": 61.7000, "lon": 30.6833,
                    },
                },
            },
            "irkutsk-region": {
                "name_ru": "Иркутская область",
                "name_en": "Irkutsk Oblast",
                "slug": "irkutsk-region",
                "cities": {
                    "irkutsk": {
                        "name_ru": "Иркутск",
                        "name_en": "Irkutsk",
                        "slug": "irkutsk",
                        "airport_codes": ["IKT"],
                        "lat": 52.2855, "lon": 104.2890,
                    },
                    "listvyanka": {
                        "name_ru": "Листвянка",
                        "name_en": "Listvyanka",
                        "slug": "listvyanka",
                        "airport_codes": ["IKT"],
                        "lat": 51.8592, "lon": 104.8545,
                    },
                },
            },
            "republic-of-altai": {
                "name_ru": "Республика Алтай",
                "name_en": "Republic of Altai",
                "slug": "republic-of-altai",
                "cities": {
                    "gorno-altaysk": {
                        "name_ru": "Горно-Алтайск",
                        "name_en": "Gorno-Altaysk",
                        "slug": "gorno-altaysk",
                        "airport_codes": ["BAX"],
                        "lat": 51.9586, "lon": 85.9364,
                    },
                },
            },
            "republic-of-dagestan": {
                "name_ru": "Республика Дагестан",
                "name_en": "Republic of Dagestan",
                "slug": "republic-of-dagestan",
                "cities": {
                    "makhachkala": {
                        "name_ru": "Махачкала",
                        "name_en": "Makhachkala",
                        "slug": "makhachkala",
                        "airport_codes": ["MCX"],
                        "lat": 42.9849, "lon": 47.5047,
                    },
                    "derbent": {
                        "name_ru": "Дербент",
                        "name_en": "Derbent",
                        "slug": "derbent",
                        "airport_codes": ["MCX"],
                        "lat": 42.0578, "lon": 48.2964,
                    },
                },
            },
            "kamchatka-krai": {
                "name_ru": "Камчатский край",
                "name_en": "Kamchatka Krai",
                "slug": "kamchatka-krai",
                "cities": {
                    "petropavlovsk-kamchatsky": {
                        "name_ru": "Петропавловск-Камчатский",
                        "name_en": "Petropavlovsk-Kamchatsky",
                        "slug": "petropavlovsk-kamchatsky",
                        "airport_codes": ["PKC"],
                        "lat": 53.0133, "lon": 158.6539,
                    },
                },
            },
            "stavropol-krai": {
                "name_ru": "Ставропольский край",
                "name_en": "Stavropol Krai",
                "slug": "stavropol-krai",
                "cities": {
                    "pyatigorsk": {
                        "name_ru": "Пятигорск",
                        "name_en": "Pyatigorsk",
                        "slug": "pyatigorsk",
                        "airport_codes": ["MRV"],
                        "lat": 44.0414, "lon": 43.0606,
                    },
                    "kislovodsk": {
                        "name_ru": "Кисловодск",
                        "name_en": "Kislovodsk",
                        "slug": "kislovodsk",
                        "airport_codes": ["MRV"],
                        "lat": 43.9053, "lon": 42.7206,
                    },
                },
            },
            "primorsky-krai": {
                "name_ru": "Приморский край",
                "name_en": "Primorsky Krai",
                "slug": "primorsky-krai",
                "cities": {
                    "vladivostok": {
                        "name_ru": "Владивосток",
                        "name_en": "Vladivostok",
                        "slug": "vladivostok",
                        "airport_codes": ["VVO"],
                        "lat": 43.1332, "lon": 131.9113,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # TURKEY
    # ═══════════════════════════════════════════════════════════════
    "turkey": {
        "name_ru": "Турция",
        "name_ru_prepositional": "Турции",
        "name_en": "Turkey",
        "name_es": "Turquía",
        "slug": "turkey",
        "currency": "TRY",
        "visa_ru": "безвизовый въезд до 90 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 90 days",
        "visa_es": "sin visa para ciudadanos rusos hasta 90 días",
        "airport_code": "IST",
        "regions": {
            "marmara-region": {
                "name_ru": "Мраморноморский регион",
                "name_en": "Marmara Region",
                "slug": "marmara-region",
                "cities": {
                    "istanbul": {
                        "name_ru": "Стамбул",
                        "name_en": "Istanbul",
                        "slug": "istanbul",
                        "airport_codes": ["IST", "SAW"],
                        "lat": 41.0082, "lon": 28.9784,
                    },
                },
            },
            "mediterranean-coast": {
                "name_ru": "Средиземноморское побережье",
                "name_en": "Mediterranean Coast",
                "slug": "mediterranean-coast",
                "cities": {
                    "antalya": {
                        "name_ru": "Анталья",
                        "name_en": "Antalya",
                        "slug": "antalya",
                        "airport_codes": ["AYT"],
                        "lat": 36.8969, "lon": 30.7133,
                    },
                    "alanya": {
                        "name_ru": "Аланья",
                        "name_en": "Alanya",
                        "slug": "alanya",
                        "airport_codes": ["AYT"],
                        "lat": 36.2975, "lon": 32.2981,
                    },
                },
            },
            "aegean-coast": {
                "name_ru": "Эгейское побережье",
                "name_en": "Aegean Coast",
                "slug": "aegean-coast",
                "cities": {
                    "bodrum": {
                        "name_ru": "Бодрум",
                        "name_en": "Bodrum",
                        "slug": "bodrum",
                        "airport_codes": ["BJV"],
                        "lat": 37.0344, "lon": 27.4305,
                    },
                    "kusadasi": {
                        "name_ru": "Кушадасы",
                        "name_en": "Kusadasi",
                        "slug": "kusadasi",
                        "airport_codes": ["ADB"],
                        "lat": 37.8586, "lon": 27.3416,
                    },
                },
            },
            "cappadocia": {
                "name_ru": "Каппадокия",
                "name_en": "Cappadocia",
                "slug": "cappadocia",
                "cities": {
                    "goreme": {
                        "name_ru": "Гёреме",
                        "name_en": "Goreme",
                        "slug": "goreme",
                        "airport_codes": ["ASR", "NAV"],
                        "lat": 38.6431, "lon": 34.8306,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # THAILAND
    # ═══════════════════════════════════════════════════════════════
    "thailand": {
        "name_ru": "Таиланд",
        "name_ru_prepositional": "Таиланде",
        "name_en": "Thailand",
        "name_es": "Tailandia",
        "slug": "thailand",
        "currency": "THB",
        "visa_ru": "безвизовый въезд до 60 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 60 days",
        "visa_es": "sin visa para ciudadanos rusos hasta 60 días",
        "airport_code": "BKK",
        "regions": {
            "bangkok-region": {
                "name_ru": "Бангкок и окрестности",
                "name_en": "Bangkok & Surroundings",
                "slug": "bangkok-region",
                "cities": {
                    "bangkok": {
                        "name_ru": "Бангкок",
                        "name_en": "Bangkok",
                        "slug": "bangkok",
                        "airport_codes": ["BKK", "DMK"],
                        "lat": 13.7563, "lon": 100.5018,
                    },
                },
            },
            "phuket-province": {
                "name_ru": "Провинция Пхукет",
                "name_en": "Phuket Province",
                "slug": "phuket-province",
                "cities": {
                    "phuket": {
                        "name_ru": "Пхукет",
                        "name_en": "Phuket",
                        "slug": "phuket",
                        "airport_codes": ["HKT"],
                        "lat": 7.8804, "lon": 98.3923,
                    },
                },
            },
            "chonburi-province": {
                "name_ru": "Провинция Чонбури",
                "name_en": "Chonburi Province",
                "slug": "chonburi-province",
                "cities": {
                    "pattaya": {
                        "name_ru": "Паттайя",
                        "name_en": "Pattaya",
                        "slug": "pattaya",
                        "airport_codes": ["UTP"],
                        "lat": 12.9333, "lon": 100.8833,
                    },
                },
            },
            "surat-thani-province": {
                "name_ru": "Провинция Сураттхани",
                "name_en": "Surat Thani Province",
                "slug": "surat-thani-province",
                "cities": {
                    "koh-samui": {
                        "name_ru": "Ко Самуи",
                        "name_en": "Koh Samui",
                        "slug": "koh-samui",
                        "airport_codes": ["USM"],
                        "lat": 9.5120, "lon": 100.0136,
                    },
                },
            },
            "krabi-province": {
                "name_ru": "Провинция Краби",
                "name_en": "Krabi Province",
                "slug": "krabi-province",
                "cities": {
                    "krabi": {
                        "name_ru": "Краби",
                        "name_en": "Krabi",
                        "slug": "krabi",
                        "airport_codes": ["KBV"],
                        "lat": 8.0863, "lon": 98.9063,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # EGYPT
    # ═══════════════════════════════════════════════════════════════
    "egypt": {
        "name_ru": "Египет",
        "name_ru_prepositional": "Египте",
        "name_en": "Egypt",
        "name_es": "Egipto",
        "slug": "egypt",
        "currency": "EGP",
        "visa_ru": "виза по прибытии ($25)",
        "visa_en": "visa on arrival ($25)",
        "visa_es": "visa a la llegada ($25)",
        "airport_code": "SSH",
        "regions": {
            "red-sea": {
                "name_ru": "Красноморское побережье",
                "name_en": "Red Sea Coast",
                "slug": "red-sea",
                "cities": {
                    "sharm-el-sheikh": {
                        "name_ru": "Шарм-эль-Шейх",
                        "name_en": "Sharm El Sheikh",
                        "slug": "sharm-el-sheikh",
                        "airport_codes": ["SSH"],
                        "lat": 27.9158, "lon": 34.3300,
                    },
                    "hurghada": {
                        "name_ru": "Хургада",
                        "name_en": "Hurghada",
                        "slug": "hurghada",
                        "airport_codes": ["HRG"],
                        "lat": 27.2579, "lon": 33.8116,
                    },
                    "marsa-alam": {
                        "name_ru": "Марса-Алам",
                        "name_en": "Marsa Alam",
                        "slug": "marsa-alam",
                        "airport_codes": ["RMF"],
                        "lat": 25.0671, "lon": 34.8900,
                    },
                },
            },
            "cairo-region": {
                "name_ru": "Каир и окрестности",
                "name_en": "Cairo & Surroundings",
                "slug": "cairo-region",
                "cities": {
                    "cairo": {
                        "name_ru": "Каир",
                        "name_en": "Cairo",
                        "slug": "cairo",
                        "airport_codes": ["CAI"],
                        "lat": 30.0444, "lon": 31.2357,
                    },
                },
            },
            "luxor-region": {
                "name_ru": "Луксор и Долина Царей",
                "name_en": "Luxor & Valley of Kings",
                "slug": "luxor-region",
                "cities": {
                    "luxor": {
                        "name_ru": "Луксор",
                        "name_en": "Luxor",
                        "slug": "luxor",
                        "airport_codes": ["LXR"],
                        "lat": 25.6872, "lon": 32.6396,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # UAE
    # ═══════════════════════════════════════════════════════════════
    "uae": {
        "name_ru": "ОАЭ",
        "name_ru_prepositional": "ОАЭ",
        "name_en": "UAE",
        "name_es": "EAU",
        "slug": "uae",
        "currency": "AED",
        "visa_ru": "безвизовый въезд до 90 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 90 days",
        "visa_es": "sin visa para ciudadanos rusos hasta 90 días",
        "airport_code": "DXB",
        "regions": {
            "dubai-emirate": {
                "name_ru": "Эмират Дубай",
                "name_en": "Dubai Emirate",
                "slug": "dubai-emirate",
                "cities": {
                    "dubai": {
                        "name_ru": "Дубай",
                        "name_en": "Dubai",
                        "slug": "dubai",
                        "airport_codes": ["DXB"],
                        "lat": 25.2048, "lon": 55.2708,
                    },
                },
            },
            "abu-dhabi-emirate": {
                "name_ru": "Эмират Абу-Даби",
                "name_en": "Abu Dhabi Emirate",
                "slug": "abu-dhabi-emirate",
                "cities": {
                    "abu-dhabi": {
                        "name_ru": "Абу-Даби",
                        "name_en": "Abu Dhabi",
                        "slug": "abu-dhabi",
                        "airport_codes": ["AUH"],
                        "lat": 24.4539, "lon": 54.3773,
                    },
                },
            },
            "sharjah-emirate": {
                "name_ru": "Эмират Шарджа",
                "name_en": "Sharjah Emirate",
                "slug": "sharjah-emirate",
                "cities": {
                    "sharjah": {
                        "name_ru": "Шарджа",
                        "name_en": "Sharjah",
                        "slug": "sharjah",
                        "airport_codes": ["SHJ"],
                        "lat": 25.3225, "lon": 55.4197,
                    },
                },
            },
            "ras-al-khaimah-emirate": {
                "name_ru": "Эмират Рас-эль-Хайма",
                "name_en": "Ras Al Khaimah Emirate",
                "slug": "ras-al-khaimah-emirate",
                "cities": {
                    "ras-al-khaimah": {
                        "name_ru": "Рас-эль-Хайма",
                        "name_en": "Ras Al Khaimah",
                        "slug": "ras-al-khaimah",
                        "airport_codes": ["RKT"],
                        "lat": 25.8007, "lon": 55.9762,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # INDONESIA
    # ═══════════════════════════════════════════════════════════════
    "indonesia": {
        "name_ru": "Индонезия",
        "name_ru_prepositional": "Индонезии",
        "name_en": "Indonesia",
        "name_es": "Indonesia",
        "slug": "indonesia",
        "currency": "IDR",
        "visa_ru": "виза по прибытии (500 000 IDR)",
        "visa_en": "visa on arrival (500,000 IDR)",
        "visa_es": "visa a la llegada (500,000 IDR)",
        "airport_code": "DPS",
        "regions": {
            "bali": {
                "name_ru": "Бали",
                "name_en": "Bali",
                "slug": "bali",
                "cities": {
                    "ubud": {
                        "name_ru": "Убуд",
                        "name_en": "Ubud",
                        "slug": "ubud",
                        "airport_codes": ["DPS"],
                        "lat": -8.5069, "lon": 115.2625,
                    },
                    "kuta": {
                        "name_ru": "Кута",
                        "name_en": "Kuta",
                        "slug": "kuta",
                        "airport_codes": ["DPS"],
                        "lat": -8.7233, "lon": 115.1725,
                    },
                    "seminyak": {
                        "name_ru": "Семиньяк",
                        "name_en": "Seminyak",
                        "slug": "seminyak",
                        "airport_codes": ["DPS"],
                        "lat": -8.6914, "lon": 115.1550,
                    },
                    "canggu": {
                        "name_ru": "Чангу",
                        "name_en": "Canggu",
                        "slug": "canggu",
                        "airport_codes": ["DPS"],
                        "lat": -8.6478, "lon": 115.1386,
                    },
                    "nusa-dua": {
                        "name_ru": "Нуса-Дуа",
                        "name_en": "Nusa Dua",
                        "slug": "nusa-dua",
                        "airport_codes": ["DPS"],
                        "lat": -8.8060, "lon": 115.2333,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # CHINA
    # ═══════════════════════════════════════════════════════════════
    "china": {
        "name_ru": "Китай",
        "name_ru_prepositional": "Китае",
        "name_en": "China",
        "slug": "china",
        "currency": "CNY",
        "visa_ru": "виза требуется (оформление через туроператора)",
        "visa_en": "visa required (processed via tour operator)",
        "airport_code": "PEK",
        "regions": {
            "hainan": {
                "name_ru": "Хайнань",
                "name_en": "Hainan",
                "slug": "hainan",
                "cities": {
                    "sanya": {
                        "name_ru": "Санья",
                        "name_en": "Sanya",
                        "slug": "sanya",
                        "airport_codes": ["SYX"],
                        "lat": 18.2528, "lon": 109.5120,
                    },
                    "haikou": {
                        "name_ru": "Хайкоу",
                        "name_en": "Haikou",
                        "slug": "haikou",
                        "airport_codes": ["HAK"],
                        "lat": 20.0174, "lon": 110.3492,
                    },
                },
            },
            "beijing-region": {
                "name_ru": "Пекин и окрестности",
                "name_en": "Beijing & Surroundings",
                "slug": "beijing-region",
                "cities": {
                    "beijing": {
                        "name_ru": "Пекин",
                        "name_en": "Beijing",
                        "slug": "beijing",
                        "airport_codes": ["PEK", "PKX"],
                        "lat": 39.9042, "lon": 116.4074,
                    },
                },
            },
            "shanghai-region": {
                "name_ru": "Шанхай и окрестности",
                "name_en": "Shanghai & Surroundings",
                "slug": "shanghai-region",
                "cities": {
                    "shanghai": {
                        "name_ru": "Шанхай",
                        "name_en": "Shanghai",
                        "slug": "shanghai",
                        "airport_codes": ["PVG", "SHA"],
                        "lat": 31.2304, "lon": 121.4737,
                    },
                },
            },
            "shaanxi": {
                "name_ru": "Шэньси",
                "name_en": "Shaanxi",
                "slug": "shaanxi",
                "cities": {
                    "xian": {
                        "name_ru": "Сиань",
                        "name_en": "Xi'an",
                        "slug": "xian",
                        "airport_codes": ["XIY"],
                        "lat": 34.3416, "lon": 108.9398,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # MALDIVES
    # ═══════════════════════════════════════════════════════════════
    "maldives": {
        "name_ru": "Мальдивы",
        "name_ru_prepositional": "Мальдивах",
        "name_en": "Maldives",
        "slug": "maldives",
        "currency": "MVR",
        "visa_ru": "безвизовый въезд до 30 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 30 days",
        "airport_code": "MLE",
        "regions": {
            "north-male-atoll": {
                "name_ru": "Северный Мале Атолл",
                "name_en": "North Malé Atoll",
                "slug": "north-male-atoll",
                "cities": {
                    "male": {
                        "name_ru": "Мале",
                        "name_en": "Male",
                        "slug": "male",
                        "airport_codes": ["MLE"],
                        "lat": 4.1755, "lon": 73.5093,
                    },
                    "hulhumale": {
                        "name_ru": "Хулхумале",
                        "name_en": "Hulhumale",
                        "slug": "hulhumale",
                        "airport_codes": ["MLE"],
                        "lat": 4.2119, "lon": 73.5398,
                    },
                },
            },
            "south-male-atoll": {
                "name_ru": "Южный Мале Атолл",
                "name_en": "South Malé Atoll",
                "slug": "south-male-atoll",
                "cities": {
                    "maafushi": {
                        "name_ru": "Маафуши",
                        "name_en": "Maafushi",
                        "slug": "maafushi",
                        "airport_codes": ["MLE"],
                        "lat": 3.9404, "lon": 73.4896,
                    },
                },
            },
            "other-atolls": {
                "name_ru": "Другие атоллы",
                "name_en": "Other Atolls",
                "slug": "other-atolls",
                "cities": {
                    "thulusdhoo": {
                        "name_ru": "Тулусду",
                        "name_en": "Thulusdhoo",
                        "slug": "thulusdhoo",
                        "airport_codes": ["MLE"],
                        "lat": 4.3744, "lon": 73.6519,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # SRI LANKA
    # ═══════════════════════════════════════════════════════════════
    "sri-lanka": {
        "name_ru": "Шри-Ланка",
        "name_ru_prepositional": "Шри-Ланке",
        "name_en": "Sri Lanka",
        "slug": "sri-lanka",
        "currency": "LKR",
        "visa_ru": "электронная виза (ETA) для граждан РФ",
        "visa_en": "electronic visa (ETA) for Russian citizens",
        "airport_code": "CMB",
        "regions": {
            "western-province": {
                "name_ru": "Западная провинция",
                "name_en": "Western Province",
                "slug": "western-province",
                "cities": {
                    "colombo": {
                        "name_ru": "Коломбо",
                        "name_en": "Colombo",
                        "slug": "colombo",
                        "airport_codes": ["CMB"],
                        "lat": 6.9271, "lon": 79.8612,
                    },
                },
            },
            "southern-province": {
                "name_ru": "Южная провинция",
                "name_en": "Southern Province",
                "slug": "southern-province",
                "cities": {
                    "bentota": {
                        "name_ru": "Бентота",
                        "name_en": "Bentota",
                        "slug": "bentota",
                        "airport_codes": ["CMB"],
                        "lat": 6.4270, "lon": 79.9960,
                    },
                    "unawatuna": {
                        "name_ru": "Унаватуна",
                        "name_en": "Unawatuna",
                        "slug": "unawatuna",
                        "airport_codes": ["CMB"],
                        "lat": 6.0210, "lon": 80.2470,
                    },
                },
            },
            "central-province": {
                "name_ru": "Центральная провинция",
                "name_en": "Central Province",
                "slug": "central-province",
                "cities": {
                    "sigiriya": {
                        "name_ru": "Сигирия",
                        "name_en": "Sigiriya",
                        "slug": "sigiriya",
                        "airport_codes": ["CMB"],
                        "lat": 7.9572, "lon": 80.7603,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # MONTENEGRO
    # ═══════════════════════════════════════════════════════════════
    "montenegro": {
        "name_ru": "Черногория",
        "name_ru_prepositional": "Черногории",
        "name_en": "Montenegro",
        "slug": "montenegro",
        "currency": "EUR",
        "visa_ru": "безвизовый въезд до 30 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 30 days",
        "airport_code": "TGD",
        "regions": {
            "budva-riviera": {
                "name_ru": "Будванская ривьера",
                "name_en": "Budva Riviera",
                "slug": "budva-riviera",
                "cities": {
                    "budva": {
                        "name_ru": "Будва",
                        "name_en": "Budva",
                        "slug": "budva",
                        "airport_codes": ["TGD", "TIV"],
                        "lat": 42.2894, "lon": 18.8400,
                    },
                },
            },
            "kotor-bay": {
                "name_ru": "Которская бухта",
                "name_en": "Bay of Kotor",
                "slug": "kotor-bay",
                "cities": {
                    "kotor": {
                        "name_ru": "Котор",
                        "name_en": "Kotor",
                        "slug": "kotor",
                        "airport_codes": ["TIV", "TGD"],
                        "lat": 42.4247, "lon": 18.7712,
                    },
                },
            },
            "tivat-area": {
                "name_ru": "Тиват и окрестности",
                "name_en": "Tivat & Surroundings",
                "slug": "tivat-area",
                "cities": {
                    "tivat": {
                        "name_ru": "Тиват",
                        "name_en": "Tivat",
                        "slug": "tivat",
                        "airport_codes": ["TIV"],
                        "lat": 42.4304, "lon": 18.7000,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # VIETNAM
    # ═══════════════════════════════════════════════════════════════
    "vietnam": {
        "name_ru": "Вьетнам",
        "name_ru_prepositional": "Вьетнаме",
        "name_en": "Vietnam",
        "slug": "vietnam",
        "currency": "VND",
        "visa_ru": "безвизовый въезд до 45 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 45 days",
        "airport_code": "SGN",
        "regions": {
            "south": {
                "name_ru": "Юг Вьетнама",
                "name_en": "Southern Vietnam",
                "slug": "south",
                "cities": {
                    "hochiminh": {
                        "name_ru": "Хо Ши Мин",
                        "name_en": "Ho Chi Minh City",
                        "slug": "hochiminh",
                        "airport_codes": ["SGN"],
                        "lat": 10.8231, "lon": 106.6297,
                    },
                    "phu-quoc": {
                        "name_ru": "Фукуок",
                        "name_en": "Phu Quoc",
                        "slug": "phu-quoc",
                        "airport_codes": ["PQC"],
                        "lat": 10.2270, "lon": 103.9635,
                    },
                },
            },
            "central": {
                "name_ru": "Центральный Вьетнам",
                "name_en": "Central Vietnam",
                "slug": "central",
                "cities": {
                    "da-nang": {
                        "name_ru": "Дананг",
                        "name_en": "Da Nang",
                        "slug": "da-nang",
                        "airport_codes": ["DAD"],
                        "lat": 16.0544, "lon": 108.2022,
                    },
                    "nha-trang": {
                        "name_ru": "Нячанг",
                        "name_en": "Nha Trang",
                        "slug": "nha-trang",
                        "airport_codes": ["CXR"],
                        "lat": 12.2389, "lon": 109.1967,
                    },
                },
            },
            "north": {
                "name_ru": "Север Вьетнама",
                "name_en": "Northern Vietnam",
                "slug": "north",
                "cities": {
                    "hanoi": {
                        "name_ru": "Ханой",
                        "name_en": "Hanoi",
                        "slug": "hanoi",
                        "airport_codes": ["HAN"],
                        "lat": 21.0285, "lon": 105.8542,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # GEORGIA
    # ═══════════════════════════════════════════════════════════════
    "georgia": {
        "name_ru": "Грузия",
        "name_ru_prepositional": "Грузии",
        "name_en": "Georgia",
        "slug": "georgia",
        "currency": "GEL",
        "visa_ru": "безвизовый въезд до 1 года для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 1 year",
        "airport_code": "TBS",
        "regions": {
            "tbilisi-region": {
                "name_ru": "Тбилиси и окрестности",
                "name_en": "Tbilisi & Surroundings",
                "slug": "tbilisi-region",
                "cities": {
                    "tbilisi": {
                        "name_ru": "Тбилиси",
                        "name_en": "Tbilisi",
                        "slug": "tbilisi",
                        "airport_codes": ["TBS"],
                        "lat": 41.7151, "lon": 44.8271,
                    },
                },
            },
            "adjara": {
                "name_ru": "Аджария",
                "name_en": "Adjara",
                "slug": "adjara",
                "cities": {
                    "batumi": {
                        "name_ru": "Батуми",
                        "name_en": "Batumi",
                        "slug": "batumi",
                        "airport_codes": ["BUS"],
                        "lat": 41.6168, "lon": 41.6367,
                    },
                },
            },
            "imereti": {
                "name_ru": "Имеретия",
                "name_en": "Imereti",
                "slug": "imereti",
                "cities": {
                    "kutaisi": {
                        "name_ru": "Кутаиси",
                        "name_en": "Kutaisi",
                        "slug": "kutaisi",
                        "airport_codes": ["KUT"],
                        "lat": 42.2679, "lon": 42.7180,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # CYPRUS
    # ═══════════════════════════════════════════════════════════════
    "cyprus": {
        "name_ru": "Кипр",
        "name_ru_prepositional": "Кипре",
        "name_en": "Cyprus",
        "slug": "cyprus",
        "currency": "EUR",
        "visa_ru": "безвизовый въезд до 90 дней для граждан РФ",
        "visa_en": "visa-free for Russian citizens up to 90 days",
        "airport_code": "LCA",
        "regions": {
            "limassol-district": {
                "name_ru": "Лимасольский район",
                "name_en": "Limassol District",
                "slug": "limassol-district",
                "cities": {
                    "limassol": {
                        "name_ru": "Лимассол",
                        "name_en": "Limassol",
                        "slug": "limassol",
                        "airport_codes": ["LCA"],
                        "lat": 34.7071, "lon": 33.0224,
                    },
                },
            },
            "famagusta-district": {
                "name_ru": "Фамагустский район",
                "name_en": "Famagusta District",
                "slug": "famagusta-district",
                "cities": {
                    "ayia-napa": {
                        "name_ru": "Айя-Напа",
                        "name_en": "Ayia Napa",
                        "slug": "ayia-napa",
                        "airport_codes": ["LCA", "ECN"],
                        "lat": 34.9859, "lon": 34.0021,
                    },
                },
            },
            "paphos-district": {
                "name_ru": "Пафосский район",
                "name_en": "Paphos District",
                "slug": "paphos-district",
                "cities": {
                    "paphos": {
                        "name_ru": "Пафос",
                        "name_en": "Paphos",
                        "slug": "paphos",
                        "airport_codes": ["PFO"],
                        "lat": 34.7720, "lon": 32.4297,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # OMAN
    # ═══════════════════════════════════════════════════════════════
    "oman": {
        "name_ru": "Оман",
        "name_ru_prepositional": "Омане",
        "name_en": "Oman",
        "slug": "oman",
        "currency": "OMR",
        "visa_ru": "виза по прибытии (20 OMR) для граждан РФ",
        "visa_en": "visa on arrival (20 OMR) for Russian citizens",
        "airport_code": "MCT",
        "regions": {
            "muscat-region": {
                "name_ru": "Маскат и окрестности",
                "name_en": "Muscat & Surroundings",
                "slug": "muscat-region",
                "cities": {
                    "muscat": {
                        "name_ru": "Маскат",
                        "name_en": "Muscat",
                        "slug": "muscat",
                        "airport_codes": ["MCT"],
                        "lat": 23.5880, "lon": 58.3829,
                    },
                },
            },
            "dhofar": {
                "name_ru": "Дофар",
                "name_en": "Dhofar",
                "slug": "dhofar",
                "cities": {
                    "salalah": {
                        "name_ru": "Салала",
                        "name_en": "Salalah",
                        "slug": "salalah",
                        "airport_codes": ["SLL"],
                        "lat": 17.0151, "lon": 54.0924,
                    },
                },
            },
            "musandam": {
                "name_ru": "Мусандам",
                "name_en": "Musandam",
                "slug": "musandam",
                "cities": {
                    "khasab": {
                        "name_ru": "Хасаб",
                        "name_en": "Khasab",
                        "slug": "khasab",
                        "airport_codes": ["KHS"],
                        "lat": 26.1985, "lon": 56.2491,
                    },
                },
            },
        },
    },

    # ═══════════════════════════════════════════════════════════════
    # RUSSIAN REGIONS (standalone)
    # ═══════════════════════════════════════════════════════════════
    "baikal": {
        "name_ru": "Байкал",
        "name_ru_prepositional": "Байкале",
        "name_en": "Lake Baikal",
        "slug": "baikal",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "IKT",
        "cities": {
            "irkutsk": {
                "name_ru": "Иркутск",
                "name_en": "Irkutsk",
                "slug": "irkutsk",
                "airport_codes": ["IKT"],
                "lat": 52.2855, "lon": 104.2890,
            },
            "listvyanka": {
                "name_ru": "Листвянка",
                "name_en": "Listvyanka",
                "slug": "listvyanka",
                "airport_codes": ["IKT"],
                "lat": 51.8592, "lon": 104.8545,
            },
            "olkhon": {
                "name_ru": "Остров Ольхон",
                "name_en": "Olkhon Island",
                "slug": "olkhon",
                "airport_codes": ["IKT"],
                "lat": 53.1500, "lon": 107.4500,
            },
        },
    },
    "altai": {
        "name_ru": "Алтай",
        "name_ru_prepositional": "Алтае",
        "name_en": "Altai",
        "slug": "altai",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "BAX",
        "cities": {
            "gorno-altaysk": {
                "name_ru": "Горно-Алтайск",
                "name_en": "Gorno-Altaysk",
                "slug": "gorno-altaysk",
                "airport_codes": ["BAX"],
                "lat": 51.9586, "lon": 85.9364,
            },
            "chemyal": {
                "name_ru": "Чемал",
                "name_en": "Chemal",
                "slug": "chemyal",
                "airport_codes": ["BAX"],
                "lat": 51.4167, "lon": 86.0000,
            },
            "akkem": {
                "name_ru": "Аккем",
                "name_en": "Akkem",
                "slug": "akkem",
                "airport_codes": ["BAX"],
                "lat": 51.7500, "lon": 87.6667,
            },
        },
    },
    "karelia": {
        "name_ru": "Карелия",
        "name_ru_prepositional": "Карелии",
        "name_en": "Karelia",
        "slug": "karelia",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "PES",
        "cities": {
            "petrozavodsk": {
                "name_ru": "Петрозаводск",
                "name_en": "Petrozavodsk",
                "slug": "petrozavodsk",
                "airport_codes": ["PES"],
                "lat": 61.7850, "lon": 34.3469,
            },
            "sortavala": {
                "name_ru": "Сортавала",
                "name_en": "Sortavala",
                "slug": "sortavala",
                "airport_codes": ["PES"],
                "lat": 61.7000, "lon": 30.6833,
            },
            "kizhi": {
                "name_ru": "Кижинский остров",
                "name_en": "Kizhi Island",
                "slug": "kizhi",
                "airport_codes": ["PES"],
                "lat": 62.0670, "lon": 35.2330,
            },
        },
    },
    "dagestan": {
        "name_ru": "Дагестан",
        "name_ru_prepositional": "Дагестане",
        "name_en": "Dagestan",
        "slug": "dagestan",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "MCX",
        "cities": {
            "makhachkala": {
                "name_ru": "Махачкала",
                "name_en": "Makhachkala",
                "slug": "makhachkala",
                "airport_codes": ["MCX"],
                "lat": 42.9849, "lon": 47.5047,
            },
            "derbent": {
                "name_ru": "Дербент",
                "name_en": "Derbent",
                "slug": "derbent",
                "airport_codes": ["MCX"],
                "lat": 42.0578, "lon": 48.2964,
            },
            "kizlyar": {
                "name_ru": "Кизляр",
                "name_en": "Kizlyar",
                "slug": "kizlyar",
                "airport_codes": ["MCX"],
                "lat": 43.8472, "lon": 46.7114,
            },
        },
    },
    "kamchatka": {
        "name_ru": "Камчатка",
        "name_ru_prepositional": "Камчатке",
        "name_en": "Kamchatka",
        "slug": "kamchatka",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "PKC",
        "cities": {
            "petropavlovsk-kamchatsky": {
                "name_ru": "Петропавловск-Камчатский",
                "name_en": "Petropavlovsk-Kamchatsky",
                "slug": "petropavlovsk-kamchatsky",
                "airport_codes": ["PKC"],
                "lat": 53.0133, "lon": 158.6539,
            },
            "paratunka": {
                "name_ru": "Паратунка",
                "name_en": "Paratunka",
                "slug": "paratunka",
                "airport_codes": ["PKC"],
                "lat": 52.9583, "lon": 158.2500,
            },
        },
    },
    "mineral-vody": {
        "name_ru": "Кавказские Минеральные Воды",
        "name_ru_prepositional": "Кавказских Минеральных Водах",
        "name_en": "Caucasian Mineral Waters",
        "slug": "mineral-vody",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "MRV",
        "cities": {
            "pyatigorsk": {
                "name_ru": "Пятигорск",
                "name_en": "Pyatigorsk",
                "slug": "pyatigorsk",
                "airport_codes": ["MRV"],
                "lat": 44.0414, "lon": 43.0606,
            },
            "kislovodsk": {
                "name_ru": "Кисловодск",
                "name_en": "Kislovodsk",
                "slug": "kislovodsk",
                "airport_codes": ["MRV"],
                "lat": 43.9053, "lon": 42.7206,
            },
            "essentuki": {
                "name_ru": "Ессентуки",
                "name_en": "Essentuki",
                "slug": "essentuki",
                "airport_codes": ["MRV"],
                "lat": 44.0464, "lon": 42.8556,
            },
        },
    },
    "kavkaz": {
        "name_ru": "Кавказ",
        "name_ru_prepositional": "Кавказе",
        "name_en": "Caucasus",
        "slug": "kavkaz",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "MRV",
        "cities": {
            "dombay": {
                "name_ru": "Домбай",
                "name_en": "Dombay",
                "slug": "dombay",
                "airport_codes": ["MRV"],
                "lat": 43.2961, "lon": 41.6297,
            },
            "elbrus": {
                "name_ru": "Эльбрус",
                "name_en": "Elbrus",
                "slug": "elbrus",
                "airport_codes": ["MRV"],
                "lat": 43.2522, "lon": 42.4567,
            },
            "kislovodsk-c": {
                "name_ru": "Кисловодск",
                "name_en": "Kislovodsk",
                "slug": "kislovodsk-c",
                "airport_codes": ["MRV"],
                "lat": 43.9053, "lon": 42.7206,
            },
        },
    },
    "kaliningrad": {
        "name_ru": "Калининград",
        "name_ru_prepositional": "Калининграде",
        "name_en": "Kaliningrad",
        "slug": "kaliningrad",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "KGD",
        "cities": {
            "kaliningrad-city": {
                "name_ru": "Калининград",
                "name_en": "Kaliningrad",
                "slug": "kaliningrad-city",
                "airport_codes": ["KGD"],
                "lat": 54.7104, "lon": 20.4522,
            },
            "zelenogradsk": {
                "name_ru": "Зеленоградск",
                "name_en": "Zelenogradsk",
                "slug": "zelenogradsk",
                "airport_codes": ["KGD"],
                "lat": 54.9667, "lon": 20.4833,
            },
            "svetlogorsk": {
                "name_ru": "Светлогорск",
                "name_en": "Svetlogorsk",
                "slug": "svetlogorsk",
                "airport_codes": ["KGD"],
                "lat": 54.9500, "lon": 20.1833,
            },
        },
    },
    "vladivostok": {
        "name_ru": "Владивосток",
        "name_ru_prepositional": "Владивостоке",
        "name_en": "Vladivostok",
        "slug": "vladivostok",
        "currency": "RUB",
        "visa_ru": "внутренний паспорт гражданина РФ",
        "visa_en": "Russian internal passport (domestic travel)",
        "airport_code": "VVO",
        "cities": {
            "vladivostok-city": {
                "name_ru": "Владивосток",
                "name_en": "Vladivostok",
                "slug": "vladivostok-city",
                "airport_codes": ["VVO"],
                "lat": 43.1332, "lon": 131.9113,
            },
            "russky-island": {
                "name_ru": "Русский остров",
                "name_en": "Russky Island",
                "slug": "russky-island",
                "airport_codes": ["VVO"],
                "lat": 43.0000, "lon": 132.0000,
            },
        },
    },

    "uzbekistan": {
        "name_ru": "Узбекистан",
        "name_ru_prepositional": "Узбекистане",
        "name_en": "Uzbekistan",
        "slug": "uzbekistan",
        "currency": "UZS",
        "visa_ru": "безвизовый въезд до 30 дней для граждан РФ",
        "visa_en": "visa-free entry up to 30 days for Russian citizens",
        "airport_code": "TAS",
        "cities": {
            "tashkent": {
                "name_ru": "Ташкент",
                "name_en": "Tashkent",
                "slug": "tashkent",
                "airport_codes": ["TAS"],
                "lat": 41.2995, "lon": 69.2401,
            },
            "samarkand": {
                "name_ru": "Самарканд",
                "name_en": "Samarkand",
                "slug": "samarkand",
                "airport_codes": ["SKD"],
                "lat": 39.6542, "lon": 66.9597,
            },
            "bukhara": {
                "name_ru": "Бухара",
                "name_en": "Bukhara",
                "slug": "bukhara",
                "airport_codes": ["BHK"],
                "lat": 39.7681, "lon": 64.4556,
            },
            "khiva": {
                "name_ru": "Хива",
                "name_en": "Khiva",
                "slug": "khiva",
                "airport_codes": ["UGC"],
                "lat": 41.3786, "lon": 60.3564,
            },
        },
    },

    "kazakhstan": {
        "name_ru": "Казахстан",
        "name_ru_prepositional": "Казахстане",
        "name_en": "Kazakhstan",
        "slug": "kazakhstan",
        "currency": "KZT",
        "visa_ru": "безвизовый въезд до 30 дней для граждан РФ",
        "visa_en": "visa-free entry up to 30 days for Russian citizens",
        "airport_code": "NQZ",
        "cities": {
            "almaty": {
                "name_ru": "Алматы",
                "name_en": "Almaty",
                "slug": "almaty",
                "airport_codes": ["ALA"],
                "lat": 43.2380, "lon": 76.9455,
            },
            "astana": {
                "name_ru": "Астана",
                "name_en": "Astana",
                "slug": "astana",
                "airport_codes": ["NQZ"],
                "lat": 51.1282, "lon": 71.4304,
            },
            "charyn": {
                "name_ru": "Чарынский каньон",
                "name_en": "Charyn Canyon",
                "slug": "charyn",
                "airport_codes": ["ALA"],
                "lat": 43.3558, "lon": 79.0711,
            },
            "burabay": {
                "name_ru": "Бурабай",
                "name_en": "Burabay",
                "slug": "burabay",
                "airport_codes": ["NQZ"],
                "lat": 53.0833, "lon": 70.2833,
            },
        },
    },
}