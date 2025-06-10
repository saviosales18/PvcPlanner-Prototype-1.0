import matplotlib.pyplot as plt
import matplotlib.patches as patches
import tkinter as tk
import math

PLACA_W = 0.625
PLACA_H = 1.25
CANTONEIRA = 3.00
PERFIL_PRINCIPAL = 3.00
PERFIL_DERIVADO = 1.25

SALAS = {
    "Sala 01": (17.00, 15.00),
    "Sala 07": (7.10, 6.10),
    "Sala 08": (7.00, 7.00),
    "Circulação": (12.00, 1.20),
    "Área da escada": (6.80, 3.00),
    "Sanitário Feminino": (4.00, 2.80)
}

class Layout:
    def __init__(self, root):
        self.root = root
        self.root.title("Pvc Planner")
        self.root.geometry("800x400")

        self.roll_width = tk.DoubleVar(value=3000)
        self.roll_height = tk.DoubleVar(value=150)
        self.cuts = []

def calcular_materiais(comp, larg):
    if comp >= larg:
        sentido = "horizontal"
        n_placas_linha = math.ceil(comp / PLACA_H)
        n_linhas = math.ceil(larg / PLACA_W)
        dim_placa1 = PLACA_H
        dim_placa2 = PLACA_W
    else:
        sentido = "vertical"
        n_placas_linha = math.ceil(comp / PLACA_W)
        n_linhas = math.ceil(larg / PLACA_H)
        dim_placa1 = PLACA_W
        dim_placa2 = PLACA_H

    area_sala = comp * larg
    quantidade_pvc = n_placas_linha * n_linhas
    area_total_pvc = (PLACA_W * PLACA_H) * quantidade_pvc

    comprimento_cantoneira_total = 2 * (comp + larg)
    quantidade_cantoneira = math.ceil(comprimento_cantoneira_total / CANTONEIRA)
    sobra_cantoneira = quantidade_cantoneira * CANTONEIRA - comprimento_cantoneira_total

    n_colunas = n_placas_linha - 1
    comprimento_perfil_principal_total = n_colunas * (larg if sentido == "horizontal" else comp)
    quantidade_perfil_principal = math.ceil(comprimento_perfil_principal_total / PERFIL_PRINCIPAL)
    sobra_perfil_principal = quantidade_perfil_principal * PERFIL_PRINCIPAL - comprimento_perfil_principal_total

    quantidade_perfil_derivado = (n_linhas - 1) * n_placas_linha
    comprimento_perfil_derivado_total = quantidade_perfil_derivado * PERFIL_DERIVADO
    sobra_perfil_derivado = comprimento_perfil_derivado_total % PERFIL_DERIVADO

    return {
        "sentido": sentido,
        "n_placas_linha": n_placas_linha,
        "n_linhas": n_linhas,
        "dim_placa1": dim_placa1,
        "dim_placa2": dim_placa2,
        "area_sala": area_sala,
        "quantidade_pvc": quantidade_pvc,
        "area_total_pvc": area_total_pvc,
        "comprimento_cantoneira_total": comprimento_cantoneira_total,
        "quantidade_cantoneira": quantidade_cantoneira,
        "sobra_cantoneira": sobra_cantoneira,
        "comprimento_perfil_principal_total": comprimento_perfil_principal_total,
        "quantidade_perfil_principal": quantidade_perfil_principal,
        "sobra_perfil_principal": sobra_perfil_principal,
        "quantidade_perfil_derivado": quantidade_perfil_derivado,
        "comprimento_perfil_derivado_total": comprimento_perfil_derivado_total,
        "sobra_perfil_derivado": sobra_perfil_derivado
    }

def desenhar_sala(sala_nome, comp, larg):
    materiais = calcular_materiais(comp, larg)
    fig, ax = plt.subplots(figsize=(10, 6))

    for i in range(materiais["n_linhas"]):
        for j in range(materiais["n_placas_linha"]):
            x = j * materiais["dim_placa1"]
            y = i * materiais["dim_placa2"]
            rect = patches.Rectangle(
                (x, y),
                materiais["dim_placa1"],
                materiais["dim_placa2"],
                edgecolor='black',
                facecolor='lightgray'
            )
            ax.add_patch(rect)

    outline = patches.Rectangle(
        (0, 0), comp, larg,
        linewidth=2, edgecolor='blue',
        facecolor='none', linestyle='--'
    )
    ax.add_patch(outline)

    for j in range(1, materiais["n_placas_linha"]):
        x = j * materiais["dim_placa1"]
        ax.plot([x, x], [0, larg], color='red', linewidth=1)

    for i in range(1, materiais["n_linhas"]):
        y = i * materiais["dim_placa2"]
        ax.plot([0, comp], [y, y], color='yellow', linewidth=1)

    label = (
        f"Tamanho da Sala: {comp:.2f}m x {larg:.2f}m / {materiais['area_sala']:.2f}m²\n"
        f"Dimensões do PVC: {PLACA_H:.2f}m x {PLACA_W:.2f}m\n"
        f"Placas de PVC utilizadas: {materiais['quantidade_pvc']} unidades\n"
        f"Sobra de Placas PVC: {materiais['area_total_pvc'] - materiais['area_sala']:.2f}m²\n"
        f"Cantoneira: {materiais['quantidade_cantoneira']} unidades ({materiais['comprimento_cantoneira_total']:.2f}m), sobra: {materiais['sobra_cantoneira']:.2f}m\n"
        f"Perfil Principal: {materiais['quantidade_perfil_principal']} unidades ({materiais['comprimento_perfil_principal_total']:.2f}m), sobra: {materiais['sobra_perfil_principal']:.2f}m\n"
        f"Perfil Derivado: {materiais['quantidade_perfil_derivado']} unidades ({materiais['comprimento_perfil_derivado_total']:.2f}m), sobra: {materiais['sobra_perfil_derivado']:.2f}m"
    )
    ax.text(0, -0.5, label, fontsize=10, ha='left', va='top', bbox=dict(facecolor='white', alpha=0.7))

    ax.set_xlim(-3, comp + 3)
    ax.set_ylim(-3, larg + 3)
    ax.set_anchor('S')
    ax.set_aspect('equal')
    ax.set_title(
        f"{sala_nome} | Sentido: {'Comprimento (→)' if materiais['sentido'] == 'horizontal' else 'Largura (↑)'}",
        fontsize=14
    )
    ax.axis('off')
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    for nome, (comp, larg) in SALAS.items():
        desenhar_sala(nome, comp, larg)