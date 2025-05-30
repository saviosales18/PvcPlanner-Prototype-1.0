import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
import math

class Layout:
    def __init__(self, root):
        self.root = root
        self.root.title("Pvc Planner")
        self.root.geometry("800x400")

        self.roll_width = tk.DoubleVar(value=3000)
        self.roll_height = tk.DoubleVar(value=150)
        self.cuts = []

placa_w = 0.625
placa_h = 1.25

comprimento_cantoneira = 3.00
comprimento_perfil_principal = 3.00
comprimento_perfil_derivado = 1.25

salas = {
    "Sala 01": (17.00, 15.00),
    "Sala 07": (7.10, 6.10),
    "Sala 08": (7.00, 7.00),
    "Circulação": (12.00, 1.20),
    "Área da escada": (6.80, 3.00),
    "Sanitário Feminino": (4.00, 2.80)
}

def desenhar_sala(sala_nome, comp, larg):
    fig, ax = plt.subplots(figsize=(10, 6))

    # Determinar o sentido de paginação no diagrama
    if comp >= larg:
        sentido = "horizontal"
        n_placas_linha = math.ceil(comp / placa_h)
        n_linhas = math.ceil(larg / placa_w)
    else:
        sentido = "vertical"
        n_placas_linha = math.ceil(comp / placa_w)
        n_linhas = math.ceil(larg / placa_h)

    area_sala = comp * larg

    quantidade_pvc = n_placas_linha * n_linhas
    area_total_pvc = (placa_w * placa_h) * quantidade_pvc

    comprimento_cantoneira_total = 2 * (comp + larg)
    quantidade_cantoneira = math.ceil(comprimento_cantoneira_total / comprimento_cantoneira)
    sobra_cantoneira = quantidade_cantoneira * comprimento_cantoneira - comprimento_cantoneira_total

    # Cálculo do perfil principal
    if sentido == "horizontal":
        n_colunas = n_placas_linha - 1
        comprimento_perfil_principal_total = n_colunas * larg
    else:
        n_colunas = n_placas_linha - 1
        comprimento_perfil_principal_total = n_colunas * comp

    quantidade_perfil_principal = math.ceil(comprimento_perfil_principal_total / comprimento_perfil_principal)
    sobra_perfil_principal = quantidade_perfil_principal * comprimento_perfil_principal - comprimento_perfil_principal_total

    quantidade_perfil_derivado = (n_linhas - 1) * n_placas_linha
    comprimento_perfil_derivado_total = quantidade_perfil_derivado * comprimento_perfil_derivado
    sobra_perfil_derivado = comprimento_perfil_derivado_total % comprimento_perfil_derivado

    for i in range(n_linhas):
        for j in range(n_placas_linha):
            x = j * (placa_h if sentido == "horizontal" else placa_w)
            y = i * (placa_w if sentido == "horizontal" else placa_h)
            rect = patches.Rectangle((x, y), (placa_h if sentido == "horizontal" else placa_w),
                                      (placa_w if sentido == "horizontal" else placa_h),
                                      edgecolor='black', facecolor='lightgray')
            ax.add_patch(rect)

    # Contorno da sala
    outline = patches.Rectangle((0, 0), comp, larg, linewidth=2, edgecolor='blue', facecolor='none', linestyle='--')
    ax.add_patch(outline)

    # Perfis principais
    for j in range(1, n_placas_linha):
        x = j * (placa_h if sentido == "horizontal" else placa_w)
        ax.plot([x, x], [0, larg], color='red', linewidth=1)

    # Perfis derivados
    for i in range(1, n_linhas):
        y = i * (placa_w if sentido == "horizontal" else placa_h)
        ax.plot([0, comp], [y, y], color='yellow', linewidth=1)

    label = (
        f"Tamanho da Sala: {comp:.2f}m x {larg:.2f}m / {area_sala:.2f}m²\n"
        f"Dimensões do PVC: {placa_h:.2f}m x {placa_w:.2f}m\n"
        f"Placas de PVC utilizadas: {quantidade_pvc} unidades\n"
        f"Sobra de Placas PVC: {area_total_pvc - area_sala:.2f}m²\n"
        f"Cantoneira: {quantidade_cantoneira} unidades ({comprimento_cantoneira_total:.2f}m), sobra: {sobra_cantoneira:.2f}m\n"
        f"Perfil Principal (Vertical): {quantidade_perfil_principal} unidades ({comprimento_perfil_principal_total:.2f}m), sobra: {sobra_perfil_principal:.2f}m\n"
        f"Perfil Derivado (Horizontal): {quantidade_perfil_derivado} unidades ({comprimento_perfil_derivado_total:.2f}m), sobra: {sobra_perfil_derivado:.2f}m"
    )
    ax.text(0 ,-0.5 , label, fontsize=10, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7))

    ax.set_xlim(-3, comp + 3)
    ax.set_ylim(-3, larg + 3)
    ax.set_anchor('S')
    ax.set_aspect('equal')
    ax.set_title(f"{sala_nome} | Sentido: {'Comprimento (→)' if sentido == "horizontal" else 'Largura (↑)'}", fontsize=14)
    ax.axis('off')
    plt.tight_layout()
    plt.show()

for nome, (comp, larg) in salas.items():
    desenhar_sala(nome, comp, larg)