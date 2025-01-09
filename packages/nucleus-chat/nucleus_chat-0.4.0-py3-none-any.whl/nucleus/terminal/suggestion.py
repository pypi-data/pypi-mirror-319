from prompt_toolkit import PromptSession
from prompt_toolkit.completion import Completer, Completion
from prompt_toolkit.key_binding import KeyBindings
from prompt_toolkit.keys import Keys
from prompt_toolkit.shortcuts import CompleteStyle, PromptSession
from prompt_toolkit.styles import Style

import os

PLACEHOLDER = [('gray', 'ask me anything')]

FILE_DISPLAY_PLACEHOLDER = [('gray', '')]


class FilePathCompleter(Completer):

    def handle_tags(self, text):
        """
        """
        if '!' in text:
            if len(text)==1:
                text = ''
            else:
                text = text[1:]
        return text

    def get_completions(self, document, complete_event):
        text = document.text_before_cursor

        text = self.handle_tags(text)

        word = text.split(" ")[-1]

        dirname, partial_name = os.path.split(word)

        if not dirname:  # Default to the current directory if none is specified
            dirname = "."
        
        try:
            # List entries in the directory
            if os.path.isdir(dirname):
                entries = os.listdir(dirname)
            else:
                entries = []
        except FileNotFoundError:
            return

        # Filter entries based on partial matching
        for entry in entries:
            full_path = os.path.join(dirname, entry)
            if partial_name.lower() in entry.lower():  # Case-insensitive substring match
                # Add a trailing '/' to directories
                display = entry if os.path.isdir(full_path) else entry                
                yield Completion(
                    display,
                    start_position=-len(partial_name),
                    # display_meta="Directory" if os.path.isdir(full_path) else "File",
                )


# Custom key bindings to handle TAB key press
kb = KeyBindings()


@kb.add(Keys.Tab)
def _(event):
    "Handle tab key press for completion."
    b = event.current_buffer
    if b.complete_state:
        b.complete_next()
    return True


custom_style = Style.from_dict({
    'prompt': 'bold green',  # Style for the prompt text
    '': 'white',           # Default text style
})


session = PromptSession(completer=FilePathCompleter(), 
                        key_bindings=kb, 
                        complete_style=CompleteStyle.MULTI_COLUMN,
                        style=custom_style
                        )



def main():


    session = PromptSession(completer=FilePathCompleter(), 
                            key_bindings=kb, 
                            complete_style=CompleteStyle.MULTI_COLUMN,
                            style=custom_style
                            )
    while True:
        try:
            user_input = session.prompt("Enter path: ")
            print(f"You selected: {user_input}")
        except (KeyboardInterrupt, EOFError):
            break


if __name__ == "__main__":
    main()

