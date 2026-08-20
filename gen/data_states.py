"""12 state landing pages. Copy verbatim from the content doc (United States tabs).
Rebrand rule applied per the doc: Back-to-School references become Classroom of Change.
NY and PA hero intros are newly written per the doc's instruction (flagged for Naman).
"""

STATES = [
    {
        "slug": "arizona", "name": "Arizona", "svg": "AZ", "cities": "Phoenix",
        "hero": "The Phoenix chapter of Shrimad Rajchandra Love and Care has been a steady light of compassion, benefiting thousands of lives through various acts of service! Month after month, volunteers came together to prepare nourishing meals and lovingly delivered them to the ones most in need.",
        "gallery": 1,
        "stats": [("50+", "Total volunteers mobilized"), ("500+", "Total service hours"), ("5,000+", "Total beneficiaries reached")],
        "centers": [{
            "name": "Phoenix",
            "sections": [
                ("Hunger Relief", "Our Phoenix volunteers come together year-round to prepare and distribute hot meals, PB&amp;J kits, and breakfast packs for individuals experiencing food insecurity. Partnering with organizations such as Tempe Community Action Agency (TCAA) and Andre House, these efforts help serve underserved communities across the region with dignity and care."),
                ("Classroom of Change", "In addition to food relief, our Phoenix team supports local Title I schools through the successful Classroom of Change campaign. Volunteers also donate clothing, toys, blankets, kitchenware, and other essential items throughout the year, helping uplift underprivileged communities and extend consistent support across Arizona."),
            ],
            "contact": ("Kiran Shah", "phoenix@srlc-usa.org", "email"),
            "partners": "Tempe Community Action Agency, Andre House",
        }],
    },
    {
        "slug": "california", "name": "California", "svg": "CA", "cities": "San Francisco, Los Angeles, San Diego",
        "hero": "From the sunlit shores of San Diego to the bustling streets of San Francisco and Los Angeles, our centers unite local partners and volunteers in transformative acts of service. To get involved in these exciting activities, contact your local SRLC leaders!",
        "gallery": 8,
        "stats": [("200+", "Total volunteers mobilized"), ("2,200+", "Total service hours"), ("85,000+", "Total beneficiaries reached")],
        "centers": [
            {
                "name": "San Diego",
                "sections": [
                    ("Community Stewardship", "Throughout the year, our San Diego team actively serves the local community by participating in Adopt-a-Beach and Adopt-a-Highway initiatives. Volunteers dedicate their time to restoring coastal areas and maintaining roadways, helping preserve the natural beauty of the region while fostering a sense of environmental responsibility and civic pride."),
                    ("Hunger Relief", "Our San Diego volunteers also collaborate with partners, including Target and National Hunger Relief, to assemble food parcels and distribute warm meals. These efforts support individuals experiencing food insecurity at the Neil Good Day Center, ensuring access to nourishing food while offering care and compassion to those in need."),
                ],
                "contact": ("Punita Shah", "sandiego@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "San Francisco",
                "sections": [
                    ("Community Care", "In the heart of the Bay Area, our San Francisco team partners with organizations such as Noah&rsquo;s Bagels and Safeway to support local shelters and community programs. Volunteers help prepare and distribute meals while organizing care packages filled with essential items to meet immediate community needs."),
                    ("Family &amp; Student Support", "Our volunteers also assemble care packages containing diapers, baby wipes, and household essentials for families and students in San Leandro and Castro Valley through Building Futures. These efforts help support vulnerable families while strengthening stability and well-being across the surrounding communities."),
                ],
                "contact": ("Divya Doshi", "sf@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Los Angeles",
                "sections": [
                    ("Education Support", "Across Los Angeles, our volunteers partner with organizations like Dreams for Schools to spark curiosity and learning among local students. By assembling STEM kits and backpacks filled with school supplies, the team helps provide children with the tools they need to succeed both inside and outside the classroom."),
                    ("Hunger Relief &amp; Essential Needs", "In addition to education initiatives, our Los Angeles volunteers work with local partners to gather clothing, hygiene supplies, and pantry staples. These items are distributed to underserved communities, helping address food insecurity and essential needs while reinforcing a culture of generosity and service."),
                ],
                "contact": ("Aditi Shah", "la@srlc-usa.org", "email"),
                "partners": "Dreams for Schools",
            },
        ],
    },
    {
        "slug": "georgia", "name": "Georgia", "svg": "GA", "cities": "Atlanta",
        "hero": "From the heart of Georgia, our Atlanta center radiates warmth and service through consistent food relief, school supply drives, and clothing distributions. Volunteers of all ages come together, transforming warehouses into food pantries and classrooms into brighter places of learning. To get involved, connect with your local SRLC leaders!",
        "gallery": 6,
        "stats": [("250+", "Volunteers mobilized"), ("4,300+", "Service hours"), ("90,000+", "Beneficiaries served"), ("Atlanta", "Communities served")],
        "centers": [{
            "name": "Atlanta",
            "sections": [
                ("Hunger Relief", "Our Atlanta volunteers lead large-scale hunger relief efforts throughout the year, donating thousands of pounds of food to support families facing food insecurity. Working with partners such as North Fulton Community Charities, Meals by Grace, and New Bethel Church, these initiatives help ensure consistent access to nourishing meals across the community."),
                ("Education &amp; Essential Support", "In addition to food relief, our Atlanta team supports local schools by donating Classroom of Change supply kits filled with notebooks, pencils, and backpacks. Volunteers also organize clothing drives and distribute hygiene and essential items, helping uplift students, families, and individuals in need while restoring dignity and stability during challenging times."),
            ],
            "contact": ("Dipal Gandhi", "atlanta@srlc-usa.org", "email"),
            "partners": None,
        }],
    },
    {
        "slug": "illinois", "name": "Illinois", "svg": "IL", "cities": "Chicago",
        "hero": "In Illinois, SRLC volunteers serve with heart in partnership with local organizations to combat hunger and uplift education, with the Chicago center leading impactful initiatives that reach children, families, and neighbors in need.",
        "gallery": 5,
        "stats": [("40+", "Volunteers mobilized"), ("150+", "Service hours"), ("2,400+", "Beneficiaries served")],
        "centers": [{
            "name": "Chicago",
            "sections": [
                ("Classroom of Change", "At the beginning of each school year, our Chicago team comes together while mobilizing friends and family to fund and assemble hundreds of Classroom of Change kits. Filled with essential supplies like notebooks, pencils, scissors, and gluesticks, these kits are distributed to Title I schools throughout the city, giving local children the tools they need to thrive in the classroom."),
                ("Hunger Relief", "Our Chicago volunteers also recently joined forces to pack over 500 peanut butter and jelly sandwiches and donate over 1,000 pounds of food. These contributions are delivered to The Salvation Army, Crystal Lake Food Pantry, Veterans Path to Hope, Frida&rsquo;s Place, and Elgin Cares, ensuring that vulnerable individuals across the city and surrounding communities have access to nourishing meals."),
            ],
            "contact": ("Paavan Shah", "chicago@srlc-usa.org", "email"),
            "partners": "The Salvation Army, Crystal Lake Food Pantry, Veterans Path to Hope, Frida&rsquo;s Place",
        }],
    },
    {
        "slug": "indiana", "name": "Indiana", "svg": "IN", "cities": "Indianapolis",
        "hero": "From the crossroads of Indianapolis to communities across the Hoosier State, our Indiana center embraces volunteering in many forms: feeding the hungry, uplifting youth, protecting the environment, and extending compassion beyond borders.",
        "gallery": 5,
        "stats": [("40+", "Volunteers mobilized"), ("700+", "Service hours"), ("5,000+", "Lives impacted")],
        "centers": [{
            "name": "Indianapolis",
            "sections": [
                ("Hunger Relief", "Our Indianapolis volunteers regularly prepare and distribute meals, snacks, and grocery items to local shelters and families facing food insecurity. These ongoing efforts help provide nourishment and dignity while supporting individuals and households in need across the community through consistent, hands-on service."),
                ("Local Community", "Beyond food relief, the Indianapolis team supports education and community well-being through supply drives, mentoring, and learning-focused activities that help children build confidence and stability. Volunteers also take part in environmental stewardship efforts, including Adopt-a-Street cleanups, helping care for shared spaces while reinforcing responsibility, pride, and long-term community health."),
            ],
            "contact": ("Sonal Sanghani", "indianapolis@srlc-usa.org", "email"),
            "partners": "We Care Charity",
        }],
    },
    {
        "slug": "massachusetts", "name": "Massachusetts", "svg": "MA", "cities": "Boston",
        "hero": "From the cobblestone streets of Beacon Hill to the vibrant harbors of the North Shore, our Boston community unites families and volunteers in service projects that nourish both body and spirit.",
        "gallery": 5,
        "stats": [("20+", "Volunteers mobilized"), ("300+", "Beneficiaries served")],
        "centers": [{
            "name": "Boston",
            "sections": [
                ("Hunger Relief", "Our Boston volunteers come together across generations to assemble meal kits filled with breakfast foods, hearty meals, snacks, and beverages. Each bag is thoughtfully decorated with drawings and notes and delivered through Open Table, helping provide nourishment while offering moments of comfort and joy."),
                ("Community Support", "In partnership with We Care Charity, volunteers also prepare and distribute lunch bags containing peanut butter and jelly sandwiches, juice, and granola bars. Shared with individuals experiencing homelessness in Salem, New Hampshire, these efforts help extend dignity, care, and consistent support to those in need."),
            ],
            "contact": ("Shaileja Mittal", "boston@srmd.org", "email"),
            "partners": "Open Table, We Care Charity",
        }],
    },
    {
        "slug": "new-jersey", "name": "New Jersey", "svg": "NJ", "cities": "Parsippany, Edison, Princeton, Cherry Hill",
        "hero": "From the serene suburbs of Princeton, Parsippany, and Cherry Hill to the bustling centers of Jersey City and Edison, our centers come together with local partners and volunteers to serve with compassion and purpose. Join hands with SRLC New Jersey to make a difference in your community. Reach out to your local SRLC leaders to get involved!",
        "gallery": 20,
        "stats": [("150+", "Volunteers mobilized"), ("1,700+", "Service hours"), ("40,000+", "Beneficiaries served")],
        "centers": [
            {
                "name": "Edison",
                "sections": [
                    ("Hunger Relief", "Our Edison volunteers support families in need through recurring food drives and meal distributions. By donating pantry staples and preparing lunch bags filled with sandwiches, fruit, and juice, these efforts help ensure access to nourishing meals for households facing food insecurity."),
                    ("Education &amp; Community Support", "In addition to food relief, volunteers organize Classroom of Change drives to provide children with essential supplies and donate hygiene kits, toys, and books to patients in local hospitals. Clothing and blanket drives further extend care across the community, helping uplift families while reinforcing a steady commitment to dignity and support."),
                ],
                "contact": ("Chintan Sheth", "edison@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Cherry Hill",
                "sections": [
                    ("Hunger Relief", "Our Cherry Hill volunteers regularly prepare and serve meals while hosting community lunches for individuals experiencing homelessness at local shelters and churches. These efforts help provide nourishment and consistent care to those facing food insecurity across the community."),
                    ("Education &amp; Community Support", "In addition to meal service, volunteers participate in neighborhood cleanups and organize donation drives that provide clothing, jackets, and hygiene items to families in need. The Cherry Hill team also supports education by delivering backpacks and school supplies through the Center for Family Services, helping equip students for a successful school year."),
                ],
                "contact": ("Ketki Shah", "cherryhill@srlc-usa.org", "email"),
                "partners": "Cathedral Kitchen, St. Joseph&rsquo;s, Asbury, Center for Family Services",
            },
            {
                "name": "Princeton",
                "sections": [
                    ("Hunger Relief", "Our Princeton volunteers support local families through ongoing hunger relief efforts, preparing and distributing essential food items to individuals facing food insecurity. Working in partnership with RISE Food Pantry, these initiatives help provide consistent nourishment while addressing immediate community needs."),
                    ("Education &amp; Community Support", "In addition to food relief, volunteers organize Classroom of Change drives at Klockner Elementary School to help students begin the year with essential supplies. The Princeton team also leads clothing and essentials drives, donating warm clothing, shoes, scarves, and blankets to families supported by HomeFront NJ, helping uplift vulnerable households with dignity and care."),
                ],
                "contact": ("Ketan &amp; Bhavna Ravani", "princeton@srmd.org", "email"),
                "partners": "RISE, HomeFront",
            },
            {
                "name": "Parsippany",
                "sections": [
                    ("Hunger Relief", "Our Parsippany volunteers regularly support families facing food insecurity through recurring food distributions and community partnerships. Working with local delis, volunteers collect and donate hundreds of bagels and essential food items to nearby shelters and households in need."),
                    ("Community Support", "In addition to local efforts, the Parsippany team partners with corporate groups such as AIG to lead large-scale food drives that bring together dozens of volunteers. These initiatives help assemble and distribute essential supplies while strengthening community bonds and reinforcing a shared commitment to service and compassion."),
                ],
                "contact": ("Vikas Shah", "parsippany@srlc-usa.org", "email"),
                "partners": None,
            },
        ],
    },
    {
        "slug": "new-york", "name": "New York", "svg": "NY", "cities": "Long Island, Queens, Manhattan",
        # Newly written per the doc instruction (no hero on the live page). Flag for Naman.
        "hero": "From Long Island to Queens and Manhattan, our New York centers bring volunteers together to nourish neighbors, support students, and stand with families navigating hard seasons. To get involved, connect with your local SRLC leaders!",
        "gallery": 5,
        "stats": [("150+", "Volunteers mobilized"), ("1,800+", "Service hours"), ("52,000+", "Lives impacted")],
        "centers": [
            {
                "name": "Long Island",
                "sections": [
                    ("Hunger Relief", "Across Nassau and Suffolk counties, Long Island volunteers regularly gather and deliver fresh food and pantry staples to support families facing food insecurity. Working with partners such as Ronald McDonald House Charities, Soup to Nuts Soup Kitchen, The Interfaith Nutrition Network, Pax Christi Hospitality Center, Faith Mission Food Pantry, and Tri Community &amp; Youth Agency, these efforts help keep community kitchens stocked and households supported."),
                    ("Education &amp; Community Support", "In addition to food relief, volunteers lead Classroom of Change and mid-year drives that distribute backpacks and school supply kits to local schools and youth organizations. Support also extends to seniors and patients through meal deliveries, comfort-item donations to hospitals, and wellness-focused community programs, helping strengthen care and connection across Long Island."),
                ],
                "contact": ("Dharmendra Mehta", "longisland@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Manhattan",
                "sections": [
                    ("Hunger Relief &amp; Essential Support", "Our Manhattan volunteers assemble and deliver warm clothing and essential items to support children and families facing immediate need. Working in coordination with the NYC Mayor&rsquo;s Office, these efforts help ensure that newly arrived and immigrant households receive timely, dignified assistance."),
                    ("Community Care", "Through focused distribution efforts, volunteers help provide stability and comfort to families navigating challenging transitions. These initiatives reinforce Manhattan&rsquo;s commitment to compassionate service while addressing essential needs with care and respect."),
                ],
                "contact": ("Parth Kamdar", "newyork.youth@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Queens",
                "sections": [
                    ("Hunger Relief", "Queens volunteers regularly prepare and distribute hearty meals and care packs to support families facing food insecurity. Partnering with organizations such as Ronald McDonald House Charities and Commonpoint Queens, these efforts help deliver ready-to-eat meals, fresh fruit, and pantry staples to local households."),
                    ("Community Support", "In addition to meal distribution, service days bring volunteers together with partners like Sairam Narayana Seva to expand outreach across the borough. Through collaboration and consistent service, the Queens team helps strengthen community connections while extending care to those in need."),
                ],
                "contact": ("Pramodini Mehta", "queens@srlc-usa.org", "email"),
                "partners": None,
            },
        ],
    },
    {
        "slug": "pennsylvania", "name": "Pennsylvania", "svg": "PA", "cities": "East Stroudsburg, Philadelphia",
        # Newly written per the doc instruction (no hero on the live page). Flag for Naman.
        "hero": "From the Pocono foothills of East Stroudsburg to the historic streets of Philadelphia, our Pennsylvania centers keep pantry shelves stocked, students supplied, and families supported through every season. To get involved, connect with your local SRLC leaders!",
        "gallery": 5,
        "stats": [("1,000+", "Volunteers mobilized"), ("200+", "Service hours"), ("4,000+", "Lives impacted")],
        "centers": [
            {
                "name": "East Stroudsburg",
                "sections": [
                    ("Food Security &amp; Pantry Support", "Near the Shrimad Rajchandra Spiritual Center, volunteers built a reliable rhythm of pantry support: preparing PB&amp;J materials, gathering bakery items (including bagels donated by a local deli), and delivering staples to Christ Episcopal Church Food Pantry, East Stroudsburg Salvation Army, Stroudsburg Wesleyan Pantry &amp; SK, and Swiftwater Eglise Evangelique Renaissance Pantry. Each visit kept shelves a bit fuller and spirits a bit lighter."),
                    ("Hygiene &amp; Clothing Essentials", "Care took practical form with hygiene kits and new clothing assembled and distributed through trusted local channels. Partners included Christ Episcopal Church Food Pantry and Violette Stand for the Children Home, ensuring families received exactly the kind of everyday essentials that ease the month."),
                    ("Classroom of Change &amp; Youth Support", "Volunteers readied kids for learning with school kits, sling bags, and essential kits shared through Monroe County Children Youth and Foster Care and Christ Episcopal Church, supporting students in neighborhoods surrounding the ashram."),
                ],
                "contact": None,
                "partners": None,
            },
            {
                "name": "Philadelphia",
                "sections": [
                    ("Hunger Relief", "Our Philadelphia volunteers focus on steady, reliable nourishment to support families facing food insecurity. Through PB&amp;J donations and pantry staple distributions, volunteers partner with organizations such as Somerset County Food Pantry and the People&rsquo;s Pantry of Malvern to ensure neighbors have access to consistent, nourishing meals."),
                    ("Education &amp; Community Support", "In addition to food relief, volunteers prepare and distribute school bags and essential supplies for students, including deliveries to Dr. Tanner G. Duckrey Public School and Monroe County Children &amp; Youth and Foster Care. The team also supports families through donation drives benefiting the Coatesville Community Youth and Women&rsquo;s Alliance, helping ensure household essentials remain within reach during challenging times."),
                ],
                "contact": ("Priti Jain", "philadelphia@srlc-usa.org", "email"),
                "partners": None,
            },
        ],
    },
    {
        "slug": "texas", "name": "Texas", "svg": "TX", "cities": "Dallas, Austin, Houston",
        "hero": "From the cultural vibrancy of Dallas to the creative energy of Austin and the welcoming neighborhoods of Houston, our centers weave compassion into the fabric of Texas life. Volunteers of all ages roll up their sleeves, prepare meals, and uplift underserved families. To join in, connect with your local SRLC leaders!",
        "gallery": 8,
        "stats": [("300+", "Volunteers mobilized"), ("1,150+", "Service hours"), ("10,000+", "Beneficiaries served")],
        "centers": [
            {
                "name": "Dallas",
                "sections": [
                    ("Hunger Relief", "In the heart of North Texas, our Dallas team organizes food drives and grocery distributions to support families facing food insecurity. Volunteers work closely with local partners to ensure that meals and essential items reach vulnerable households across the community."),
                    ("Community Engagement", "Partnering with organizations such as Community Partners of Dallas, Dallas Life, and Malvern Elementary School, our volunteers bring families and youth together through service. These efforts combine hands-on support with values-based activities that strengthen compassion and foster a shared spirit of service."),
                ],
                "contact": ("Dhaval Shah", "dallas@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Austin",
                "sections": [
                    ("Hunger Relief", "Our Austin volunteers regularly prepare and deliver food packs and lunch bags to shelters, schools, and local families in need. These consistent efforts help provide nourishment while supporting community members experiencing food insecurity."),
                    ("Youth &amp; Family Support", "Families and young volunteers often serve side by side at partner locations such as Texas Baptist Children&rsquo;s Home, as well as schools, including McBee Elementary and Round Rock High School. Through these ongoing initiatives, volunteers help instill compassion, responsibility, and service from an early age."),
                ],
                "contact": ("Nirmal Khanderia", "austin@srlc-usa.org", "email"),
                "partners": None,
            },
            {
                "name": "Houston",
                "sections": [
                    ("Hunger Relief", "In Houston, families gather in community kitchens to donate ingredients and prepare warm meals for neighbors experiencing hunger. These efforts help ensure that individuals and families have access to nourishing food during times of need."),
                    ("Community Partnerships", "Working alongside partners such as Loaves and Fishes Soup Kitchen and Pantry and Fort Bend ISD, our Houston volunteers support both food relief and educational needs. Through shared service, these initiatives build resilience, strengthen community bonds, and promote dignity and care."),
                ],
                "contact": ("Naresh Shah", "houston@srlc-usa.org", "email"),
                "partners": None,
            },
        ],
    },
    {
        "slug": "washington", "name": "Washington", "svg": "WA", "cities": "Seattle",
        "hero": "In Washington, SRLC&rsquo;s Seattle volunteers are dedicated to compassion, stepping in where the need is greatest. From gathering essential supplies to sharing snack boxes with shelters, their work is guided by a simple but powerful goal: making life a little brighter and easier for neighbors experiencing hardship.",
        "gallery": 5,
        "stats": [("20+", "Volunteers mobilized"), ("Seattle", "Eastside communities served")],
        "centers": [{
            "name": "Seattle",
            "sections": [
                ("Hunger Relief", "Our Seattle volunteers assemble and deliver snack boxes and essential food items to local organizations serving families and individuals in need throughout the Eastside region. These efforts help ensure that community members facing food insecurity receive consistent access to nourishing meals."),
                ("Community Support", "In partnership with shelters such as New Bethlehem Day Center and The Sophia Way, our Seattle team supports individuals experiencing homelessness with both food and care. Through regular service efforts, volunteers help foster dignity, stability, and a sense of support during challenging times."),
            ],
            "contact": ("Jayesh Khandhar", "(425) 753-2900", "phone"),
            "partners": "New Bethlehem Day Center, The Sophia Way",
        }],
    },
    {
        "slug": "washington-dc", "name": "Washington, D.C.", "svg": "DC", "cities": "Washington, D.C.",
        "hero": "From the nation&rsquo;s capital, our Washington, D.C. volunteers show up for neighbors through steady food relief, educational aid drives, environmental stewardship, and essential needs distributions.",
        "gallery": 5,
        "stats": [("40+", "Volunteers mobilized"), ("300+", "Service hours"), ("2,600+", "Lives impacted")],
        "centers": [{
            "name": "Washington, D.C.",
            "sections": [
                ("Hunger Relief", "Our Washington, D.C. volunteers host monthly service events where families prepare and deliver sandwiches to individuals experiencing food insecurity. Working in partnership with organizations such as Martha&rsquo;s Table, Artemis House, Christ House, Friendship Place &ndash; La Casa, and the Loudoun Homeless Shelter, these efforts help ensure consistent access to nourishing meals for those in need."),
                ("Education &amp; Essential Support", "In addition to food relief, volunteers assemble school supply kits for Title I schools in Fairfax County, helping students begin the school year with essential materials. The D.C. team also organizes annual hygiene kit drives, collecting personal care items that are distributed through local shelters and service organizations to support individuals experiencing homelessness with dignity and care."),
            ],
            "contact": ("Bella Desai", "washingtondc@srlc-usa.org", "email"),
            "partners": None,
        }],
    },
]

CAMPAIGNS = [
    {
        "name": "Classroom of Change",
        "img_label": "Classroom of Change distribution photo &middot; Media Bank",
        "body": "Access to supplies can transform a student&rsquo;s journey. Each year, SRLC USA donors and volunteers unite across the country to pack and distribute backpacks, learning materials, and digital tools to Title 1 schools, leveling the playing field and igniting hope in classrooms.",
        "cta": "Support a Student Today",
    },
    {
        "name": "Giving Tuesday",
        "img_label": "Volunteer group photo &middot; Media Bank",
        "body": "SRLC USA&rsquo;s largest annual campaign, channeling donor support into our most pertinent global initiatives. From healthcare to educational care to direct aid, your gift reaches the underserved communities that need it most, in the United States and around the world.",
        "cta": "Help Provide Care",
    },
    {
        "name": "Meals of Love and Care",
        "img_label": "Food packing photo &middot; Media Bank",
        "body": "Year-round, SRLC USA centers across the country pack and distribute food in partnership with local food banks and pantries, putting meals in the hands of families, seniors, and neighbors facing food insecurity right where they live.",
        "cta": "Share Compassion",
    },
]

US_HERO_BODY = ("SRLC operates across 25+ cities in the United States, bringing compassionate "
                "service and community-driven initiatives to thousands of lives. Explore our work "
                "by state and find out how you can get involved near you.")
