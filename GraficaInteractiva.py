import numpy as np
import matplotlib.pyplot as plt

h=428
f=1000
# Función 1:
def f1(x):
    return (x)*((1-x)**(h-1))*h*f

# Función 2:
def f2(x):
    return (f-(x)*((1-x)**(h-1))*h*f-((1-x)**h)*f)

# Función 3:
def f3(x):
    return ((1-x)**h)*f

# Crear un rango de valores x
x = np.arange(0.0001, 0.701, 0.0001)

# Calcular los valores correspondientes para cada función
y1 = [f1(val) for val in x]
y2 = [f2(val) + f1(val) for val in x]
y3 = [f3(val) + f2(val) + f1(val) for val in x]

# Crear el gráfico
fig, ax = plt.subplots()

# Graficar las líneas
line1, = ax.plot(x, y1, label='Recepción correcta 1 NACK')
line2, = ax.plot(x, y2, label='Colisiones NACK + Recepción correcta 1 NACK')
line3, = ax.plot(x, y3, label='Silencio NACK + Colisiones NACK + Recepción correcta 1 NACK')

# Agregar etiquetas a los ejes
ax.set_xlabel('probabilidad p')
ax.set_ylabel('Σ de eventos')

# Agregar título al gráfico
ax.set_title(f'Σ de eventos para {h} nodos,  y {f} frames, probabilidad 0.0001 a 0.1')

# Mostrar una leyenda con la descripción de las funciones
ax.legend(loc='upper right', bbox_to_anchor=(1, 0.9))

ax.set_xscale('log')


lines = [line1, line2, line3]
line_labels = [line.get_label() for line in lines]
line_handles = [line for line in lines]

annotations = []
vlines = []
hlines = []
fill_between = []

def create_annotation(ax, x, y, label):
    text = f'{label}: {y:.2f}'
    annot = ax.annotate(text, xy=(x, y), xytext=(20, -20), textcoords="offset points",
                        bbox=dict(boxstyle="round", fc="w"),
                        arrowprops=dict(arrowstyle="->"))
    return annot

def update_annotations(event):
    x_val = event.xdata
    if x_val is not None:
        y_vals = []
        for line_handle in line_handles:
            x_vals = line_handle.get_xdata()
            y_vals_line = line_handle.get_ydata()
            nearest_idx = np.abs(x_vals - x_val).argmin()
            y_vals.append(y_vals_line[nearest_idx])
        for annotation in annotations:
            annotation.remove()
        annotations.clear()
        for vline in vlines:
            vline.remove()
        vlines.clear()
        for hline in hlines:
            hline.remove()
        hlines.clear()
        for fill in fill_between:
            fill.remove()
        fill_between.clear()
        if any(y_vals) > 0:
            for line_handle, y_val, line_label in zip(line_handles, y_vals, line_labels):
                x_vals = line_handle.get_xdata()
                y_nearest = y_val
                nearest_idx = np.abs(x_vals - x_val).argmin()
                x_nearest = x_vals[nearest_idx]
                line_label_coords = (x_nearest, y_nearest)
                annot = create_annotation(ax, x_nearest, y_nearest, line_label)
                annotations.append(annot)
                vline = ax.axvline(x_nearest, ymin=0, ymax=y_nearest / ax.get_ylim()[1], linestyle='--', color='gray')
                vlines.append(vline)
                hline = ax.axhline(y_nearest, xmin=0, xmax=x_nearest / ax.get_xlim()[1], linestyle='--', color='gray')
                hlines.append(hline)
                fill = ax.fill_between(x_vals[:nearest_idx+1], y_vals_line[:nearest_idx+1], alpha=0.1, color='gray')
                fill_between.append(fill)
        fig.canvas.draw_idle()

fig.canvas.mpl_connect("motion_notify_event", update_annotations)

# Mostrar el gráfico
plt.show()






