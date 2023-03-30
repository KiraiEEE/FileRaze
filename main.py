import os
import fitz
from tkinter import *
from tkinter import filedialog
from sklearn.feature_extraction.text import TfidfVectorizer

def get_pdf_content(pdf_path):
    with fitz.open(pdf_path) as pdf:
        content = ""
        for page in pdf:
            content += page.get_text("text")
        return content.lower()

def get_pdf_files(directory):
    pdf_files = []
    for filename in os.listdir(directory):
        if filename.endswith('.pdf'):
            pdf_files.append(os.path.join(directory, filename))
    return pdf_files

def search_query(query, documents, file_names):
    tfidf_vectorizer = TfidfVectorizer()
    tfidf_matrix = tfidf_vectorizer.fit_transform(documents)
    query_words = query.split()
    query_tfidf = tfidf_vectorizer.transform([query])
    scores = (query_tfidf * tfidf_matrix.T).A[0]
    results = []
    for i, score in enumerate(scores):
        if score > 0 and all(word.lower() in documents[i].lower() for word in query_words):
            results.append((file_names[i], score))
    return results

def browse_directory():
    global directory_entry
    directory = filedialog.askdirectory()
    directory_entry.delete(0, END)
    directory_entry.insert(0, directory)

def search_files():
    query = query_entry.get()
    directory = directory_entry.get()
    pdf_files = get_pdf_files(directory)
    pdf_contents = [get_pdf_content(pdf_file) for pdf_file in pdf_files]
    results = search_query(query, pdf_contents, pdf_files)
    result_listbox.delete(0, END)
    if len(results) > 0:
        sorted_results = sorted(results, key=lambda x: x[1], reverse=True)
        for pdf_file, score in sorted_results:
            result_listbox.insert(END, os.path.basename(pdf_file))
    else:
        result_listbox.insert(END, 'No results found')

def open_file(event):
    widget = event.widget
    selection = widget.curselection()
    if selection:
        index = selection[0]
        pdf_file = result_listbox.get(index)
        os.startfile(pdf_file)

root = Tk()
root.title('FileRaze')
root.geometry('550x580')
root.configure(bg='#212121')
root.iconbitmap('icon.ico')

logo = PhotoImage(file="logo.png")
logo_label = Label(root, image=logo, bg="#1f1f1f")
logo_label.grid(row=0, column=1, padx=10, pady=10)

directory_label = Label(root, text='Select folder :', bg='#212121', fg='white')
directory_label.grid(row=1, column=0, padx=40, pady=20)
directory_entry = Entry(root,width= 40)
directory_entry.grid(row=1, column=1, padx=10, pady=10)

browse_button = Button(root, text='Browse', command=browse_directory, bg='#616161', fg='white')
browse_button.grid(row=1, column=2, padx=10, pady=10)

query_label = Label(root, text='Enter words :', bg='#212121', fg='white')
query_label.grid(row=2, column=0, padx=10, pady=10)
query_entry = Entry(root,width= 40)
query_entry.grid(row=2, column=1, padx=10, pady=10)


search_button = Button(root, text='Search', command=search_files, bg='#03a9f4', fg='white',width= 20,height=2)
search_button.grid(row=3, column=1, padx=10, pady=10)

result_label = Label(root, text='Results:', bg='#212121', fg='white')
result_label.grid(row=4, column=1, padx=10, pady=10)
result_listbox = Listbox(root, bg='#424242', fg='white',width= 40,height=11)
result_listbox.grid(row=5, column=1, padx=10, pady=10)
result_listbox.bind('<Double-Button-1>', open_file)

kiraieee = Label(root, text='by Ben Fekih Akram', bg='#212121', fg='#dddddd')
kiraieee.grid(row=6, column=2, padx=2, pady=10)

root.mainloop()
