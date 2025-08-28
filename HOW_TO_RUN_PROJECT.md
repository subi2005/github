# 🚀 How to Run Your Risk Stratification Dashboard

## **Quick Start Guide**

### **1. Start the Web Application**
```bash
python app.py
```

### **2. Access Your Dashboard**
- **URL**: http://localhost:5000
- **Dashboard**: Main patient data table with risk predictions
- **Features**: Email management, PDF generation, AI recommendations

---

## **📊 What You'll See**

### **Main Dashboard Features:**
1. **📋 Patient Data Table** - Shows all patients with:
   - Risk scores (30-day, 60-day, 90-day)
   - Risk labels (Very High, High, Moderate, Low, Very Low)
   - AI recommendations
   - Email addresses
   - Top risk features

2. **🎯 New Patient Prediction Form** - Input new patient details for immediate risk assessment

3. **📧 Email Management** - Update patient emails and send recommendations

4. **📄 PDF Generation** - Download patient reports as PDF

---

## **🔧 Complete Project Setup (If Starting Fresh)**

### **Step 1: Install Dependencies**
```bash
pip install -r requirements.txt
```

### **Step 2: Setup Database**
```bash
python setup_database.py
```

### **Step 3: Train the Model**
```bash
python train.py
```

### **Step 4: Generate Predictions**
```bash
python predict.py
```

### **Step 5: Start Web Application**
```bash
python app.py
```

---

## **📱 Available Features**

### **1. View Patient Data**
- **URL**: http://localhost:5000
- **Shows**: All patients with risk predictions and recommendations

### **2. New Patient Prediction**
- **Form**: Enter patient details (age, gender, conditions)
- **Result**: Immediate risk score and label
- **Storage**: Saves to database with dummy ID

### **3. Email Management**
- **Update Emails**: Click save button (💾) next to email fields
- **Send Recommendations**: Use email buttons for high-risk patients
- **PDF Reports**: Generate and email PDF reports

### **4. Database Operations**
- **Predict All**: Run predictions for all patients in database
- **Bulk Email**: Send emails to multiple high-risk patients

---

## **🗄️ Data Storage Locations**

### **Database**
- **File**: `risk_data.db` (SQLite database)
- **Table**: `risk_training`
- **Records**: 56,641 patients with predictions

### **Model Files**
- **Trained Model**: Saved in project directory
- **Predictions**: Stored in database columns

### **Configuration**
- **Email Settings**: `email_config.py`
- **Database**: SQLite file-based

---

## **🔍 Viewing Saved Data**

### **Option 1: Web Dashboard (Recommended)**
- Go to http://localhost:5000
- View patient table with all data

### **Option 2: Database Scripts**
```bash
# View all saved data
python view_saved_data.py

# Check database structure
python check_database_columns.py

# Search specific patient
python search_patient.py
```

### **Option 3: Database Browser**
- Open `risk_data.db` with SQLite browser
- Browse table `risk_training`

---

## **📊 Current Project Status**

### **✅ Working Features:**
- ✅ **56,641 patients** with risk predictions
- ✅ **18 patients** with email addresses
- ✅ **AI recommendations** for each patient
- ✅ **Email input/update** functionality
- ✅ **PDF generation** capability
- ✅ **New patient prediction** form
- ✅ **Risk distribution** analysis

### **📈 Risk Distribution:**
- **High Risk**: 28.79% (16,308 patients)
- **Moderate Risk**: 23.59% (13,359 patients)
- **Very Low Risk**: 17.22% (9,756 patients)
- **Low Risk**: 15.91% (9,014 patients)
- **Very High Risk**: 14.48% (8,204 patients)

---

## **🎯 Key API Endpoints**

### **Data Access**
- `GET /api/data` - Patient data with pagination
- `GET /api/summary` - Summary statistics
- `GET /api/health` - Health check

### **Predictions**
- `POST /api/predict` - Predict for new patient
- `POST /api/predict-all` - Predict for all patients

### **Email Management**
- `POST /api/update-patient-email` - Update patient email
- `POST /api/send-recommendations-email` - Send text email
- `POST /api/send-pdf-email` - Send PDF via email
- `POST /api/send-bulk-emails` - Bulk email sending

### **PDF Generation**
- `GET /api/export-patient-pdf/<patient_id>` - Download PDF

---

## **🚨 Troubleshooting**

### **If Flask App Won't Start:**
1. Check if port 5000 is available
2. Ensure all dependencies are installed
3. Check for syntax errors in app.py

### **If Database Issues:**
1. Run `python setup_database.py`
2. Check `risk_data.db` file exists
3. Verify table structure with `check_database_columns.py`

### **If Email Features Don't Work:**
1. Configure `email_config.py` with your email settings
2. Check internet connection
3. Verify email credentials

---

## **🎉 Success!**

Your Risk Stratification Dashboard is now running with:
- ✅ **Web Interface**: http://localhost:5000
- ✅ **Database**: 56,641 patients with predictions
- ✅ **Email System**: 18 patients with emails
- ✅ **AI Recommendations**: Personalized for each patient
- ✅ **PDF Reports**: Professional patient reports

**Start exploring your dashboard at http://localhost:5000!** 🏥✨
