import tkinter
import customtkinter
from Cyberminer import SearchEngine

class DataPoolApp:
    def __init__(self):
        self.search_engine = SearchEngine()
        self.words_set = set()
        self.all_results = []
        self.current_page = 1
        self.results_per_page = 10  # Default results per page
        self.previous_page = 1  # Store the previous page number

        # Initialize UI
        self.app = customtkinter.CTk()
        self.app.geometry("1920x800")
        self.app.title("DATAPOOL")
        self.build_ui()
        self.load_words_for_autocomplete()

    def build_ui(self):
        """Build the UI components."""
        customtkinter.set_appearance_mode("System")
        customtkinter.set_default_color_theme("blue")

        title = customtkinter.CTkLabel(self.app, text="DATAPOOL", font=("Arial", 24, "bold"))
        title.pack(padx=10, pady=20)

        # Search bar and search button next to it
        self.search_var = tkinter.StringVar()
        self.input_frame = customtkinter.CTkFrame(self.app)
        self.input_frame.pack(padx=10, pady=20)

        self.input_field = customtkinter.CTkEntry(
            self.input_frame, textvariable=self.search_var, width=400, height=40, placeholder_text="Enter search query..."
        )
        self.input_field.pack(side="left", padx=10)

        self.search_button = customtkinter.CTkButton(self.input_frame, text="Search", command=self.on_search)
        self.search_button.pack(side="left")

        # Suggestions Listbox with fixed size (static height)
        self.suggestions = tkinter.Listbox(self.app, height=5, width=30, font=("Arial", 12), selectmode=tkinter.SINGLE)
        self.suggestions.pack(pady=(0, 10))
        self.suggestions.bind("<ButtonRelease-1>", self.select_suggestion)

        # Frame for search results
        self.search_results_frame = customtkinter.CTkFrame(self.app)
        self.search_results_frame.pack(padx=10, pady=10, fill="both", expand=True)

        # Scrollable frame for search results
        self.scrollable_frame = customtkinter.CTkScrollableFrame(self.search_results_frame, width=1400, height=400)
        self.scrollable_frame.pack(padx=10, pady=10)

        # Pagination controls at the bottom
        self.pagination_frame = customtkinter.CTkFrame(self.app)
        self.pagination_frame.pack(pady=10, fill="x")

        self.previous_button = customtkinter.CTkButton(
            self.pagination_frame, text="Previous", command=self.previous_page_action, state="disabled"
        )
        self.previous_button.pack(side="left", padx=10)

        self.next_button = customtkinter.CTkButton(
            self.pagination_frame, text="Next", command=self.next_page_action, state="disabled"
        )
        self.next_button.pack(side="right", padx=10)

        # Results per page input and update button at the bottom
        self.results_per_page_frame = customtkinter.CTkFrame(self.app)
        self.results_per_page_frame.pack(pady=10, fill="x")

        self.results_per_page_label = customtkinter.CTkLabel(self.results_per_page_frame, text="Results per page:")
        self.results_per_page_label.pack(side="left", padx=10)

        self.results_per_page_entry = customtkinter.CTkEntry(
            self.results_per_page_frame, width=100, placeholder_text="Enter number"
        )
        self.results_per_page_entry.insert(0, "10")  # Default value
        self.results_per_page_entry.pack(side="left", padx=10)

        self.update_button = customtkinter.CTkButton(
            self.results_per_page_frame, text="Update Results per Page", command=self.update_results_per_page
        )
        self.update_button.pack(side="left", padx=10)

        # Initialize page view flag
        self.is_search_results = True  # Flag to track whether we are showing search results or content

        # Bind autocomplete function
        self.input_field.bind("<KeyRelease>", self.update_autocomplete)

    def load_words_for_autocomplete(self):
        """Load phrases and build mappings for word completion and next-word prediction."""
        self.word_map = {}  # Maps phrases to next words
        self.completion_set = set()  # Tracks all unique words for word completion
        try:
            with open("output.txt", "r", encoding="utf-8") as f:
                for line in f:
                    words = line.strip().split()
                    self.completion_set.update(words)  # Add all words for completions
                    for i in range(len(words)):
                        prefix = " ".join(words[:i])  # Sequence so far
                        next_word = words[i]
                        if prefix not in self.word_map:
                            self.word_map[prefix] = set()
                        self.word_map[prefix].add(next_word)
        except FileNotFoundError:
            print("Autocomplete file not found.")

    def update_autocomplete(self, event):
        """Update autocomplete suggestions dynamically based on input."""
        query = self.input_field.get().strip()  # Current input in the search bar

        # If no query is entered, clear suggestions
        if not query:
            self.suggestions.delete(0, tkinter.END)
            return

        # Split the input to check the last word typed
        words = query.split()
        if len(words) == 1:
            # Typing the first word: Find completions for the current word
            current_word = query
            suggestions = [word for word in self.completion_set if word.startswith(current_word)]
        else:
            # Predict next words based on the last completed word
            prefix = " ".join(words[:-1])  # All words except the last
            last_word = words[-1]
            # Fetch next-word suggestions and also refine completions for the last word
            next_words = self.word_map.get(prefix, [])
            suggestions = [word for word in next_words if word.startswith(last_word)]

        # Update the suggestions listbox
        self.suggestions.delete(0, tkinter.END)
        max_suggestions = self.suggestions.cget("height")
        for suggestion in sorted(suggestions)[:max_suggestions]:
            self.suggestions.insert(tkinter.END, suggestion)

    def select_suggestion(self, event):
        """Select an autocomplete suggestion."""
        selected = self.suggestions.curselection()
        if selected:
            suggestion = self.suggestions.get(selected)
            current_text = self.input_field.get().strip()
            last_space_index = current_text.rfind(" ")
            if last_space_index == -1:
                # Replace the current word with the suggestion
                self.input_field.delete(0, tkinter.END)
                self.input_field.insert(0, suggestion)
            else:
                # Append the suggestion after the last word
                self.input_field.delete(0, tkinter.END)
                new_text = f"{current_text[:last_space_index+1]}{suggestion}"
                self.input_field.insert(0, new_text)

    def on_search(self):
        """Perform search and initialize pagination."""
        query = self.input_field.get()
        self.all_results = self.search_engine.case_sensitive_search(query)
        self.current_page = 1  # Reset to the first page
        self.is_search_results = True  # Switch to search results view
        self.display_results()

    def display_results(self):
        """Display paginated search results."""
        # Clear previous content (if any)
        self.clear_search_results()

        if self.is_search_results:
            # Calculate start and end index for the current page
            start_idx = (self.current_page - 1) * self.results_per_page
            end_idx = start_idx + self.results_per_page
            results_to_display = self.all_results[start_idx:end_idx]

            if not results_to_display:
                result_label = customtkinter.CTkLabel(self.scrollable_frame, text="No Results Found", font=("Arial", 12))
                result_label.pack(fill="x", padx=5, pady=5)
            else:
                for url, score, content in results_to_display:
                    result_label = customtkinter.CTkLabel(
                        self.scrollable_frame,
                        text=url,
                        font=("Arial", 12),
                        cursor="hand2",
                        text_color="#0066cc"
                    )
                    result_label.pack(fill="x", padx=5, pady=5)
                    result_label.bind("<Button-1>", lambda e, content=content: self.show_content(content))

            # Update pagination buttons
            self.update_pagination_buttons()
        else:
            self.show_back_button()

    def update_results_per_page(self):
        """Update the number of results per page based on user input."""
        try:
            new_value = int(self.results_per_page_entry.get())
            if new_value > 0:
                self.results_per_page = new_value
                self.current_page = 1  # Reset to the first page after updating
                self.display_results()  # Re-display results with the updated page size
            else:
                self.show_error_message("Please enter a positive number.")
        except ValueError:
            self.show_error_message("Invalid input. Please enter a valid number.")

    def show_error_message(self, message):
        """Show error message to the user."""
        error_label = customtkinter.CTkLabel(self.app, text=message, font=("Arial", 12), text_color="red")
        error_label.pack(pady=10)

    def show_content(self, content):

        self.previous_page = self.current_page
        
        self.is_search_results = False  
        self.clear_search_results()  

     
        content_label = customtkinter.CTkLabel(self.scrollable_frame, text=content, font=("Arial", 12), wraplength=1400)
        content_label.pack(padx=10, pady=10)

     
        back_button = customtkinter.CTkButton(self.scrollable_frame, text="Back", command=self.back_to_results)
        back_button.pack(pady=10)

    def back_to_results(self):
        """Switch back to displaying search results and restore the previous page."""
        self.is_search_results = True
        self.current_page = self.previous_page  
        self.display_results()  

        # Scroll to the top of the scrollable frame
        #self.scrollable_frame._scrollbar.set(0, 0)
        self.scrollable_frame._canvas.yview_moveto(0)

    def clear_search_results(self):
        """Clear the current search results."""
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    def update_pagination_buttons(self):
        """Update the state of pagination buttons."""
        if self.current_page > 1:
            self.previous_button.configure(state="normal")
        else:
            self.previous_button.configure(state="disabled")

        if self.current_page * self.results_per_page < len(self.all_results):
            self.next_button.configure(state="normal")
        else:
            self.next_button.configure(state="disabled")

    def previous_page_action(self):
        """Navigate to the previous page."""
        if self.current_page > 1:
            self.current_page -= 1
            self.display_results()

    def next_page_action(self):
        """Navigate to the next page."""
        if self.current_page * self.results_per_page < len(self.all_results):
            self.current_page += 1
            self.display_results()

# Run the app
if __name__ == "__main__":
    app = DataPoolApp()
    app.app.mainloop()
