import sys

# Set the recursion limit to 1500
sys.setrecursionlimit(1500)

# Function to read a cube file and return the number of variables, number of cubes, and the cubes themselves
def read_cube_file(file_path):
    try:
        with open(file_path, 'r') as file:
            num_variables = int(file.readline().strip())  # Read number of variables
            num_cubes = int(file.readline().strip())  # Read number of cubes
            cubes = []
            for _ in range(num_cubes):
                line = file.readline().strip()  # Read each line (cube)
                parts = list(map(int, line.split()))  # Split the line into integers
                num_non_dont_cares = parts[0]  # First number is the count of non-don't-care variables
                variables = parts[1:num_non_dont_cares + 1]  # Next numbers are the variables
                formatted_variables = ['11'] * num_variables  # Initialize all to 'don't-care'
                for var in variables:
                    if var > 0:
                        formatted_variables[var - 1] = '01'  # Positive variable
                    else:
                        formatted_variables[-var - 1] = '10'  # Negative variable
                cubes.append(formatted_variables)
            return num_variables, num_cubes, cubes
    except FileNotFoundError:
        print(f"The file {file_path} does not exist.")
        return None
    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# Function to process the cubes (currently just a placeholder)
def process_cubes(cubes):
    return cubes

# Function to compute the complement of the cubes (using recursion)
def complement(result, depth=0, max_depth=1000):
    if depth > max_depth:
        raise RecursionError("Maximum recursion depth exceeded")

    num_variables, num_cubes, cubes = result
    processed_cubes = process_cubes(cubes)

    if num_cubes == 0:
        return all_dont_care_cube(num_variables)

    elif contains_all_dont_care(processed_cubes):
        return empty_cube_list()

    elif len(processed_cubes) == 1:
        return complement_single_cube(processed_cubes[0])
    else:
        var_index = select_most_binate_variable(processed_cubes, num_variables)
        x = f"x{var_index + 1}"
        not_x = f"x{var_index + 1}'"
        
        # Compute positive and negative cofactors
        P_num_vars, P_cubes = positive_cofactor(processed_cubes, var_index)
        N_num_vars, N_cubes = negative_cofactor(processed_cubes, var_index)
        
        # Recursively compute complements
        P = complement((P_num_vars, len(P_cubes), P_cubes), depth + 1, max_depth)
        N = complement((N_num_vars, len(N_cubes), N_cubes), depth + 1, max_depth)
        
        # Combine results using AND and OR operations
        P = and_operation(x, P)
        N = and_operation(not_x, N)
        result = or_operation(P, N)
        
    return result

# Function to return a cube with all 'don't-care' values
def all_dont_care_cube(num_variables):
    return [['11'] * num_variables]

# Function to return an empty list of cubes
def empty_cube_list():
    return []

# Function to complement a single cube
def complement_single_cube(cube):
    complemented_cubes = []
    for i in range(len(cube)):
        if cube[i] != "11":
            new_cube = ["11"] * len(cube)
            if cube[i] == "01":
                new_cube[i] = "10"
            elif cube[i] == "10":
                new_cube[i] = "01"
            complemented_cubes.append(new_cube)
    return complemented_cubes

# Function to check if any cube contains all 'don't-care' values
def contains_all_dont_care(cubes):
    for cube in cubes:
        if all(var == '11' for var in cube):
            return True
    return False

# Function to select the most binate variable (one with both positive and negative occurrences)
def select_most_binate_variable(cubes, num_variables):
    variable_stats = {i: {"true": 0, "complement": 0} for i in range(num_variables)}

    for cube in cubes:
        for i in range(num_variables):
            if cube[i] == "01":
                variable_stats[i]["true"] += 1
            elif cube[i] == "10":
                variable_stats[i]["complement"] += 1

    binate_variables = []
    max_occurrences = 0

    for var, stats in variable_stats.items():
        if stats["true"] > 0 and stats["complement"] > 0:
            total_occurrences = stats["true"] + stats["complement"]
            if total_occurrences > max_occurrences:
                max_occurrences = total_occurrences
                binate_variables = [var]
            elif total_occurrences == max_occurrences:
                binate_variables.append(var)

    if binate_variables:
        min_difference = float('inf')
        best_var = None
        for var in binate_variables:
            difference = abs(variable_stats[var]["true"] - variable_stats[var]["complement"])
            if difference < min_difference:
                min_difference = difference
                best_var = var
            elif difference == min_difference and (best_var is None or var < best_var):
                best_var = var
        return best_var

    unate_variables = []
    max_occurrences = 0
    for var, stats in variable_stats.items():
        if stats["true"] > 0 and stats["complement"] == 0:
            if stats["true"] > max_occurrences:
                max_occurrences = stats["true"]
                unate_variables = [var]
            elif stats["true"] == max_occurrences:
                unate_variables.append(var)
        elif stats["complement"] > 0 and stats["true"] == 0:
            if stats["complement"] > max_occurrences:
                max_occurrences = stats["complement"]
                unate_variables = [var]
            elif stats["complement"] == max_occurrences:
                unate_variables.append(var)

    if unate_variables:
        return min(unate_variables)

    return 0

# Function to compute the positive cofactor of cubes with respect to a variable
def positive_cofactor(cubes, var_index):
    cofactor = []
    for cube in cubes:
        if cube[var_index] in ["01", "11"]:
            new_cube = cube[:]
            if cube[var_index] == "01":
                new_cube[var_index] = "11"
            cofactor.append(new_cube)
    return len(cubes[0]), cofactor

# Function to compute the negative cofactor of cubes with respect to a variable
def negative_cofactor(cubes, var_index):
    cofactor = []
    for cube in cubes:
        if cube[var_index] in ["10", "11"]:
            new_cube = cube[:]
            if cube[var_index] == "10":
                new_cube[var_index] = "11"
            cofactor.append(new_cube)
    return len(cubes[0]), cofactor

# Function to perform the AND operation on a variable and a set of cubes
def and_operation(variable, cubes):
    var_index = int(variable[1:-1]) - 1 if variable.endswith("'") else int(variable[1:]) - 1
    
    new_cubes = []
    for cube in cubes:
        new_cube = cube[:]
        if not variable.endswith("'"):
            new_cube[var_index] = "01"
        else:
            new_cube[var_index] = "10"
        new_cubes.append(new_cube)
    return new_cubes

# Function to perform the OR operation on two sets of cubes
def or_operation(P, N):
    return P + N

# Function to write the result cubes to an output file
def write_output_file(file_path, data):
    try:
        with open(file_path, 'w') as file:
            num_variables = len(data[0]) if data else 0
            num_cubes = len(data)
            file.write(f"{num_variables}\n")
            file.write(f"{num_cubes}\n")
            for cube in data:
                non_dont_cares = [
                    i + 1 if var == "01" else -(i + 1)
                    for i, var in enumerate(cube)
                    if var != "11"
                ]
                file.write(f"{len(non_dont_cares)} {' '.join(map(str, non_dont_cares))}\n")
    except Exception as e:
        print(f"An error occurred while writing to the file: {e}")

# Main function to read input file, compute complement, and write output file
def main():
    file_path = 'C:\\Users\\hp\\Desktop\\VLSI\\input.txt'
    file_path_output = 'C:\\Users\\hp\\Desktop\\VLSI\\output.txt'
    result = read_cube_file(file_path)
    if result:
        F_prime = complement(result)
        write_output_file(file_path_output, F_prime)

# Execute main function when script is run directly
if __name__ == "__main__":
    main()
