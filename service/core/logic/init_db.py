from sqlalchemy import create_engine
from os import path
from sqlalchemy.orm import sessionmaker
from service.core.schemas.models import Base, Parent, Teacher, Task,School, Student,Playground
from datetime import date, time


cd = path.abspath(path.dirname(__file__))
DATABASE_URL = "sqlite:///" + path.join(cd, "database.sqlite3")

engine = create_engine(DATABASE_URL, echo=True, future=True)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    # Create tables
    Base.metadata.create_all(bind=engine)
    
    # Create a new session
    db = SessionLocal()
    
    try:
        # Check if data already exists
        if db.query(Parent).first():
            return
        
        # Assign cluster IDs based on school locations
        cluster1 = 1  # Azadpur and Adarsh Nagar
        cluster2 = 2  # Paschim Vihar

        # Assign cluster 1 to Azadpur and Adarsh Nagar, cluster 2 to the rest
        address1 = "P5CF+74X, Bunglow Rd, Adarsh Nagar Extension, Adarsh Nagar, Delhi, 110033"
        address2 = "3A, Model Town Rd, Institutional Area, Phase 3, Azadpur, Delhi, 110009"
        address3 = "B Block, Nilothi - Meera Bagh Rd, Block 8, Meera Bagh, Paschim Vihar, New Delhi, Delhi, 110087"
        address4 = "Chaudhary Prem Sukh Marg, Guru Harkishan Nagar, Paschim Vihar, New Delhi, Delhi, 110087"

        # Define parents
        parents = [
            Parent(email="rinku.chopra@gmail.com", name="Rinku Chopra",password="password", address="Adarsh Nagar, Delhi", cluster=cluster1, profile_pic=b"parent1.png",role='parent'),
            Parent(email="yaga.mehra@gmail.com", name="Yaga Mehra",password="password", address="Azadpur, Delhi", cluster=cluster1, profile_pic=b"parent2.png",role='parent'),
            Parent(email="ronit.kulkarni@gmail.com", name="Ronit Kulkarni",password="password",  address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"parent3.png",role='parent'),
            Parent(email="meena.tiwari@gmail.com", name="Meena Tiwari",password="password", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"parent4.png",role='parent'),
            Parent(email="preti.bhusan@gmail.com", name="Preti Bhusan",password="password", address="Azadpur, Delhi", cluster=cluster1, profile_pic=b"parent5.png",role='parent'),
            Parent(email="tisha.yadav@gmail.com", name="Tisha Yadav",password="password", address="Adarsh Nagar, Delhi", cluster=cluster1, profile_pic=b"parent6.png",role='parent'),
            Parent(email="ramesh.dhokla@gmail.com", name="Ramesh Dhokla",password="password", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"parent7.png",role='parent'),
            Parent(email="ujeet.umrant@gmail.com", name="Ujeet Umrant",password="password", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"parent8.png",role='parent')
        ]
        
        # Define schools
        schools = [
            School(schoolid='S1', name="Sri Guru Nanak Public School", address=address1, cluster=cluster1, profile_pic=b"school1.png"),
            School(schoolid='S2', name="G D Goenka Public School", address=address2, cluster=cluster1, profile_pic=b"school2.png"),
            School(schoolid='S3', name="St. Mark's Senior Secondary Public School", address=address3, cluster=cluster2, profile_pic=b"school3.png"),
            School(schoolid='S4', name="S. S. Mota Singh Model Sr. Sec. School", address=address4, cluster=cluster2, profile_pic=b"school4.png")
        ]
        
        # Define teachers
        teachers = [
            Teacher(email="arun.kumar@gmail.com", name="Arun Kumar", password="password", school_id="S1", address="Adarsh Nagar, Delhi", cluster=cluster1, profile_pic=b"teacher1.png",role='teacher'),
            Teacher(email="prashant.20106107023@mitmuzaffarpur.org", name="Ramesh Pal",password="password", school_id="S1", address="Adarsh Nagar, Delhi", cluster=cluster1, profile_pic=b"teacher2.png",role='teacher'),
            Teacher(email="brij.singh@gmail.com", name="Brij Bihari Singh",password="password", school_id="S2", address="Azadpur, Delhi", cluster=cluster1, profile_pic=b"teacher3.png",role='teacher'),
            Teacher(email="ramita.kamlesh@gmail.com", name="Ramita Kamlesh",password="password", school_id="S2", address="Azadpur, Delhi", cluster=cluster1, profile_pic=b"teacher4.png",role='teacher'),
            Teacher(email="rohit.chaudhery@gmail.com", name="Rohit Chaudhery",password="password", school_id="S3", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher5.png",role='teacher'),
            Teacher(email="tarun.verma@gmail.com", name="Tarun Verma", password="password",school_id="S3", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher6.png",role='teacher'),
            Teacher(email="reshma.maheshwari@gmail.com", name="Reshma Maheshwari",password="password", school_id="S4", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher7.png",role='teacher'),
            Teacher(email="rita.mengde@gmail.com", name="Rita Mengde", school_id="S4", password="password",address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher8.png",role='teacher'),
            Teacher(email="tina.joseph@gmail.com", name="Tina Joseph", password="password",school_id="S4", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher9.png",role='teacher'),
            Teacher(email="ekta.yadav@gmail.com", name="Ekta Yadav", password="password", school_id="S4", address="Paschim Vihar, Delhi", cluster=cluster2, profile_pic=b"teacher10.png",role='teacher')
        ]
        # Define students
        students = [
            Student(email="fana.chopra@gmail.com", name="Fana Chopra",password="password", school_id="S1", class_name="VI", address="Adarsh Nagar, Delhi", cluster=cluster1, fathers_name="Rinku Chopra", parent_id="rinku.chopra@gmail.com", profile_pic=b"student1.png",role='student'),
            Student(email="shivkumar851127@gmail.com", name="Yukti Chopra",password="password", school_id="S1", class_name="VIII", address="Adarsh Nagar, Delhi", cluster=cluster1, fathers_name="Rinku Chopra", parent_id="rinku.chopra@gmail.com", profile_pic=b"student2.png",role='student'),
            Student(email="ritik.mehra@gmail.com", name="Ritik Mehra",password="password", school_id="S1", class_name="IX", address="Azadpur, Delhi", cluster=cluster1, fathers_name="Yaga Mehra", parent_id="yaga.mehra@gmail.com", profile_pic=b"student3.png",role='student'),
            Student(email="shana.mehra@gmail.com", name="Shana Mehra",password="password", school_id="S2", class_name="VII", address="Azadpur, Delhi", cluster=cluster1, fathers_name="Yaga Mehra", parent_id="yaga.mehra@gmail.com", profile_pic=b"student4.png",role='student'),
            Student(email="roshan.mehra@gmail.com", name="Roshan Mehra", password="password",school_id="S2", class_name="VI", address="Azadpur, Delhi", cluster=cluster1, fathers_name="Yaga Mehra", parent_id="yaga.mehra@gmail.com", profile_pic=b"student5.png",role='student'),
            Student(email="isha.kulkarni@gmail.com", name="Isha Kulkarni", password="password",school_id="S3", class_name="VIII", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ronit Kulkarni", parent_id="ronit.kulkarni@gmail.com", profile_pic=b"student6.png",role='student'),
            Student(email="nayna.kulkarni@gmail.com", name="Nayna Kulkarni",password="password", school_id="S3", class_name="VII", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ronit Kulkarni", parent_id="ronit.kulkarni@gmail.com", profile_pic=b"student7.png",role='student'),
            Student(email="uma.tiwari@gmail.com", name="Uma Tiwari", password="password",school_id="S4", class_name="IX", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Trikam Tiwari", parent_id="meena.tiwari@gmail.com", profile_pic=b"student8.png",role='student'),
            Student(email="rama.tiwari@gmail.com", name="Rama Tiwari",password="password", school_id="S4", class_name="VII", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Trikam Tiwari", parent_id="meena.tiwari@gmail.com", profile_pic=b"student9.png",role='student'),
            Student(email="pramita.bhusan@gmail.com", name="Pramita Bhusan",password="password", school_id="S2", class_name="IX", address="Azadpur, Delhi", cluster=cluster1, fathers_name="Neel Bhusan", parent_id="preti.bhusan@gmail.com", profile_pic=b"student10.png",role='student'),
            Student(email="pramit.bhusan@gmail.com", name="Pramit Bhusan",password="password", school_id="S2", class_name="VI", address="Azadpur, Delhi", cluster=cluster1, fathers_name="Neel Bhusan", parent_id="preti.bhusan@gmail.com", profile_pic=b"student11.png",role='student'),
            Student(email="reet.yadav@gmail.com", name="Reet Yadav",password="password", school_id="S1", class_name="VIII", address="Adarsh Nagar, Delhi", cluster=cluster1, fathers_name="Krishna Yadav", parent_id="tisha.yadav@gmail.com", profile_pic=b"student12.png",role='student'),
            Student(email="preet.yadav@gmail.com", name="Preet Yadav",password="password", school_id="S1", class_name="VII", address="Adarsh Nagar, Delhi", cluster=cluster1, fathers_name="Krishna Yadav", parent_id="tisha.yadav@gmail.com", profile_pic=b"student13.png",role='student'),
            Student(email="manmeet.yadav@gmail.com", name="Manmeet Yadav",password="password", school_id="S1", class_name="VI", address="Adarsh Nagar, Delhi", cluster=cluster1, fathers_name="Krishna Yadav", parent_id="tisha.yadav@gmail.com", profile_pic=b"student14.png",role='student'),
            Student(email="usha.dhokla@gmail.com", name="Usha Dhokla",password="password", school_id="S3", class_name="IX", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ramesh Dhokla", parent_id="ramesh.dhokla@gmail.com", profile_pic=b"student15.png",role='student'),
            Student(email="isha.dhokla@gmail.com", name="Isha Dhokla",password="password", school_id="S3", class_name="VII", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ramesh Dhokla", parent_id="ramesh.dhokla@gmail.com", profile_pic=b"student16.png",role='student'),
            Student(email="tanya.nikunj@gmail.com", name="Tanya Nikunj",password="password", school_id="S4", class_name="VIII", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ujeet Umrant", parent_id="ujeet.umrant@gmail.com", profile_pic=b"student17.png",role='student'),
            Student(email="rudransh.priyadarshi@gmail.com", name="Rudransh Priyadarshi",password="password", school_id="S4", class_name="IX", address="Paschim Vihar, Delhi", cluster=cluster2, fathers_name="Ujeet Umrant", parent_id="ujeet.umrant@gmail.com", profile_pic=b"student18.png",role='student')
        ]
        
        playgrounds=[
            # Playgrounds
        Playground(groundid='G1',name="Subhash Park",cluster=cluster1, address="C-5, Arya Samaj Rd, Block C, Adarsh Nagar, New Delhi, Delhi, 110033", profile_pic=b"playground1.png"),
        Playground(groundid='G2',name="Spiritual Refreshing Park",cluster=cluster1, address="C571, New Ashok Nagar, Majlis Park, Azadpur, Delhi, 110033", profile_pic=b"playground2.png"),
        Playground(groundid='G3',name="Paschim Vihar District Park",cluster=cluster2, address="M3CW+FCF, Outer Ring Rd, A-2 Paschim Vihar, Pocket GH2, Paschim Vihar, Delhi, 110063", profile_pic=b"playground3.png"),
        Playground(groundid='G4',name="DDA Park", cluster=cluster2, address="1091, Block GH 14, GH 14, Extension, Paschim Vihar, Delhi, 110087", profile_pic=b"playground4.png"),
        
        ]

        tasks=[
            Task(student_id="yukti.chopra@gmail.com",task_name= "Maths Chapter 5 Revision", task_date= date(2024, 8, 1), task_time= time(10, 0), task_deadline=date(2024, 8, 7), status= "completed"),
            Task(student_id="yukti.chopra@gmail.com",task_name= "Maths Chapter 6 Worksheet 4", task_date= date.today(), task_time= time(11, 0), task_deadline=date(2024, 8, 25), status= "ongoing"),
            Task(student_id="yukti.chopra@gmail.com",task_name= "Maths Chapter 5 Revision", task_date= date.today(), task_time= time(12, 0), task_deadline=date(2024, 8, 30), status= "pending"),
            Task(student_id="yukti.chopra@gmail.com",task_name= "Maths Chapter 5 Revision", task_date= date(2024, 7, 15), task_time= time(9, 0), task_deadline=date(2024, 7, 20), status= "completed")


        ]


        # Add everything to the session
        db.add_all(parents + schools + teachers + students+playgrounds+tasks)

        # Commit the session
        db.commit()
    
    except Exception as e:
        # Log the exception
        print(f"An error occurred: {e}")
        db.rollback()
    
    finally:
        db.close()
