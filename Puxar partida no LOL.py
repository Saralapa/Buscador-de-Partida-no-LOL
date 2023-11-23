import pyautogui
import subprocess
import pygetwindow as gw
import time
import tkinter as tk
import os
import webbrowser
import threading

# Variáveis globais
screen = "game mode selection"
Role_1 = None
Role_2 = None
game_mode = None
botoes2 = []

def encontrar_e_salvar_pasta_instalacao_lol(unidade, flagPF):
    unidade=unidade+"\\"
    global pasta_instalacao
    pasta_instalacao=None
    if flagPF==1:
        # Verifica os possíveis diretórios padrão de instalação do League of Legends
        pastas_padrao = rf"{unidade}\Riot Games\League of Legends"

        for pasta in pastas_padrao:
            if os.path.exists(pastas_padrao):
                pasta_instalacao=pastas_padrao
                pasta_instalacao = os.path.dirname(pasta_instalacao)
                pasta_instalacao = os.path.join(pasta_instalacao, "Riot Client", "RiotClientServices.exe")
                pasta_instalacao = pasta_instalacao.replace("\\\\", "\\")

                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),"league_of_legends_path.txt"), 'w') as arquivo:
                    arquivo.write(pasta_instalacao)

                if pasta_instalacao:
                    return 23
                else:
                    return

        # Se não encontrar em nenhum dos diretórios padrão, você pode buscar recursivamente por toda a unidade
        for pasta, subpastas, arquivos in os.walk(unidade):
            if "Program Files" in pasta or "ProgramData" in pasta or "AppData" in pasta or "Windows" in pasta:
                del subpastas[:]
                continue
            if "League of Legends" in subpastas and "Riot Games" in pasta:
                pasta_instalacao = os.path.join(pasta, "Riot Client", "RiotClientServices.exe")
                pasta_instalacao = pasta_instalacao.replace(f"{unidade}",f"{unidade}\\")
                pasta_instalacao = pasta_instalacao.replace("\\\\","\\")

                with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "league_of_legends_path.txt"), 'w') as arquivo:
                    arquivo.write(pasta_instalacao)

                return 23
            
            if pasta_instalacao:
                return

        if not pasta_instalacao:
            print("A pasta de instalação do League of Legends não foi encontrada.")
    
    elif flagPF==2:
        for pasta, subpastas, arquivos in os.walk(unidade):
            print(pasta, subpastas, arquivos)
            if "Riot Client" in subpastas and "League of Legends" in subpastas:
                riot_client_index = subpastas.index("Riot Client")
                lol_index = subpastas.index("League of Legends")

                if lol_index == riot_client_index + 1:  # Verifica se "League of Legends" está dentro de "Riot Client"
                    pasta_instalacao = os.path.join(pasta, "Riot Client", "RiotClientServices.exe")
                    pasta_instalacao = pasta_instalacao.replace(f"{unidade}", f"{unidade}\\")  # Corrigido

                    with open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "league_of_legends_path.txt"), 'w') as arquivo:
                        arquivo.write(pasta_instalacao)

                    return 23
            
            if pasta_instalacao:
                return

        if not pasta_instalacao:
            print("A pasta de instalação do League of Legends não foi encontrada.")

def LOL():
    global screen, Role_1, Role_2, game_mode, botoes2

    try:
        [window for window in gw.getWindowsWithTitle("Puxar partida no LOL") if window.title == "Puxar partida no LOL"][0].restore()
        [window for window in gw.getWindowsWithTitle("Puxar partida no LOL") if window.title == "Puxar partida no LOL"][0].minimize()
    except:
        None

    def game_mode_selection():
        global screen
        screen = "game mode selection"
        window.overrideredirect(True)
        window.wm_attributes("-topmost", 1)
        frame2.pack_forget()
        label_auto.pack_forget()
        frame_menu.pack_forget()
        menu_button.pack_forget()

        frame_undo.pack(side="bottom", fill="both", expand=True)
        frame1.pack()
        border_label.config(text="Escolha o modo de jogo")
        variable.set("Modo de jogo\nescolhido:")
        undo_button.config(text="Desfazer")
        center_window(window, 375, 334)

    def role_selection():
        global screen, botoes2
        screen = "role selection"
        frame1.pack_forget()
        frame2.pack()
        border_label.config(text="Escolha em que posição você vai jogar")
        if Role_1 == None:
            undo_button.config(text="Menu anterior")
        else:
            undo_button.config(text="Desfazer")
        if game_mode == "Blitz do Nexus":
            variable.set("Posição escolhida:")
            for botao in botoes2:
                botao.destroy()
            textos_botões2_novos = ["Jungle", "Rota", "Preencher"]
            botoes2 = [tk.Button(frame2, text=texto2, command=lambda t=texto2: update_roles(t)) for texto2 in textos_botões2_novos]
            for botao in botoes2:
                botao.config(width=47, height=2, bg="#1f1f1f", fg="#f0f0f0")
                botao.pack(padx=17, pady=5)
        else:
            variable.set(f"Primeira role:\nSegunda role:")
            for botao in botoes2:
                botao.destroy()
            textos_botões2 = ["Top", "Jungle", "Mid", "ADC", "Suporte", "Preencher"]
            botoes2 = [tk.Button(frame2, text=texto2, command=lambda t=texto2: update_roles(t)) for texto2 in textos_botões2]
            for botao in botoes2:
                botao.config(width=47, height=2, bg="#1f1f1f", fg="#f0f0f0")
                botao.pack(padx=17, pady=5)
        if game_mode != "Blitz do Nexus":
            center_window(window, 375, 385)
        else:
            center_window(window, 375, 235)

    def auto_aceitar():
        global screen
        screen="auto aceitar"
        window.overrideredirect(False)
        window.wm_attributes("-topmost", 0)
        frame1.pack_forget()
        frame2.pack_forget()
        frame_undo.pack_forget()
        variable.set("")
        border_label.config(text="")

        label_auto.pack()
        frame_menu.pack()
        menu_button.pack()

        center_window(window, 300, 100)

        thread_imagem = threading.Thread(target=WhereToClick)
        thread_imagem.daemon = True
        thread_imagem.start()
    
    def atualizar_mensagem():
        mensagens = ["Encontrando partida", "Encontrando partida.", "Encontrando partida..", "Encontrando partida..."]
        index = 0
        while True:
            try:
                label_auto.config(text=mensagens[index])
                index = (index + 1) % len(mensagens)
                time.sleep(0.5)
            except:
                None

    def center_window(window, width, height):
        global screen_width, screen_height, x, y
        screen_width = window.winfo_screenwidth()
        screen_height = window.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        window.geometry(f"{width}x{height}+{x}+{y}")

    def Update_Game_Mode(valor):
        global game_mode, textos_botões2
        game_mode = valor
        variable.set(f"Modo de jogo\nescolhido: {game_mode}")

    def Confirm():
        if screen == "game mode selection":
            if game_mode == "Apenas auto aceitar":
                window.after(500, lambda: auto_aceitar() if game_mode == "Apenas auto aceitar" else None)
                if game_mode == "Apenas auto aceitar":
                    return 23

            if game_mode == None:
                variable.set("Selecione um modo de jogo!")
                window.after(2000, lambda: variable.set("Modo de jogo\nescolhido:") if game_mode == None else None)
            window.after(0, lambda: auto_aceitar() if game_mode == "ARAM" else role_selection() if game_mode is not None else None)
        elif screen == "role selection":
            if (game_mode != "Blitz do Nexus" and (Role_1 != "Preencher" and Role_2 == None)) or (game_mode== "Blitz do Nexus" and Role_1==None):
                variable.set("As duas roles devem\nser preenchidas!")
                if game_mode!="Blitz do Nexus":
                    window.after(2000, lambda: variable.set("Primeira role:\nSegunda role:") if screen=="role selection" else None if Role_1 == None else None)
                    window.after(2000, lambda: variable.set(f"Primeira role: {Role_1}\nSegunda role:") if screen=="role selection" else None if Role_1 != None and Role_2==None else None)
                else: window.after(2000, lambda: variable.set("Posição escolhida:") if screen=="role selection" else None if Role_1 == None else None)
            else:
                window.after(500, lambda: auto_aceitar())

    def desfazer():
        global game_mode, screen, Role_1, Role_2
        if screen == "game mode selection":
            game_mode = None
            variable.set("Modo de jogo\nescolhido:")
        elif screen == "role selection":
            if Role_2 != None:
                Role_2 = None
                if game_mode!="Blitz do Nexus":
                    variable.set(f"Primeira role: {Role_1}\nSegunda role:")
                else: variable.set("Posição escolhida:")
            elif Role_1 != None:
                Role_1 = None
                undo_button.config(text="Menu anterior")
                if game_mode!="Blitz do Nexus":
                    variable.set(f"Primeira role:\nSegunda role:")
                else: variable.set("Posição escolhida:")
            else:
                game_mode = None
                game_mode_selection()
        elif screen=="auto aceitar":
            game_mode=None
            Role_1=None
            Role_2=None
            game_mode_selection()

    def close_program():
        window.destroy()
        os.sys.exit()

    def update_roles(valor):
        global Role_1, Role_2
        if Role_1 == None:
            Role_1 = valor
            undo_button.config(text="Desfazer")
            if game_mode != "Blitz do Nexus":
                variable.set(f"Primeira role: {Role_1}\nSegunda role:")
            else:
                variable.set(f"Posição escolhida: {Role_1}")
        elif Role_2 == None and Role_1 != "Preencher" and game_mode != "Blitz do Nexus":
            Role_2 = valor
            variable.set(f"Primeira role: {Role_1}\nSegunda role: {Role_2}")
            if Role_1 == Role_2:
                Role_2 = None
                variable.set(f"A primeira e a segunda\nposição não podem ser iguais!")
                window.after(2000, lambda: variable.set(f"Primeira role: {Role_1}\nSegunda role:"))

    def KeepSearchingImageAndClickWhenFound(image):
        # Localize the position of "image" on the screen
        image_path_image = os.path.join("Images", image)

        while True:
            image_position_image = pyautogui.locateOnScreen(image_path_image, confidence=0.8)

            # If the image is found, click on it
            if image_position_image:
                image_center = pyautogui.center(image_position_image)
                pyautogui.click(image_center.x, image_center.y)
                if image=="Aceitar.png": time.sleep(5)
                break

            # Wait a short time before trying again
            time.sleep(0.5)

    def SearchImageForXSecondsAndClickWhenFound(image, seconds):
        # Localize the position of "image" on the screen
        image_path_image = os.path.join("Images", image)
        start_time = time.time()

        while (time.time() - start_time) < seconds:  # Keep searching for X seconds tops
            image_position_image = pyautogui.locateOnScreen(image_path_image, confidence=0.8)

            # If the image is found, click on it
            if image_position_image:
                image_center = pyautogui.center(image_position_image)
                pyautogui.click(image_center.x, image_center.y)
                return 23

            # Wait a short time before trying again
            time.sleep(0.5)

    def Role1(image):
        # Localize the position of "Encontrar partida" on the screen
        image_path_Encontrar_partida = os.path.join("Images", "Encontrar partida.png")

        while True:
            image_position_Encontrar_partida = pyautogui.locateOnScreen(image_path_Encontrar_partida, confidence=0.8)

            # If the image is found, click on it with x adjusted
            if image_position_Encontrar_partida:
                image_center = pyautogui.center(image_position_Encontrar_partida)
                x_adjusted = image_center.x + 155  # Ajuste a coordenada x aqui
                pyautogui.click(x_adjusted, image_center.y)
                break

            # Wait a short time before trying again
            time.sleep(0.5)

        # Localize the position of "image" on the screen
        image_path_image = os.path.join("Images", image + ".png")

        while True:
            image_position_image = pyautogui.locateOnScreen(image_path_image, confidence=0.8)

            # If the image is found, click on it
            if image_position_image:
                image_center = pyautogui.center(image_position_image)
                pyautogui.click(image_center.x, image_center.y)
                break

            # Wait a short time before trying again
            time.sleep(0.5)
        time.sleep(0.5)
        if (image_path_image == os.path.join("Images", "Preencher" + ".png")):
            return 23

    def Role2(image):
        # Localize the position of "Encontrar partida" on the screen
        image_path_Encontrar_partida = os.path.join("Images", "Encontrar partida.png")

        while True:
            image_position_Encontrar_partida = pyautogui.locateOnScreen(image_path_Encontrar_partida, confidence=0.8)

            # If the image is found, click on it with x adjusted
            if image_position_Encontrar_partida:
                image_center = pyautogui.center(image_position_Encontrar_partida)
                x_adjusted = image_center.x + 200  # Ajuste a coordenada x aqui
                pyautogui.click(x_adjusted, image_center.y)
                break

            # Wait a short time before trying again
            time.sleep(0.5)

        # Localize the position of "image" on the screen
        image_path_image = os.path.join("Images", image + ".png")

        while True:
            image_position_image = pyautogui.locateOnScreen(image_path_image, confidence=0.8)

            # If the image is found, click on it
            if image_position_image:
                image_center = pyautogui.center(image_position_image)
                pyautogui.click(image_center.x, image_center.y)
                break

            # Wait a short time before trying again
            time.sleep(0.5)
        time.sleep(0.5)
    
    def WhereToClick():
        if not game_mode=="Apenas auto aceitar":
            [window for window in gw.getWindowsWithTitle("League of Legends") if window.title == "League of Legends"][0].minimize()
            [window for window in gw.getWindowsWithTitle("League of Legends") if window.title == "League of Legends"][0].restore()
            KeepSearchingImageAndClickWhenFound("inicio.png")
            if SearchImageForXSecondsAndClickWhenFound("OK.png", 1) == 23:
                KeepSearchingImageAndClickWhenFound("inicio.png")
            if SearchImageForXSecondsAndClickWhenFound("grupo.png",1) == 23:
                KeepSearchingImageAndClickWhenFound("sair do grupo.png")
                SearchImageForXSecondsAndClickWhenFound("sair do grupo.png",1)
                time.sleep(0.5)
                SearchImageForXSecondsAndClickWhenFound("sair do grupo.png",1)
            KeepSearchingImageAndClickWhenFound("Jogar.png")
            KeepSearchingImageAndClickWhenFound("PVP.png")
            if game_mode=="Escolha alternada" or game_mode=="Ranqueada solo duo":
                KeepSearchingImageAndClickWhenFound("Summoner's Rift.png")
            KeepSearchingImageAndClickWhenFound(game_mode+".png")
            time.sleep(0.5)
            KeepSearchingImageAndClickWhenFound("Confirmar.png")
            if game_mode!="ARAM":
                if not Role1(Role_1)==23:
                    Role2(Role_2)
            KeepSearchingImageAndClickWhenFound("Encontrar partida.png")
        while True:
            KeepSearchingImageAndClickWhenFound("Aceitar.png")

    # Criar a janela principal
    window = tk.Tk()

    window.title("Encontrar partida no LOL")
    window.configure(bg="#151515")
    window.wm_attributes("-topmost", 1)
    window.resizable(False, False)
    window.overrideredirect(True)

    frame_close = tk.Frame(window, bg="#151515")
    frame_close.pack(side="top", fill="both", expand=False, pady=3)
    
    border_label = tk.Label(window, text="Escolha o modo de jogo", bg="#151515", fg="#f0f0f0", height=2)
    border_label.pack(fill="x")

    # Textos dos botões
    textos_botões1 = ["Escolha alternada", "Ranqueada solo duo", "ARAM", "Blitz do Nexus", "Apenas auto aceitar"]
    textos_botões2 = ["Top", "Jungle", "Mid", "ADC", "Suporte", "Preencher"]

    frame_menu = tk.Frame(window, bg="#151515")
    frame_menu.pack(side="bottom", fill="both", expand=False)

    # Criar os frames para as duas telas
    frame1 = tk.Frame(window, bg="#151515")
    frame2 = tk.Frame(window, bg="#151515")

    # Botões da primeira tela
    botoes1 = [tk.Button(frame1, text=texto1, command=lambda t=texto1: Update_Game_Mode(t)) for texto1 in textos_botões1]

    # Botões da segunda tela
    botoes2 = [tk.Button(frame2, text=texto2, command=lambda t=texto2: update_roles(t)) for texto2 in textos_botões2]

    # Empacotar botões da primeira tela
    for botao in botoes1:
        botao.config(width=47, height=2, bg="#1f1f1f", fg="#f0f0f0", bd=1)  # Ajusta a largura e a altura do botão
        botao.pack(padx=17, pady=5)

    # Empacotar botões da segunda tela (inicialmente oculta)
    for botao in botoes2:
        botao.config(width=47, height=2, bg="#1f1f1f", fg="#f0f0f0", bd=1)  # Ajusta a largura e a altura do botão
        botao.pack()
    
    # Crie um Frame para agrupar o botão de desfazer e o rótulo
    frame_undo = tk.Frame(window, bg="#151515")
    frame_undo.pack(side="bottom", fill="both", expand=True)

    # Crie o botão "Desfazer" no mesmo Frame e posicione-o à direita, tocando a borda
    undo_button = tk.Button(frame_undo, text="Desfazer", command=lambda: desfazer(), bg="#1f1f1f", fg="#f0f0f0", bd=1)
    undo_button.pack(side="left", anchor="w", padx=17, pady=0)  # Adicione espaçamento

    confirm_button = tk.Button(frame_undo, text="Confirmar", command=lambda: Confirm(), bg="#1f1f1f", fg="#f0f0f0", bd=1)
    confirm_button.pack(side="right", anchor="e", padx=17, pady=0)  # Adicione espaçamento

    close_button = tk.Button(border_label, text="X", command=lambda: close_program(), bg="#d0011b", fg="#ffffff", bd=1)
    close_button.pack(side="right", anchor="e", padx=7, pady=0)

    # Redimensionar o botão para 15x16 pixels
    close_button.config(width=2, height=0, font=("Arial", 8)) # Ajustando a fonte para 8pt

    variable = tk.StringVar()
    variable.set("Modo de jogo\nescolhido:")

    label = tk.Label(frame_undo, textvariable=variable, bg="#151515", fg="white")
    label.pack(side="bottom", expand=True)  # Expande para ocupar o espaço restante

    label_auto = tk.Label(window, font=("Arial", 18), bg="#151515", fg="#f0f0f0")
    label_auto.pack(padx=0.5, pady=0.5, anchor="center", expand=True)

    thread_mensagem = threading.Thread(target=atualizar_mensagem)
    thread_mensagem.daemon = True
    thread_mensagem.start()

    frame_menu = tk.Frame(window, bg="#151515")
    frame_menu.pack(side="bottom", fill="both", expand=True, padx=10, pady=10)
    
    menu_button = tk.Button(frame_menu, text="Menu principal", command=lambda: desfazer(), bg="#1f1f1f", fg="#f0f0f0", bd=1)
    menu_button.pack(side="bottom", padx=10, pady=10)  # Adicione espaçamento

    # Iniciar na primeira tela
    game_mode_selection()

    # Iniciar o loop da aplicação
    window.mainloop()

    if not [window for window in gw.getWindowsWithTitle("League of Legends") if window.title == "League of Legends"]:
        # Wait until the window is fully open
        while not [window for window in gw.getWindowsWithTitle("League of Legends") if
                    window.title == "League of Legends"]:
            time.sleep(1)

    if Role_1=="Preencher": Role_2=0
    if game_mode=="Blitz do Nexus":
        if Role_1 == "Rota":
            Role_1 = "ADC"
            Role_2="Jungle"
        elif Role_1 == "Jungle":
            Role_2 == "ADC"

unidades = [f"{disco}:" for disco in "ABCDEFGHIJKLMNOPQRSTUVWXYZ" if os.path.exists(f"{disco}:")]
if not [window for window in gw.getWindowsWithTitle("League of Legends") if window.title == "League of Legends"]:
    if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),"league_of_legends_path.txt")):
        None
        
    else:
        def abrir_video():
            webbrowser.open("https://youtu.be/dQw4w9WgXcQ?t=0")
        video_thread = threading.Timer(20, abrir_video)
        video_thread.start()
        for unidade in unidades:
            if encontrar_e_salvar_pasta_instalacao_lol(unidade, 1) == 23:
                break
        if pasta_instalacao==None:
            for unidade in unidades:
                if encontrar_e_salvar_pasta_instalacao_lol(unidade, 2) == 23:
                  break
        
    LOL_path = os.path.join(os.path.dirname(os.path.abspath(__file__)),"league_of_legends_path.txt")
    LOL_path = LOL_path.replace("\\\\", "\\")
    
    try:
        with open(LOL_path, "r") as file:
            subprocess.Popen([file.read().strip(), '--launch-product=league_of_legends', '--launch-patchline=live'])
    except:
        try:
            os.remove(LOL_path)
        except:
            None
        for unidade in unidades:
            if encontrar_e_salvar_pasta_instalacao_lol(unidade, 1) == 23:
                break
        if pasta_instalacao==None:
            for unidade in unidades:
                if encontrar_e_salvar_pasta_instalacao_lol(unidade, 2) == 23:
                  break
        time.sleep(0.5)
        try:
            with open("league_of_legends_path.txt", "r") as file:
                subprocess.Popen([file.read().strip(), '--launch-product=league_of_legends', '--launch-patchline=live'])
        except:
            None

LOL()