import customtkinter as ctk
import time
import winsound  # Para tocar um som de alarme no Windows

class RelogioDigital:
    def __init__(self, master):
        self.master = master
        master.title("Relógio com Alarme")
        master.geometry("550x300") # Aumentei um pouco a largura para caber o novo campo
        master.resizable(False, False)

        # --- Variáveis de estado para o alarme ---
        self.alarme_hora_definida = None
        self.alarme_minuto_definido = None
        # <-- CORREÇÃO 1: Inicializar a variável de segundo
        self.alarme_segundo_definido = None 
        self.alarme_ativo = False
        self.alarme_tocando = False

        # --- Configuração do Relógio ---
        self.fonte_relogio = ('Comic Sans', 80, 'bold')
        self.cor_normal_relogio = "cyan"
        self.cor_alarme_relogio = "red"
        
        self.label_relogio = ctk.CTkLabel(master, text="00:00:00", font=self.fonte_relogio, text_color=self.cor_normal_relogio)
        self.label_relogio.pack(pady=20)

        # --- Frame para os controles do Alarme ---
        frame_alarme = ctk.CTkFrame(master)
        frame_alarme.pack(pady=10, padx=20, fill="x")

        label_definir_alarme = ctk.CTkLabel(frame_alarme, text="Definir Alarme (HH:MM:SS):")
        label_definir_alarme.pack(side="left", padx=(10, 5))

        self.entry_hora = ctk.CTkEntry(frame_alarme, width=50, justify="center", placeholder_text="HH")
        self.entry_hora.pack(side="left", padx=5)

        self.entry_minuto = ctk.CTkEntry(frame_alarme, width=50, justify="center", placeholder_text="MM")
        self.entry_minuto.pack(side="left", padx=5)

        self.entry_segundo = ctk.CTkEntry(frame_alarme, width=50, justify="center", placeholder_text="SS")
        self.entry_segundo.pack(side="left", padx=5)

        self.botao_definir = ctk.CTkButton(frame_alarme, text="Definir Alarme", command=self.definir_alarme)
        self.botao_definir.pack(side="left", padx=10)

        self.botao_parar = ctk.CTkButton(frame_alarme, text="Parar Alarme", command=self.parar_alarme, fg_color="red", hover_color="#C40000")
        
        self.label_status = ctk.CTkLabel(master, text="Alarme não definido.", font=("Calibri", 14))
        self.label_status.pack(pady=10)

        self.atualizar_relogio()

    # <-- CORREÇÃO 2: Lógica de validação totalmente refatorada
    def definir_alarme(self):
        """Lê os valores dos campos de entrada, valida e ativa o alarme."""
        hora_str = self.entry_hora.get()
        minuto_str = self.entry_minuto.get()
        segundo_str = self.entry_segundo.get()

        try:
            # Valida hora e minuto (obrigatórios)
            if not (hora_str.isdigit() and minuto_str.isdigit()):
                raise ValueError("Hora e Minuto devem ser números.")
            
            h = int(hora_str)
            m = int(minuto_str)

            # Valida segundo (opcional, assume 00 se vazio)
            if segundo_str.isdigit() and segundo_str:
                s = int(segundo_str)
            elif not segundo_str: # Se o campo estiver vazio
                s = 0
                segundo_str = "00"
            else: # Se não for dígito e não estiver vazio
                raise ValueError("Segundo deve ser um número.")

            # Valida os intervalos
            if not (0 <= h <= 23 and 0 <= m <= 59 and 0 <= s <= 59):
                raise ValueError("Valores de HH, MM ou SS fora do intervalo.")

            # Se tudo for válido, define o alarme
            self.alarme_hora_definida = hora_str.zfill(2)
            self.alarme_minuto_definido = minuto_str.zfill(2)
            self.alarme_segundo_definido = segundo_str.zfill(2)
            
            self.alarme_ativo = True
            self.alarme_tocando = False # Garante que um novo alarme possa ser definido
            
            # <-- CORREÇÃO 3: Mensagem de status corrigida para incluir segundos
            self.label_status.configure(text=f"Alarme definido para {self.alarme_hora_definida}:{self.alarme_minuto_definido}:{self.alarme_segundo_definido}", text_color="yellow")
            
            # Limpa os campos e foca na hora
            self.entry_hora.delete(0, 'end')
            self.entry_minuto.delete(0, 'end')
            self.entry_segundo.delete(0, 'end')
            self.entry_hora.focus()

        except ValueError as e:
            self.label_status.configure(text=f"Erro: {e}", text_color="orange")
        except Exception as e:
            self.label_status.configure(text=f"Ocorreu um erro inesperado: {e}", text_color="red")
            
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
        self.label_status.configure(text="ALARME!", text_color="red", font=("Calibri", 16, "bold"))
        self.botao_definir.pack_forget()
        self.botao_parar.pack(side="left", padx=10)
        self.piscar_relogio()
        try:
            winsound.PlaySound("SystemAsterisk", winsound.SND_LOOP | winsound.SND_ASYNC)
        except Exception as e:
            print(f"Não foi possível tocar o som: {e}")

    def piscar_relogio(self):
        """Faz a cor do relógio piscar."""
        if self.alarme_tocando:
            cor_atual = self.label_relogio.cget("text_color")
            nova_cor = self.cor_normal_relogio if cor_atual == self.cor_alarme_relogio else self.cor_alarme_relogio
            self.label_relogio.configure(text_color=nova_cor)
            self.master.after(500, self.piscar_relogio)
        else:
            self.label_relogio.configure(text_color=self.cor_normal_relogio)

    def parar_alarme(self):
        """Para o alarme e reseta o estado."""
        self.alarme_ativo = False
        self.alarme_tocando = False
        winsound.PlaySound(None, winsound.SND_PURGE)
        self.label_status.configure(text="Alarme não definido.", text_color="white", font=("Calibri", 14))
        self.label_relogio.configure(text_color=self.cor_normal_relogio)
        self.botao_parar.pack_forget()
        self.botao_definir.pack(side="left", padx=10)

    def atualizar_relogio(self):
        """Atualiza o texto do relógio e verifica o alarme a cada segundo."""
        self.label_relogio.configure(text=time.strftime('%H:%M:%S'))
        self.verificar_alarme()
        self.master.after(1000, self.atualizar_relogio)

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    root = ctk.CTk()
    meu_relogio = RelogioDigital(root)
    root.mainloop()