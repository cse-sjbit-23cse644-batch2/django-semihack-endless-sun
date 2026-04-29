# 🎯 CORE PROJECT QUESTIONS

### 1. What is the main objective of your project?

Answer:
“To automate the complete event lifecycle — from registration to certificate verification — using a secure and centralized Django-based system.”

---

### 2. Why did you choose Django?

Answer:
“Django provides built-in features like authentication, admin panel, ORM, and security, which helped us rapidly develop a scalable and secure full-stack application.”

---

### 3. Explain MVT architecture in your project.

Answer:
“Model handles database structure like students and events, View processes logic like registration and validation, and Template handles frontend display. Django internally manages controller logic through URL routing.”

---

### 4. What models did you create?

Answer:
“Event, Participant (Student), Attendance, Feedback, and Enrollment. These models define relationships and store all system data.”

---

### 5. What is the role of UUID in your system?

Answer:
“UUID is used to generate a unique identifier for each certificate, ensuring it cannot be duplicated or forged.”

---

### 6. How does certificate verification work?

Answer:
“Each certificate has a QR code linked to a unique hash. When scanned, it hits a Django URL which checks the hash in the database and returns validity.”

---

### 7. Why did you use AJAX?

Answer:
“To update attendance in real-time without reloading the page, improving user experience and performance.”

---

### 8. Where exactly is AJAX used?

Answer:
“In admin attendance marking — sending asynchronous requests to update student attendance instantly.”

---

### 9. What is role-based access in your project?

Answer:
“Students can only access their own data, while admins have control over events, payments, and approvals using Django authentication and permissions.”

---

### 10. How do you prevent fake certificates?

Answer:
“Using UUID-based hash, QR verification, and backend validation — certificate is generated only if all conditions are met.”

---

# 🎯 DJANGO + TECH QUESTIONS

### 11. What is URLConf in Django?

Answer:
“It maps URLs to views. For example, /verify/<hash>/ maps to a view that validates certificate authenticity.”

---

### 12. What is a View in Django?

Answer:
“A view is a Python function or class that processes requests and returns responses like HTML or JSON.”

---

### 13. What is a Template?

Answer:
“A template is the frontend layer that displays dynamic data using Django template language.”

---

### 14. What is ORM?

Answer:
“Object Relational Mapping allows interaction with database using Python code instead of SQL queries.”

---

### 15. What is Model in Django?

Answer:
“A model defines the structure of database tables using Python classes.”

---

# 🎯 SECURITY + VALIDATION QUESTIONS

### 16. How is data validated in your system?

Answer:
“Through server-side validation in Django views — checking file type, duplicate transaction ID, and required conditions.”

---

### 17. What happens if a student skips feedback?

Answer:
“The backend blocks certificate generation. The condition check fails, so access is denied.”

---

### 18. How do you secure admin routes?

Answer:
“Using Django authentication and restricting access with login-required decorators and role checks.”

---

# 🎯 ADVANCED / IMPRESSIVE QUESTIONS

### 19. How can you scale this system?

Answer:
“By using PostgreSQL for large data, deploying on cloud, adding caching, and integrating APIs for mobile apps.”

---

### 20. What improvements can be added?

Answer:
“Payment gateway integration, email notifications, mobile app support, and AI-based analytics for events.”

---

# ⚡ BONUS RAPID-FIRE (if they push you)

👉 Difference between GET and POST
GET: fetch data
POST: send secure data

👉 Why Django over Flask
Django: built-in features
Flask: lightweight but requires more setup

👉 What is migration
“Process of applying model changes to database”

---
