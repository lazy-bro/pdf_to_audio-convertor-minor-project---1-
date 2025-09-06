import tkinter as tk
from tkinter import filedialog
import pyttsx3
import pdfplumber

def extract_text_from_pdf(pdf_file):
    text = ''
    with pdfplumber.open(pdf_file) as pdf:
        for page in pdf.pages:
            extracted_text = page.extract_text()
            if extracted_text:
                text += extracted_text + " "
    return text

def convert_text_to_audio(text, output_file, voice_name='Microsoft Zira Desktop'):
    engine = pyttsx3.init()
    voices = engine.getProperty('voices')
    selected_voice = None

    for voice in voices:
        if voice.name == voice_name:
            selected_voice = voice
            break

    if selected_voice is not None:
        engine.setProperty('voice', selected_voice.id)
    else:
        print(f"{voice_name}'s voice not found. Using the default voice.")

    engine.save_to_file(text, output_file)
    engine.runAndWait()

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF files", "*.pdf")])
    pdf_entry.delete(0, tk.END)
    pdf_entry.insert(0, file_path)

def browse_output_dir():
    output_dir = filedialog.askdirectory()
    output_entry.delete(0, tk.END)
    output_entry.insert(0, output_dir)

def convert_pdf_to_audio():
    pdf_file = pdf_entry.get()
    output_dir = output_entry.get()
    output_file = f"{output_dir}/output1.mp3"

    try:
        text = extract_text_from_pdf(pdf_file)
        convert_text_to_audio(text, output_file)
        result_label.config(text=f"Conversion successful. Audio saved to {output_file}")

    except Exception as e:
        result_label.config(text=f"An error occurred: {str(e)}")

# Create the main Tkinter window
root = tk.Tk()
root.title("PDF to Audio Converter")

# Create and place widgets
tk.Label(root, text="Select PDF File:").grid(row=0, column=0, padx=10, pady=5, sticky="e")
pdf_entry = tk.Entry(root, width=40)
pdf_entry.grid(row=0, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_pdf).grid(row=0, column=2, padx=5, pady=5)

tk.Label(root, text="Select Output Directory:").grid(row=1, column=0, padx=10, pady=5, sticky="e")
output_entry = tk.Entry(root, width=40)
output_entry.grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=browse_output_dir).grid(row=1, column=2, padx=5, pady=5)

tk.Button(root, text="Convert", command=convert_pdf_to_audio).grid(row=2, column=1, pady=10)

result_label = tk.Label(root, text="")
result_label.grid(row=3, column=0, columnspan=3, pady=10)

# Start the Tkinter event loop
root.mainloop()