from tests import run_toc_tests, run_parsing_tests
import pandas as pd
# 10 K parsing tests - need to cleanup code for reuse - add global?
dir_10k = "../Data/10K/"
dir_10k_parsed = "../Data/Parsed/10K"
test_csv_path = "parsing_tests.csv"


run_toc_tests(dir_10k,test_csv_path,new=False)
run_parsing_tests(test_csv_path,dir_10k_parsed,new=False)

# view results
parsing_df = pd.read_csv(test_csv_path)
toc_parsed_counts = parsing_df.toc_parsed.value_counts()
html_parsed_counts = parsing_df.html_parsed.value_counts()

# Calculate percentages
toc_parsed_percentages = (toc_parsed_counts / len(parsing_df[parsing_df.toc_parsed.notna()])) * 100

# Print percentages
print(toc_parsed_percentages)

# Calculate percentages
html_parsed_percentages = (html_parsed_counts / len(parsing_df[parsing_df.html_parsed.notna()])) * 100

# Print percentages
print(html_parsed_percentages)