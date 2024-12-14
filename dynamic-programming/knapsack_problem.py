import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
from tqdm import tqdm
from io import BytesIO

def knapsack_01_with_gif_and_progress(values, weights, capacity, gif_name="knapsack_steps.gif"):
    n = len(values)
    
    # Creiamo una matrice DP di dimensioni (n+1) x (capacity+1)
    dp = [[0] * (capacity + 1) for _ in range(n + 1)]
    
    # Lista per salvare i frame della GIF
    frames = []
    
    # Funzione per disegnare la matrice DP
    def plot_dp_matrix(dp, step, i, w, selected=False):
        plt.figure(figsize=(20, 5))
        matrix = np.array(dp)
        plt.imshow(matrix, cmap="viridis", interpolation="nearest")
        plt.colorbar(label="Value")
        plt.title(f"Step {step}: i={i}, w={w}{' (Selected)' if selected else ''}")
        plt.xlabel("Capacity")
        plt.ylabel("Items")
        plt.xticks(range(capacity + 1))
        plt.yticks(range(n + 1))
        for r in range(len(dp)):
            for c in range(len(dp[0])):
                plt.text(c, r, f"{dp[r][c]}", ha='center', va='center', color='white')
        plt.tight_layout()
        
        # Salva il grafico come immagine in memoria
        buffer = BytesIO()
        plt.savefig(buffer, format="png")
        buffer.seek(0)
        frames.append(Image.open(buffer))
        plt.close()
    
    step = 1
    # Progress bar con tqdm
    total_steps = n * (capacity + 1)
    with tqdm(total=total_steps, desc="Calcolo matrice DP") as pbar:
        # Riempimento della matrice
        for i in range(1, n + 1):
            for w in range(capacity + 1):
                if weights[i - 1] <= w:  # Se possiamo prendere l'oggetto
                    dp[i][w] = max(dp[i - 1][w], dp[i - 1][w - weights[i - 1]] + values[i - 1])
                    plot_dp_matrix(dp, step, i, w, selected=True)
                else:  # Non possiamo prendere l'oggetto
                    dp[i][w] = dp[i - 1][w]
                    plot_dp_matrix(dp, step, i, w, selected=False)
                step += 1
                pbar.update(1)  # Aggiorna la barra di progresso
    
    # Tracciamento degli oggetti inclusi nello zaino
    w = capacity
    selected_items = []
    for i in range(n, 0, -1):
        if dp[i][w] != dp[i - 1][w]:
            selected_items.append(i - 1)  # Aggiungiamo l'indice dell'oggetto
            w -= weights[i - 1]
    
    # Creazione della GIF
    frames[0].save(
        gif_name,
        save_all=True,
        append_images=frames[1:],
        duration=100,
        loop=0
    )
    
    return dp[n][capacity], selected_items

# Esempio di utilizzo
values = [60, 100, 120]
weights = [10, 20, 30]
capacity = 50

max_value, items = knapsack_01_with_gif_and_progress(values, weights, capacity, gif_name="knapsack_animation.gif")
print(f"Valore massimo: {max_value}")
print(f"Oggetti selezionati (indici): {items}")
