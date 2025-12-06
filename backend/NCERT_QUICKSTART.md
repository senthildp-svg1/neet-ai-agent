# Quick Start: Adding NCERT Content

## ✅ What's Ready
- Enhanced PDF/TXT ingestion script created (`ingest_pdf.py`)
- Current knowledge base: 7 chunks (Biology + Physics samples)
- System supports both PDF and text files

## 📥 Next Steps (Manual)

### 1. Download NCERT PDFs
Visit: https://ncert.nic.in/textbook.php

**Recommended downloads:**
- **Class 11 Biology** (kebo1)
- **Class 12 Biology** (lebo1)
- **Class 11 Physics Part 1 & 2** (keph1, keph2)
- **Class 12 Physics Part 1 & 2** (leph1, leph2)
- **Class 11 Chemistry Part 1 & 2** (kech1, kech2)
- **Class 12 Chemistry Part 1 & 2** (lech1, lech2)

### 2. Place PDFs in Data Directory
```
c:\AI\Antigravity\neet_ai_agent\backend\data\
```

### 3. Run Ingestion Script
```bash
cd c:\AI\Antigravity\neet_ai_agent\backend
.\venv\Scripts\python ingest_pdf.py
```

## 📊 Expected Results
- Each book: ~500-1000 chunks
- Total for all books: ~6,000-10,000 chunks
- Free tier limit: 100,000 vectors ✅

## 🔍 Verify Ingestion
The script will show:
- Files being processed
- Number of chunks uploaded
- Updated total vector count

## 💡 Tips
- Process books one at a time if needed
- Larger chunk size (700) works better for formulas
- Script handles both .pdf and .txt files automatically
