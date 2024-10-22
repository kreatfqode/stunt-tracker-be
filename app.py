from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin

app = Flask(__name__)

# Configure CORS to allow specific origin
cors = CORS(app, resources={r"/*": {"origins": "http://localhost:5173"}})

# Konfigurasi koneksi ke database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:tesdoang@localhost/decision_ml'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Product(db.Model):
    __tablename__ = 'products'
    id = db.Column(db.Integer, primary_key=True)
    check_up_result_id = db.Column(db.Integer, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    energi_kcal = db.Column(db.Float, nullable=False)
    protein_g = db.Column(db.Float, nullable=False)
    kalsium_mg = db.Column(db.Float, nullable=False)
    zat_besi_mg = db.Column(db.Float, nullable=False)
    gula_g = db.Column(db.Float, nullable=False)
    lemak_g = db.Column(db.Float, nullable=False)
    vitamin_a_ug = db.Column(db.Float, nullable=False)
    vitamin_d_ug = db.Column(db.Float, nullable=False)
    vitamin_c_mg = db.Column(db.Float, nullable=False)
    zinc_mg = db.Column(db.Float, nullable=False)
    omega_3_mg = db.Column(db.Float, nullable=False)
    omega_6_mg = db.Column(db.Float, nullable=False)
    folate_ug = db.Column(db.Float, nullable=False)
    magnesium_mg = db.Column(db.Float, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "energi_kcal": self.energi_kcal,
            "protein_g": self.protein_g,
            "kalsium_mg": self.kalsium_mg,
            "zat_besi_mg": self.zat_besi_mg,
            "gula_g": self.gula_g,
            "lemak_g": self.lemak_g,
            "vitamin_a_ug": self.vitamin_a_ug,
            "vitamin_d_ug": self.vitamin_d_ug,
            "vitamin_c_mg": self.vitamin_c_mg,
            "zinc_mg": self.zinc_mg,
            "omega_3_mg": self.omega_3_mg,
            "omega_6_mg": self.omega_6_mg,
            "folate_ug": self.folate_ug,
            "magnesium_mg": self.magnesium_mg,
        }

class CheckUpResult(db.Model):
    __tablename__ = 'check_up_results'  # Nama tabel diperbaiki sesuai skema
    id = db.Column(db.Integer, primary_key=True)
    weight = db.Column(db.Enum('Underweight', 'Normal', 'Overweight'), nullable=False)
    height = db.Column(db.Enum('Underheight', 'Normal', 'Overheight'), nullable=False)
    head_circumference = db.Column(db.Enum('Undersize', 'Normal', 'Oversize'), nullable=False)
    recomendation = db.Column(db.Text, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "weight": self.weight,
            "height": self.height,
            "head_circumference": self.head_circumference,
            "recomendation": self.recomendation,
        }

# Model Zscore Berat
class ZscoreBerat(db.Model):
    __tablename__ = 'zscore_berat'
    id = db.Column(db.Integer, primary_key=True)
    jenis_kelamin = db.Column(db.Enum("L", "P"), nullable=False)
    umur_bulan = db.Column(db.Integer, nullable=False)
    sangat_kurus = db.Column(db.Float, nullable=False)
    kurus = db.Column(db.Float, nullable=False)
    normal_kurus = db.Column(db.Float, nullable=False)
    baik = db.Column(db.Float, nullable=False)
    normal_gemuk = db.Column(db.Float, nullable=False)
    gemuk = db.Column(db.Float, nullable=False)
    sangat_gemuk = db.Column(db.Float, nullable=False)

# Model Zscore Tinggi
class ZscoreTinggi(db.Model):
    __tablename__ = 'zscore_tinggi'
    id = db.Column(db.Integer, primary_key=True)
    jenis_kelamin = db.Column(db.Enum("L", "P"), nullable=False)
    umur_bulan = db.Column(db.Integer, nullable=False)
    sangat_pendek = db.Column(db.Float, nullable=False)
    pendek = db.Column(db.Float, nullable=False)
    normal_pendek = db.Column(db.Float, nullable=False)
    baik = db.Column(db.Float, nullable=False)
    normal_tinggi = db.Column(db.Float, nullable=False)
    tinggi = db.Column(db.Float, nullable=False)
    sangat_tinggi = db.Column(db.Float, nullable=False)

# Model Zscore Lingkar Kepala
class ZscoreLingkarKepala(db.Model):
    __tablename__ = 'zscore_lingkar_kepala'
    id = db.Column(db.Integer, primary_key=True)
    jenis_kelamin = db.Column(db.Enum("L", "P"), nullable=False)
    umur_bulan = db.Column(db.Integer, nullable=False)
    sangat_kecil = db.Column(db.Float, nullable=False)
    kecil = db.Column(db.Float, nullable=False)
    normal_kecil = db.Column(db.Float, nullable=False)
    baik = db.Column(db.Float, nullable=False)
    normal_besar = db.Column(db.Float, nullable=False)
    besar = db.Column(db.Float, nullable=False)
    sangat_besar = db.Column(db.Float, nullable=False)

# Fungsi untuk menentukan status berdasarkan zscore berat
def get_check_up_weight(berat_badan, zscore_berat):
    if berat_badan > zscore_berat.sangat_gemuk:
        return "Overweight"
    elif berat_badan > zscore_berat.gemuk:
        return "Overweight"
    elif berat_badan > zscore_berat.normal_gemuk:
        return "Normal"
    elif berat_badan > zscore_berat.baik:
        return "Normal"
    elif berat_badan > zscore_berat.normal_kurus:
        return "Normal"
    elif berat_badan > zscore_berat.kurus:
        return "Underweight"
    elif berat_badan > zscore_berat.sangat_kurus:
        return "Underweight"
    else:
        return "Underweight"

# Fungsi untuk menentukan status berdasarkan zscore tinggi
def get_check_up_height(tinggi_badan, zscore_tinggi):
    if tinggi_badan > zscore_tinggi.sangat_tinggi:
        return "Overheight"
    elif tinggi_badan > zscore_tinggi.tinggi:
        return "Overheight"
    elif tinggi_badan > zscore_tinggi.normal_tinggi:
        return "Normal"
    elif tinggi_badan > zscore_tinggi.baik:
        return "Normal"
    elif tinggi_badan > zscore_tinggi.normal_pendek:
        return "Normal"
    elif tinggi_badan > zscore_tinggi.pendek:
        return "Underheight"
    elif tinggi_badan > zscore_tinggi.sangat_pendek:
        return "Underheight"
    else:
        return "Underheight"

# Fungsi untuk menentukan status berdasarkan zscore lingkar kepala
def get_check_up_head_circumference(lingkar_kepala, zscore_lingkar_kepala):
    if lingkar_kepala > zscore_lingkar_kepala.sangat_besar:
        return "Oversize"
    elif lingkar_kepala > zscore_lingkar_kepala.besar:
        return "Oversize"
    elif lingkar_kepala > zscore_lingkar_kepala.normal_besar:
        return "Normal"
    elif lingkar_kepala > zscore_lingkar_kepala.baik:
        return "Normal"
    elif lingkar_kepala > zscore_lingkar_kepala.normal_kecil:
        return "Normal"
    elif lingkar_kepala > zscore_lingkar_kepala.kecil:
        return "Undersize"
    elif lingkar_kepala > zscore_lingkar_kepala.sangat_kecil:
        return "Undersize"
    else:
        return "Undersize"

# Endpoint untuk menerima data berat badan, tinggi badan, lingkar kepala, dan umur
@app.route("/check-up", methods=["POST"])
@cross_origin()
def check_up():
    data = request.get_json()

    berat_badan = int(data.get('berat_badan'))
    tinggi_badan = int(data.get('tinggi_badan'))
    lingkar_kepala = int(data.get('lingkar_kepala'))
    umur_bulan = int(data.get('umur_bulan'))
    jenis_kelamin = data.get('jenis_kelamin')

    if not (berat_badan and tinggi_badan and lingkar_kepala and umur_bulan and jenis_kelamin):
        return jsonify({"error": "Missing required fields"}), 400

    # Ambil data zscore dari database berdasarkan jenis kelamin dan umur
    zscore_berat = ZscoreBerat.query.filter_by(jenis_kelamin=jenis_kelamin, umur_bulan=umur_bulan).first()
    zscore_tinggi = ZscoreTinggi.query.filter_by(jenis_kelamin=jenis_kelamin, umur_bulan=umur_bulan).first()
    zscore_lingkar_kepala = ZscoreLingkarKepala.query.filter_by(jenis_kelamin=jenis_kelamin, umur_bulan=umur_bulan).first()

    if not (zscore_berat and zscore_tinggi and zscore_lingkar_kepala):
        return jsonify({"error": "No zscore data found for given age and gender"}), 404

    # Tentukan status berdasarkan data zscore
    status_berat = get_check_up_weight(berat_badan, zscore_berat)
    status_tinggi = get_check_up_height(tinggi_badan, zscore_tinggi)
    status_lingkar_kepala = get_check_up_head_circumference(lingkar_kepala, zscore_lingkar_kepala)

    # Ambil data rekomendasi dari tabel check_up_results
    result = CheckUpResult.query.filter_by(weight=status_berat, height=status_tinggi, head_circumference=status_lingkar_kepala).first()

    if not result:
        return jsonify({"error": "No recommendation found"}), 404

    return jsonify(result.to_dict()), 200

@app.route("/check-up/<int:check_up_result_id>/product", methods=["GET"])
@cross_origin()
def check_up_product(check_up_result_id):
    result = Product.query.filter_by(check_up_result_id=check_up_result_id).all()
    result_list = [r.to_dict() for r in result]

    return jsonify(result_list), 200

if __name__ == "__main__":
    app.run(debug=True)
