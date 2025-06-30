# 📊 CSV Analyzer with Smart Insights & Database Storage

A powerful and elegant *CSV/JSON Analyzer Web App* built with *Streamlit* that helps you upload, clean, filter, visualize, and analyze data on the fly. It also stores file metadata like filename, rows, and columns in a local *SQLite database* for upload history tracking.

---

## 🚀 Features

✅ Upload *CSV or JSON* files  
✅ Convert *JSON to CSV* with download option  
✅ Get *instant data preview* and *summary*  
✅ Smart *missing value handling* (drop, fill with 0, fill with mean)  
✅ Interactive *filtering, grouping, and top-k frequency* charts  
✅ Beautiful *correlation heatmaps, pie charts, and custom plots*  
✅ Integrated *SQLite database* to store file metadata  
✅ View *upload history* (last 10 files)

---

## 🛠 Tech Stack

- *Frontend*: [Streamlit](https://streamlit.io)
- *Backend/Logic*: Python, Pandas, NumPy, Seaborn, Matplotlib
- *Database*: SQLite (via sqlite3)

---

## 📁 Folder Structure

📦csv-analyzer-app/
├── app.py # Main Streamlit app
├── database.py # SQLite DB connection + table management
├── csv_analyzer.db # Generated DB file (auto-created on first run)
└── README.md

---

## ⚙ How to Run Locally

1. *Clone the Repository*

git clone https://github.com/Vinayg24/csv-analyzer-app.git
cd csv-analyzer-app
Install Required Packages

bash
Copy
Edit
pip install -r requirements.txt
If requirements.txt doesn't exist, install manually:

bash
Copy
Edit
pip install streamlit pandas matplotlib seaborn numpy
Run the App

bash
Copy
Edit
streamlit run app.py
Open in browser: http://localhost:8501

💾 Database Info
This app automatically creates a local SQLite database named csv_analyzer.db and stores:

Filename

Number of rows

Number of columns

Upload timestamp

You can find the DB file in the same folder after first upload.

📌 Upcoming Features (Ideas)
Save filtered or cleaned datasets

User login to store personal upload history

Export reports as Excel or PDF

Add cloud database (MySQL/PostgreSQL)

🙌 Author
Made with ❤ by vinay goswami
📧 vinaygoswami2404@gmail.com

📜 License
This project is open-source and available under the MIT License.

yaml
Copy
Edit

---

## ✅ Bonus: Add requirements.txt

Create a requirements.txt in the same folder with:

streamlit
pandas
numpy
matplotlib
seaborn
