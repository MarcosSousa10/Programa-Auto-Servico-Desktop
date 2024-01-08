import PySimpleGUI as sg
import tkinter as tk
import requests
import webbrowser

sg.theme('pythonplus')
font = ("Arial", 13)
def usuario (usuario,senha) :
    try:
        response = requests.get(f"http://192.168.0.23:4444/login/{usuario}/{senha}")
        return response.status_code           
    except Exception as e:
        return None, False


def drop (data_selecionada) :
    try:
        response = requests.delete("http://192.168.0.23:4444/drop")
        create(data_selecionada)

            
    except Exception as e:
        return None, False

def create (data_selecionada) :
        response = requests.get("http://192.168.0.23:4444/tu")
        insert(data_selecionada)    
  
def insert (data_selecionada) :
    try:
        response = requests.get(f"http://192.168.0.23:4444/in/{data_selecionada}")
    except Exception as e:
        return None, False
def reset (data_selecionada):
    try :
        drop(data_selecionada)
    except:
        try :
            create(data_selecionada)
            insert(data_selecionada)
        except:
            insert(data_selecionada)
        
    
    
        
    
def build_layout(largura_monitor):
    return [
        [sg.Text('Nome de Usuário', size=(largura_monitor // 20, 1), justification='center')],
        [sg.Input(key='username', font=font, expand_x=True, pad=(0, 0), size=(largura_monitor // 20, 1))],
        [sg.Text('Senha', size=(largura_monitor // 20, 1), justification='center')],
        [sg.Input(key="password", font=font, password_char='*', expand_x=True, pad=(0, 0), size=(largura_monitor // 30, 1))],
        [sg.Text(size=(1, 1))],
        [sg.Button('Login', size=(15, 2)), sg.Button('Cancelar', size=(15, 2))],
    ]

def build_layout2(largura_monitor):
    return [
        [sg.Text('Bem-vindo! Faça o download do PDF ou selecione uma data.', size=(largura_monitor // 15, 1), justification='center')],
        [sg.Text(key='download_status', visible=False, size=(largura_monitor // 15, 1), justification='center')],
        [sg.CalendarButton('Selecione a Data', target='data', key='calendario', size=(50, 1), format='%d-%m-%Y'),
         sg.InputText(key='data', size=(50, 1), justification='center', disabled=True, text_color='black')],
        [sg.Button('Atualizar PDF', key='OK', size=(largura_monitor // 15, 1))],
        [sg.Text(size=(1, 1))],
        [sg.Text(size=(1, 1))],
        [sg.Button('Download PDF', size=(largura_monitor // 15, 1), key='download_button')],
    ]

def download_pdf(link):
    try:
        response = requests.get(link)
        with open("arquivo.pdf", "wb") as pdf_file:
            pdf_file.write(response.content)
        webbrowser.open("arquivo.pdf")
        if response.status_code == 200:
            return response.content, True
        else:
            return None, False
    except Exception as e:
        return None, False

pdf_url = "http://192.168.0.23:4444/relatorio-vendas"

def main():
    root = tk.Tk()
    root.withdraw()
    largura_monitor = root.winfo_screenwidth()
    altura_monitor = root.winfo_screenheight()

    layout = [
        [sg.Text(size=(1, 5))],
        [sg.Col(build_layout(largura_monitor), key='-COL-', justification='c')],
        [sg.Text(size=(1, 1))],
    ]
    window1 = sg.Window('Othon de Carvalho - Login', layout=layout, element_justification='center',
                        resizable=True, use_default_focus=False, finalize=True)
    window_size = window1.Size

    while True:
        event, values = window1.read()

        if event == sg.WINDOW_CLOSED or event == 'Cancelar':
            break
        elif event == 'Login':
            
            username = values['username']
            password = values['password']
            usuario(username,password)
            if usuario(username,password) == 202:
                window1.close()
                layout = [
                    [sg.Text(size=(1, 5))],
                    [sg.Col(build_layout2(largura_monitor), key='-COL-', justification='c')],
                    [sg.Text(size=(1, 1))],
                ]
                window = sg.Window('Othon de Carvalho - Interactions', layout=layout,
                                    element_justification='center', resizable=True, use_default_focus=False, finalize=True)
                window.set_min_size((largura_monitor // 20, altura_monitor - 700))
                window_size = window.Size

                while True:
                    event, values = window.read()

                    if event == sg.WINDOW_CLOSED or event == 'Cancelar':
                        break
                    elif event == 'download_button':
                        pdf_content, download_success = download_pdf(pdf_url)

                        if download_success:
                            window['download_status'].update('Download bem-sucedido!', visible=True)
                        else:
                            window['download_status'].update('Falha ao baixar o PDF. Tente novamente.', visible=True)
                    elif event == 'OK':
                        data_selecionada = values['data']
                        drop(data_selecionada)
                window.close()
                window1.close()

if __name__ == '__main__':
    main()
