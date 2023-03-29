import os
import PyPDF2
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def extract_text(folder_path):
    pdf_files = [f for f in os.listdir(folder_path) if f.endswith('.pdf')]
    corpus = []
    filenames = []
    for pdf_file in pdf_files:
        pdf_file_path = os.path.join(folder_path, pdf_file)
        with open(pdf_file_path, 'rb') as f:
            reader = PyPDF2.PdfFileReader(f)
            text = ''
            for page in reader.pages:
                text += page.extractText()
            corpus.append(text)
            filenames.append(pdf_file)
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(corpus)
    feature_names = vectorizer.get_feature_names()
    return tfidf_matrix, feature_names, filenames


def select_folder_path():
    folder_path = filedialog.askdirectory()
    if folder_path:
        global tfidf_matrix, feature_names, filenames, vectorizer
        tfidf_matrix, feature_names, filenames = extract_text(folder_path)
        vectorizer = TfidfVectorizer()


def search():
    query = search_entry.get()
    query_tokens = query.lower().split()
    query_vector = vectorizer.transform([' '.join(query_tokens)])
    similarity_scores = cosine_similarity(tfidf_matrix, query_vector)
    results = []
    for i, score in enumerate(similarity_scores):
        if score > 0:
            results.append((filenames[i], score[0]))
    results.sort(key=lambda x: x[1], reverse=True)
    search_listbox.delete(0, END)
    for result in results:
        search_listbox.insert(END, result[0])


root = Tk()
root.title("PDF Text Search")
root.geometry("600x500")

select_folder_label = Label(root, text="Select PDF Folder")
select_folder_label.pack(pady=(20, 10))

select_folder_button = Button(root, text="Select", command=select_folder_path)
select_folder_button.pack()

search_label = Label(root, text="Enter Search Query")
search_label.pack(pady=(20, 10))

search_entry = Entry(root)
search_entry.pack()

search_button = Button(root, text="Search", command=search)
search_button.pack(pady=(10, 20))

search_listbox = Listbox(root, height=20, width=80)
search_listbox.pack()

root.mainloop()
