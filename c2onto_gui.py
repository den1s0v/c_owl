from tkinter import *
from tkinter import messagebox
from tkinter import Menu
from tkinter.ttk import Checkbutton, Notebook
from tkinter import filedialog
from tkinter import scrolledtext

from c2onto import *

class App:
    def __init__(self):

        # setup window
        self.window = Tk()
        self.window.title("C-2-Onto Gui")
        # self.window.geometry("700x500+300+100")

        # init data
        # self.ontology = Ontology()
        self.code_ast = None

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
        filepath = filedialog.askopenfilename(filetypes = (("RDF/XML files","*.rdf;*.xml;*.owl;*.n3;*.turtle"),("All files","*.*")))
        if not os.path.exists(filepath):
            self.status_label.configure(text='Открытие файла отменено: файл не найден: ' + filepath)
            return

        # error = self.ontology.load(filepath)
        if error is not None:
            self.status_label.configure(text='Открыть файл: ошибка: ' + error[:100])
            messagebox.showerror('Открыть файл: ошибка', error)
            filepath = None  # to clear status in file_panel

        self.file_panel.set_filepath(filepath)
        self.status_label.configure(text='Открытие и загрузка файла прошли успешно')

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
        return (f, 'Code')

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
        else:
            self.tab.select(1)

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

        self.goto_upload_button = Button(f, text="Proceed to upload ...", padx="15", command=lambda *_: self.tab.select(2))
        self.goto_upload_button.pack()  # (side=RIGHT)

        return (f, 'Triples')

    def check_triples_exist(self):
        button_state = NORMAL if self.triples_list else DISABLED
        self.goto_upload_button["state"] = button_state

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
