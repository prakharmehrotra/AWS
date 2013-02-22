cd /Users/lavanya/ENV/ &&
source bin/activate &&
cd AWS/ &&
python Feed_Database.py &&
python Feed_Analysis.py &&
python Keyword_Identification.py &&
python Database_copy.py
