import pandas as pd

data = pd.read_excel(r"C:\Users\DELL\Downloads\AC.xlsx")

AC = {
    "General condition": ['Visual : Component Damaged', 'Visual'],
    "Markings": ["Labeling : Illegible Etch"],
    "sticky Trigger": ["Functional : Sticky Trigger", 'Trigger'],
    "Check function of device": ["Functional : Will Not Run", "Functional : Does Not Function"]
}

analysis_code = {
    "General condition": 'Visual : Component Damaged',
    "Markings": "Labeling : Illegible Etch",
    "sticky Trigger": "Functional : Sticky Trigger",
    "Check function of device": "Functional : Will Not Run"
}

def find_failures(row):
    failures = []
    failures_found = row['Test'].splitlines()
    codes = row['Code'].splitlines()
    for key, expected_codes in AC.items():
        if any(key in line for line in failures_found) and all(code not in codes for code in expected_codes):
            failures.append(analysis_code[key])
    return "\n".join(failures)
# data['Failures Found'] = data.apply(
#     lambda row: "\n".join(
#         map(lambda k: analysis_code[k],
#             filter(
#                 lambda k: any(k in line for line in row['Test'].splitlines()) and
#                           all(code not in row['Code'].splitlines() for code in AC[k]),
#                 AC
#             )
#         )
#     ), axis=1
# )
data['Failures Found'] = data.apply(find_failures, axis=1)
print(data['Failures Found'])
