from tests import run_toc_tests, run_parsing_tests
import pandas as pd
# 10 K parsing tests
# previous results: as of 6/26 - on subsamble about 80% of toc parsed, and then 95% of that was parsed correctly
dir_10k = "../Data/10K/"
out_path = "parsing_tests.csv"

run_toc_tests(dir_10k,out_path,new=False)
run_parsing_tests(out_path,new=False)

# view results
parsing_df = pd.read_csv("parsing_tests.csv")
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