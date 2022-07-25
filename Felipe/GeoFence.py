import pandas as pd

# ======================================================================================================================
# Manually collect geofence points

# Landscape 3

# Rep 3 Plot 6
l3r3p6_start_lat = 42.0425640767
l3r3p6_end_lat = 42.0426471388

# Rep 2 Plot 5
l3r2p5_start_lat = 42.0426730045
l3r2p5_end_lat = 42.0427574495

# Rep 1 Plot 4
l3r1p4_start_lat = 42.0427836224
l3r1p4_end_lat = 42.0428665763

# Landscape 2

# Rep 3 Plot 9
l2r3p9_start_lat = 42.0433896299
l2r3p9_end_lat = 42.0434726279

# Rep 2 Plot 8
l2r2p8_start_lat = 42.0434984055
l2r2p8_end_lat = 42.0435827218

# Rep 1 Plot 7
l2r1p7_start_lat = 42.0436098616
l2r1p7_end_lat = 42.0436923796

# Landscape 1

# Rep 3 Plot 3
l1r3p3_start_lat = 42.0449303913
l1r3p3_end_lat = 42.0450127569

# Rep 2 Plot 2
l1r2p2_start_lat = 42.0450397184
l1r2p2_end_lat = 42.0451223721

# Rep 1 Plot 1
l1r1p1_start_lat = 42.0451495375
l1r1p1_end_lat = 42.0452334986

# ======================================================================================================================

# Actually geofence data

df = pd.read_csv(r'ImageData_DigitalAcre.csv')
print(df)
var = df.query('42.0425640767 <= Latitude <= 42.0426471388 or '
               '42.0426730045 <= Latitude <= 42.0427574495 or '
               '42.0427836224 <= Latitude <= 42.0428665763 or '
               '42.0433896299 <= Latitude <= 42.0434726279 or '
               '42.0434984055 <= Latitude <= 42.0435827218 or '
               '42.0436098616 <= Latitude <= 42.0436923796 or '
               '42.0449303913 <= Latitude <= 42.0450127569 or '
               '42.0450397184 <= Latitude <= 42.0451223721 or '
               '42.0451495375 <= Latitude <= 42.0452334986 ')

var.to_csv('ImageData_DigitalAcre_Treatments.csv')