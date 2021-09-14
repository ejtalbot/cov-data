## Running the script

Clone the repo. 
At the root of the cloned repo, in a terminal run `docker build -t cov-data .` build the container
Run the container with the following `docker run -v $(pwd)/output:/cov-data/output cov-data`
Once the container has finished executing the script, a csv with the results will be on your local machine: `covid_infection_count_<timestamp>.csv`

## Running the script
- Sanity Checks
  - Used pdb to explore the dataframe:
  	- would slice on indiviudal fips to check incrementing
  	- sorted df
  	- checked rows with columns with empty values (seems like some of the census data was missing mappings to fips)
  	- Reran with sample files while testing, rather than downloading entire datasets
- Learnings / Thoughts on datasets
  - The census seemed like it would be static - could download locally rather than fetching each time
  - Read in the census data that one county didn't exist before a certain year - would want to handle those edge cases
  - The repo for ny times data included rolling averages in another file
  - The linked census datset was for 2019, but ny times data went into 2020 and 2021 - would clarify which to use
  - Sobering the rolling averages over time - I'm sure some data visualiztion would be even more eye opening
- Future todos
  - Tests - unit tests for individual functions
  - If building out, would look at data stores for both the census and ny times data - different options because of different refresh rates
  - Look into unmatched data (originally merged dataframes on left, but found rows with incomplete data, so went with inner for cleaner output)
  - parameterize the run / command for the output and change where output would go
  - look into most efficient ways for df manipulation
