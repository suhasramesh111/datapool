# import tkinter
# import customtkinter
# import csv 


# class Search: 
#     def __init__(self,path="Index.csv"):
#         self.data=[]
#         with open(path,'r') as file:
#             content=csv.reader(file)
#             for line in content:
#                 self.data.append(line)
    
#     def fetch_word(self,word):
#         self.output=[]
#         self.output.clear()
#         for line in self.data:
#             if word in line:
#                 self.output.append(line)
#                 #break
#             else:
#                 continue   
#                 #output.append("LineNotFound")
#         if len(self.output)==0:
#             print("No Results Found")
#         else:
#             return (self.output)
    


# # print(Search().fetch_word(w))

# # System setting
# customtkinter.set_appearance_mode("System")
# customtkinter.set_default_color_theme("blue")

# # app frame 
# app = customtkinter.CTk()
# app.geometry("720x480")
# app.title("DATAPOOL")

# # adding the UI elements
# title=customtkinter.CTkLabel(app,text="DATAPOOL")
# title.pack(padx=10,pady=10)


# #input
# search_word = tkinter.StringVar()
# input=customtkinter.CTkEntry(app,width=350,height=40 ,textvariable=search_word)
# input.pack()


# #creating the search instance
# search_instance = Search()
# result_label = customtkinter.CTkLabel(app, text="")
# result_label.pack(padx=10, pady=10)


# def on_search():
#     word = input.get()  # Get the text from the input
#     result = search_instance.fetch_word(word) 
#     #print(f"Search result: {result}")  # You can print or display the result
#     if isinstance(result, list):
#         result_text = "\n".join([", ".join(row) for row in result])  
#     else:
#         result_text = "No Results Found"#result "" # In case of "No Results Found"
    
#     result_label.configure(text=result_text)

# # Add the search button
# search_button = customtkinter.CTkButton(app, text="Search", command=on_search)
# search_button.pack(padx=10, pady=10)

# # finished=customtkinter.CTkLabel(app,search_button)
# # finished.pack()

# # run the app as a loop 
# app.mainloop()


import tkinter
import customtkinter
import csv


class Search:
    def __init__(self, path="Index.csv"):
        self.data = []
        with open(path, 'r') as file:
            content = csv.reader(file)
            for line in content:
                self.data.append(line)

    def fetch_word(self, word):
        self.output = []
        self.output.clear()
        for line in self.data:
            if word in line:
                self.output.append(line)
            else:
                continue
        if len(self.output) == 0:
            return "No Results Found"
        else:
            return self.output


# System setting
customtkinter.set_appearance_mode("System")
customtkinter.set_default_color_theme("blue")

# app frame
app = customtkinter.CTk()
app.geometry("720x480")
app.title("DATAPOOL")

# adding the UI elements
title = customtkinter.CTkLabel(app, text="DATAPOOL")
title.pack(padx=10, pady=10)

# input
search_word = tkinter.StringVar()
input = customtkinter.CTkEntry(app, width=350, height=40, textvariable=search_word)
input.pack(pady=(0, 10))

# creating the search instance
search_instance = Search()

# Scrollable frame for results
scrollable_frame = customtkinter.CTkScrollableFrame(app, width=680, height=300)
scrollable_frame.pack(padx=10, pady=10)

# Function to perform the search and display results
def on_search():
    for widget in scrollable_frame.winfo_children():
        widget.destroy()  # Clear previous results from the scrollable frame

    word = input.get()  # Get the text from the input
    result = search_instance.fetch_word(word)

    if isinstance(result, list):
        for row in result:
            result_text = ", ".join(row)
            result_label = customtkinter.CTkLabel(scrollable_frame, text=result_text, anchor="w")
            result_label.pack(fill="x", padx=5, pady=2)
    else:
        result_label = customtkinter.CTkLabel(scrollable_frame, text="No Results Found")
        result_label.pack(fill="x", padx=5, pady=2)

# Add the search button
search_button = customtkinter.CTkButton(app, text="Search", command=on_search)
search_button.pack(pady=10)

# run the app as a loop
app.mainloop()
