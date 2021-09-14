from datetime import datetime

import pandas as pd

NY_TIMES_SOURCE = (
    "https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-counties.csv"
)
CENSUS_SOURCE = "https://www2.census.gov/programs-surveys/popest/datasets/2010-2019/counties/totals/co-est2019-alldata.csv"


def get_ny_times_df(csv_source_file: str) -> pd.DataFrame:
    """Fetch ny times covid data for the following columns: "date", "fips", "cases", "deaths"

    Args:
        csv_source_file: name of csv with ny times covid data

    Returns:
        A DataFrame of the ny times covid data

    """
    ny_times_column_types = {
        "country": str,
        "state": str,
        "fips": str,
        "cases": "Int64",
        "deaths": "Int64",
    }
    ny_times_covid_df = pd.read_csv(csv_source_file, dtype=ny_times_column_types)
    ny_times_covid_df = ny_times_covid_df[["date", "fips", "cases", "deaths"]]
    ny_times_covid_df.sort_values(by=["fips", "date"], inplace=True)
    return ny_times_covid_df


def get_census_df(csv_source_file: str) -> pd.DataFrame:
    """Fetch census data, deriving fips value from STATE and COUNTY columns

    Args:
        csv_source_file: name of csv with census data

    Returns:
        A DataFrame of the census data with the population for each fips

    """
    census_column_types = {
        "STATE": str,
        "COUNTY": str,
        "POPESTIMATE2019": "Int64",
    }
    census_df = pd.read_csv(
        csv_source_file, encoding="latin-1", dtype=census_column_types
    )
    census_df["fips"] = census_df["STATE"] + census_df["COUNTY"]
    census_2019_df = census_df[["fips", "POPESTIMATE2019"]]
    return census_2019_df


def generate_combined_dataset(
    ny_times_covid_df: pd.DataFrame, census_2019_df: pd.DataFrame
) -> pd.DataFrame:
    """Combine covid and census dataframes

    Args:
        ny_times_covid_df: DataFrame of ny times covid data
        census_2019_df: DataFrame of census data

    Returns:
        A DataFrame with the following columns: date, fips, cases, deaths, population, cumulative_cases, cumulative_deaths

    """
    combined_df = pd.merge(ny_times_covid_df, census_2019_df, on="fips")
    combined_df["cumulative_cases"] = combined_df.groupby(["fips"])["cases"].apply(
        lambda x: x.cumsum()
    )
    combined_df["cumulative_deaths"] = combined_df.groupby(["fips"])["deaths"].apply(
        lambda x: x.cumsum()
    )
    combined_df.rename(columns={"POPESTIMATE2019": "population"}, inplace=True)
    return combined_df


def output_covid_results(combined_df: pd.DataFrame) -> None:
    """Outputs a DataFrame to a csv with timestamp

    Args:
        combined_df: df to output to csv

    """
    timestamp = datetime.now().strftime("%Y-%m-%d_%H%M%S")
    output_file = f"output/covid_infection_count_{timestamp}.csv"
    combined_df.to_csv(output_file, index=False)


if __name__ == "__main__":
    ny_times_covid_df = get_ny_times_df(NY_TIMES_SOURCE)
    census_df = get_census_df(CENSUS_SOURCE)
    combined_df = generate_combined_dataset(ny_times_covid_df, census_df)
    output_covid_results(combined_df)
