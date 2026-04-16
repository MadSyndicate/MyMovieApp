# Source - https://stackoverflow.com/a/287944
class Bcolors:
    """
    holds the used style colors and formats
    """
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def get_input(prompt, cast_type, error_msg, limit=0):
    """
    helper-function to validate different input types and respond to the user
    what went wrong if needed

    :param prompt: Print out to get user input
    :param cast_type: the expected input type we want to get from the user
    :param error_msg: in case casting to cast_type fails, this gets printed out
    :param limit: if not specified means no limit; otherwise error message with input limit
    :return: returns the user input in the given cast_type or prints out an error message
    """
    while True:
        if cast_type == str:
            value = input(f"{Bcolors.BOLD}{prompt}{Bcolors.ENDC}")
            if len(value) == 0:
                print(error_msg)
                continue
            return value

        try:
            value = cast_type(input(prompt))
            if limit != 0 and value > limit:
                print(f"{Bcolors.FAIL}Input {value} is bigger then allowed limit ({limit}). "
                      f"Please try again.{Bcolors.ENDC}")
                continue
            return value
        except ValueError:
            print(error_msg)
