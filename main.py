from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import re
import os
import shutil
import argparse

class Dashboard:
    def __init__(self, id) -> None:
        self.url = f"https://codeforces.com/contest/{id}"

    def get_problems_list(self) -> list:
        # Configure Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the URL
        driver.get(self.url)
        time.sleep(3)  # Wait for the page to load

        # Extract links
        links = []
        elements = driver.find_elements(By.TAG_NAME, "a")
        for element in elements:
            href = element.get_attribute("href")
            if href:
                links.append(href)

        # Close the driver
        driver.quit()

        pattern = fr"https://codeforces\.com/contest/{id}/problem/([A-Z0-9]+)"
        # Extract and deduplicate problem names
        problem_names = list(set(re.findall(pattern, " ".join(links))))
        problem_names.sort()

        # Print the result
        return problem_names

class Problem:
    def __init__(self, id, problem) -> None:
        self.url = f"https://codeforces.com/contest/{id}/problem/{problem}"

    def get_problem_test(self) -> list:
        
        # Configure Chrome options
        chrome_options = Options()
        # chrome_options.add_argument("--headless")  # Run in headless mode
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")

        # Initialize Chrome WebDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)

        # Open the URL
        driver.get(self.url)
        time.sleep(1.5)

        # Extract elements with class 'test-example-line'
        inputs = driver.find_elements(By.CLASS_NAME, "test-example-line")
        
        # Collect the text content of each element
        input = [element.text for element in inputs]

        # Find each `div` with class "output"
        output_divs = driver.find_elements(By.CLASS_NAME, "output")
        for output_div in output_divs:
            # Look for nested elements inside each "output" div
            title_element = output_div.find_element(By.CLASS_NAME, "title")  # Locate the title div within the output div
            title_text = title_element.text.strip()

            # Find all <pre> elements within the output div (they have dynamic IDs)
            pre_elements = output_div.find_elements(By.TAG_NAME, "pre")
            output = [pre.text.strip() for pre in pre_elements]  # Extract text from each <pre> element

        # Close the driver
        driver.quit()

        return '\n'.join(input) + '\n', '\n'.join(output) + '\n'

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Codeforces Scraper")
    parser.add_argument("id", type=int, help="Contest ID")
    args = parser.parse_args()
    id = args.id
    contest = Dashboard(id)
    list_problems = contest.get_problems_list()
    print(list_problems)

    # Create a main repository directory with the name `{id}`
    base_repo_path = f"{id}"
    os.makedirs(base_repo_path, exist_ok=True)

    for problem in list_problems:
        # Create a directory for each problem inside the main repository directory
        problem_repo_path = os.path.join(base_repo_path, problem)
        os.makedirs(problem_repo_path, exist_ok=True)
        
        # Copy the template repository to the new problem directory
        src_path = "/home/{USER}/Codeforces Helper/tps-sample"
        dest_path = os.path.join(problem_repo_path, "tps-sample")
        shutil.copytree(src_path, dest_path, dirs_exist_ok=True)
        
        # Create main.cpp, input.txt, and output.txt files for each problem
        open(os.path.join(problem_repo_path, "main.cpp"), 'w').close()
        open(os.path.join(problem_repo_path, "input.txt"), 'w').close()
        open(os.path.join(problem_repo_path, "output.txt"), 'w').close()
        
        # Retrieve the input and output data for the problem
        input_data, output_data = Problem(id, problem).get_problem_test()
        
        # Define file names for input and output inside the tps-sample/tests directory
        test_path = os.path.join(dest_path, "tests")
        os.makedirs(test_path, exist_ok=True)
        
        input_filename = os.path.join(test_path, f"0-01.in")
        output_filename = os.path.join(test_path, f"0-01.out")
        
        # Write input and output data to respective files
        with open(input_filename, 'w') as f_in:
            f_in.write(input_data)
        
        with open(output_filename, 'w') as f_out:
            f_out.write(output_data)
