# Email Setup Guide for Risk Stratification System

## 🚀 **Automated Email Recommendations System**

Your Risk Stratification Dashboard now includes an automated email system that sends AI-generated recommendations to high-risk patients. This system only sends emails to patients classified as "High Risk" or "Very High Risk".

## 📧 **Features**

### **1. Individual Patient Email**
- Send personalized recommendations to specific high-risk patients
- Email includes risk scores, top factors, and AI recommendations
- Only sends to patients with email addresses and high-risk status

### **2. Bulk Email System**
- Automatically send emails to all high-risk patients
- Batch processing for efficient communication
- Success tracking and reporting

### **3. PDF Export**
- Download individual patient recommendations as PDF
- Professional formatting with patient details and recommendations
- Available for all patients regardless of risk level

## ⚙️ **Email Configuration Setup**

### **Step 1: Configure Email Settings**

Edit the `email_config.py` file with your email provider details:

```python
# Gmail Configuration (Recommended)
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False

# Your Gmail credentials
MAIL_USERNAME = 'your-email@gmail.com'  # Replace with your Gmail
MAIL_PASSWORD = 'your-app-password'     # Replace with your Gmail App Password
MAIL_DEFAULT_SENDER = 'your-email@gmail.com'  # Replace with your Gmail
```

### **Step 2: Gmail App Password Setup**

For Gmail users, you need to create an App Password:

1. **Enable 2-Factor Authentication** on your Google account
2. Go to **Google Account settings** > **Security** > **App passwords**
3. Generate an app password for "Mail"
4. Use that password in `MAIL_PASSWORD` above
5. **Never use your regular Gmail password**

### **Step 3: Alternative Email Providers**

#### **Outlook/Hotmail:**
```python
MAIL_SERVER = 'smtp-mail.outlook.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'your-email@outlook.com'
MAIL_PASSWORD = 'your-password'
MAIL_DEFAULT_SENDER = 'your-email@outlook.com'
```

#### **Yahoo:**
```python
MAIL_SERVER = 'smtp.mail.yahoo.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USE_SSL = False
MAIL_USERNAME = 'your-email@yahoo.com'
MAIL_PASSWORD = 'your-app-password'
MAIL_DEFAULT_SENDER = 'your-email@yahoo.com'
```

## 🗄️ **Database Setup**

### **Add Email Addresses to Patients**

The system requires patient email addresses in the database. You can add them manually or update the database:

```sql
-- Add email column if not exists
ALTER TABLE risk_training ADD COLUMN EMAIL TEXT;

-- Update patient emails (example)
UPDATE risk_training 
SET EMAIL = 'patient@example.com' 
WHERE DESYNPUF_ID = 'PATIENT_ID';
```

## 🎯 **How to Use**

### **1. Individual Patient Email**

1. **Navigate to Dashboard**: Go to http://localhost:5000
2. **Find Patient**: Locate the patient in the table
3. **Send Email**: Click the envelope icon (📧) next to their recommendations
4. **Confirmation**: System will confirm if email was sent successfully

### **2. Bulk Email System**

1. **Click "Send Bulk Emails"**: Use the blue button in the table header
2. **System Processing**: Automatically identifies high-risk patients with emails
3. **Results**: Shows how many emails were sent successfully

### **3. PDF Export**

1. **Find Patient**: Locate the patient in the table
2. **Download PDF**: Click the PDF icon (📄) next to their recommendations
3. **File Download**: PDF will download with patient details and recommendations

## 📋 **Email Content**

### **What Patients Receive:**

```
Subject: Important Health Recommendations - Patient ID: [ID]

Dear Patient,

Based on your recent health assessment, we have identified that you are at [Risk Level] for health complications.

Your Risk Assessment:
- 30-Day Risk: [X]%
- 60-Day Risk: [X]%
- 90-Day Risk: [X]%

Top Risk Factors: [Factors]

AI-Generated Recommendations:
[Personalized recommendations]

Please take these recommendations seriously and consult with your healthcare provider to discuss appropriate interventions.

Important Next Steps:
1. Schedule an appointment with your primary care physician
2. Review your current medications with your pharmacist
3. Implement the lifestyle changes recommended above
4. Monitor your symptoms and report any changes

If you have any questions or concerns, please contact your healthcare provider immediately.

Best regards,
Your Healthcare Team

---
This is an automated message. Please do not reply to this email.
For medical emergencies, call 911 or your local emergency number.
```

## 🔒 **Security Features**

### **Risk-Based Filtering**
- Only high-risk patients receive emails
- Automatic filtering based on risk labels
- Prevents unnecessary communication

### **Email Validation**
- Checks for valid email addresses
- Validates patient exists in database
- Confirms high-risk status before sending

### **Rate Limiting**
- Built-in email frequency limits
- Prevents spam and abuse
- Configurable daily limits

## 🚨 **Troubleshooting**

### **Common Issues:**

1. **"Email sending failed"**
   - Check email configuration in `email_config.py`
   - Verify Gmail App Password is correct
   - Ensure 2-Factor Authentication is enabled

2. **"No high-risk patients found"**
   - Run predictions first using "Predict All Patients"
   - Check if patients have email addresses in database
   - Verify risk labels are properly set

3. **"Patient not found"**
   - Ensure patient ID exists in database
   - Check database connection
   - Verify table structure

### **Testing Email Setup:**

1. **Configure email settings** in `email_config.py`
2. **Add test email** to a patient in database
3. **Run predictions** to generate risk assessments
4. **Send test email** using individual patient email button
5. **Check inbox** for test email

## 📊 **API Endpoints**

### **Email Endpoints:**

- `POST /api/send-recommendations-email` - Send email to specific patient
- `POST /api/send-bulk-emails` - Send emails to all high-risk patients
- `GET /api/export-patient-pdf/<patient_id>` - Download patient PDF

### **Example API Usage:**

```bash
# Send email to specific patient
curl -X POST http://localhost:5000/api/send-recommendations-email \
  -H "Content-Type: application/json" \
  -d '{"patient_id": "PATIENT_ID"}'

# Send bulk emails
curl -X POST http://localhost:5000/api/send-bulk-emails

# Download patient PDF
curl -O http://localhost:5000/api/export-patient-pdf/PATIENT_ID
```

## 🎉 **Success!**

Your Risk Stratification System now includes:

✅ **Automated email recommendations for high-risk patients**  
✅ **Individual patient PDF export**  
✅ **Bulk email processing**  
✅ **Professional email templates**  
✅ **Security and validation**  
✅ **Easy configuration setup**  

**Access your enhanced dashboard**: http://localhost:5000

The system will automatically send personalized AI recommendations to high-risk patients, helping improve patient outcomes through proactive communication! 🏥✨
