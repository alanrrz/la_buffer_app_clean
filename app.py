import streamlit as st
import pandas as pd
import numpy as np
import math
import folium
from streamlit_folium import st_folium

# 📄 Your schools file
SCHOOLS_URL = "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/schools.csv"

# 🔷 ZipCode → CSV URL mapping
ZIPCODE_URLS = {
    "90001": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90001.0.csv",
    "90002": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90002.0.csv",
    "90003": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90003.0.csv",
    "90004": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90004.0.csv",
    "90005": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90005.0.csv",
    "90006": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90006.0.csv",
    "90007": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90007.0.csv",
    "90008": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90008.0.csv",
    "90010": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90010.0.csv",
    "90011": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90011.0.csv",
    "90012": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90012.0.csv",
    "90013": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90013.0.csv",
    "90014": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90014.0.csv",
    "90015": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90015.0.csv",
    "90016": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90016.0.csv",
    "90017": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90017.0.csv",
    "90018": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90018.0.csv",
    "90019": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90019.0.csv",
    "90020": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90020.0.csv",
    "90021": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90021.0.csv",
    "90022": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90022.0.csv",
    "90023": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90023.0.csv",
    "90024": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90024.0.csv",
    "90025": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90025.0.csv",
    "90026": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90026.0.csv",
    "90027": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90027.0.csv",
    "90028": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90028.0.csv",
    "90029": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90029.0.csv",
    "90031": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90031.0.csv",
    "90032": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90032.0.csv",
    "90033": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90033.0.csv",
    "90034": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90034.0.csv",
    "90035": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90035.0.csv",
    "90036": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90036.0.csv",
    "90037": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90037.0.csv",
    "90038": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90038.0.csv",
    "90039": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90039.0.csv",
    "90040": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90040.0.csv",
    "90041": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90041.0.csv",
    "90042": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90042.0.csv",
    "90043": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90043.0.csv",
    "90044": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90044.0.csv",
    "90045": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90045.0.csv",
    "90046": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90046.0.csv",
    "90047": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90047.0.csv",
    "90048": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90048.0.csv",
    "90049": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90049.0.csv",
    "90056": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90056.0.csv",
    "90057": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90057.0.csv",
    "90058": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90058.0.csv",
    "90059": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90059.0.csv",
    "90061": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90061.0.csv",
    "90062": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90062.0.csv",
    "90063": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90063.0.csv",
    "90064": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90064.0.csv",
    "90065": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90065.0.csv",
    "90066": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90066.0.csv",
    "90067": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90067.0.csv",
    "90068": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90068.0.csv",
    "90069": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90069.0.csv",
    "90071": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90071.0.csv",
    "90073": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90073.0.csv",
    "90077": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90077.0.csv",
    "90089": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90089.0.csv",
    "90094": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90094.0.csv",
    "90108": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90108.0.csv",
    "90201": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90201.0.csv",
    "90210": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90210.0.csv",
    "90211": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90211.0.csv",
    "90212": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90212.0.csv",
    "90220": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90220.0.csv",
    "90221": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90221.0.csv",
    "90230": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90230.0.csv",
    "90232": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90232.0.csv",
    "90245": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90245.0.csv",
    "90247": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90247.0.csv",
    "90248": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90248.0.csv",
    "90249": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90249.0.csv",
    "90250": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90250.0.csv",
    "90255": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90255.0.csv",
    "90262": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90262.0.csv",
    "90270": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90270.0.csv",
    "90272": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90272.0.csv",
    "90275": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90275.0.csv",
    "90280": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90280.0.csv",
    "90290": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90290.0.csv",
    "90291": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90291.0.csv",
    "90292": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90292.0.csv",
    "90293": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90293.0.csv",
    "90302": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90302.0.csv",
    "90303": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90303.0.csv",
    "90402": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90402.0.csv",
    "90403": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90403.0.csv",
    "90404": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90404.0.csv",
    "90405": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90405.0.csv",
    "90501": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90501.0.csv",
    "90502": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90502.0.csv",
    "90505": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90505.0.csv",
    "90640": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90640.0.csv",
    "90710": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90710.0.csv",
    "90717": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90717.0.csv",
    "90731": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90731.0.csv",
    "90732": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90732.0.csv",
    "90744": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90744.0.csv",
    "90745": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90745.0.csv",
    "90746": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90746.0.csv",
    "90810": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/90810.0.csv",
    "91030": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91030.0.csv",
    "91040": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91040.0.csv",
    "91042": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91042.0.csv",
    "91205": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91205.0.csv",
    "91214": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91214.0.csv",
    "91302": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91302.0.csv",
    "91303": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91303.0.csv",
    "91304": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91304.0.csv",
    "91306": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91306.0.csv",
    "91307": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91307.0.csv",
    "91311": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91311.0.csv",
    "91316": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91316.0.csv",
    "91321": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91321.0.csv",
    "91324": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91324.0.csv",
    "91325": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91325.0.csv",
    "91326": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91326.0.csv",
    "91330": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91330.0.csv",
    "91331": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91331.0.csv",
    "91335": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91335.0.csv",
    "91340": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91340.0.csv",
    "91342": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91342.0.csv",
    "91343": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91343.0.csv",
    "91344": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91344.0.csv",
    "91345": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91345.0.csv",
    "91352": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91352.0.csv",
    "91356": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91356.0.csv",
    "91364": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91364.0.csv",
    "91367": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91367.0.csv",
    "91387": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91387.0.csv",
    "91401": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91401.0.csv",
    "91402": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91402.0.csv",
    "91403": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91403.0.csv",
    "91405": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91405.0.csv",
    "91406": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91406.0.csv",
    "91411": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91411.0.csv",
    "91423": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91423.0.csv",
    "91436": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91436.0.csv",
    "91504": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91504.0.csv",
    "91505": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91505.0.csv",
    "91506": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91506.0.csv",
    "91510": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91510.0.csv",
    "91601": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91601.0.csv",
    "91602": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91602.0.csv",
    "91604": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91604.0.csv",
    "91605": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91605.0.csv",
    "91606": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91606.0.csv",
    "91607": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91607.0.csv",
    "91608": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91608.0.csv",
    "91754": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91754.0.csv",
    "91801": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91801.0.csv",
    "91803": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/91803.0.csv",
    "92008": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/92008.0.csv",
    "93063": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/93063.0.csv",
    "97439": "https://raw.githubusercontent.com/alanrrz/la_buffer_app_clean/main/zipcodes/97439.0.csv",
}

# 👇 Neighbor ZIP mapping
NEIGHBOR_ZIPS = {
    "90001": ['90002', '90003', '90011', '90058', '90255', '90280'],
    "90002": ['90001', '90003', '90059', '90061', '90262', '90280'],
    "90003": ['90001', '90002', '90011', '90037', '90044', '90061'],
    "90004": ['90020', '90026', '90029', '90036', '90038', '90057'],
    "90005": ['90006', '90019', '90020', '90036', '90057'],
    "90006": ['90005', '90007', '90015', '90018', '90019', '90057'],
    "90007": ['90006', '90011', '90015', '90018', '90037', '90062', '90089'],
    "90008": ['90016', '90018', '90043', '90056', '90062', '90230', '90232'],
    "90010": ['90036', '90057'],
    "90011": ['90001', '90003', '90007', '90015', '90021', '90037', '90058'],
    "90012": ['90017', '90031', '90071', '90090'],
    "90014": ['90015', '90017', '90021', '90071', '90013'],
    "90015": ['90006', '90007', '90011', '90014', '90017', '90021', '90057'],
    "90016": ['90008', '90018', '90019', '90034', '90232'],
    "90017": ['90012', '90014', '90015', '90026', '90057', '90071'],
    "90018": ['90006', '90007', '90008', '90016', '90019', '90062'],
    "90019": ['90005', '90006', '90016', '90018', '90034', '90035', '90036', '90048'],
    "90020": ['90004', '90005', '90036', '90057'],
    "90021": ['90011', '90014', '90015', '90023', '90033', '90058', '90013'],
    "90022": ['90023', '90040', '90063', '90640', '91754'],
    "90023": ['90021', '90022', '90033', '90040', '90058', '90063'],
    "90024": ['90025', '90049', '90067', '90073', '90077', '90095', '90210', '90212'],
    "90025": ['90024', '90049', '90064', '90067', '90073', '90403', '90404'],
    "90026": ['90004', '90017', '90027', '90029', '90031', '90039', '90057'],
    "90027": ['90026', '90028', '90029', '90038', '90039', '90068', '91201', '91202', '91506'],
    "90028": ['90027', '90029', '90038', '90046', '90068'],
    "90029": ['90004', '90026', '90027', '90028', '90038', '90039'],
    "90031": ['90012', '90026', '90032', '90033', '90039', '90042', '90065'],
    "90032": ['90031', '90033', '90042', '90063', '91030', '91754', '91801', '91803'],
    "90033": ['90021', '90023', '90031', '90032', '90063'],
    "90034": ['90016', '90019', '90035', '90064', '90066', '90230', '90232'],
    "90035": ['90019', '90034', '90048', '90064', '90067', '90211', '90212'],
    "90036": ['90004', '90005', '90010', '90019', '90020', '90038', '90046', '90048'],
    "90037": ['90003', '90007', '90011', '90044', '90047', '90062', '90089'],
    "90038": ['90004', '90027', '90028', '90029', '90036', '90046'],
    "90039": ['90026', '90027', '90029', '90031', '90065', '91202', '91203', '91204'],
    "90040": ['90022', '90023', '90058', '90640'],
    "90041": ['90042', '90065', '91105', '91205', '91206'],
    "90042": ['90031', '90032', '90041', '90065', '91030', '91105'],
    "90043": ['90008', '90047', '90056', '90062', '90301', '90302', '90305'],
    "90044": ['90003', '90037', '90047', '90061', '90247', '90248'],
    "90045": ['90056', '90094', '90230', '90245', '90250', '90293', '90301', '90302', '90304'],
    "90046": ['90028', '90036', '90038', '90048', '90068', '90069', '90210', '91604'],
    "90047": ['90037', '90043', '90044', '90062', '90247', '90249', '90250', '90303', '90305'],
    "90048": ['90019', '90035', '90036', '90046', '90069', '90210', '90211'],
    "90049": ['90024', '90025', '90073', '90077', '90272', '90402', '90403', '91316', '91403', '91436'],
    "90056": ['90008', '90043', '90045', '90230', '90302'],
    "90057": ['90004', '90005', '90006', '90010', '90015', '90017', '90020', '90026'],
    "90058": ['90001', '90011', '90021', '90023', '90040', '90201', '90255'],
    "90059": ['90002', '90061', '90220', '90248', '90262'],
    "90061": ['90002', '90003', '90044', '90059', '90248'],
    "90062": ['90007', '90008', '90018', '90037', '90043', '90047'],
    "90063": ['90022', '90023', '90032', '90033', '91754'],
    "90064": ['90025', '90034', '90035', '90066', '90067', '90404', '90405'],
    "90065": ['90031', '90039', '90041', '90042', '91204', '91205'],
    "90066": ['90034', '90064', '90094', '90230', '90232', '90291', '90292', '90405'],
    "90067": ['90024', '90025', '90035', '90064', '90210', '90212'],
    "90068": ['90027', '90028', '90046', '91505', '91506', '91522', '91602', '91604', '91608'],
    "90069": ['90046', '90048', '90210'],
    "90071": ['90012', '90014', '90017', '90013'],
    "90073": ['90024', '90025', '90049'],
    "90077": ['90024', '90049', '90095', '90210', '91403', '91423'],
    "90089": ['90007', '90037'],
    "90094": ['90045', '90066', '90230', '90292', '90293'],
    "90095": ['90024', '90077'],
    "90201": ['90058', '90241', '90280'],
    "90210": ['90024', '90046', '90048', '90067', '90069', '90077', '90211', '90212', '91423', '91604'],
    "90211": ['90035', '90048', '90210', '90212'],
    "90212": ['90024', '90035', '90067', '90210', '90211'],
    "90220": ['90059', '90221', '90248', '90746', '90810'],
    "90221": ['90220', '90262', '90805', '90810'],
    "90230": ['90008', '90034', '90045', '90056', '90066', '90094', '90232'],
    "90232": ['90008', '90016', '90034', '90066', '90230'],
    "90241": ['90201', '90280'],
    "90245": ['90045', '90250', '90293', '90304'],
    "90247": ['90044', '90047', '90248', '90249', '90504'],
    "90248": ['90044', '90059', '90061', '90220', '90247', '90501', '90502', '90504', '90745', '90746'],
    "90249": ['90047', '90247', '90250', '90504', '90506'],
    "90250": ['90045', '90047', '90245', '90249', '90303', '90304'],
    "90255": ['90001', '90058', '90280'],
    "90262": ['90002', '90059', '90221', '90280'],
    "90265": ['90272', '90290', '91302'],
    "90270": [],
    "90272": ['90049', '90265', '90290', '90402', '91316', '91356'],
    "90274": ['90275', '90505', '90717'],
    "90275": ['90274', '90717', '90731', '90732'],
    "90280": ['90001', '90002', '90201', '90241', '90255', '90262'],
    "90290": ['90265', '90272', '91302', '91356', '91364'],
    "90291": ['90066', '90292', '90405'],
    "90292": ['90066', '90094', '90291', '90293'],
    "90293": ['90045', '90094', '90245', '90292'],
    "90301": ['90043', '90045', '90302', '90303', '90304', '90305'],
    "90302": ['90043', '90045', '90056', '90301'],
    "90303": ['90047', '90250', '90301', '90304', '90305'],
    "90304": ['90045', '90245', '90250', '90301', '90303'],
    "90305": ['90043', '90047', '90301', '90303'],
    "90402": ['90049', '90272', '90403'],
    "90403": ['90025', '90049', '90402', '90404'],
    "90404": ['90025', '90064', '90403', '90405'],
    "90405": ['90064', '90066', '90291', '90404'],
    "90501": ['90248', '90502', '90504', '90505', '90710', '90717'],
    "90502": ['90248', '90501', '90710', '90745'],
    "90504": ['90247', '90248', '90249', '90501', '90506'],
    "90505": ['90274', '90501', '90717'],
    "90506": ['90249', '90504'],
    "90640": ['90022', '90040', '91754'],
    "90710": ['90501', '90502', '90717', '90731', '90732', '90744', '90745'],
    "90717": ['90274', '90275', '90501', '90505', '90710', '90732'],
    "90731": ['90275', '90710', '90732', '90744', '90802'],
    "90732": ['90275', '90710', '90717', '90731', '90744'],
    "90744": ['90710', '90731', '90732', '90745', '90802', '90810', '90813'],
    "90745": ['90248', '90502', '90710', '90744', '90746', '90810'],
    "90746": ['90220', '90248', '90745', '90747', '90810'],
    "90747": ['90746'],
    "90802": ['90731', '90744', '90813'],
    "90805": ['90221', '90810'],
    "90806": ['90810', '90813'],
    "90810": ['90220', '90221', '90744', '90745', '90746', '90805', '90806', '90813'],
    "90813": ['90744', '90802', '90806', '90810'],
    "91011": ['91042', '91206', '91208', '91214', '93550'],
    "91030": ['90032', '90042', '91105', '91801'],
    "91040": ['91042', '91331', '91342', '91352'],
    "91042": ['91011', '91040', '91214', '91342', '91352', '93550'],
    "91105": ['90041', '90042', '91030', '91206'],
    "91201": ['90027', '91202', '91208', '91501', '91506'],
    "91202": ['90027', '90039', '91201', '91203'],
    "91203": ['90039', '91202', '91204', '91205', '91206'],
    "91204": ['90039', '90065', '91203', '91205'],
    "91205": ['90041', '90065', '91203', '91204', '91206'],
    "91206": ['90041', '91011', '91105', '91203', '91205', '91208'],
    "91208": ['91011', '91201', '91206', '91214', '91352', '91501'],
    "91214": ['91011', '91042', '91208', '91352'],
    "91302": ['90265', '90290', '91364', '91367'],
    "91303": ['91304', '91306', '91307', '91367'],
    "91304": ['91303', '91306', '91307', '91311'],
    "91306": ['91303', '91304', '91311', '91324', '91335', '91367'],
    "91307": ['91303', '91304', '91367'],
    "91311": ['91304', '91306', '91324', '91326', '91381', '91382'],
    "91316": ['90049', '90272', '91335', '91356', '91406', '91436'],
    "91324": ['91306', '91311', '91325', '91326', '91335'],
    "91325": ['91324', '91326', '91330', '91335', '91343', '91344', '91406'],
    "91326": ['91311', '91324', '91325', '91344', '91381', '91321'],
    "91330": ['91325'],
    "91331": ['91040', '91340', '91342', '91345', '91352', '91402'],
    "91335": ['91306', '91316', '91324', '91325', '91356', '91367', '91406'],
    "91340": ['91331', '91342', '91345'],
    "91342": ['91040', '91042', '91331', '91340', '91344', '91345', '91387', '91321'],
    "91343": ['91325', '91344', '91345', '91402', '91406'],
    "91344": ['91325', '91326', '91342', '91343', '91345', '91321'],
    "91345": ['91331', '91340', '91342', '91343', '91344', '91402'],
    "91352": ['91040', '91042', '91208', '91214', '91331', '91402', '91501', '91504', '91505', '91605'],
    "91356": ['90272', '90290', '91316', '91335', '91364', '91367'],
    "91364": ['90290', '91302', '91356', '91367'],
    "91367": ['91302', '91303', '91306', '91307', '91335', '91356', '91364'],
    "91381": ['91311', '91326', '91382', '91321'],
    "91382": ['91311', '91381'],
    "91387": ['91342'],
    "91401": ['91403', '91405', '91411', '91423', '91605', '91606', '91607'],
    "91402": ['91331', '91343', '91345', '91352', '91405', '91406', '91605'],
    "91403": ['90049', '90077', '91401', '91411', '91423', '91436'],
    "91405": ['91401', '91402', '91406', '91411', '91605'],
    "91406": ['91316', '91325', '91335', '91343', '91402', '91405', '91411', '91436'],
    "91411": ['91401', '91403', '91405', '91406', '91436'],
    "91423": ['90077', '90210', '91401', '91403', '91604', '91607'],
    "91436": ['90049', '91316', '91403', '91406', '91411'],
    "91501": ['91201', '91208', '91352', '91504'],
    "91504": ['91352', '91501', '91505', '91506'],
    "91505": ['90068', '91352', '91504', '91506', '91522', '91601', '91602', '91605', '91606'],
    "91506": ['90027', '90068', '91201', '91504', '91505'],
    "91522": ['90068', '91505'],
    "91601": ['91505', '91602', '91606', '91607'],
    "91602": ['90068', '91505', '91601', '91604', '91607', '91608'],
    "91604": ['90046', '90068', '90210', '91423', '91602', '91607', '91608'],
    "91605": ['91352', '91401', '91402', '91405', '91505', '91606'],
    "91606": ['91401', '91505', '91601', '91605', '91607'],
    "91607": ['91401', '91423', '91601', '91602', '91604', '91606'],
    "91608": ['90068', '91602', '91604'],
    "91754": ['90022', '90032', '90063', '90640', '91801', '91803'],
    "91801": ['90032', '91030', '91754', '91803'],
    "91803": ['90032', '91754', '91801'],
    "93550": ['91011', '91042'],
    "91321": ['91326', '91342', '91344', '91381'],
    "90013": ['90014', '90021', '90071'],
    "90090": ['90012'],
}

@st.cache_data
def load_schools():
    df = pd.read_csv(SCHOOLS_URL)
    df.columns = df.columns.str.strip()
    df["ZIPCODE"] = (
        df["ZIP"]
        .astype(str)
        .str.replace(".0", "", regex=False)
        .str.zfill(5)
    )
    return df

@st.cache_data
def load_addresses(url):
    df = pd.read_csv(url)
    df.columns = df.columns.str.strip()
    df["LAT"] = pd.to_numeric(df["LAT"], errors="coerce")
    df["LON"] = pd.to_numeric(df["LON"], errors="coerce")
    return df

def haversine(lon1, lat1, lon2, lat2):
    R = 3959  # miles
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = (
        math.sin(dlat/2)**2
        + math.cos(math.radians(lat1))
        * math.cos(math.radians(lat2))
        * math.sin(dlon/2)**2
    )
    return 2 * R * math.asin(math.sqrt(a))

st.title("📍 School Community Address Finder (by ZipCode)")
st.caption("Find addresses near your selected school site based on its ZIP code and neighboring areas.")

schools = load_schools()
site_list = schools["LABEL"].sort_values().tolist()
site_selected = st.selectbox("Select Campus", site_list)

if site_selected:
    selected_school_row = schools[schools["LABEL"] == site_selected].iloc[0]
    school_zip = selected_school_row["ZIPCODE"]
    slon, slat = selected_school_row["LON"], selected_school_row["LAT"]

    st.write(f"📌 Selected School: **{site_selected}** (ZIP code: `{school_zip}`)")

    # collect ZIPs to load
    zips_to_load = [school_zip] + NEIGHBOR_ZIPS.get(school_zip, [])
    urls_to_load = [ZIPCODE_URLS[z] for z in zips_to_load if z in ZIPCODE_URLS]

    if not urls_to_load:
        st.error(f"No addresses file found for ZIP code: {school_zip} or its neighbors.")
    else:
        dfs = [load_addresses(url) for url in urls_to_load]
        addresses = pd.concat(dfs, ignore_index=True)

        radius_selected = st.select_slider(
            "Select Radius (miles)",
            options=[round(x, 2) for x in np.arange(0.1, 3.01, 0.01)],
            value=0.5
        )

        if "show_map" not in st.session_state:
            st.session_state["show_map"] = False

        col1, col2 = st.columns([1, 1])
        with col1:
            if st.button("Preview Map"):
                st.session_state["show_map"] = True
        with col2:
            if st.button("Reset"):
                st.session_state["show_map"] = False

        if st.session_state["show_map"]:
            addresses["distance"] = addresses.apply(
                lambda r: haversine(slon, slat, r["LON"], r["LAT"]), axis=1
            )
            within = addresses[addresses["distance"] <= radius_selected]

            csv = within[["FullAddress"]].rename(columns={"FullAddress": "Address"}).to_csv(index=False)

            st.download_button(
                label=f"📥 Download Nearby Addresses ({site_selected}_{radius_selected}mi.csv)",
                data=csv,
                file_name=f"{site_selected.replace(' ', '_')}_{radius_selected}mi.csv",
                mime='text/csv'
            )

            fmap = folium.Map(location=[slat, slon], zoom_start=15)
            folium.Marker([slat, slon], tooltip=site_selected, icon=folium.Icon(color="blue")).add_to(fmap)
            folium.Circle([slat, slon], radius=radius_selected * 1609.34, color='red', fill=True, fill_opacity=0.1).add_to(fmap)

            st.write("### 📍 Map Preview")
            st.write("The red circle shows all addresses included in your download. Adjust your campus or radius as needed before downloading.")
            st_folium(fmap, width=700, height=500)
        else:
            st.info("Select campus and radius, then click 'Preview Map' to see results.")
