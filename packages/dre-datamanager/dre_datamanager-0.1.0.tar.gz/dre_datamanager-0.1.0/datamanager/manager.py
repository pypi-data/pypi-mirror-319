from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import col, year, month, broadcast
from pyspark.sql.types import LongType
from datetime import datetime
from typing import List, Optional, Dict, Callable

class DataManager:
    def __init__(
        self,
        spark: SparkSession,
        logger_callback: Optional[Callable[[str], None]] = None,
        date_columns: Optional[Dict[str, str]] = None,
        years_back: int = 3  # Number of years back from the current year
    ):
        """
        Initialize the DataManager with a Spark session and prepare to extract unique years,
        including only the current year and a specified number of preceding years.

        :param spark: SparkSession for Spark operations.
        :param logger_callback: A callback function that accepts a string message to log progress.
        :param date_columns: A dictionary mapping table names to their respective date columns.
                             Example: {"member_details": "EvidenceDate", "prospectdetail": "created"}
        :param years_back: Number of years to include back from the current year.
                           For example, 3 includes current year and three previous years.
        """
        self.spark = spark
        self._dataframes = {}
        self.logger_callback = logger_callback

        # Define tables and their respective date columns for extracting unique years
        self.tables = {
            "member_details": "dre_parallel_test.member_details",
            "disabilitymodelrule": "rules_engine.disabilitymodelrule",
            "disabilitymodelcomponent": "rules_engine.disabilitymodelcomponent",
            "bodysystemlisting": "rules_engine.bodysystemlisting",
            "prospectdetail": "dre_parallel_test.prospectdetail",
            "loadaudithistory": "bbprod.loadaudithistory"
        }

        self.date_columns = date_columns if date_columns else {
            "member_details": "EvidenceDate",
            "prospectdetail": "created"
            # Add other tables and their date columns if needed
        }

        # Get the current year from the system
        self.current_year = datetime.now().year
        self.years_back = years_back
        self.min_year = self.current_year - self.years_back
        self.log(f"Current system year: {self.current_year}")
        self.log(f"Including data from {self.min_year} to {self.current_year}.")

        # Extract unique years from the data, within the specified range
        self.unique_years = self.extract_unique_years()

    def log(self, message: str):
        """Helper method to log messages if a logger callback is provided."""
        if self.logger_callback:
            try:
                self.logger_callback(message)
            except Exception as e:
                # Avoid raising exceptions from the logger
                print(f"Logging failed: {e}")

    def extract_unique_years(self) -> Dict[str, List[int]]:
        """
        Extracts a unique list of years from the specified date columns in each table,
        including only years within the specified range (current_year - years_back to current_year).

        :return: A dictionary mapping table names to a list of unique years.
        """
        unique_years = {}
        for table_name, table_path in self.tables.items():
            if table_name in self.date_columns:
                date_col = self.date_columns[table_name]
                self.log(f"Extracting unique years from {table_name} using column '{date_col}'...")
                try:
                    df = self.spark.table(table_path).select(year(col(date_col)).alias("year")).distinct()
                    years = [row['year'] for row in df.collect()]
                    # Filter years within the specified range
                    filtered_years = [yr for yr in years if self.min_year <= yr <= self.current_year]
                    unique_years[table_name] = sorted(filtered_years)
                    self.log(f"Found years for {table_name} (within {self.min_year}-{self.current_year}): {unique_years[table_name]}")
                except Exception as e:
                    self.log(f"Error extracting years from {table_name}: {e}")
                    unique_years[table_name] = []
            else:
                self.log(f"No date column specified for {table_name}. Skipping year extraction.")
                unique_years[table_name] = []
        return unique_years

    def load_data(self, cache: bool = True, years: Optional[Dict[str, List[int]]] = None):
        """
        Loads and prepares all necessary DataFrames with optional caching.

        :param cache: Whether to cache the DataFrames after loading.
        :param years: Optional dictionary specifying which years to load for each table.
                      If not provided, all unique years (within the specified range) are loaded.
                      Example: {"member_details": [2022, 2023, 2024, 2025], "prospectdetail": [2023, 2024]}
        """
        if years is None:
            years = self.unique_years

        for name, table in self.tables.items():
            # Log that we're starting to load this table
            self.log(f"Loading {name} from {table}...")

            try:
                df = self.spark.table(table)

                # Apply filters based on table name and specified years
                if name in self.date_columns:
                    date_col = self.date_columns[name]
                    if name in years and years[name]:
                        year_filters = [year(col(date_col)) == yr for yr in years[name]]
                        combined_filter = year_filters[0]
                        for f in year_filters[1:]:
                            combined_filter = combined_filter | f
                        df = df.filter(combined_filter)
                        self.log(f"Applied year filters for {name}: {years[name]}")
                    else:
                        self.log(f"No years specified for {name}, loading all available data.")

                # **Add additional filters for specific tables here**
                if name == "disabilitymodelrule":
                    df = df.filter(col("Deactivated").isNull())

                # **New filter to exclude rows where Name contains 'OBSOLETE-DO NOT USE' in 'bodysystemlisting'**
                if name == "bodysystemlisting":
                    df = df.filter(~col("Name").like("%OBSOLETE-DO NOT USE%"))
                    self.log("Applied filter to exclude rows where Name contains 'OBSOLETE-DO NOT USE'.")

                # Cache the DataFrame if requested
                if cache:
                    df = df.cache()

                # Trigger an action to ensure filters and caching apply
                count = df.count()

                # Store the DataFrame in our dictionary
                self._dataframes[name] = df

                # Log completion and number of records
                self.log(f"Finished loading {name}: {count} records.")

            except Exception as e:
                self.log(f"Error loading {name} from {table}: {e}")
                raise

    def get_unique_years(self, table_name: str) -> List[int]:
        """
        Retrieves the list of unique years for a specific table.

        :param table_name: The name of the table.
        :return: A list of unique years.
        """
        return self.unique_years.get(table_name, [])

    def get_dataframe(self, table_name: str) -> DataFrame:
        """
        Retrieves a DataFrame by its name.

        :param table_name: The name of the DataFrame to retrieve.
        :return: The DataFrame if it exists, otherwise raises an error.
        """
        if table_name in self._dataframes:
            return self._dataframes[table_name]
        raise ValueError(f"DataFrame {table_name} not found in DataManager.")

    def uncache_dataframes(self):
        """
        Uncaches all DataFrames to free up memory.
        """
        for name, df in self._dataframes.items():
            self.log(f"Uncaching DataFrame {name}...")
            try:
                df.unpersist()
            except Exception as e:
                self.log(f"Error uncaching DataFrame {name}: {e}")

    def optimize_joins(self, small_df_name: str, large_df_name: str, join_column: str):
        """
        Optimizes joins by broadcasting the smaller DataFrame if below size threshold.

        :param small_df_name: Name of the smaller DataFrame.
        :param large_df_name: Name of the larger DataFrame.
        :param join_column: The column name to join on.
        :return: DataFrame with optimized join.
        """
        small_df = self.get_dataframe(small_df_name)
        large_df = self.get_dataframe(large_df_name)

        small_df_size = small_df.count() * len(small_df.columns) * 100  

        if small_df_size < (10 * 1024 * 1024):
            self.log(f"Broadcasting {small_df_name} for join with {large_df_name}.")
            return large_df.join(broadcast(small_df), on=join_column)
        self.log(f"Performing regular join between {large_df_name} and {small_df_name}.")
        return large_df.join(small_df, on=join_column)

    def repartition_data(self, df_name: str, num_partitions: int):
        """
        Repartitions a DataFrame to optimize the number of partitions for performance.

        :param df_name: Name of the DataFrame to repartition.
        :param num_partitions: Target number of partitions.
        """
        df = self.get_dataframe(df_name)
        if df:
            self.log(f"Repartitioning DataFrame {df_name} to {num_partitions} partitions.")
            self._dataframes[df_name] = df.repartition(num_partitions)

    def close(self):
        """
        Explicitly cleans up resources by uncaching DataFrames.
        """
        self.uncache_dataframes()
        self.log("DataManager resources have been cleaned up.")

    # Implementing context manager methods
    def __enter__(self):
        """Enter the runtime context related to this object."""
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exit the runtime context and clean up resources."""
        self.close()
