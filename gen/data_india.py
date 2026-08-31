"""India hub + institute pages. Hub descriptions are the approved verbatim set
from the India hub tab. Detail-page intros/metas come from the Document C specs
(Aug 20, Parshva) for Hospital/Jivamaitridham/COEW and the Riyan tabs for
Gurukul/SRSDC. Long approved descriptions for Hospital/Jivamaitridham/COEW are
PENDING; their pages carry an empty slot per the build rules."""

INSTITUTES = [
    {
        "slug": "hospital-and-research-center",
        "name": "Shrimad Rajchandra Hospital and Research Center",
        "tag": "Hospital &amp; Research Center", "care": "Health Care",
        "care_url": "/our-work/10-care-program/health-care/",
        "desc": "A NABH-accredited, 250-bed, multi-specialty charitable hospital in Dharampur, with 20+ departments and specialties, including a Neonatal Intensive Care Unit and District Early Intervention Center. The hospital was virtually inaugurated by Shri Narendra Modi, Hon&rsquo;ble Prime Minister of India, in 2022.",
        "intro": "In a region where quality healthcare was once a long journey away, this hospital brings it next door.",
        "desc_full": False,
        "cta": "Give to This Work",
        "img": "Establishing shot with one human element for scale. Not an empty building. Media Bank.",
        "meta_title": "Shrimad Rajchandra Hospital and Research Center | SRLC USA",
        "meta_desc": "A multispecialty hospital in Dharampur, India, where quality care is no longer a long journey away. See how it works and how to support it. SRLC USA.",
    },
    {
        "slug": "vidyapeeth",
        "name": "Shrimad Rajchandra Vidyapeeth",
        "tag": "Science College", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "The first science college across 238 villages of South Gujarat, offering B.Sc., B.Voc., M.Sc., PGDMLT, and certificate courses, paired with holistic learning and career support.",
        "full_page": True,
        "img": "Students working at lab benches in a science laboratory. Warm, energetic light. Media Bank.",
    },
    {
        "slug": "gurukul",
        "name": "Shrimad Rajchandra Gurukul",
        "tag": "High School", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "A progressive secondary and higher-secondary school for underserved students.",
        "intro": "A school built on the belief that every child deserves excellent teachers and a safe place to grow.",
        "desc_full": True,
        "cta": "Give to This Work",
        "img": "Exterior or courtyard shot plus one human moment: students in a classroom or activity, active and engaged. Media Bank.",
        "meta_title": "Shrimad Rajchandra Gurukul | Rural School India | SRLC USA",
        "meta_desc": "A progressive secondary and higher-secondary school for underserved students in South Gujarat. Support through SRLC USA&rsquo;s Educational Care program.",
    },
    {
        "slug": "skill-development-center",
        "name": "Shrimad Rajchandra Skill Development Center",
        "tag": "Skill Development Center", "care": "Educational Care",
        "care_url": "/our-work/10-care-program/educational-care/",
        "desc": "A hub for relevant, technical courses preparing a new generation to enter the workforce.",
        "intro": "Practical training that turns ambition into a livelihood.",
        "desc_full": True,
        "cta": "Give to This Work",
        "img": "Exterior shot of the center plus one human moment: hands mastering a trade, a student at a workstation. Media Bank.",
        "meta_title": "Shrimad Rajchandra Skill Development Center | SRLC USA",
        "meta_desc": "A hub for technical vocational training for tribal youth in South Gujarat. Preparing a new generation to enter the workforce. Support through SRLC USA.",
    },
    {
        "slug": "jivamaitridham",
        "name": "Shrimad Rajchandra Jivamaitridham",
        "tag": "Animal Sanctuary", "care": "Animal Care",
        "care_url": "/our-work/10-care-program/animal-care/",
        "desc": "An upcoming animal sanctuary comprising a 150-ward animal hospital, veterinary college, ahimsa experience center, and animal shelters.",
        "intro": "A sanctuary where injured and abandoned animals are treated, sheltered, and given a life of dignity.",
        "desc_full": False,
        "cta": "Give to This Work",
        "img": "Establishing shot with one human element for scale. No animals in visible distress. Media Bank.",
        "meta_title": "Shrimad Rajchandra Jivamaitridham | SRLC USA",
        "meta_desc": "An animal care campus in Dharampur, India, where injured and abandoned animals are treated, sheltered, and given a life of dignity. See the work. SRLC USA.",
    },
    {
        "slug": "center-of-excellence-for-women",
        "name": "Shrimad Rajchandra Center of Excellence for Women",
        "tag": "Women&rsquo;s Empowerment", "care": "Woman Care",
        "care_url": "/our-work/10-care-program/woman-care/",
        "desc": "A state-of-the-art facility dedicated to the holistic development and empowerment of tribal women, reaching 10,000&ndash;12,000 women annually through an integrated program spanning awareness, social security, skilling, and leadership.",
        "intro": "Skills, artisanship, and steady income for women building independence.",
        "desc_full": False,
        "cta": "Give to This Work",
        "img": "Establishing shot with one human element for scale. Artisans at work need written consent. Media Bank.",
        "meta_title": "Shrimad Rajchandra Center of Excellence for Women | SRLC USA",
        "meta_desc": "A center in Dharampur, India, where women build skills, artisanship, and steady income. See how the work runs and how to support it. SRLC USA.",
    },
]

INDIA_INTRO = "Six permanent institutes in India, each built around a specific need."

SRV = {
    "h1": "The First Science College Across 238 Villages",
    "sub": "Across 238 villages in South Gujarat, young people who dreamed of a science career had nowhere close to go. Shrimad Rajchandra Vidyapeeth changed that in 2016. Your support keeps the doors open.",
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
    # Not rendered (Naman, Aug 24): global statistics appear on the homepage and
    # Our Impact only. Kept for reference; the tab's stat flag is still open.
    "impact_h2": "Your gift joins a network that has reached millions.",
    "impact": [("3.28M+", "students reached globally through Educational Care"), ("33M+", "lives touched globally across all SRLC programs")],
    "close_h2": "Be the reason a student graduates.",
    "close": "When a young person in Dharampur, India walks into a science lab for the first time, or earns a degree their family never had access to before, that is the outcome of your gift. SRV has made that possible for students across 238 villages. Your support makes it possible for the next generation.",
    "cta": "Support Shrimad Rajchandra Vidyapeeth",
    "title": "Shrimad Rajchandra Vidyapeeth | Educational Care | SRLC USA",
    "desc": "Support the first science college serving 238 villages in South Gujarat. SRLC USA funds education that changes lives. Give today.",
}
