from tkinter import *
from tkinter import messagebox
from tkinter import Menu
from tkinter.ttk import Checkbutton, Notebook
from tkinter import filedialog
from tkinter import scrolledtext
import os

import stardog

from c2onto import *

"""
External dependencies:
$ pip install pystardog pycparser
"""

class App:
    def __init__(self):

        # setup window
        self.window = Tk()
        self.window.title("C-2-Onto Gui")
        # self.window.geometry("700x500+300+100")

        # init data
        # self.ontology = Ontology()
        self.code_ast = None
        self.conn_details = None
        self.open_conn_details = None

        # setup widgets
        # self.file_panel = FilePanel(self.window, self.ontology)
        # self.file_panel.grid(column=0, row=0)

        self.tabs_panel = TabsPanel(self.window, self)
        self.tabs_panel.grid(column=0, row=1)

        # self.status_label = Label(self.window, text="Готов")
        # self.status_label.grid(column=0, row=2, padx=10)

        self.init_menu()

        # run GUI
        self.window.mainloop()

    def init_menu(self):
        menu = Menu(self.window)

        # Файл
        cascade = Menu(menu, tearoff=0)

        # cascade.add_command(label='Новый', command=self.on_menu_file_new)

        cascade.add_command(label='Load code from file', command=self.on_menu_file_open)
        self.window.bind("<Control-Key-o>", self.on_menu_file_open)

        # cascade.add_command(label='Сохранить', command=self.on_menu_file_save)
        # self.window.bind("<Control-Key-s>", self.on_menu_file_save)

        cascade.add_separator()

        cascade.add_command(label='Quit', command=self.on_close_app, accelerator = 'Esc')
        self.window.bind("<Escape>", self.on_close_app)  # callback must recieve 1 positional argument

        menu.add_cascade(label='File', menu=cascade)

        # Edit
        cascade = Menu(menu, tearoff=0)
        cascade.add_command(label='Format code', command=self.tabs_panel.on_format_code)
        menu.add_cascade(label='Edit', menu=cascade)

        self.window.config(menu=menu)

    def on_close_app(self, *args):
        ### messagebox.showinfo('Выход', 'Программа будет закрыта.\nСпасибо, что были с нами!')
        # self.window.close()
        self.window.destroy()
        # exit()

    def on_menu_file_new(self, *args):
        # self.ontology.clear()
        self.status_label.configure(text='New!..')
        messagebox.showinfo('Меню/Файл', 'New!..')

    def on_menu_file_open(self, *args):
        # messagebox.showinfo('Меню/Файл', 'Open!..')
        filepath = filedialog.askopenfilename(initialdir='.', filetypes = (("All files","*.*"),))
        # if not os.path.exists(filepath):
        if os.path.exists(filepath):
            self.tabs_panel.load_file(filepath)
            # self.status_label.configure(text='Открытие файла отменено: файл не найден: ' + filepath)
            # return

        # # error = self.ontology.load(filepath)
        # if error is not None:
        #     self.status_label.configure(text='Открыть файл: ошибка: ' + error[:100])
        #     messagebox.showerror('Открыть файл: ошибка', error)
        #     filepath = None  # to clear status in file_panel

        # self.file_panel.set_filepath(filepath)
        # self.status_label.configure(text='Открытие и загрузка файла прошли успешно')

    def on_menu_file_save(self, *args):
        # self.ontology.save_as()
        messagebox.showinfo('Меню/Файл', 'Saved!..')

    def parse_code(self, text):
        # text = self.tabs_panel.code_used_str
        self.code_ast = None
        try:
            parser = c_parser.CParser()
            self.code_ast = parser.parse(text)
        except Exception as e:
            # raise e
            return str(e)

    def get_code_norm_format(self):
        if not self.code_ast:
            return ''
        else:
            return ast_to_code(self.code_ast)

    def get_code_triples(self):
        """ -> (triples_list, error_str) """
        if not self.code_ast:
            return [], None
        try:
            uniq_names.clear()
            alg = Algorithm(self.code_ast)
            triples = alg.get_triples()
        except Exception as e:
            # raise e
            return [], str(e)
        return triples, None

    def set_connection_details(self, conn_details):
        # conn_details = {
        #   'endpoint':   self.server_url_var.get(),
        #   'username': 'admin',
        #   'password': 'admin',
        #   'schemafile': self.schema_file_var.get(),
        #   'dbname':     self.server_dbname_var.get(),
        #   'createdb':   self.server_db_create_var.get(),
        #   'dropdb':     self.server_db_drop_var.get(),
        # }
        self.conn_details = conn_details
        self.open_conn_details = {
          key: self.conn_details[key]
            for key in ('endpoint','username','password')
        }

    def upload_triples(self, triples, progress_callback=None):
        try:
            assert self.conn_details
            if progress_callback: progress_callback("establishing connection ...")

            self.stardog_create_db_if_set()

            prefix_str = """
            BASE <http://vstu.ru/poas/se/c_schema_2020-01#>
            PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
            """
            f = lambda s: make_namespace_prefix(s, default_prefix=':', known_prefixes=('rdf'))

            dbname = self.conn_details['dbname']

            with stardog.Connection(dbname, **self.open_conn_details) as conn:
                if progress_callback: progress_callback("connection OK")

                for i,trpl in enumerate(triples):
                    # ensure prefixes OK
                    trpl = tuple(f(a) for a in trpl)

                    q = triple_to_sparql_insert(trpl, prefix_str)
                    print('Send: ', trpl, end='')
                    # отправка запросов SPARQL UPDATE
                    results = conn.update(q, reasoning=False)
                    print(' done!')
                    if progress_callback: progress_callback("%d/%d done" % ((i+1), len(triples)))
            if progress_callback: progress_callback("100% finished!")
        except Exception as e:
            print(e)
            return str(e)

    def download_ontology(self, save_as, progress_callback=None):
        try:
            assert self.conn_details
            if progress_callback: progress_callback("establishing connection ...")

            dbname = self.conn_details['dbname']

            with stardog.Connection(dbname, **self.open_conn_details) as conn:
                if progress_callback: progress_callback("connection OK")
                contents = str(conn.export())
                # contents = contents[2:-1]  # ??
                contents = contents.replace('\\n', '\n')

                # запись в файл
                if not save_as.endswith('.ttl'):
                    save_as += '.ttl'
                if progress_callback: progress_callback("writing to file: " + save_as[-50:])
                with open(save_as, 'w') as f:
                    f.write(contents)


            if progress_callback: progress_callback("dropping database if set so...")
            self.stardog_drop_db_if_set()

            if progress_callback: progress_callback("finished!")
        except Exception as e:
            print(e)
            return str(e)


    def stardog_create_db_if_set(self):
        # conn_details = {
        #   'endpoint':   self.server_url_var.get(),
        #   'username': 'admin',
        #   'password': 'admin',
        #   'schemafile': self.schema_file_var.get(),
        #   'dbname':     self.server_dbname_var.get(),
        #   'createdb':   self.server_db_create_var.get(),
        #   'dropdb':     self.server_db_drop_var.get(),
        # }
        assert self.conn_details

        if self.conn_details['createdb']:
            dbname = self.conn_details['dbname']
            schema_file = stardog.content.File(self.conn_details['schemafile'])
            print('Probably schema_file OK: ',self.conn_details['schemafile'])

            with stardog.Admin(**self.open_conn_details) as admin:
                db = admin.new_database(dbname)
                db = None  # forget pointer
                # init schema
                with stardog.Connection(dbname, **self.open_conn_details) as conn:
                    conn.begin()
                    conn.add(schema_file)
                    conn.commit()

    def stardog_drop_db_if_set(self):
        assert self.conn_details
        if self.conn_details['dropdb']:
            dbname = self.conn_details['dbname']
            with stardog.Admin(**self.open_conn_details) as admin:
                db = admin.database(dbname)
                db.drop()




class TabsPanel(Frame):
    """All tabs in main screen"""
    def __init__(self, parent, app):
        Frame.__init__(self, parent)
        self.app = app
        self.initUI()
    def initUI(self):
        # self.tabs = []

       # init tabs
        self.tab = Notebook(self)
        self.tab.bind('<<NotebookTabChanged>>', self.on_tab_changed)
        created_tab = [
            self.make_code_tab(),
            self.make_triples_tab(),
            self.make_upload_tab(),
        ]
        for frame,name in created_tab:
            self.tab.add(frame, text=name)
#         self.tabs[0] = Frame(self.editor_tab)
#         self.tabs[1] = Frame(self.editor_tab)
#         self.tab.add(self.editor_tabs[0], text='SELECT/ASK')
#         self.tab.add(self.editor_tabs[1], text='INSERT/DELETE')
        self.tab.grid(column=0, row=0)

    def updateUI(self):
        self.check_code_modified()
        self.check_triples_exist()

    def make_code_tab(self):
        f = Frame(self.tab)
        Label(f, text='Open .c file or paste code here').pack()

        self.code_edit = scrolledtext.ScrolledText(f, wrap="word", width=70, height=20)
        self.code_edit.pack()

        self.code_var = StringVar(self.code_edit)
        attach_StrVar_to_Text(self.code_var, self.code_edit)
        # listen code changes
        self.code_var.trace_add('write', self.check_code_modified)

        self.code_used_str = None

        self.code_modified = False
        self.code_modified_label = Label(f, text='no code yet...', justify='left')
        # self.code_modified_label.pack(expand=True, fill=X)
        self.code_modified_label.pack(side=LEFT)

        self.get_triples_button = Button(f, text="Convert code to triples ...", padx="15", bg='#bbddbb', command=self.on_get_triples_button)
        self.get_triples_button.pack(side=RIGHT)
        # self.code_modified_label["text"] = 'ABCDE!'

        self.load_file('default.c')

        return (f, 'Code')

    def load_file(self, filepath):
        try:
            with open(filepath) as f:
                t = f.read()
            self.code_var.set(t)
            self.code_modified_label["text"] = "loaded file: "+filepath
        except:
            err_msg = "file no found: "+filepath
            self.code_modified_label["text"] = err_msg
            print(err_msg)



    def check_code_modified(self, *_):
        if self.code_var.get() == self.code_used_str:
            text = 'code not modified'
            self.code_modified = False
        else:
            text = 'code was changed'
            self.code_modified = True

        button_state = NORMAL if self.code_modified else DISABLED
        self.get_triples_button["state"] = button_state

        if self.code_used_str is None:
            text = 'no code in use'
            self.code_modified = False

        self.code_modified_label["text"] = text

    def on_get_triples_button(self):
        self.code_used_str = self.code_var.get()
        self.code_modified = False
        # call app action ...
        error = self.app.parse_code(self.code_used_str)
        if error:
            messagebox.showinfo('Code error', error)
            # print(error)
            self.code_used_str = None
            return

        triples, error = self.app.get_code_triples()
        if error:
            messagebox.showinfo('Triples obtaining error', error)
            # print(error)
            self.code_used_str = None
            return
        self.triples_list = triples
        self.tab.select(1)

        self.set_upload_status("Ready to upload triples to server")


    def on_format_code(self):
        # call app action ...
        error = self.app.parse_code(self.code_var.get())
        if error:
            messagebox.showinfo('Code parse error', error)
            self.highlight_char_by_error(error)
        else:
            formatted_code = self.app.get_code_norm_format()
            self.code_var.set(formatted_code)

    def highlight_char_by_error(self, err_string):
        sep = ':'
        # print(err_string)
        dd = err_string.strip(sep).split(sep)
        # print(dd)
        try:
            r,c = dd[:2]
            r = int(r)
            c = int(c)
        except:
            return
        # f = "%d.%d" % (r,c)
        # t = "%d.%d" % (r,c+1)
        f = "%d.0" % (r,)
        t = "%d.end" % (r,)
         # self.code_edit.selection_set(f,t)
        # print(f,t)
        self.code_edit.tag_add(SEL, f, t)

    def make_triples_tab(self):
        f = Frame(self.tab)
        Label(f, text='Triples obtained from code. Changes to this text have no effect on stored triples.').pack()

        self.triples_edit = scrolledtext.ScrolledText(f, wrap="word", width=70, height=20)
        self.triples_edit.pack()

        self.triples_list = None

        self.triples_count_label = Label(f, text='Click "Code to Triples" button first', justify='left')
        self.triples_count_label.pack(side=LEFT)

        self.goto_upload_button = Button(f, text="Proceed to upload ...", padx="15", bg='#bbddbb', command=lambda *_: self.tab.select(2))
        self.goto_upload_button.pack(side=RIGHT)

        return (f, 'Triples')

    def check_triples_exist(self):
        button_state = NORMAL if self.triples_list else DISABLED
        self.goto_upload_button["state"] = button_state
        self.run_upload_button["state"] = button_state

        if self.triples_list:
            count_text = 'Triples count: %d' % len(self.triples_list)
        else:
            count_text = 'No triples'
        self.triples_count_label["text"] = count_text
        self.show_triples()

    def show_triples(self):
        if self.triples_list:
            triples_str = '\n'.join(map(str, self.triples_list))
        else:
            triples_str = 'No triples generated from code'
        self.triples_edit.delete(1.0,END)
        self.triples_edit.insert(1.0, triples_str)

    def make_upload_tab(self):
        f = Frame(self.tab)
        Label(f, text='Set up connection and click "Upload"').pack()

        # Remote configuration
        g = LabelFrame(f, text="Remote configuration")

        row = 0

        Label(g, text='Stardog server location:').grid(row=row, column=0, rowspan=1, sticky=E, padx=20, pady=5)

        self.server_url_var = StringVar()
        serv_url = Entry(g, width=60, textvariable=self.server_url_var)
        self.server_url_var.set("http://localhost:5820")
        serv_url.grid(row=row, column=1, sticky=W)

        row += 1

        Label(g, text='(Using default username & password: admin, admin)').grid(row=row, column=0, columnspan=2)

        row += 1

        Label(g, text='Stardog database name:').grid(row=row, column=0, rowspan=1, sticky=E, padx=20, pady=5)

        self.server_dbname_var = StringVar()
        serv_dbname = Entry(g, width=60, textvariable=self.server_dbname_var)
        self.server_dbname_var.set("sem_alg_db")
        serv_dbname.grid(row=row, column=1, sticky=W)

        row += 1

        Label(g, text='Ontology schema file:').grid(row=row, column=0, rowspan=1, sticky=E, padx=20, pady=5)

        self.schema_file_var = StringVar()
        serv_dbname = Entry(g, width=60, textvariable=self.schema_file_var)
        self.schema_file_var.set("c_schema_2020-01.rdf")
        serv_dbname.grid(row=row, column=1, sticky=W)

        row += 1

        self.server_db_create_var = BooleanVar()
        self.server_db_create_var.set(1)
        chk = Checkbutton(g, text="Create a new DB on server", variable=self.server_db_create_var, onvalue=1, offvalue=0)
        chk.grid(row=row, column=1, sticky=W)

        row += 1

        self.server_db_drop_var = BooleanVar()
        self.server_db_drop_var.set(0)
        chk = Checkbutton(g, text="Drop DB on closing connection", variable=self.server_db_drop_var, onvalue=1, offvalue=0)
        chk.grid(row=row, column=1, sticky=W)
        # text="Drop DB after whole data export"

        g.pack(expand=1, fill=X)

        self.run_upload_button = Button(f, text="Upload !", bg='#ff99dd', command=self.on_upload_button)
        self.run_upload_button.pack(expand=1, fill=BOTH, padx=50, pady=45)

        self.upload_status_label = Label(f, text='No upload performed', justify='left')
        self.upload_status_label.pack(side=LEFT)

        return (f, 'Upload data')

    def get_conn_details(self):
        conn_details = {
          'endpoint':   self.server_url_var.get(),
          'username': 'admin',
          'password': 'admin',
          'schemafile': self.schema_file_var.get(),
          'dbname':     self.server_dbname_var.get(),
          'createdb':   self.server_db_create_var.get(),
          'dropdb':     self.server_db_drop_var.get(),
        }
        return conn_details

    def on_upload_button(self):
        self.set_upload_status("Upload in progress ...")
        self.app.set_connection_details(self.get_conn_details())
        error = self.app.upload_triples(self.triples_list, progress_callback=self.set_upload_status)
        if error:
            messagebox.showinfo('Upload error', error)
            self.set_upload_status("Upload error")
        else:
            self.set_upload_status("Upload success")

    def set_upload_status(self, text):
            self.upload_status_label["text"] = str(text)



    def on_tab_changed(self, ev):
        # print('on_tab_changed:')
        # print(ev)
        self.updateUI()


def attach_StrVar_to_Text(sv, txt):
    """ Привязать строковую переменную tkinter к текстовому полю.
    Работает в обе стороны: Задание переменной <-> Отпускание клавиши """
    assert isinstance(sv, StringVar)
    assert isinstance(txt, Text)
    def _set_sv(ev):
        new_str = txt.get(1.0,END)
        if sv.get() != new_str:
            sv.set(new_str)
    txt.bind('<KeyRelease>', _set_sv)
    def _set_txt(*args):
        old_str = txt.get(1.0,END)
        if sv.get() != old_str:
            txt.delete(1.0,END)
            txt.insert(1.0, sv.get())
    sv.trace_add(("write", "unset"), _set_txt)

if __name__ == '__main__':
    App()
