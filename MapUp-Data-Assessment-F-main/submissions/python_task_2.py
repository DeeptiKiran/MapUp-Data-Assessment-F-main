import pandas as pd
import networkx as nx

# Question 1: Distance Matrix Calculation

def calculate_distance_matrix(df: pd.DataFrame)->pd.Series:
    graph = nx.DiGraph()

    for _, row in df.iterrows():
        source = row['id_start']
        target = row['id_end']
        distance = row['distance']

        graph.add_edge(source, target, weight=distance)
        graph.add_edge(target, source, weight=distance)

    shortest_paths = dict(nx.all_pairs_dijkstra_path_length(graph))

    # Create a DataFrame to store the distance matrix
    locations = sorted(graph.nodes())
    distance_matrix = pd.DataFrame(index=locations, columns=locations)

    for source in locations:
        for target in locations:
            if source == target:
                distance_matrix.loc[source, target] = 0
            else:
                distance_matrix.loc[source, target] = shortest_paths[source][target]

    return distance_matrix

data = pd.read_csv('../datasets/dataset-3.csv')
result = calculate_distance_matrix(data)
print(result)


# Question 2: Unroll Distance Matrix

def unroll_distance_matrix(df)->pd.DataFrame():
    unrolled_df = pd.DataFrame(columns=['id_start', 'id_end', 'distance'])

    # Iterate through the rows of the distance matrix
    for index, row in df.iterrows():
        id_start = row.name
        for id_end, distance in row.items():
            # Skip the diagonal entries (id_start to itself)
            if id_start != id_end:
                unrolled_df = unrolled_df.append({'id_start': id_start, 'id_end': id_end, 'distance': distance}, ignore_index=True)

    return unrolled_df
distance_matrix = calculate_distance_matrix(data)
unrolled_result = unroll_distance_matrix(distance_matrix)
print(unrolled_result)


# Question 3: Finding IDs within Percentage Threshold

def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    reference_rows = df[df['id_start'] == reference_id]

    # Calculate the average distance for the reference_id
    reference_average_distance = reference_rows['distance'].mean()

    # Calculate the lower and upper bounds for the threshold (within 10%)
    lower_bound = reference_average_distance - 0.1 * reference_average_distance
    upper_bound = reference_average_distance + 0.1 * reference_average_distance

    # Filter the DataFrame for rows within the threshold
    result_df = df[(df['id_start'] != reference_id) & (df['distance'] >= lower_bound) & (df['distance'] <= upper_bound)]

    # Sort the result DataFrame by id_start
    result_df = result_df.sort_values(by='id_start')

    return result_df 
unrolled_data = unroll_distance_matrix(distance_matrix)
result = find_ids_within_ten_percentage_threshold(unrolled_data, reference_id=1001400)
print(result)

# Question 4: Calculate Toll Rate

def calculate_toll_rate(df)->pd.DataFrame():
    df['moto'] = 0.8 * df['distance']
    df['car'] = 1.2 * df['distance']
    df['rv'] = 1.5 * df['distance']
    df['bus'] = 2.2 * df['distance']
    df['truck'] = 3.6 * df['distance']

    return df
unrolled_data = unroll_distance_matrix(distance_matrix)
result = calculate_toll_rate(unrolled_data)
print(result)


# Question 5: Calculate Time-Based Toll Rates

import datetime
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    def get_discount_factor(hour, day):
        if day in ['Saturday', 'Sunday']:
            return 0.7
        elif 0 <= hour < 10 or 18 <= hour <= 23:
            return 0.8
        elif 10 <= hour < 18:
            return 1.2
        else:
            return 1.0

    # Extracting start_day, end_day, start_time, and end_time from id_start and id_end
    df['start_day'] = pd.to_datetime(df['id_start'], format='%d%H%M%S').dt.day_name()
    df['end_day'] = pd.to_datetime(df['id_end'], format='%d%H%M%S').dt.day_name()
    df['start_time'] = pd.to_datetime(df['id_start'], format='%d%H%M%S').dt.time
    df['end_time'] = pd.to_datetime(df['id_end'], format='%d%H%M%S').dt.time

    # Calculate the discount factor for each row based on start_time and start_day
    df['discount_factor'] = df.apply(lambda row: get_discount_factor(row['start_time'].hour, row['start_day']), axis=1)

    # Apply the discount factor to the toll rates for each vehicle
    vehicles = ['moto', 'car', 'rv', 'bus', 'truck']
    for vehicle in vehicles:
        df[vehicle] *= df['discount_factor']

    # Drop unnecessary columns
    df = df.drop(columns=['discount_factor'])

    return df
unrolled_data = unroll_distance_matrix(calculate_distance_matrix(data))
result = calculate_time_based_toll_rates(calculate_toll_rate(unrolled_data))
print(result)