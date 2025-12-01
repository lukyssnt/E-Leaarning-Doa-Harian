from app import create_app, db
from app.models import User, Course, Module, Assessment, Enrollment, Result
from datetime import datetime

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        # Create tables
        db.create_all()
        
        # Check if data already exists
        if User.query.count() == 0:
            print("Seeding database with sample data...")
            
            # Create admin user
            admin = User(
                username='admin',
                email='admin@elearning.com',
                full_name='Admin Platform',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            
            # Create instructor users
            instructor1 = User(
                username='instructor1',
                email='instructor1@elearning.com',
                full_name='Budi Santoso',
                role='instructor'
            )
            instructor1.set_password('instructor123')
            db.session.add(instructor1)
            
            instructor2 = User(
                username='instructor2',
                email='instructor2@elearning.com',
                full_name='Siti Nurhaliza',
                role='instructor'
            )
            instructor2.set_password('instructor123')
            db.session.add(instructor2)
            
            # Create student users
            student1 = User(
                username='student1',
                email='student1@elearning.com',
                full_name='Ahmad Rahman',
                role='student'
            )
            student1.set_password('student123')
            db.session.add(student1)
            
            student2 = User(
                username='student2',
                email='student2@elearning.com',
                full_name='Dina Wijaya',
                role='student'
            )
            student2.set_password('student123')
            db.session.add(student2)
            
            db.session.commit()
            
            # Create Hifzhul Ad'iyyah course and modules (Islamic content)
            course1 = Course(
                title="Hifzhul Ad'iyyah - Doa Harian",
                description=(
                    "Kursus ini dirancang untuk membantu peserta menghafal dan mengamalkan doa-doa harian (yaumiyyah), "
                    "memahami waktu dan adab berdoa, serta menguatkan kebiasaan ibadah harian melalui materi audio, teks, "
                    "dan kuis interaktif."
                ),
                instructor_id=instructor1.id,
                category='Keagamaan',
                level='beginner',
                status='published'
            )
            db.session.add(course1)
            db.session.commit()

            # Modules for Hifzhul Ad'iyyah
            module1 = Module(
                course_id=course1.id,
                title='Waktu, Adab, dan Tujuan Doa',
                description='Pengantar kapan dan di mana doa disunnahkan/diwajibkan; adab ketika berdoa; tujuan pembelajaran.',
                content=(
                    '<h3>Tujuan Pembelajaran</h3>'
                    '<ul>'
                    '<li>Memahami waktu dan tempat disunnahkannya doa.</li>'
                    '<li>Memahami adab berdoa dan niat yang benar.</li>'
                    '<li>Menyiapkan diri untuk menghafal matan doa dengan tata cara yang tepat.</li>'
                    '</ul>'
                    '<h3>Ringkasan</h3>'
                    '<p>Doa yang dipelajari dalam kursus ini berfokus pada doa-doa routin (pagi, petang, sebelum makan, setelah wudhu, dll.).</p>'
                ),
                file_url='',
                duration_minutes=20,
                status='published',
                order=1
            )
            db.session.add(module1)

            module2 = Module(
                course_id=course1.id,
                title='Doa Pagi dan Petang (Al-Subh wal-Masa)',
                description='Matan, terjemahan singkat, fadhilah, serta audio murattal untuk talqin.',
                content=(
                    '<h3>Doa Pagi</h3>'
                    '<p>Contoh matan: <em>"...lafadz doa pagi..."</em></p>'
                    '<h4>Terjemahan singkat</h4>'
                    '<p>Doa pagi ini digunakan untuk...</p>'
                ),
                file_url='/static/audio/doa_pagi.mp3',
                duration_minutes=8,
                status='published',
                order=2
            )
            db.session.add(module2)

            module3 = Module(
                course_id=course1.id,
                title='Doa Sebelum dan Sesudah Makan',
                description='Matan singkat untuk sebelum/sesudah makan, aturan praktik, dan latihan hafalan audio.',
                content=(
                    '<h3>Doa Sebelum Makan</h3>'
                    '<p>Contoh: <em>"Bismillah" atau lafadz lengkap...</em></p>'
                    '<h3>Doa Sesudah Makan</h3>'
                    '<p>Contoh matan dan penjelasan singkat</p>'
                ),
                file_url='/static/audio/doa_makan.mp3',
                duration_minutes=6,
                status='published',
                order=3
            )
            db.session.add(module3)

            module4 = Module(
                course_id=course1.id,
                title='Jurnal Amalan Harian (Mini Project)',
                description='Format jurnal harian untuk mencatat pengamalan doa selama 7 hari dan refleksi.',
                content=(
                    '<h3>Instruksi Jurnal</h3>'
                    '<p>Catat setiap hari doa yang diamalkan, waktu, dan kendala. Unggah ringkasan mingguan pada tugas.</p>'
                ),
                file_url='',
                duration_minutes=10,
                status='published',
                order=4
            )
            db.session.add(module4)
            db.session.commit()

            # Assessments for Hifzhul Ad'iyyah
            a1 = Assessment(
                module_id=module1.id,
                course_id=course1.id,
                title='Kuis: Adab dan Waktu Doa',
                description='Kuis singkat untuk menguji pemahaman konteks penggunaan doa dan adabnya.',
                assessment_type='quiz',
                instructions='Pilih jawaban yang paling tepat untuk setiap pertanyaan.',
                max_score=100,
                status='published'
            )
            db.session.add(a1)

            a2 = Assessment(
                module_id=module2.id,
                course_id=course1.id,
                title='Latihan Hafalan: Doa Pagi',
                description='Tugas unggah rekaman audio murattal atau teks hafalan untuk dinilai oleh instruktur.',
                assessment_type='assignment',
                instructions='Rekam bacaan Anda (audio) atau unggah file teks materinya.',
                max_score=100,
                status='published',
                allow_multiple_attempts=True
            )
            db.session.add(a2)

            a3 = Assessment(
                module_id=module4.id,
                course_id=course1.id,
                title='Mini Project: Jurnal Amalan 7 Hari',
                description='Unggah ringkasan mingguan jurnal amalan doa (format teks/PDF).',
                assessment_type='submission',
                instructions='Unggah file PDF atau tulis ringkasan mingguan dalam kotak teks.',
                max_score=100,
                status='published',
            )
            db.session.add(a3)
            db.session.commit()

            # Enroll sample students into Hifzhul Ad'iyyah
            enrollment1 = Enrollment(
                user_id=student1.id,
                course_id=course1.id,
                progress_percentage=20,
                status='active'
            )
            db.session.add(enrollment1)

            enrollment2 = Enrollment(
                user_id=student2.id,
                course_id=course1.id,
                progress_percentage=45,
                status='active'
            )
            db.session.add(enrollment2)
            db.session.commit()

            # Create sample results (graded + submitted)
            result1 = Result(
                user_id=student2.id,
                assessment_id=a1.id,
                score=90,
                max_score=100,
                percentage=90,
                submission_text='Jawaban kuis adab doa',
                status='graded',
                feedback='Bagus, pahami konteks doa sebelum praktik'
            )
            db.session.add(result1)
            
            db.session.commit()
            
            print("✓ Database seeded successfully!")
            print("\nTest Credentials:")
            print("Admin: admin / admin123")
            print("Instructor: instructor1 / instructor123")
            print("Student: student1 / student123")
    
    app.run(debug=True)
