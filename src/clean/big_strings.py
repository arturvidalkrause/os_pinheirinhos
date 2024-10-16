"""
Módulo de Listas de Países e Produtos Agrícolas

Este módulo contém várias listas que agrupam países e produtos agrícolas
para diferentes contextos de análise de dados. As listas incluem países selecionados
para análises de temperatura, FAOstat, Banco Mundial, e outras categorias econômicas
ou climáticas, além de listas de vegetais e produtos agrícolas específicos para
análises de produção.

As listas são usadas para filtrar e segmentar dados em diversas áreas de estudo,
como clima, economia e agricultura.

"""

countries_to_keep_temperatura = [
    'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antarctica',
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
    'Belgium', 'Belize', 'Benin', 'Bolivia', 'Bosnia and Herzegovina',
    'Botswana', 'Brazil', 'Bulgaria', 'Burkina Faso', 'Burma', 
    'Cambodia', 'Cameroon', 'Canada', 'Cape Verde', 'Central African Republic',
    'Chad', 'Chile', 'China', 'Colombia', 'Comoros',
    'Congo (Brazzaville)', 'Congo (Kinshasa)', 'Costa Rica', 
    "Cote D'Ivoire", 'Croatia', 'Cuba', 'Cyprus', 'Czech Republic',
    'Denmark', 'Dominican Republic', 'Ecuador', 'Egypt', 
    'El Salvador', 'Eritrea', 'Estonia', 'Ethiopia', 
    'Fiji', 'Finland', 'France', 'Gabon', 'Gambia',
    'Georgia', 'Germany', 'Ghana', 'Greece', 'Greenland',
    'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 'Guyana',
    'Haiti', 'Honduras', 'Hungary', 'Iceland', 'India',
    'Indonesia', 'Iran', 'Iraq', 'Ireland', 'Israel',
    'Italy', 'Jamaica', 'Japan', 'Jordan', 'Kazakhstan',
    'Kenya', 'Korea, North', 'Korea, South', 'Kuwait', 
    'Kyrgyzstan', 'Laos', 'Latvia', 'Lebanon', 'Liberia',
    'Libya', 'Lithuania', 'Luxembourg', 'Malaysia', 'Malawi',
    'Malta', 'Mexico', 'Moldova', 'Mongolia', 'Montenegro',
    'Morocco', 'Mozambique', 'Namibia', 'Nepal', 'Netherlands',
    'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 'Norway',
    'Oman', 'Pakistan', 'Palau', 'Panama', 'Papua New Guinea',
    'Paraguay', 'Peru', 'Philippines', 'Poland', 'Portugal',
    'Romania', 'Russia', 'Saudi Arabia', 'Senegal', 'Serbia',
    'Seychelles', 'Sierra Leone', 'Singapore', 'Slovakia', 
    'Slovenia', 'Solomon Islands', 'Somalia', 'South Africa', 
    'Spain', 'Sri Lanka', 'Sudan', 'Suriname', 'Sweden', 
    'Switzerland', 'Syria', 'Taiwan', 'Tajikistan', 'Tanzania',
    'Thailand', 'Timor-Leste', 'Togo', 'Tonga', 'Tunisia', 
    'Turkey', 'Turkmenistan', 'Tuvalu', 'Uganda', 'Ukraine',
    'United Arab Emirates', 'United Kingdom', 'United States',
    'Uruguay', 'Uzbekistan', 'Vanuatu', 'Venezuela', 
    'Vietnam', 'Yemen', 'Zambia', 'Zimbabwe', 'Qatar', 
    'Rwanda', 'Burundi', 'Maldives', 'Brunei', 'Swaziland',
    'Hong Kong', 'Equatorial Guinea'
    ]

countries_to_keep_faostat = [
    'Afghanistan', 'Albania', 'Algeria', 'Angola', 'Antigua and Barbuda', 
    'Argentina', 'Armenia', 'Australia', 'Austria', 'Azerbaijan',
    'Bahamas', 'Bahrain', 'Bangladesh', 'Barbados', 'Belarus',
    'Belgium', 'Belize', 'Benin', 'Bolivia', 'Bosnia and Herzegovina',
    'Botswana', 'Brazil', 'Brunei Darussalam', 'Bulgaria', 'Burkina Faso', 
    'Burundi', 'Cabo Verde', 'Cambodia', 'Cameroon', 'Canada', 
    'Central African Republic', 'Chad', 'Chile', 'China', 
    'Colombia', 'Comoros', 'Congo', 'Costa Rica', 'Croatia', 
    'Cuba', 'Cyprus', 'Czechia', 'Côte d\'Ivoire',
    'Democratic Republic of the Congo', 'Denmark', 'Djibouti', 
    'Dominican Republic', 'Ecuador', 'Egypt', 'El Salvador', 
    'Equatorial Guinea', 'Eritrea', 'Estonia', 'Eswatini', 
    'Ethiopia', 'Fiji', 'Finland', 'France', 'Gabon', 
    'Gambia', 'Georgia', 'Germany', 'Ghana', 'Greece', 
    'Grenada', 'Guatemala', 'Guinea', 'Guinea-Bissau', 
    'Guyana', 'Haiti', 'Honduras', 'Hungary', 'Iceland', 
    'India', 'Indonesia', 'Iran', 'Iraq', 'Ireland', 
    'Israel', 'Italy', 'Jamaica', 'Japan', 'Jordan', 
    'Kazakhstan', 'Kenya', 'Kuwait', 'Kyrgyzstan', 
    'Latvia', 'Lebanon', 'Lesotho', 'Liberia', 'Libya', 
    'Lithuania', 'Luxembourg', 'Madagascar', 'Malawi', 
    'Malaysia', 'Maldives', 'Mali', 'Malta', 'Mexico', 
    'Mongolia', 'Montenegro', 'Morocco', 'Mozambique', 
    'Myanmar', 'Namibia', 'Nepal', 'Netherlands', 
    'New Zealand', 'Nicaragua', 'Niger', 'Nigeria', 
    'Norway', 'Oman', 'Pakistan', 'Panama', 
    'Papua New Guinea', 'Paraguay', 'Peru', 'Philippines', 
    'Poland', 'Portugal', 'Romania', 'Russian Federation', 
    'Rwanda', 'Saint Kitts and Nevis', 'Saint Lucia', 
    'Samoa', 'Sao Tome and Principe', 'Saudi Arabia', 
    'Senegal', 'Serbia', 'Seychelles', 'Sierra Leone', 
    'Singapore', 'Slovakia', 'Slovenia', 'Solomon Islands', 
    'Somalia', 'South Africa', 'Spain', 'Sri Lanka', 
    'Sudan', 'Suriname', 'Sweden', 'Switzerland', 
    'Syrian Arab Republic', 'Tajikistan', 'Thailand', 
    'Timor-Leste', 'Togo', 'Tonga', 'Tunisia', 
    'Turkey', 'Uganda', 'Ukraine', 
    'United Arab Emirates', 'United Kingdom of Great Britain and Northern Ireland', 
    'United States of America', 'Uruguay', 'Uzbekistan', 
    'Vanuatu', 'Venezuela', 'Vietnam', 'World', 
    'USSR', 'Yugoslav SFR'
    ]

countries_to_keep_worldbank = [
    'Aruba', 'Afghanistan', 'Angola', 'Albania', 'Andorra', 
    'United Arab Emirates', 'Argentina', 'Armenia', 'American Samoa', 
    'Antigua and Barbuda', 'Australia', 'Austria', 'Azerbaijan', 
    'Burundi', 'Belgium', 'Benin', 'Burkina Faso', 'Bangladesh', 
    'Bulgaria', 'Bahrain', 'Bahamas, The', 'Bosnia and Herzegovina', 
    'Belarus', 'Belize', 'Bermuda', 'Bolivia', 'Brazil', 
    'Barbados', 'Brunei Darussalam', 'Bhutan', 'Botswana', 
    'Central African Republic', 'Canada', 'Switzerland', 
    'Channel Islands', 'Chile', 'China', "Cote d'Ivoire", 
    'Cameroon', 'Congo, Dem. Rep.', 'Congo, Rep.', 'Colombia', 
    'Comoros', 'Cabo Verde', 'Costa Rica', 'Cuba', 'Curacao', 
    'Cayman Islands', 'Cyprus', 'Czechia', 'Germany', 
    'Djibouti', 'Dominica', 'Denmark', 'Dominican Republic', 
    'Algeria', 'Ecuador', 'Egypt, Arab Rep.', 'Spain', 
    'Estonia', 'Ethiopia', 'Finland', 'Fiji', 'France', 
    'Faroe Islands', 'Gabon', 'United Kingdom', 'Georgia', 
    'Ghana', 'Gibraltar', 'Guinea', 'Gambia, The', 
    'Guinea-Bissau', 'Equatorial Guinea', 'Greece', 'Grenada', 
    'Greenland', 'Guatemala', 'Guam', 'Guyana', 
    'Hong Kong SAR, China', 'Honduras', 'Croatia', 'Haiti', 
    'Hungary', 'Indonesia', 'Isle of Man', 'India', 
    'Ireland', 'Iran, Islamic Rep.', 'Iraq', 'Iceland', 
    'Israel', 'Italy', 'Jamaica', 'Jordan', 'Japan', 
    'Kazakhstan', 'Kenya', 'Kyrgyz Republic', 'Cambodia', 
    'Kiribati', 'St. Kitts and Nevis', 'Korea, Rep.', 
    'Kuwait', 'Lao PDR', 'Lebanon', 'Liberia', 'Libya', 
    'St. Lucia', 'Liechtenstein', 'Sri Lanka', 'Lithuania', 
    'Luxembourg', 'Latvia', 'Macao SAR, China', 
    'St. Martin (French part)', 'Morocco', 'Monaco', 
    'Moldova', 'Madagascar', 'Maldives', 'Mexico', 
    'Marshall Islands', 'North Macedonia', 'Mali', 'Malta', 
    'Myanmar', 'Montenegro', 'Mongolia', 'Northern Mariana Islands', 
    'Mozambique', 'Mauritania', 'Mauritius', 'Malawi', 
    'Malaysia', 'Namibia', 'New Caledonia', 'Niger', 
    'Nigeria', 'Nicaragua', 'Netherlands', 'Norway', 
    'Nepal', 'Nauru', 'New Zealand', 'Oman', 
    'Pakistan', 'Panama', 'Peru', 'Philippines', 
    'Palau', 'Papua New Guinea', 'Poland', 'Portugal', 
    'Paraguay', 'Romania', 'Russian Federation', 'Rwanda', 
    'Saudi Arabia', 'Sudan', 'Senegal', 'Singapore', 
    'Solomon Islands', 'Sierra Leone', 'El Salvador', 
    'San Marino', 'Somalia', 'Serbia', 'South Sudan', 
    'Sao Tome and Principe', 'Suriname', 'Slovak Republic', 
    'Slovenia', 'Sweden', 'Eswatini', 'Seychelles', 
    'Chad', 'Togo', 'Thailand', 'Tajikistan', 
    'Turkmenistan', 'Timor-Leste', 'Tonga', 'Trinidad and Tobago', 
    'Tunisia', 'Turkiye', 'Tuvalu', 'Tanzania', 
    'Uganda', 'Ukraine', 'Uruguay', 'United States', 
    'Uzbekistan', 'Vanuatu', 'World', 'Samoa', 
    'Kosovo', 'Yemen, Rep.', 'South Africa', 'Zambia', 'Zimbabwe'
]

vegetais_producao = [
    'Almonds, in shell',
    'Anise, badian, coriander, cumin, caraway, fennel and juniper berries, raw',
    'Apples',
    'Apricots',
    'Barley',
    'Butter and ghee of sheep milk',
    'Butter of cow milk',
    'Buttermilk, dry',
    'Cantaloupes and other melons',
    'Cotton lint, ginned',
    'Cotton seed',
    'Cottonseed oil',
    'Figs',
    'Grapes',
    'Linseed',
    'Maize (corn)',
    'Millet',
    'Molasses',
    'Mustard seed',
    'Natural honey',
    'Oil of linseed',
    'Oil of sesame seed',
    'Olive oil',
    'Olives',
    'Onions and shallots, dry (excluding dehydrated)',
    'Oranges',
    'Other berries and fruits of the genus vaccinium n.e.c.',
    'Other citrus fruit, n.e.c.',
    'Other fruits, n.e.c.',
    'Other nuts (excluding wild edible nuts and groundnuts), in shell, n.e.c.',
    'Other pulses n.e.c.',
    'Other stimulant, spice and aromatic crops, n.e.c.',
    'Other stone fruits',
    'Other vegetables, fresh n.e.c.',
    'Peaches and nectarines',
    'Pears',
    'Pistachios, in shell',
    'Plums and sloes',
    'Potatoes',
    'Raw cane or beet sugar (centrifugal only)',
    'Rice',
    'Sesame seed',
    'Sugar beet',
    'Sugar cane',
    'Sunflower seed',
    'Walnuts, in shell',
    'Watermelons',
    'Wheat',
    'Beans, dry',
    'Beer of barley, malted',
    'Broad beans and horse beans, dry',
    'Broad beans and horse beans, green',
    'Cabbages',
    'Carrots and turnips',
    'Cauliflowers and broccoli',
    'Cherries',
    'Chestnuts, in shell',
    'Chillies and peppers, green (Capsicum spp. and Pimenta spp.)',
    'Cucumbers and gherkins',
    'Dates',
    'Eggplants (aubergines)',
    'Green garlic',
    'Lemons and limes',
    'Lettuce and chicory',
    'Mushrooms and truffles',
    'Oats',
    'Okra',
    'Other beans, green',
    'Palm oil',
    'Peas, green',
    'Pumpkins, squash and gourds',
    'Quinces',
    'Safflower seed',
    'Spinach',
    'Strawberries',
    'Tangerines, mandarins, clementines',
    'Tomatoes',
    'Unmanufactured tobacco',
    'Vetches',
    'Artichokes',
    'Bananas',
    'Chick peas, dry',
    'Chillies and peppers, dry (Capsicum spp., Pimenta spp.), raw',
    'Groundnuts, excluding shelled',
    'Lentils, dry',
    'Papayas',
    'Peppermint, spearmint',
    'String beans',
    'Tea leaves',
    'Yams',
    'Asparagus',
    'Canary seed',
    'Cereals n.e.c.',
    'Flax, raw or retted',
    'Ginger, raw',
    'Jute, raw or retted',
    'Natural rubber in primary forms',
    'Other sugar crops n.e.c.',
    'Other pome fruits',
    'Chicory roots',
    'Vanilla, raw',
    'Edible roots and tubers with high starch or inulin content, n.e.c., fresh',
    'Yautia',
    'Fonio',
    'Kola nuts',
    'Melonseed',
    'Nutmeg, mace, cardamoms, raw',
    'Quinoa',
    'Brazil nuts, in shell'
    ]

paises_desenvolvidos = [
    "BHR",  # Bahrein
    "SGP",  # Cingapura
    "HRV",  # Croácia
    "SVN",  # Eslovênia
    "ESP",  # Espanha
    "FIN",  # Finlândia
    "FRA",  # França
    "HUN",  # Hungria
    "NOR",  # Noruega
    "SWE",  # Suécia
    "CHE",  # Suíça
    "THA",  # Tailândia
    "AUS",  # Austrália
    "AUT",  # Áustria
    "CAN",  # Canadá
    "CYP",  # Chipre
    "SLV",  # El Salvador
    "USA",  # Estados Unidos
    "GRC",  # Grécia
    "YEM",  # Iémen
    "ITA",  # Itália
    "JPN",  # Japão
    "PRT",  # Portugal
    "GBR",  # Reino Unido
    "TUN",  # Tunísia
]

paises_emergentes = [
    "ZAF",  # África do Sul
    "BRA",  # Brasil
    "CHL",  # Chile
    "CHN",  # China
    "KOR",  # Coréia do Sul
    "IND",  # Índia
    "IDN",  # Indonésia
    "MYS",  # Malásia
    "MEX",  # México
    "TUR"   # Turquia
]