import pandas as pd

# Question 1: Car Matrix Generation

def generate_car_matrix(df)->pd.DataFrame:
    # Write your logic here
    car_matrix = df.pivot(index='id_1', columns='id_2', values='car')
    
    # Fill NaN values with 0
    car_matrix = car_matrix.fillna(0)
    
    # Set diagonal values to 0
    for i in car_matrix.index:
        car_matrix.at[i, i] = 0
    
    return car_matrix

data = pd.read_csv('../datasets/dataset-1.csv')
result_df = generate_car_matrix(data)
print(result_df)


# Question 2: Car Type Count Calculation

def get_type_count(df: pd.DataFrame)->dict:
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    # Calculate the count of occurrences for each car_type category
    type_counts = df['car_type'].value_counts().to_dict()

    # Sort the dictionary alphabetically based on keys
    type_counts = dict(sorted(type_counts.items()))

    return type_counts

data = pd.read_csv('../datasets/dataset-1.csv')
result_dict = get_type_count(data)
print(result_dict)


# Question 3: Bus Count Index Retrieval

def get_bus_indexes(df: pd.DataFrame)->list:
    # Calculate the mean value of the 'bus' column
    bus_mean = df['bus'].mean()

    # Identify the indices where 'bus' values are greater than twice the mean
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()

    # Sort the list of indexes in ascending order
    bus_indexes.sort()

    return bus_indexes

    # return list()

data = pd.read_csv('../datasets/dataset-1.csv')
result_list = get_bus_indexes(data)
print(result_list)


# Question 4: Route Filtering

def filter_routes(df:pd.DataFrame)->list:
    # Calculate the average 'truck' values for each route
    route_avg_truck = df.groupby('route')['truck'].mean()

    # Filter routes where the average 'truck' value is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()

    # Sort the list of routes in ascending order
    filtered_routes.sort()

    return filtered_routes

    # return list()

data = pd.read_csv('../datasets/dataset-1.csv')
result_list = filter_routes(data)
print(result_list)


# Question 5: Matrix Value Modification

def multiply_matrix(matrix: pd.DataFrame)->pd.DataFrame:
    for i in range(len(matrix)):
        for j in range(len(matrix.columns)):
            value = matrix.iloc[i, j]

            # Apply conditions based on the value
            if value > 20:
                matrix.iloc[i, j] = round(value * 0.75, 1)
            else:
                matrix.iloc[i, j] = round(value * 1.25, 1)

    return matrix
result_matrix = multiply_matrix(result_df)
print(result_matrix)

# Question 6: Time Check

def time_check(df: pd.DataFrame)->pd.Series:
    df['start_timestamp'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'],errors='coerce')
    df['end_timestamp'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'],errors='coerce')
    
    # Create a date range covering a full 24-hour period and 7 days
    full_date_range = pd.date_range('00:00:00', '23:59:59', freq='15T')  # 15-minute intervals
    full_week_days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    
    # Create a MultiIndex from id and id_2
    multi_index = pd.MultiIndex.from_frame(df[['id', 'id_2']])
    
    # Initialize a boolean series with True for all pairs
    result_series = pd.Series(True, index=multi_index, name='time_check')
    
    # Check each (id, id_2) pair
    for (id_val, id_2_val), group in df.groupby(['id', 'id_2']):
        # Check if the timestamps cover a full 24-hour period
        start_diff = (group['start_timestamp'].min() - full_date_range.min()).total_seconds()
        end_diff = (full_date_range.max() - group['end_timestamp'].max()).total_seconds()
        full_24_hours = start_diff >= 0 and end_diff >= 0

        # Check if the timestamps span all 7 days of the week
        unique_days = group['startDay'].unique()
        full_week = set(unique_days) == set(full_week_days)

        # Update the result series based on the checks
        result_series.loc[(id_val, id_2_val)] = full_24_hours and full_week

    return result_series


data = pd.read_csv('../datasets/dataset-2.csv')
result_series = time_check(data)
print(result_series)