"""India hub + institute pages. Approved descriptions verbatim, Center spelling.
Option A/B choices from the doc are resolved to Option A (recorded for Naman's review).
Institute URLs standardized under /our-work/india/ (doc candidates varied; flagged)."""

INSTITUTES = [
    {
        "slug": "hospital-and-research-center",
        "name": "Shrimad Rajchandra Hospital and Research Center",
        "abbr": "SRHRC", "tag": "Hospital &amp; Research Center", "care": "Health Care",
        "care_url": "/our-work/10-care-program/health-care/",
        "desc": "A NABH-accredited, 250-bed, multi-specialty charitable hospital in Dharampur, with 20+ departments and specialties, including a Neonatal Intensive Care Unit and District Early Intervention Center. The hospital was virtually inaugurated by Shri Narendra Modi, Hon&rsquo;ble Prime Minister of India, in 2022.",
        "intro": "Care of the highest standard, for the families least able to reach it.",
        "extra": "The hospital anchors SRLC&rsquo;s Health Care work in South Gujarat: primary, secondary, and tertiary treatment at no cost or highly subsidized rates, extended by medical camps and outreach programs that carry care into the surrounding villages. It earned accreditation from the National Accreditation Board for Hospitals and Healthcare Providers (NABH) within its first year of operation, and its surgeons performed the region&rsquo;s first open-heart cardiothoracic surgery.",
        "img": "Hospital campus &middot; Media Bank",
    },
    {
        "slug": "vidyapeeth",
        "name": "Shrimad Rajchandra Vidyapeeth",
        "abbr": "SRV", "tag": "Science College", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "The first science college across 238 villages of South Gujarat, offering B.Sc., B.Voc., M.Sc., PGDMLT, and certificate courses, paired with holistic learning and career support.",
        "full_page": True,
        "img": "Students in the science laboratory &middot; Media Bank",
    },
    {
        "slug": "gurukul",
        "name": "Shrimad Rajchandra Gurukul",
        "abbr": "SRG", "tag": "High School", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "A progressive secondary and higher-secondary school for underserved students.",
        "intro": "A school built on the belief that every child deserves excellent teachers and a safe place to grow.",
        "extra": None,
        "img": "School courtyard and classroom &middot; Media Bank",
        "meta_title": "Shrimad Rajchandra Gurukul | Rural School India | SRLC USA",
        "meta_desc": "A progressive secondary and higher-secondary school for underserved students in South Gujarat. Support through SRLC USA&rsquo;s Educational Care program.",
    },
    {
        "slug": "skill-development-center",
        "name": "Shrimad Rajchandra Skill Development Center",
        "abbr": "SRSDC", "tag": "Skill Development Center", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "A hub for relevant, technical courses preparing a new generation to enter the workforce.",
        "intro": "Practical training that turns ambition into a livelihood.",
        "extra": None,
        "img": "Hands mastering a trade &middot; Media Bank",
        "meta_title": "Shrimad Rajchandra Skill Development Center | SRLC USA",
        "meta_desc": "A hub for technical vocational training for tribal youth in South Gujarat. Preparing a new generation to enter the workforce. Support through SRLC USA.",
    },
    {
        "slug": "jivamaitridham",
        "name": "Shrimad Rajchandra Jivamaitridham",
        "abbr": "SRJMD", "tag": "Animal Sanctuary", "care": "Animal Care",
        "care_url": "/our-work/10-care-program/animal-care/",
        "desc": "An upcoming animal sanctuary comprising a 150-ward animal hospital, veterinary college, ahimsa experience center, and animal shelters.",
        "intro": "Compassion extended to every life, beginning with the ones who cannot ask.",
        "extra": "Satellite clinics and animal outreach programs extend rescue and treatment into the surrounding region, alongside the sanctuary&rsquo;s hospital wards and shelters.",
        "img": "An animal receiving care &middot; Media Bank",
    },
    {
        "slug": "center-of-excellence-for-women",
        "name": "Shrimad Rajchandra Sarvamangal Center of Excellence for Women",
        "abbr": "SRCOEW", "tag": "Women&rsquo;s Empowerment", "care": "Woman Care",
        "care_url": "/our-work/10-care-program/woman-care/",
        "desc": "A state-of-the-art facility dedicated to the holistic development and empowerment of tribal women, reaching 10,000&ndash;12,000 women annually through an integrated program spanning awareness, social security, skilling, and leadership.",
        "intro": "Independence built skill by skill, leader by leader.",
        "extra": None,
        "img": "Women in training &middot; Media Bank",
    },
]

INDIA_INTRO = ("Permanent institutions in Dharampur, South Gujarat, each built to serve the "
               "underserved for generations: a charitable hospital, schools and colleges, "
               "vocational training, an animal sanctuary, and a center for the empowerment of women.")

# Vidyapeeth full page content (em dash removed per A4; finance/story sections held)
SRV = {
    "h1": "The First Science College Across 238 Villages",
    "sub": "Across 238 villages in South Gujarat, young people who dreamed of a science career had nowhere close to go. Shrimad Rajchandra Vidyapeeth changed that in 2016. Your support keeps the doors open.",
    "trust": ["501(c)(3) Nonprofit", "3.28M+ Students Reached Globally", "Parent body: UN ECOSOC Special Consultative Status"],
    "need_h2": "Before 2016, a science degree meant leaving home or giving up.",
    "need": [
        "The 238 villages of Dharampur and Kaprada in South Gujarat are home to tens of thousands of young people. For years, if a student there wanted to study science at the undergraduate level, there was no local college to go to. The closest options required leaving the community entirely. For students from families with limited resources, that meant most of them didn&rsquo;t go.",
        "That&rsquo;s the gap Shrimad Rajchandra Vidyapeeth (SRV) was built to close. Dedicated to the community in October 2016 in Dharampur, India, SRV became the first and only science college to serve this entire region.",
    ],
    "programs_h2": "A full path from enrollment to career.",
    "programs_intro": "SRV offers a range of science degrees and professional programs built around students who are the first in their families to reach higher education.",
    "programs": [
        ("Bachelor of Science (B.Sc.)", "A three-year undergraduate degree in Chemistry, Microbiology, Botany, or Mathematics."),
        ("Master of Science (M.Sc.)", "A two-year postgraduate degree in Chemistry or Microbiology for students who want to go further in their field."),
        ("B.Voc. in Industrial Management", "A vocational degree that connects science training directly to employment in the region&rsquo;s industries."),
        ("PGDMLT", "A professional credential preparing graduates for careers in diagnostics and clinical laboratory care."),
        ("Certificate Courses", "Specialized programs that build specific career skills alongside or after a degree."),
    ],
    "support_intro": "Getting into college is only part of the challenge for students who have had limited academic preparation. SRV pairs every program with bridge courses for students who need academic reinforcement, English language coaching, personal counseling, and career placement support through a dedicated Placement Cell. The Placement Cell works directly with regional employers, manages career counseling and professional skills training, and stays connected with graduates through an alumni network after they leave campus. SRV is the first science college in Gujarat to earn both ISO 9001 and ISO 29990 certifications.",
    "pillars": [
        ("Academic Support", "Bridge courses for students who need academic reinforcement."),
        ("Language Coaching", "English language coaching alongside every program."),
        ("Career Placement", "A dedicated Placement Cell working directly with regional employers."),
        ("Alumni Network", "Staying connected with graduates after they leave campus."),
    ],
    "impact_h2": "Your gift joins a network that has reached millions.",
    "impact": [("3.28M+", "students reached globally through Educational Care"), ("33M+", "lives touched globally across all SRLC programs")],
    "close_h2": "Be the reason a student graduates.",
    "close": "When a young person in Dharampur, India walks into a science lab for the first time, or earns a degree their family never had access to before, that is the outcome of your gift. SRV has made that possible for students across 238 villages. Your support makes it possible for the next generation.",
    "cta": "Support Shrimad Rajchandra Vidyapeeth",
    "title": "Shrimad Rajchandra Vidyapeeth | Educational Care | SRLC USA",
    "desc": "Support the first science college serving 238 villages in South Gujarat. SRLC USA funds education that changes lives. Give today.",
}
