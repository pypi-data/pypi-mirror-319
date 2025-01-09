import itertools
import sys
import time
from rich.markdown import Markdown
from rich.console import Console
from rich.text import Text
from langchain_openai import ChatOpenAI
from prompt_toolkit.formatted_text import HTML

import re
import subprocess
import threading

from nucleus.logger import log

console = Console()

class MessagePrinter:
    def __init__(self):
        self.console = Console()
        self.style="#fafcfb"

    def system_message(self, message):
        """
        Prints a system message with specific styling.
        """
        system_text = Text(message, style="yellow")
        self.console.print(system_text)

    def user_message(self, message):
        """
        Prints a user message with Markdown rendering.
        """
        user_text = Text(f"{message}")
        self.console.print(user_text, style=self.style)

    def assistant_message(self, message, type=None):
        """
        Prints an assistant message with optional Markdown rendering.
        """
        if type=='command':
            print("\n"+ message)
        else:
            # pprint(message)
            assistant_text = Markdown(f"<br>{message}")
            self.console.print(assistant_text)

def command_provider(message , model_name):
    """
    """

    llm = None

    if model_name == 'openai':
        llm = ChatOpenAI(
                model="gpt-4o",
                temperature=0,
                max_tokens=None,
                timeout=None,
                max_retries=2
            )
        
    if llm is not None:
        message = f"Be precise in your response. Here is the question: {message}"
        response = llm.invoke(message)
    else:
        return "No LLM chosen"
    
    return response.content

def format_message(message, role):
    """
    """
    if role=='user':
        return (
            'human', message
        )
    else:
        return (
            'assistant', message
        )


def show_spinner(stop_event):
    """Display a rotating cursor."""
    spinner = itertools.cycle(["|", "/", "-", "\\"])
    while not stop_event.is_set():
        sys.stdout.write(f"\rExecuting... {next(spinner)}")
        sys.stdout.flush()
        time.sleep(0.1)
    sys.stdout.write("\rExecution complete.      \n")
    sys.stdout.flush()


def execute_command(command, message_printer=None):
    if message_printer:
        stop_event = threading.Event()
        spinner_thread = threading.Thread(target=show_spinner, args=(stop_event,))
        message_printer.system_message(f"\nExecuting command -  {command}\n")
        spinner_thread.start()
    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if message_printer:
        stop_event.set()
        spinner_thread.join()
    return result


def get_response(response, message_printer, session):

    try:

        message_printer.assistant_message(response)

        commands = extract_command(response)

        if commands:
            for i, command in enumerate(commands, start=1):
                res = confirm_ask(i)
                if res:
                    if res=='edit':
                        text = HTML(f'<ansiblue>> {command}</ansiblue> ')

                        command = session.prompt("\nedit: ", default=command, placeholder='')

                    result = execute_command(command, message_printer)
                    if result.stderr:
                        print("Error while executing")
                        message_printer.assistant_message(result.stderr, type='command')
                    else:
                        # print_response(f"command executed \n {result.stdout}", type='command')
                        message_printer.assistant_message(f"{result.stdout}", type='command')

            # # ask
            
            
            #     if res=='edit':
                    
                
            #         stop_event = threading.Event()
            #         spinner_thread = threading.Thread(target=show_spinner, args=(stop_event,))
            #         # print_response(command)
            #         message_printer.system_message(f"\nExecuting command -  {command}\n")
            #         spinner_thread.start()
            #         result = subprocess.run(command, shell=True, capture_output=True, text=True)
            #         # Stop the spinner
            #         stop_event.set()
            #         spinner_thread.join()
                    
            #         if result.stderr:
            #             print("Error while executing")
            #             message_printer.assistant_message(result.stderr, type='command')
            #         else:
            #             # print_response(f"command executed \n {result.stdout}", type='command')
            #             message_printer.assistant_message(f"{result.stdout}", type='command')

    except Exception as e:
        log.error("Error:", e)

def confirm_ask(command_index):
    """
    Prompt the user to decide whether to run or not.
    """
    if command_index == 1:
        command_txt = f"command"
    elif command_index == 2:
        command_txt = f"2nd command"
    elif command_index == 3:
        command_txt = f"3rd command"
    else:
        command_txt = f"{command_index}th command"

    ask_text = f"\n[bold cyan]Do you want to run {command_txt}?[/bold cyan] [green](Yes (y) / No (n))[/green] or [yellow]Edit (e):[/yellow]"
    # console.print(ask_text, end=" ")
    response = console.input(ask_text).strip().lower()
    if response in ['yes', 'y']:
        return True
    elif response in ['no', 'n']:
        return False
    elif response in ['edit', 'e']:
        return "edit"
    else:
        print("Invalid input. Please respond with 'Yes' or 'No'.")
        confirm_ask(command_index)  # Re-prompt the user

def extract_command(text):
    """
    Extracts all commands enclosed within ```bash ... ``` from the given text.

    Args:
        text (str): The input string containing commands.

    Returns:
        list: A list of extracted commands as strings.
    """
    # Regular expression to match text inside triple backticks with bash
    command_pattern = r"```bash\s+([\s\S]*?)```"
    commands = re.findall(command_pattern, text)
    # Strip leading and trailing whitespace from each command
    return [cmd.strip() for cmd in commands]

# Example usage
if __name__ == "__main__":
    printer = MessagePrinter()

    # Print system messages
    printer.print_system_message("Type commands as usual. Ask anything you want.")
    printer.print_system_message("Type 'exit' or 'quit' to stop the program.\n")

    # Print user message
    printer.print_user_message("Hello, how do I use this program?")

    # Print assistant message
    printer.print_assistant_message("Sure! Let me explain how it works.")

    # Print messages with Markdown rendering
    printer.print_user_message("### This is a Markdown heading")
    printer.print_assistant_message("**This text is bold in Markdown**")

