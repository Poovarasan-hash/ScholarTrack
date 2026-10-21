"""
ScholarTrack - Real Scholarship Seeder
Populates MySQL database with genuine, prestigious, and active scholarships
complete with real official application portal URLs.
"""

import sys
import json
from pathlib import Path
from datetime import date

backend_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(backend_dir))

from models.database import execute_query, fetch_all, fetch_one

REAL_SOURCES = [
    {
        "source_name": "National Scholarship Portal (NSP) - Govt. of India",
        "source_url": "https://scholarships.gov.in/",
        "source_type": "government",
        "is_approved": 1
    },
    {
        "source_name": "Reliance Foundation Scholarships Portal",
        "source_url": "https://www.scholarships.reliancefoundation.org/",
        "source_type": "foundation",
        "is_approved": 1
    },
    {
        "source_name": "Tata Trusts Education Grants Portal",
        "source_url": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "source_type": "foundation",
        "is_approved": 1
    },
    {
        "source_name": "Department of Science and Technology (DST) - INSPIRE Portal",
        "source_url": "https://online-inspire.gov.in/",
        "source_type": "government",
        "is_approved": 1
    },
    {
        "source_name": "AICTE India Scholarship Bureau",
        "source_url": "https://www.aicte-india.org/schemes/students-development-schemes",
        "source_type": "government",
        "is_approved": 1
    },
    {
        "source_name": "HDFC Bank Parivartan ECSS Portal (Buddy4Study)",
        "source_url": "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme",
        "source_type": "foundation",
        "is_approved": 1
    },
    {
        "source_name": "ONGC Foundation Scholar Portal",
        "source_url": "https://ongcscholar.org/",
        "source_type": "foundation",
        "is_approved": 1
    },
    {
        "source_name": "Sitaram Jindal Foundation Official Portal",
        "source_url": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "source_type": "foundation",
        "is_approved": 1
    },
    {
        "source_name": "Chevening UK Government Scholarships Portal",
        "source_url": "https://www.chevening.org/scholarship/india/",
        "source_type": "government",
        "is_approved": 1
    }
]

REAL_SCHOLARSHIPS = [
    {
        "source_url": "https://scholarships.gov.in/",
        "external_id": "NSP-CSSS-01",
        "title": "Central Sector Scheme of Scholarships for College and University Students (PM-USP)",
        "provider": "Department of Higher Education, Ministry of Education, Govt. of India",
        "description": "Financial assistance for meritorious students from low-income families to meet day-to-day expenses while pursuing higher education (regular degree/professional courses).",
        "scholarship_type": "government",
        "education_level": "undergraduate",
        "eligible_courses": "All Regular Undergraduate (B.Tech, MBBS, B.Sc, B.Com, BA) and Postgraduate degree programmes.",
        "eligible_states": ["All India"],
        "eligible_categories": ["General", "OBC", "SC", "ST", "EWS"],
        "minimum_marks": 80.00,
        "maximum_family_income": 450000.00,
        "amount_min": 12000.00,
        "amount_max": 20000.00,
        "deadline": "2026-11-30",
        "official_url": "https://scholarships.gov.in/",
        "application_url": "https://scholarships.gov.in/",
        "eligibility_details": "Above 80th percentile in relevant stream in Class 12 board exam. Enrolled in regular degree courses recognized by AICTE/UGC/MCI.",
        "required_documents": ["Class 12 Marksheet", "Income Certificate (< 4.5 Lakh)", "Aadhaar Card", "College Bonafide Certificate", "Bank Passbook"],
        "is_verified": 1
    },
    {
        "source_url": "https://www.scholarships.reliancefoundation.org/",
        "external_id": "REL-UG-2026",
        "title": "Reliance Foundation Undergraduate Scholarships",
        "provider": "Reliance Foundation",
        "description": "Prestigious scholarship supporting meritorious first-year undergraduate students across all fields of study in India, with special preference for girls and differently-abled students.",
        "scholarship_type": "merit",
        "education_level": "undergraduate",
        "eligible_courses": "Full-time 1st-year regular Undergraduate degree in any stream (Engineering, Sciences, Commerce, Arts, Law, Medicine).",
        "eligible_states": ["All India"],
        "eligible_categories": ["All Categories"],
        "minimum_marks": 60.00,
        "maximum_family_income": 1500000.00,
        "amount_min": 50000.00,
        "amount_max": 200000.00,
        "deadline": "2026-10-31",
        "official_url": "https://www.scholarships.reliancefoundation.org/UG_Scholarship.aspx",
        "application_url": "https://www.scholarships.reliancefoundation.org/UG_Scholarship.aspx",
        "eligibility_details": "First-year full-time undergraduate students with minimum 60% in Class 12. Household income preferably under Rs. 2.5 Lakh (up to 15 Lakh eligible).",
        "required_documents": ["Class 10 & 12 Marksheets", "College Admission Proof", "Household Income Proof", "Aadhaar Card"],
        "is_verified": 1
    },
    {
        "source_url": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "external_id": "TATA-MED-01",
        "title": "Tata Trusts Medical and Healthcare Education Grants",
        "provider": "Tata Trusts",
        "description": "Tuition fee grants for meritorious students enrolled in recognized medical and healthcare undergraduate or postgraduate programmes in India.",
        "scholarship_type": "private",
        "education_level": "undergraduate",
        "eligible_courses": "MBBS, BDS, B.Pharm, B.Sc Nursing, MD, MS, MDS.",
        "eligible_states": ["All India"],
        "eligible_categories": ["All Categories"],
        "minimum_marks": 65.00,
        "maximum_family_income": 600000.00,
        "amount_min": 30000.00,
        "amount_max": 100000.00,
        "deadline": "2026-11-15",
        "official_url": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "application_url": "https://www.tatatrusts.org/our-work/individual-grants-programme/education-grants",
        "eligibility_details": "Undergraduate medical students from 2nd year onwards with consistently strong academic standing and financial need.",
        "required_documents": ["College Fee Receipt", "Annual Academic Marksheet", "Income Proof", "Identity Document"],
        "is_verified": 1
    },
    {
        "source_url": "https://scholarships.gov.in/",
        "external_id": "AICTE-PRAGATI-01",
        "title": "AICTE Pragati Scholarship Scheme for Girl Students",
        "provider": "All India Council for Technical Education (AICTE)",
        "description": "Government scholarship empowering young women pursuing technical diploma or degree education in AICTE-approved institutions across India.",
        "scholarship_type": "government",
        "education_level": "undergraduate",
        "eligible_courses": "Technical Degree / Diploma courses (B.E., B.Tech, Polytechnic) in AICTE-approved colleges.",
        "eligible_states": ["All India"],
        "eligible_categories": ["Girls - All Categories"],
        "minimum_marks": 50.00,
        "maximum_family_income": 800000.00,
        "amount_min": 50000.00,
        "amount_max": 50000.00,
        "deadline": "2026-12-31",
        "official_url": "https://scholarships.gov.in/",
        "application_url": "https://scholarships.gov.in/",
        "eligibility_details": "Female students admitted to 1st year degree or 2nd year lateral entry in AICTE-approved technical institutions. Maximum 2 girls per family.",
        "required_documents": ["Admission Proof via Centralized Counselling", "Tuition Fee Receipt", "Family Income Certificate", "Aadhaar Card"],
        "is_verified": 1
    },
    {
        "source_url": "https://online-inspire.gov.in/",
        "external_id": "DST-INSPIRE-SHE",
        "title": "INSPIRE Scholarship for Higher Education (SHE)",
        "provider": "Department of Science and Technology (DST), Govt. of India",
        "description": "Prestigious scholarship offered to top rankers in Class 12 board examinations pursuing Natural and Basic Sciences at B.Sc., B.S., and Int. M.Sc. levels.",
        "scholarship_type": "research",
        "education_level": "undergraduate",
        "eligible_courses": "B.Sc., B.S., Int. M.Sc. in Physics, Chemistry, Mathematics, Biology, Statistics, Geology, Astrophysics.",
        "eligible_states": ["All India"],
        "eligible_categories": ["Merit - All Categories"],
        "minimum_marks": 85.00,
        "maximum_family_income": None,
        "amount_min": 60000.00,
        "amount_max": 80000.00,
        "deadline": "2026-11-20",
        "official_url": "https://online-inspire.gov.in/",
        "application_url": "https://online-inspire.gov.in/",
        "eligibility_details": "Top 1% rank in Class 12 board exams or top 10,000 in JEE/NEET enrolled in Basic Science courses.",
        "required_documents": ["Class 12 Marksheet & Certificate", "College Bonafide Certificate", "SBI Bank Account Details", "Aadhaar Card"],
        "is_verified": 1
    },
    {
        "source_url": "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme",
        "external_id": "HDFC-ECSS-2026",
        "title": "HDFC Bank Parivartan's Educational Crisis Support Scholarship (ECSS)",
        "provider": "HDFC Bank",
        "description": "Need-cum-merit scholarship for students facing personal or economic crisis to ensure they do not drop out of school, college, or diploma programmes.",
        "scholarship_type": "need",
        "education_level": "undergraduate",
        "eligible_courses": "General & Professional Undergraduate degree programmes (B.Com, B.Sc, BA, B.Tech, MBBS, BCA).",
        "eligible_states": ["All India"],
        "eligible_categories": ["All Categories"],
        "minimum_marks": 55.00,
        "maximum_family_income": 250000.00,
        "amount_min": 35000.00,
        "amount_max": 75000.00,
        "deadline": "2026-10-31",
        "official_url": "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme",
        "application_url": "https://www.buddy4study.com/page/hdfc-bank-parivartans-ecss-programme",
        "eligibility_details": "Students facing financial crisis with family income under 2.5 LPA who passed previous qualifying exam with 55% or higher.",
        "required_documents": ["Previous Year Marksheet", "Income Certificate / BPL Card", "Admission Letter / ID Card", "Proof of Crisis (if any)"],
        "is_verified": 1
    },
    {
        "source_url": "https://ongcscholar.org/",
        "external_id": "ONGC-SCH-2026",
        "title": "ONGC Foundation Scholarship Scheme for Meritorious Students",
        "provider": "ONGC Foundation",
        "description": "Exclusive scholarship supporting meritorious students pursuing Engineering, MBBS, MBA, and Master's in Geophysics/Geology.",
        "scholarship_type": "merit",
        "education_level": "undergraduate",
        "eligible_courses": "1st year B.Tech, MBBS, MBA, M.Sc. Geology/Geophysics.",
        "eligible_states": ["All India"],
        "eligible_categories": ["SC", "ST", "OBC", "General-EWS"],
        "minimum_marks": 60.00,
        "maximum_family_income": 200000.00,
        "amount_min": 48000.00,
        "amount_max": 48000.00,
        "deadline": "2026-12-15",
        "official_url": "https://ongcscholar.org/",
        "application_url": "https://ongcscholar.org/",
        "eligibility_details": "First year full-time regular students with minimum 60% in Class 12 (or graduation for PG courses) with family income under 2 LPA.",
        "required_documents": ["Caste Certificate", "Income Certificate", "Class 10 & 12 Marksheets", "College Fee Receipt", "Bank Passbook"],
        "is_verified": 1
    },
    {
        "source_url": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "external_id": "SJF-ANNUAL-01",
        "title": "Sitaram Jindal Foundation Educational Scholarship",
        "provider": "Sitaram Jindal Foundation",
        "description": "Scholarships for underprivileged and meritorious students pursuing higher secondary, diploma, ITI, undergraduate, and postgraduate courses.",
        "scholarship_type": "private",
        "education_level": "diploma",
        "eligible_courses": "Diploma, Polytechnic, B.Sc, B.Com, BA, BCA, BBA, B.Tech.",
        "eligible_states": ["All India"],
        "eligible_categories": ["All Categories"],
        "minimum_marks": 60.00,
        "maximum_family_income": 400000.00,
        "amount_min": 14000.00,
        "amount_max": 38400.00,
        "deadline": "2026-12-31",
        "official_url": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "application_url": "https://www.sitaramjindalfoundation.org/scholarships.php",
        "eligibility_details": "Enrolled in recognized schools, polytechnics, or colleges. Marks: Boys >= 65%, Girls >= 60%.",
        "required_documents": ["Marksheet of Last Exam", "Income Certificate", "Fee Receipt", "Bonafide Certificate"],
        "is_verified": 1
    },
    {
        "source_url": "https://scholarships.gov.in/",
        "external_id": "NSP-MIN-POSTMATRIC",
        "title": "Post Matric Scholarships Scheme for Minorities",
        "provider": "Ministry of Minority Affairs, Govt. of India",
        "description": "Scholarship awarded to meritorious students from minority communities (Muslim, Christian, Sikh, Buddhist, Jain, Parsi) for higher secondary through doctoral studies.",
        "scholarship_type": "government",
        "education_level": "postgraduate",
        "eligible_courses": "Class 11, 12, ITI, Diploma, Undergraduate, Postgraduate, M.Phil, and Ph.D. degrees.",
        "eligible_states": ["All India"],
        "eligible_categories": ["Minorities"],
        "minimum_marks": 50.00,
        "maximum_family_income": 200000.00,
        "amount_min": 10000.00,
        "amount_max": 30000.00,
        "deadline": "2026-12-20",
        "official_url": "https://scholarships.gov.in/",
        "application_url": "https://scholarships.gov.in/",
        "eligibility_details": "Students from notified minority communities who have secured not less than 50% marks in the previous final examination.",
        "required_documents": ["Self-Declaration of Minority Community", "Previous Exam Marksheet", "Income Certificate", "Aadhaar Card", "Bank Account Details"],
        "is_verified": 1
    },
    {
        "source_url": "https://www.chevening.org/scholarship/india/",
        "external_id": "CHEV-UK-2026",
        "title": "Chevening Scholarships for One-Year Master's in the UK",
        "provider": "Foreign, Commonwealth and Development Office (FCDO), UK Government",
        "description": "Fully-funded scholarship covering tuition fees, living expenses, return flights, and grant allowance for exceptional Indian graduates to pursue a one-year Master's degree in the United Kingdom.",
        "scholarship_type": "merit",
        "education_level": "postgraduate",
        "eligible_courses": "One-year taught Master's degree at any recognized UK university in any subject.",
        "eligible_states": ["All India"],
        "eligible_categories": ["All Categories"],
        "minimum_marks": 60.00,
        "maximum_family_income": None,
        "amount_min": 1500000.00,
        "amount_max": 3500000.00,
        "deadline": "2026-11-05",
        "official_url": "https://www.chevening.org/scholarship/india/",
        "application_url": "https://www.chevening.org/scholarship/india/",
        "eligibility_details": "Undergraduate degree that enables entry to a UK postgraduate course. Minimum 2 years of work experience (equivalent to 2,800 hours).",
        "required_documents": ["University Transcripts & Degree Certificate", "Two Reference Letters", "Three Unconditional UK University Offers", "Valid Indian Passport"],
        "is_verified": 1
    }
]


def seed_database():
    print("Seeding scholarship sources...")
    source_map = {}
    for src in REAL_SOURCES:
        execute_query(
            """
            INSERT INTO scholarship_sources (source_name, source_url, source_type, is_approved, is_active)
            VALUES (%s, %s, %s, %s, 1)
            ON DUPLICATE KEY UPDATE source_name = VALUES(source_name), is_approved = VALUES(is_approved)
            """,
            (src["source_name"], src["source_url"], src["source_type"], src["is_approved"])
        )
        row = fetch_one("SELECT id FROM scholarship_sources WHERE source_url = %s", (src["source_url"],))
        if row:
            source_map[src["source_url"]] = row["id"]

    print(f"Loaded {len(source_map)} sources.")

    print("Seeding real scholarships...")
    inserted = 0
    for sch in REAL_SCHOLARSHIPS:
        src_id = source_map.get(sch["source_url"])
        existing = fetch_one("SELECT id FROM scholarships WHERE external_id = %s", (sch["external_id"],))

        eligible_states_json = json.dumps(sch["eligible_states"])
        eligible_categories_json = json.dumps(sch["eligible_categories"])
        required_docs_json = json.dumps(sch["required_documents"])

        if existing:
            execute_query(
                """
                UPDATE scholarships
                SET title = %s, provider = %s, description = %s, scholarship_type = %s,
                    education_level = %s, eligible_courses = %s, eligible_states = %s,
                    eligible_categories = %s, minimum_marks = %s, maximum_family_income = %s,
                    amount_min = %s, amount_max = %s, deadline = %s, deadline_status = 'known',
                    official_url = %s, application_url = %s, eligibility_details = %s,
                    required_documents = %s, is_verified = 1, is_active = 1
                WHERE id = %s
                """,
                (
                    sch["title"], sch["provider"], sch["description"], sch["scholarship_type"],
                    sch["education_level"], sch["eligible_courses"], eligible_states_json,
                    eligible_categories_json, sch["minimum_marks"], sch["maximum_family_income"],
                    sch["amount_min"], sch["amount_max"], sch["deadline"],
                    sch["official_url"], sch["application_url"], sch["eligibility_details"],
                    required_docs_json, existing["id"]
                )
            )
        else:
            execute_query(
                """
                INSERT INTO scholarships (
                    source_id, external_id, title, provider, description, scholarship_type,
                    education_level, eligible_courses, eligible_states, eligible_categories,
                    minimum_marks, maximum_family_income, amount_min, amount_max,
                    deadline, deadline_status, official_url, application_url,
                    eligibility_details, required_documents, is_verified, is_active
                ) VALUES (
                    %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'known', %s, %s, %s, %s, 1, 1
                )
                """,
                (
                    src_id, sch["external_id"], sch["title"], sch["provider"], sch["description"],
                    sch["scholarship_type"], sch["education_level"], sch["eligible_courses"],
                    eligible_states_json, eligible_categories_json, sch["minimum_marks"],
                    sch["maximum_family_income"], sch["amount_min"], sch["amount_max"],
                    sch["deadline"], sch["official_url"], sch["application_url"],
                    sch["eligibility_details"], required_docs_json
                )
            )
            inserted += 1

    total = fetch_one("SELECT count(*) as cnt FROM scholarships")
    print(f"Seeding complete! Total scholarships in database: {total['cnt']}")


if __name__ == "__main__":
    seed_database()
