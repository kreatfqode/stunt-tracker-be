import pymysql
from db_connection import connection

def create_check_up_results_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS check_up_results (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        weight ENUM('Underweight', 'Normal', 'Overweight'),
        height ENUM('Underheight', 'Normal', 'Overheight'),
        head_circumference ENUM('Undersize', 'Normal', 'Oversize'),
        recomendation TEXT,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
    );
    """)

def create_products_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS products (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        check_up_result_id BIGINT,
        name VARCHAR(255),
        harga DECIMAL(20, 2),
        energi_kcal FLOAT DEFAULT 0,
        protein_g FLOAT DEFAULT 0,
        kalsium_mg FLOAT DEFAULT 0,
        zat_besi_mg FLOAT DEFAULT 0,
        gula_g FLOAT DEFAULT 0,
        lemak_g FLOAT DEFAULT 0,
        vitamin_a_ug FLOAT DEFAULT 0,
        vitamin_d_ug FLOAT DEFAULT 0,
        vitamin_c_mg FLOAT DEFAULT 0,
        zinc_mg FLOAT DEFAULT 0,
        omega_3_mg FLOAT DEFAULT 0,
        omega_6_mg FLOAT DEFAULT 0,
        folate_ug FLOAT DEFAULT 0,
        magnesium_mg FLOAT DEFAULT 0,
        created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
        FOREIGN KEY (check_up_result_id) REFERENCES check_up_results(id)
    );
    """)

def create_zscore_berat_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zscore_berat (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        jenis_kelamin ENUM('L', 'P'),
        umur_bulan INT,
        sangat_kurus FLOAT UNSIGNED,
        kurus FLOAT UNSIGNED,
        normal_kurus FLOAT UNSIGNED,
        baik FLOAT UNSIGNED,
        normal_gemuk FLOAT UNSIGNED,
        gemuk FLOAT UNSIGNED,
        sangat_gemuk FLOAT UNSIGNED
    );
    """)

def create_zscore_lingkar_kepala_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zscore_lingkar_kepala (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        jenis_kelamin ENUM('L', 'P'),
        umur_bulan INT,
        sangat_kecil FLOAT UNSIGNED,
        kecil FLOAT UNSIGNED,
        normal_kecil FLOAT UNSIGNED,
        baik FLOAT UNSIGNED,
        normal_besar FLOAT UNSIGNED,
        besar FLOAT UNSIGNED,
        sangat_besar FLOAT UNSIGNED
    );
    """)

def create_zscore_tinggi_table(cursor):
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS zscore_tinggi (
        id BIGINT AUTO_INCREMENT PRIMARY KEY,
        jenis_kelamin ENUM('L', 'P'),
        umur_bulan INT,
        sangat_pendek FLOAT UNSIGNED,
        pendek FLOAT UNSIGNED,
        normal_pendek FLOAT UNSIGNED,
        baik FLOAT UNSIGNED,
        normal_tinggi FLOAT UNSIGNED,
        tinggi FLOAT UNSIGNED,
        sangat_tinggi FLOAT UNSIGNED
    );
    """)

def migrate():
    with connection.cursor() as cursor:
        create_check_up_results_table(cursor)
        create_products_table(cursor)
        create_zscore_berat_table(cursor)
        create_zscore_lingkar_kepala_table(cursor)
        create_zscore_tinggi_table(cursor)
    connection.commit()

def refresh_migrations():
    with connection.cursor() as cursor:
        cursor.execute("DROP TABLE IF EXISTS products;")
        cursor.execute("DROP TABLE IF EXISTS zscore_berat;")
        cursor.execute("DROP TABLE IF EXISTS zscore_lingkar_kepala;")
        cursor.execute("DROP TABLE IF EXISTS zscore_tinggi;")
        cursor.execute("DROP TABLE IF EXISTS check_up_results;")
    connection.commit()
    migrate()

if __name__ == '__main__':
    print("Memulai migration")
    refresh_migrations()  # Untuk migrasi ulang (migrate refresh)
    print("Successfull")
    # migrate()  # Untuk melakukan migrasi tanpa refresh
