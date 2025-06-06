import tkinter as tk
from tkinter import font
import time
import winsound  # Para tocar um som de alarme no Windows

class RelogioDigital:
    def __init__(self, master):
        self.master = master
        master.title("Relógio com Alarme (Tkinter)")
        master.geometry("550x320") # Um pouco mais de altura para os widgets padrão
        master.resizable(False, False)
        
        # --- Configuração do Tema Escuro (Manual) ---
        self.cor_fundo = "#2B2B2B"
        self.cor_texto_normal = "cyan"
        self.cor_texto_alarme = "red"
        self.cor_widget = "#555555"
        self.cor_borda_foco = "cyan"
        master.configure(bg=self.cor_fundo)

        # --- Variáveis de estado para o alarme ---
        self.alarme_hora_definida = None
        self.alarme_minuto_definido = None
        self.alarme_segundo_definido = None 
        self.alarme_ativo = False
        self.alarme_tocando = False

        # --- Configuração do Relógio ---
        self.fonte_relogio = font.Font(family='Consolas', size=80, weight='bold')
        
        self.label_relogio = tk.Label(master, text="00:00:00", font=self.fonte_relogio, 
                                      fg=self.cor_texto_normal, bg=self.cor_fundo)
        self.label_relogio.pack(pady=20)

        # --- Frame para os controles do Alarme ---
        frame_alarme = tk.Frame(master, bg=self.cor_fundo)
        frame_alarme.pack(pady=10, padx=20, fill="x")

        label_definir_alarme = tk.Label(frame_alarme, text="Definir Alarme (HH:MM:SS):", 
                                        bg=self.cor_fundo, fg="white")
        label_definir_alarme.pack(side="left", padx=(10, 5))
        
        # --- Campos de Entrada (Entry) com Placeholder Simulado ---
        self.entry_hora = self.criar_entry_com_placeholder(frame_alarme, "HH")
        self.entry_hora.pack(side="left", padx=5)

        self.entry_minuto = self.criar_entry_com_placeholder(frame_alarme, "MM")
        self.entry_minuto.pack(side="left", padx=5)

        self.entry_segundo = self.criar_entry_com_placeholder(frame_alarme, "SS")
        self.entry_segundo.pack(side="left", padx=5)

        # --- Botões ---
        self.botao_definir = tk.Button(frame_alarme, text="Definir Alarme", command=self.definir_alarme, 
                                       fg="white", bg="#007ACC", activebackground="#005f9e", 
                                       activeforeground="white", borderwidth=0, cursor="hand2")
        self.botao_definir.pack(side="left", padx=10)
        self.adicionar_efeito_hover(self.botao_definir, "#0090f0", "#007ACC")


        self.botao_parar = tk.Button(frame_alarme, text="Parar Alarme", command=self.parar_alarme, 
                                     fg="white", bg="red", activebackground="#a10000",
                                     activeforeground="white", borderwidth=0, cursor="hand2")
        self.adicionar_efeito_hover(self.botao_parar, "#ff3333", "red")
        # O botão parar só será exibido quando o alarme tocar, então não usamos o .pack() aqui
        
        # --- Label de Status ---
        self.fonte_status = font.Font(family='Calibri', size=14)
        self.label_status = tk.Label(master, text="Alarme não definido.", font=self.fonte_status,
                                     bg=self.cor_fundo, fg="white")
        self.label_status.pack(pady=10)

        self.atualizar_relogio()

    def criar_entry_com_placeholder(self, parent, placeholder):
        """Cria um tk.Entry e simula um placeholder."""
        entry = tk.Entry(parent, width=5, justify="center", font=('Calibri', 12),
                         bg=self.cor_widget, fg="gray", borderwidth=2, relief="groove",
                         insertbackground=self.cor_texto_normal) # Cor do cursor
        entry.insert(0, placeholder)
        entry.bind("<FocusIn>", lambda event: self.on_entry_focus_in(event, placeholder))
        entry.bind("<FocusOut>", lambda event: self.on_entry_focus_out(event, placeholder))
        return entry

    def on_entry_focus_in(self, event, placeholder):
        """Limpa o placeholder quando o usuário clica no campo."""
        entry = event.widget
        if entry.get() == placeholder:
            entry.delete(0, 'end')
            entry.config(fg='white')

    def on_entry_focus_out(self, event, placeholder):
        """Recoloca o placeholder se o campo estiver vazio."""
        entry = event.widget
        if not entry.get():
            entry.insert(0, placeholder)
            entry.config(fg='gray')
            
    def adicionar_efeito_hover(self, button, hover_color, default_color):
        """Adiciona um efeito de hover a um botão."""
        button.bind("<Enter>", lambda e: button.config(bg=hover_color))
        button.bind("<Leave>", lambda e: button.config(bg=default_color))

    def definir_alarme(self):
        """Lê os valores dos campos de entrada, valida e ativa o alarme."""
        hora_str = self.entry_hora.get()
        minuto_str = self.entry_minuto.get()
        segundo_str = self.entry_segundo.get()
        
        # Ignorar placeholders na validação
        if hora_str == "HH": hora_str = ""
        if minuto_str == "MM": minuto_str = ""
        if segundo_str == "SS": segundo_str = ""
        
        try:
            if not (hora_str.isdigit() and minuto_str.isdigit()):
                raise ValueError("Hora e Minuto devem ser números.")
            
            h = int(hora_str)
            m = int(minuto_str)

            if segundo_str.isdigit() and segundo_str:
                s = int(segundo_str)
            elif not segundo_str:
                s = 0
                segundo_str = "00"
            else:
                raise ValueError("Segundo deve ser um número.")

            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValueError("Valores de HH, MM ou SS fora do intervalo.")

            self.alarme_hora_definida = hora_str.zfill(2)
            self.alarme_minuto_definido = minuto_str.zfill(2)
            self.alarme_segundo_definido = segundo_str.zfill(2)
            
            self.alarme_ativo = True
            self.alarme_tocando = False
            
            self.label_status.config(text=f"Alarme definido para {self.alarme_hora_definida}:{self.alarme_minuto_definido}:{self.alarme_segundo_definido}", fg="yellow")
            
            # Limpa os campos e reseta os placeholders
            for entry, placeholder in [(self.entry_hora, "HH"), (self.entry_minuto, "MM"), (self.entry_segundo, "SS")]:
                entry.delete(0, 'end')
                self.on_entry_focus_out(tk.Event(), placeholder) # Simula o evento de perder o foco
            self.master.focus() # Tira o foco dos campos de entrada

        except ValueError as e:
            self.label_status.config(text=f"Erro: {e}", fg="orange")
        except Exception as e:
            self.label_status.config(text=f"Ocorreu um erro inesperado: {e}", fg="red")
            
    def verificar_alarme(self):
        """Verifica se a hora atual corresponde à hora do alarme."""
        if self.alarme_ativo and not self.alarme_tocando:
            if (time.strftime('%H') == self.alarme_hora_definida and
                time.strftime('%M') == self.alarme_minuto_definido and
                time.strftime('%S') == self.alarme_segundo_definido):
                self.disparar_alarme()

    def disparar_alarme(self):
        """Ação a ser executada quando o alarme dispara."""
        self.alarme_tocando = True
        fonte_alarme = font.Font(family='Calibri', size=16, weight='bold')
        self.label_status.config(text="ALARME!", fg="red", font=fonte_alarme)
        self.botao_definir.pack_forget()
        self.botao_parar.pack(side="left", padx=10)
        self.piscar_relogio()
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_LOOP | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Não foi possível tocar o som (normal em sistemas não-Windows): {e}")

    def piscar_relogio(self):
        """Faz a cor do relógio piscar."""
        if self.alarme_tocando:
            cor_atual = self.label_relogio.cget("fg")
            nova_cor = self.cor_texto_normal if cor_atual == self.cor_texto_alarme else self.cor_texto_alarme
            self.label_relogio.config(fg=nova_cor)
            self.master.after(500, self.piscar_relogio)
        else:
            self.label_relogio.config(fg=self.cor_texto_normal)

    def parar_alarme(self):
        """Para o alarme e reseta o estado."""
        self.alarme_ativo = False
        self.alarme_tocando = False
        try:
            winsound.PlaySound(None, winsound.SND_PURGE)
        except Exception:
            pass # Ignora erro se não puder parar o som
        self.label_status.config(text="Alarme não definido.", fg="white", font=self.fonte_status)
        self.label_relogio.config(fg=self.cor_texto_normal)
        self.botao_parar.pack_forget()
        self.botao_definir.pack(side="left", padx=10)

    def atualizar_relogio(self):
        """Atualiza o texto do relógio e verifica o alarme a cada segundo."""
        self.label_relogio.config(text=time.strftime('%H:%M:%S'))
        self.verificar_alarme()
        self.master.after(1000, self.atualizar_relogio)

if __name__ == "__main__":
    root = tk.Tk()
    meu_relogio = RelogioDigital(root)
    root.mainloop()
