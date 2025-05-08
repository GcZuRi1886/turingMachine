from turing_function import TuringFunction, EMPTY

def read_binary_data() -> str:
    """
    Reads binary data from the console.
    
    Returns:
        str: The binary data entered by the user.
    """
    data = input("Enter the binary data: ")
    if not all(char in '01' for char in data):
        raise ValueError("Invalid binary data")
    return data

def read_decimal_data() -> str:
    """
    Reads decimal data from the console.
    
    Returns:
        str: The decimal data entered by the user.
    """
    data = input("Enter the decimal data: ")
    if not data.isdigit():
        raise ValueError("Invalid decimal data")
    return bin(int(data))[2:]

def read_data_from_console() -> str:
    """
    Reads data from the console.
    
    Returns:
        str: The data entered by the user.
    """
    choice = input("Do you want to enter the data binarily (1) or in decimal (2)? ")
    if choice == '1':
        return read_binary_data()
    elif choice == '2':
        return read_decimal_data()
    else:
        raise ValueError("Invalid choice")

def read_data_from_file() -> str:
    """
    Reads data from a file.
    
    Returns:
        str: The data read from the file.
    """
    filename = input("Enter the filename: ")
    with open(filename, 'r') as file:
        data = file.read().strip()
    print(f"Data read from {filename}: {data}")
    if not all(char in '01' for char in data):
        try:
            data = bin(int(data))[2:]
        except ValueError:
            raise ValueError("Invalid binary data")
    return data

def parse_functions_from_binary(data: str) -> list[TuringFunction]:
    """
    Parses binary data into a list of strings and a string.
    
    Args:
        data (str): The binary data as a string.
    
    Returns:
        tuple: A tuple containing a list of strings and a string.
    """

    functions = []
    for function_str in data.split("11"):
        if function_str:
            actions = function_str.split("1")
            if len(actions) != 5:
                raise ValueError("Invalid function format")
            function = TuringFunction(
                state=actions[0],
                read_symbol=actions[1],
                next_state=actions[2],
                write_symbol=actions[3],
                move_direction=actions[4]
            )
            functions.append(function)
    return functions

def read_input_for_tm() -> str:
    """
    Reads input from the console.
    
    Returns:
        str: The input entered by the user.
    """
    data = input("Enter the input for the Turingmachine: ")
    while not all(char in '01' for char in data):
        print("Invalid input data. Please enter binary data.")
        data = input("Enter the input for the Turingmachine: ")
    return data

def execute_turing_machine(functions: list[TuringFunction], band: str, step_mode: bool) -> str:
    """
    Executes the Turing machine with the given functions and input string.
    
    Args:
        functions (list[TuringFunction]): The list of Turing functions.
        input_str (str): The input string for the Turing machine.
        step_mode (bool): Whether to run in step mode or not.
    
    Returns:
        str: The result of the Turing machine execution.
    """
    pointer_index = 0
    current_state = 1
    counter = 0
    while True:
        state_functions = [function for function in functions if function.state == current_state]
        current_function = None
        counter += 1
        for function in state_functions:
            if function.get_function_by_symbol(band[pointer_index]):
                current_function = function
                break
        if current_function is None:
            break
        if step_mode:
            print_step_mode(band, pointer_index, current_state, counter)

        band = band[:pointer_index] + current_function.write_symbol + band[pointer_index + 1:]
        pointer_index += current_function.move_direction.value
        current_state = current_function.next_state

        if pointer_index < 0:
            pointer_index = 0
            band = EMPTY + band
        elif pointer_index >= len(band):
            band += EMPTY
        # print(f"Current state: {current_state}, Pointer index: {pointer_index}, Input string: {band}")

    result = band.replace(EMPTY, "")
    return result

def print_step_mode(band: str, pointer_index: int, current_state: int, counter: int):
    """
    Prints the current state of the Turing machine in step mode.
    
    Args:
        band (str): The current state of the Turing machine.
        pointer_index (int): The current index of the pointer.
        current_state (int): The current state of the Turing machine.
        counter (int): The current step number.
    """
    print(f"Current state: {current_state}, Pointer index: {pointer_index}, Band: {band[:pointer_index]}*{band[pointer_index:]}, Step number: {counter}")

def main():
    print("Select on how you want to enter the data:")
    print("1. Enter data manually")
    print("2. Read data from a file")
    choice = input("Enter your choice (1 or 2): ")
    data = ""
    if choice == '1':
        data = read_data_from_console()
    elif choice == '2':
        data = read_data_from_file()
    else:
        raise ValueError("Invalid choice")
    
    step_mode_choice = input("Do you want to run the Turing machine in step mode? (y/n): ")
    if step_mode_choice.lower() == 'y':
        print("Running in step mode...")
        step_mode = True
    elif step_mode_choice.lower() == 'n':
        print("Running in normal mode...")
        step_mode = False
    else:
        raise ValueError("Invalid choice")

    functions = parse_functions_from_binary(data)
    input_str = read_input_for_tm()
    
    result = execute_turing_machine(functions, input_str, step_mode)
    print(f"Final result: {result}")

if __name__ == "__main__":
    main()