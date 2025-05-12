import os
import re
import win32com.client as win32
import pandas as pd
import sys
import tkinter as tk
from tkinter import filedialog

root=tk.Tk()
root.withdraw()
path1 = filedialog.askopenfilename(title="ECM Report")
path2 = filedialog.askopenfilename(title="WO Report")
# path1 = sys.argv[1]
# path2 = sys.argv[2]

df1 = pd.DataFrame(pd.read_csv(path1, encoding='ISO-8859-1'))
# df1 = df1[df1["Product Investigation: Owner Name"] != 'S&R User']
df2 = pd.DataFrame(pd.read_csv(path2, encoding='ISO-8859-1'))
# print(df1)
# print(df2)
# result = pd.merge(df1, df2, left_on=11, right_on='Product Investigation: Product Investigation #', how='left')
# result.to_csv("1.csv", index=False)
result = pd.merge(df1,df2,left_on="Impacted Product",right_on='Impacted Product #',how='left')
# result.to_csv("2.csv", index=False)
result = pd.concat([result.iloc[:, :17], result.iloc[:, 24:25], result.iloc[:, 18:19]], axis=1)
df = pd.DataFrame(result)
filtered_df = df[(df['WO Preliminary Cause Assessment'] == 'Cause Could Not Be Determined (3217)')]
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
# Specify the output file path
output_file = os.path.join(downloads_folder, 'DHR.csv')  # This will save in Downloads
# Convert DataFrame to CSV
filtered_df.to_csv(output_file, index=False,header=True)  # Save the DataFrame as a CSV
print(f"DataFrame has been written successfully!")
# result0 = pd.merge(df0, df1, left_on=11, right_on='Product Investigation: Product Investigation #', how='left')
result = pd.merge(df1, df2, left_on="Impacted Product", right_on='Impacted Product #', how='left')
# result.to_csv("2.csv", index=False)
result.drop(result.columns[[0, 3, 5, 11, 19, 20, 22]], axis=1, inplace=True)
df = pd.DataFrame(result)
# df.to_csv("1.csv", index=False)
df = df.dropna(subset=["Impacted Product #"])
# df = df.drop_duplicates(subset=["Step Instruction: Step Instruction"])
df = df.drop_duplicates(subset=["Step Instruction: Step Instruction","Product Investigation: Product Investigation #"])
# df.to_csv("1.csv", index=False)
df = df[
        (df["Investigator Name"].isin(['Santos Brizo', 'ECM_UNITY BATCH_USER', 'Laura Nelson', 'Min Bartoe', 'Natalie Brierre', 'Gerald Mickam'])) &
        (df["WO Preliminary Cause Assessment"] != 'Evaluation Required (3218)') &
        (df['Service Site: Account Name'].isin(['Germany Depot', 'Netherlands Depot', 'Service Center Russia','J&J MedTech-IN-Bhiwandi Repair Center',
            # 'PTS-JP-Repair Center',
            'Service Center Russia',
            'DPS-SG-OneMD RC', 'Spain Depot', 'LATAM-BR-Depot', 'LATAM-CO-Field','LATAM-CO-Depot','LATAM-CL-Depot', 'LATAM-CL-Field', 'LATAM-MX-Depot', 'LATAM-MX-Field']))]

df['Description'] = df['Product Complaint #: Event Description(English)'].map(
    lambda x: re.search(r'reported:\s*(.*?)\s*$', x, re.MULTILINE).group(1).strip() if isinstance(x,
                                                                                                  str) and re.search(
        r'reported:\s*(.*?)\s*$', x, re.MULTILINE) else x.splitlines()[0].strip() if isinstance(x, str) else None)
# Service_manual
df['Service_manual'] = df['Instruction Template: Instruction Template Name'].map(
    lambda x: re.search(r'^(.*?)(?:\s+Pre-Repair|\s+Inspection Verification)?$', x).group(1).strip() if isinstance(
        x, str) else None)
# Failures
df['Failures'] = df.groupby("Product Investigation: Product Investigation #")[
    "Step Instruction: Step Instruction"].transform(
    lambda x: '\n'.join(x.dropna().apply(lambda text: re.sub(r"\(.*?\)", "", text).strip()).iloc[::-1]))
# Analysis Code
df['Analysis_code'] = df['WO Codes'].map(
    lambda x: '\n'.join(re.findall(r"Analysis Code:\s*(.*?)(?=\s*\|)", x)) if isinstance(x, str) else None)
# Resolution Code
df['resolution_code'] = df['WO Codes'].map(
    lambda x: re.search(r"Resolution Code:\s*(.*)", x).group(1) if isinstance(x, str) and re.search(
        r"Resolution Code:\s*(.*)", x) else None)
# summary
summary = '''SERVICE EVALUATION: 
Product: AAA (BBB)/ CCC DDD

Reported Issue: EEE

A visual and functional assessment was performed on the device according to FFF. 

The following steps failed:
GGG

During service/repair the following was observed (Technician Note):
HHH
III

During the service evaluation the following failures were identified: 
JJJ

OLD SN-KKK changed to New SN-LLL

CONCLUSION: 
Failure reported is confirmed 
Root cause: MMM 
Action: NNN'''


AC = {"General condition":['Visual : Component Damaged', 'Visual : Cosmetic Damage','Visual : Cosmetic Damage - Worn','Visual : Contact Damage','Visual : Missing Components',
'Visual : Cosmetic Damage - Worn Coupling'],
    "Markings":["Labeling : Illegible Etch"],
    "Marking & labeling":['Labeling : Illegible Etch'],
    "sticky Trigger":["Functional : Sticky Trigger", 'Functional : Moving Parts do not Move Smoothly - Trigger','Functional : Limited Trigger Movement Range'],
    "Check function of device":["Functional : Will Not Run", "Functional : Does Not Function","Functional : Will Not Run - Electrical Control Unit Damaged",
'Functional : Frozen/Will Not Move - Chuck Seized','Functional : Frozen/Will Not Move','Functional : Device Stops by Itself','Functional : Insufficient/Low Power',
        'Functional : Will Not Run - Motor Damaged'],
    'Leakage Test using Bubble Emission Technique':['Internal Finding : Leak Tightness Test Failure'],
    'Check Quick coupling for K-Wire':['Functional : Will Not Hold K-Wire'],
    'Charging and refreshing battery in charger UBC II':["Functional : Will Not Run", "Functional : Does Not Function","Functional : Will Not Run - Electrical Control Unit Damaged",
'Functional : Frozen/Will Not Move - Chuck Seized','Functional : Frozen/Will Not Move','Functional : Device Stops by Itself','Functional : Insufficient/Low Power',
'Functional : Will Not Charge'],
    'Check oscillation frequency with Frequency meter':["Functional : Will Not Run", "Functional : Does Not Function","Functional : Will Not Run - Electrical Control Unit Damaged",
'Functional : Frozen/Will Not Move - Chuck Seized','Functional : Frozen/Will Not Move','Functional : Device Stops by Itself','Functional : Insufficient/Low Power'],
    'Charging function with TRS Power Module & Batteries':["Functional : Will Not Run", "Functional : Does Not Function","Functional : Will Not Run - Electrical Control Unit Damaged",
'Functional : Frozen/Will Not Move - Chuck Seized','Functional : Frozen/Will Not Move','Functional : Device Stops by Itself','Functional : Insufficient/Low Power',
'Functional : Will Not Charge'],
    'Leakage test of Battery casing':['Internal Finding : Leak Tightness Test Failure'],
    'Vibration':['Functional : Vibration'],
    'Mode Switch-test':['Functional : Mode Switch Resistance too Low'],
    'Noise Assessment':['Functional : Noise - Excessive','Functional : Noise - Unexpected']}

component_dict = {'Motor(S)':'motor',
                  'Trigger':'push',
'Part/Component/Sub-assembly Term not Applicable (G07001)':'Part/Component/Sub-assembly Term not Applicable (G07001)'}
analysis_code = {"General condition": 'Visual : Component Damaged',
    "Markings": "Labeling : Illegible Etch",
    "Marking & labeling":"Labeling : Illegible Etch",
    "sticky Trigger": "Functional : Sticky Trigger",
    "Check function of device": "Functional : Will Not Run",
    'Leakage Test using Bubble Emission Technique':'Internal Finding : Leak Tightness Test Failure',
    'Check Quick coupling for K-Wire':'Functional : Will Not Hold K-Wire',
    'Charging and refreshing battery in charger UBC II':'Functional : Will Not Charge',
    'Check oscillation frequency with Frequency meter':"Functional : Will Not Run",
    'Charging function with TRS Power Module & Batteries':'Functional : Will Not Charge',
    'Leakage test of Battery casing':'Internal Finding : Leak Tightness Test Failure',
    'Vibration':'Functional : Vibration',
    'Mode Switch-test':'Functional : Mode Switch Resistance too Low',
    'Noise Assessment':'Functional : Noise - Unexpected'
    }

df['summary'] = df.apply(
    lambda row: summary
    .replace('AAA', row['Impacted Product Code'] if isinstance(row['Impacted Product Code'], str) else '')
    .replace('BBB', row['Impacted Product Name'] if isinstance(row['Impacted Product Name'], str) else '')
    .replace('CCC', row['Serial Number'] if isinstance(row['Serial Number'], str) else '')
    .replace('DDD', row['Lot Number'] if isinstance(row['Lot Number'], str) else '')
    .replace('EEE', row['Description'] if isinstance(row['Description'], str) else '')
    .replace('FFF', row['Service_manual'] if isinstance(row['Service_manual'], str) else '')
    .replace('GGG', row['Failures'] if isinstance(row['Failures'], str) else '')
    .replace('HHH', row['Comments'] if isinstance(row['Comments'], str) else '')
    .replace('III', row['Comments.1'] if isinstance(row['Comments.1'], str) else '')
    .replace('JJJ', row['Analysis_code'] if isinstance(row['Analysis_code'], str) else '')
    .replace('KKK', row['Serial Number'] if isinstance(row['Serial Number'], str) else '')
    .replace('LLL', row['Lot Number'] if isinstance(row['Lot Number'], str) else '')
    .replace('MMM',
             row['Preliminary Cause Assessment'] if isinstance(row['Preliminary Cause Assessment'], str) else '')
    .replace('NNN', row['resolution_code'] if isinstance(row['resolution_code'], str) else ''),
    axis=1)


df['AC'] = df.apply(
    lambda row: "\n".join(map(lambda k: analysis_code[k],filter(lambda k: any(k in line for line in row['Failures'].splitlines()) and
    all(code not in row['Analysis_code'].splitlines() for code in AC[k]),AC))), axis=1)
imdfr_list = ['Motor', 'Trigger', "Part/Component/Sub-assembly Term not Applicable (G07001)"]
def extract_code(text):
    text_lower = str(text).lower()
    return "\n".join(component_dict[key] for key in component_dict if key.lower() in text_lower)
df['IMDRF'] = df['Repair Analysis Code Details'].apply(extract_code)

df = df.drop_duplicates(subset=["Product Investigation: Product Investigation #"])

# print(df)
downloads_folder = os.path.join(os.path.expanduser("~"), "Downloads")
# Specify the output file path
output_file = os.path.join(downloads_folder, 'Bankai.csv')  # This will save in Downloads
# Convert DataFrame to CSV
df.to_csv(output_file, index=False, header=True)  # Save the DataFrame as a CSV
print(f"DataFrame has been written successfully!")
