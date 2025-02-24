import pandas as pd

# Q1, Q2

# Make sure that all tables are outputted with consistent formatting
pd.set_option('display.colheader_justify', 'center')

# Import all files into python
CA_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\Canada.CPI.1810000401.csv"
AB_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\AB.CPI.1810000401.csv"
BC_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\BC.CPI.1810000401.csv"
MB_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\MB.CPI.1810000401.csv"
NB_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\NB.CPI.1810000401.csv"
NL_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\NL.CPI.1810000401.csv"
NS_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\NS.CPI.1810000401.csv"
ON_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\ON.CPI.1810000401.csv"
PEI_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\PEI.CPI.1810000401.csv"
QC_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\QC.CPI.1810000401.csv"
SK_file_path = r"C:\Users\arnis\Downloads\A2 Data\A2 Data\SK.CPI.1810000401.csv"

# Read in each file and add a column named jurisdiction for each table
df_CA = pd.read_csv(CA_file_path)
df_CA["Jurisdiction"] = "Canada"

df_AB = pd.read_csv(AB_file_path)
df_AB["Jurisdiction"] = "Alberta"

df_BC = pd.read_csv(BC_file_path)
df_BC["Jurisdiction"] = "British Columbia"

df_MB = pd.read_csv(MB_file_path)
df_MB["Jurisdiction"] = "Manitoba"

df_NB = pd.read_csv(NB_file_path)
df_NB["Jurisdiction"] = "New Brunswick"

df_NL = pd.read_csv(NL_file_path)
df_NL["Jurisdiction"] = "Newfoundland & Labrador"

df_NS = pd.read_csv(NS_file_path)
df_NS["Jurisdiction"] = "Nova Scotia"

df_ON = pd.read_csv(ON_file_path)
df_ON["Jurisdiction"] = "Ontario"

df_PEI = pd.read_csv(PEI_file_path)
df_PEI["Jurisdiction"] = "Prince Edward Island"

df_QC = pd.read_csv(QC_file_path)
df_QC["Jurisdiction"] = "Quebec"

df_SK = pd.read_csv(SK_file_path)
df_SK["Jurisdiction"] = "Saskatchewan"

# combine all data files into a list
df = [df_CA, df_AB, df_BC, df_MB, df_NB, df_NL, df_NS, df_ON, df_PEI, df_QC, df_SK]

# create a dataframe which is just the 11 data files from the above list merged into one dataframe
combined_df = pd.concat(df, ignore_index = True)

# use melt function to make months list vertically by keeping item and jurisdiction, but make the months vertical and name it Month and store the CPI for each month in a column named CPI
final_df = combined_df.melt(id_vars=['Item', 'Jurisdiction'], var_name='Month', value_name='CPI')

pd.options.display.max_rows = 2000

# Display the first 12 rows of actual data
print(final_df.head(12))

print(150 * "*")

#Q3, Q4
# create a new column in the original dataframe that calculates % change in monthly CPI across all items
final_df["CPI_Change (as a %)"] = (final_df.groupby(["Jurisdiction", "Item"])["CPI"].diff()/final_df.groupby(["Jurisdiction", "Item"])["CPI"].shift(1) * 100)

# Copy dataframe from above line and alter it to only include records where the item is food, shelter, or all items excluding food and energy
new_df = final_df.copy().query("Item == 'Food' or Item == 'Shelter' or Item == 'All-items excluding food and energy'")

# Calculate the average of the monthly changes and group by jurisdiction and item to get monthly change for each jurisdication & item pair
avg_cpi_change = round((new_df.groupby(["Jurisdiction", "Item"], as_index = False)["CPI_Change (as a %)"].mean()), 1)

# Rename the column to avg cpi change instead of cpi change
avg_cpi_change = avg_cpi_change.rename(columns = {"CPI_Change (as a %)":"Avg Monthly CPI Change (as a %)"})

# for only food, this stores the monthly change in cpi by jurisdiction
all_food_cpi_change = (avg_cpi_change)[avg_cpi_change["Item"] == "Food"]

# from the output values from the above line of code, the highest avg cpi value is stored
max_food_cpi_change = all_food_cpi_change["Avg Monthly CPI Change (as a %)"].max()

# when a value in the food_cpi query = the value from the max query, this variable stores the entire record from the food_cpi query
max_food_cpi_row = all_food_cpi_change[all_food_cpi_change["Avg Monthly CPI Change (as a %)"] == max_food_cpi_change]

# print the entire row from the above line of code
print(avg_cpi_change)
print("\nThe jursidiction with the highest increase in monthly food inflation is:\n", max_food_cpi_row)

# for only shelter, this stores the monthly change in cpi by jurisdiction
all_shelter_cpi_change = (avg_cpi_change)[avg_cpi_change["Item"] == "Shelter"]

# from the output values from the above line of code, the highest avg cpi value is stored
max_shelter_cpi_change = all_shelter_cpi_change["Avg Monthly CPI Change (as a %)"].max()

# when a value in the shelter_cpi query = the value from the max query, this variable stores the entire record from the shelter_cpi table
max_shelter_cpi_row = all_shelter_cpi_change[all_shelter_cpi_change["Avg Monthly CPI Change (as a %)"] == max_shelter_cpi_change]

print("\nThe jursidiction with the highest increase in monthly Shelter inflation is:\n", max_shelter_cpi_row)

# for all items except food + energy, this stores the monthly change in cpi by jurisdiction 
all_cpi_change = (avg_cpi_change)[avg_cpi_change["Item"] == "All-items excluding food and energy"]

# from the output values from the above line of code, the highest avg cpi value is stored
max_all_cpi_change = all_cpi_change["Avg Monthly CPI Change (as a %)"].max()

# when a value in the all_cpi query = the value from the max query, this variable stores the entire record from the all_cpi table
max_all_cpi_row = all_cpi_change[all_cpi_change["Avg Monthly CPI Change (as a %)"] == max_all_cpi_change]

print("\nThe jursidiction with the highest increase monthly inflation in All-items excluding food and energy is:\n", max_all_cpi_row)

print(150*"*")

# Q5, Q6

# make a copy of the df from Q2 and then only include records for services and for January and December
last_df = final_df.copy().query("(Item == 'Services') and (Month == '24-Jan' or Month == '24-Dec')")

# create a new column that calculates % change from Jan 2024 to Dec 2024
last_df["Jan 2024 - Dec 2024 CPI Change in Services (as a %)"] = round((last_df.groupby(["Jurisdiction", "Item"])["CPI"].diff()/last_df.groupby(["Jurisdiction", "Item"])["CPI"].shift(1) * 100),1)

# delete the cpi change column; in case we need it, it will be in the original final_df dataframe
del last_df["CPI_Change (as a %)"]

# Filter the dataframe to only include non null values, and only include the columns Item, Jurisdiction, and the annual cpi change for services 
last_df = last_df[last_df["Jan 2024 - Dec 2024 CPI Change in Services (as a %)"].notna()][["Item", "Jurisdiction", "Jan 2024 - Dec 2024 CPI Change in Services (as a %)"]]

# Store the max value from the annual services cpi increase column (highest change in services CPI)
max_services_cpi_change = last_df["Jan 2024 - Dec 2024 CPI Change in Services (as a %)"].max()

# when a value from the last_df's annual services cpi increase column = the max value from variable above, this stores the entire record
max_services_cpi_row = last_df[last_df["Jan 2024 - Dec 2024 CPI Change in Services (as a %)"] == max_services_cpi_change]

print(last_df)
print("\nThe Jurisdiction with the highest annual change in CPI in the Services cateogory is: \n\n", max_services_cpi_row)

