from tkinter import *
from mydb import Database
from tkinter import messagebox

from myapi import analyze_sentiment, extract_entities


class NLPApp:


    def __init__(self):

        # create db object
        self.dbo = Database()


        #login ka gui load krna hai
        self.root = Tk()
        self.root.title('NLP App')
        try:
            self.root.iconbitmap('resources/NLPicon.ico')
        except:
            pass
        self.root.geometry('700x600')
        self.root.configure(bg='#FDF0D5')

        self.login_gui()
        self.root.mainloop()

    def login_gui(self):

        self.clear()

        heading = Label(self.root,text='Natural Language Processing App',bg='#FDF0D5',fg='#780000')
        heading.pack(pady=(30,30))
        heading.configure(font=('serif',28,'bold'))

        label1 = Label(self.root,text='Enter Email',bg='#FDF0D5',fg='#003049',justify="left")
        label1.configure(font=('serif', 12, 'bold'))
        label1.pack(pady=(10,10))

        self.email_input = Entry(self.root,width=50)
        self.email_input.pack(pady=(5,10),ipady=7)

        label2 = Label(self.root, text='Enter Password',bg='#FDF0D5',fg='#003049')
        label2.configure(font=('serif', 12, 'bold'))
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50,show='*')
        self.password_input.pack(pady=(5, 10), ipady=7)

        login_button = Button(self.root,text='Login',fg='#003049',width=15,height=2,command=self.perform_login)
        login_button.pack(pady=(20,10))

        label3 = Label(self.root, text='Not a Member ?',bg='#FDF0D5',fg='#003049')
        label3.pack(pady=(20,10))

        redirect_button = Button(self.root,text='Register Now',fg='#003049',command=self.register_gui)
        redirect_button.pack(pady=(10,10))

    def register_gui(self):
        self.clear()

        heading = Label(self.root, text='Natural Language Processing App', bg='#FDF0D5', fg='#780000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('serif', 28, 'bold'))

        label0 = Label(self.root, text='Enter Name', bg='#FDF0D5', fg='#003049', justify="left")
        label0.configure(font=('serif', 12, 'bold'))
        label0.pack(pady=(10, 10))

        self.name_input = Entry(self.root, width=50)
        self.name_input.pack(pady=(5, 10), ipady=7)

        label1 = Label(self.root, text='Enter Email', bg='#FDF0D5', fg='#003049', justify="left")
        label1.configure(font=('serif', 12, 'bold'))
        label1.pack(pady=(10, 10))

        self.email_input = Entry(self.root, width=50)
        self.email_input.pack(pady=(5, 10), ipady=7)

        label2 = Label(self.root, text='Enter Password', bg='#FDF0D5', fg='#003049')
        label2.configure(font=('serif', 12, 'bold'))
        label2.pack(pady=(10, 10))

        self.password_input = Entry(self.root, width=50, show='*')
        self.password_input.pack(pady=(5, 10), ipady=7)

        register_button = Button(self.root, text='Register', width=15, height=2, fg='#003049', command=self.perform_registration)
        register_button.pack(pady=(20, 10))

        label3 = Label(self.root, text='Already a Member ?', bg='#FDF0D5', fg='#003049')
        label3.pack(pady=(20, 10))

        redirect_button = Button(self.root, text='Login Now', fg='#003049', command=self.login_gui)
        redirect_button.pack(pady=(10, 10))

    def clear(self):
        for i in self.root.pack_slaves():
            i.destroy()

    def perform_registration(self):
        # fetch data from the gui
        name = self.name_input.get()
        email = self.email_input.get()
        password = self.password_input.get()

        response = self.dbo.add_data(name,email,password)

        if response:
            messagebox.showinfo('Success','Registration Successful. You can Login Now.')
        else:
            messagebox.showinfo('Error','Email Already Exists')

    def perform_login(self):
        # fetch details from the login page
        email = self.email_input.get().strip()
        password = self.password_input.get().strip()

        # block empty inputs
        if not email or not password:
            messagebox.showerror('Error', 'Please enter email and password.')
            return

        response = self.dbo.search(email, password)

        if response:
            self.logged_in_email = email  # mark as logged-in with a real email
            messagebox.showinfo('Success', 'Login Successful')
            self.home_gui()
        else:
            messagebox.showerror('Error', 'Incorrect Email/Password')


    def home_gui(self):

        # prevent direct access without login
        if not hasattr(self, "logged_in_email"):
            messagebox.showerror("Error", "Please login first")
            self.login_gui()
            return

        self.clear()

        heading = Label(self.root, text='Natural Language Processing App', bg='#FDF0D5', fg='#780000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('serif', 28, 'bold'))

        sentiment_button = Button(self.root, text='Sentiment Analysis', fg='#003049', width=20, height=4, command=self.sentiment_gui)
        sentiment_button.pack(pady=(10, 10))

        ner_button = Button(self.root, text='Named Entity Recognition', fg='#003049', width=20, height=4, command=self.ner_gui)
        ner_button.pack(pady=(10, 10))

        logout_button = Button(self.root, text='Logout', fg='#003049', width=7, height=2, command=self.login_gui)
        logout_button.pack(pady=(10, 10))

    def sentiment_gui(self):

        self.clear()

        heading = Label(self.root, text='Natural Language Processing App', bg='#FDF0D5', fg='#780000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('serif', 28, 'bold'))

        heading2 = Label(self.root, text='Sentiment Analysis', bg='#FDF0D5', fg='#780000')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('serif', 18, 'bold'))

        label1 = Label(self.root, text='Enter the Text', bg='#FDF0D5', fg='#003049')
        label1.pack(pady=(10, 10))

        self.sentiment_input = Entry(self.root, width=50)
        self.sentiment_input.pack(pady=(10, 10), ipady=10)

        sentiment_button = Button(self.root, text='Analyse Sentiment', fg='#003049', width=15, height=2, command=self.do_sentiment_analysis)
        sentiment_button.pack(pady=(10, 10))

        self.sentiment_result = Label(self.root, text='', bg='#FDF0D5', fg='#003049')
        self.sentiment_result.pack(pady=(10,10),ipady=10)
        self.sentiment_result.configure(font='serif')

        goback_button = Button(self.root, text='Go Back', fg='#003049', width=15, height=2, command=self.home_gui)
        goback_button.pack(pady=(10, 10))


    def ner_gui(self):
        self.clear()

        heading = Label(self.root, text='Natural Language Processing App', bg='#FDF0D5', fg='#780000')
        heading.pack(pady=(30, 30))
        heading.configure(font=('serif', 28, 'bold'))

        heading2 = Label(self.root, text='Named Entity Recognition', bg='#FDF0D5', fg='#780000')
        heading2.pack(pady=(10, 20))
        heading2.configure(font=('serif', 18, 'bold'))

        label1 = Label(self.root, text='Enter the Text', bg='#FDF0D5', fg='#003049')
        label1.pack(pady=(10, 10))

        self.ner_input = Entry(self.root, width=50)
        self.ner_input.pack(pady=(10, 10), ipady=10)

        ner_button = Button(self.root, text='Extract Entities', fg='#003049', width=15, height=2, command=self.do_ner)
        ner_button.pack(pady=(10, 10))

        self.ner_result = Label(self.root, text='', bg='#FDF0D5', fg='#003049', justify="left")
        self.ner_result.pack(pady=(10, 10), ipady=10)
        self.ner_result.configure(font='serif')

        goback_button = Button(self.root, text='Go Back', fg='#003049', width=15, height=2, command=self.home_gui)
        goback_button.pack(pady=(10, 10))


    def do_sentiment_analysis(self):
        text = self.sentiment_input.get()

        if len(text) == 0:
            messagebox.showerror('Error', 'Please enter some text to analyze.')
            self.sentiment_result.config(text="")
            return

        try:
            result = analyze_sentiment(text)  # <-- correct function
            if not result:
                output = "No result returned."
            else:
                top = result[0]  # take first prediction
                output = f"Sentiment: {top['label']}\nConfidence: {top['score']:.2f}"
        except Exception as e:
            output = f"Error: {e}"

        self.sentiment_result.config(text=output)

    def do_ner(self):
        text = self.ner_input.get()

        if len(text) == 0:
            messagebox.showerror('Error', 'Please enter some text to analyze.')
            self.ner_result.config(text="")
            return

        print(f"Text being sent to NER API: '{text}'")

        try:
            result = extract_entities(text)
            if not result:
                output = "No entities found."
            else:
                output_lines = []
                for ent in result:
                    output_lines.append(f"{ent['text']} → {ent['entity']} (score: {ent['score']:.2f})")
                output = "\n".join(output_lines)
        except Exception as e:
            output = f"Error: {str(e)}"

        self.ner_result.config(text=output)


nlp = NLPApp()