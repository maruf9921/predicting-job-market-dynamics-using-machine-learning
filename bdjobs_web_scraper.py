from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

# Function to add job entry to data list
def add_job_entry(jobName, companyName, companyAddress, requirements, experiences, additionalRequirements, skills, workPlace, employmentStatus):
    try:
        job_data = {
            "Job Title": jobName[0].text if len(jobName) > 0 else None,
            "Company Name": companyName[0].text if len(companyName) > 0 else None,
            "Company Address": companyAddress[0].text if len(companyAddress) > 0 else None,
            "Requirements": [req.text for req in requirements] if requirements else None,
            "Experiences": [exp.text for exp in experiences] if experiences else None,
            "Additional Requirements": [req.text for req in additionalRequirements] if additionalRequirements else None,
            "Skills": [skill.text for skill in skills] if skills else None,
            "WorkPlace": workPlace[0].text if len(workPlace) > 0 else None,
            "Employement Status": employmentStatus[0].text if len(employmentStatus) > 0 else None,
        }
        data.append(job_data)
    except Exception as e:
        print(f"Error adding job entry: {e}")

# Initialize variables and browser settings
id = []
data = []
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_extension('./lgblnfidahcdcjddiepkckcfdhpknnjh.crx')  # Add the extension path here

# Start WebDriver
driver = webdriver.Chrome(options=options)
for i in range(1, 52):
    url = f"https://jobs.bdjobs.com/jobsearch.asp?pg={i}&rpp=100"
    driver.get(url)
    element = driver.find_element("id", "arrTempJobIds")
    job_ids_value = element.get_attribute("value")
    job_ids = eval(job_ids_value)
    id.extend(job_ids)

# Open the target page
for i in range(1,len(id)):
    url = f"https://jobs.bdjobs.com/jobdetails.asp?id={id[i]}"
    driver.get(url)
    # Extract the job details here
    try:
        jobName = driver.find_elements(By.CLASS_NAME, 'jtitle')
        companyName = driver.find_elements(By.CLASS_NAME, 'cname')
        companyAddress = driver.find_elements(By.XPATH, '//h5[text()="Address:"]/following-sibling::p[1]')
        requirements = driver.find_elements(By.XPATH, '//h5[text()="Education"]/following-sibling::ul/li')
        experiences = driver.find_elements(By.XPATH, '//h5[text()="Experience"]/following-sibling::ul/li')
        additionalRequirements = driver.find_elements(By.XPATH, '//h5[normalize-space(text())="Additional Requirements"]/following-sibling::ul/li')
        skills = driver.find_elements(By.CSS_SELECTOR, 'div.skills button')
        workPlace = driver.find_elements(By.XPATH, '//h4[text()="Workplace"]/following-sibling::p')
        employmentStatus = driver.find_elements(By.XPATH, '//h4[normalize-space(text())="Employment Status"]/following-sibling::p')

        # Add job details to data list
        add_job_entry(jobName, companyName, companyAddress, requirements, experiences, additionalRequirements, skills, workPlace, employmentStatus)
    except Exception as e:
        print(f"Error fetching data for job {i}: {e}")
    
# Close the driver
driver.quit()

# Process data and save to Excel
try:
    for job in data:
        for key, value in job.items():
            if isinstance(value, list):
                job[key] = ", ".join(value)

    df = pd.DataFrame(data)
    excel_file_name = "bdjobs_data.xlsx"
    df.to_excel(excel_file_name, index=False)
    print(f"Data successfully saved to {excel_file_name}")
except Exception as e:
    print(f"Error saving data to Excel: {e}")
