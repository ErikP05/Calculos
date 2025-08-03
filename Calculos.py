import streamlit as st
import numpy as np
import plotly.graph_objects as go

# Funciones matemáticas
def vector(a, b):
    return np.array([b[i] - a[i] for i in range(3)])

def producto_cruz(v1, v2):
    return np.cross(v1, v2)

def distancia_punto_a_plano(G, J, S, T):
    JS = vector(J, S)
    JT = vector(J, T)
    N = producto_cruz(JS, JT)
    JG = vector(J, G)
    denominador = np.linalg.norm(N)
    if denominador == 0:
        return None
    numerador = abs(np.dot(JG, N))
    distancia = numerador / denominador
    return distancia

# Función para graficar el plano y los puntos en 3D con Plotly
def graficar_plano_y_puntos(G, J, S, T):
    J = np.array(J)
    S = np.array(S)
    T = np.array(T)
    G = np.array(G)

    u = T - J
    v = S - J

    s_vals = np.linspace(0, 1, 10)
    t_vals = np.linspace(0, 1, 10)

    # Crear todos los puntos del plano combinando s y t
    plane_points = np.array([J + s * u + t * v for s in s_vals for t in t_vals])

    x_plane = plane_points[:, 0]
    y_plane = plane_points[:, 1]
    z_plane = plane_points[:, 2]

    JS = vector(J, S)
    JT = vector(J, T)
    N = producto_cruz(JS, JT)
    N_unitario = N / np.linalg.norm(N)
    proyeccion = G - np.dot(G - J, N_unitario) * N_unitario

    fig = go.Figure(data=[
        # Puntos del plano J, S, T
        go.Scatter3d(
            x=[J[0], S[0], T[0]],
            y=[J[1], S[1], T[1]],
            z=[J[2], S[2], T[2]],
            mode='markers',
            marker=dict(size=5, color='blue'),
            name='Puntos del plano'
        ),

        # Punto G
        go.Scatter3d(
            x=[G[0]],
            y=[G[1]],
            z=[G[2]],
            mode='markers',
            marker=dict(size=7, color='pink'),
            name='Punto G'
        ),

        go.Scatter3d(
            x=[proyeccion[0]],
            y=[proyeccion[1]],
            z=[proyeccion[2]],
            mode='markers',
            marker=dict(size=6, color='green'),
            name='Proyección de G'
        ),

        go.Scatter3d(
            x=[G[0], proyeccion[0]],
            y=[G[1], proyeccion[1]],
            z=[G[2], proyeccion[2]],
            mode='lines',
            line=dict(color='red', width=4),
            name='Distancia'
        ),

        # Plano como malla
        go.Mesh3d(
            x=x_plane,
            y=y_plane,
            z=z_plane,
            alphahull=0,
            opacity=0.5,
            color='cyan',
            name='Plano'
        ),
        # Vector JT (de J a T)
        go.Scatter3d(
            x=[J[0], T[0]],
            y=[J[1], T[1]],
            z=[J[2], T[2]],
            mode='lines+markers',
            line=dict(color='orange', width=5),
            marker=dict(size=4, color='orange'),
            name='Vector JT'
        ),

        # Vector JS (de J a S)
        go.Scatter3d(
            x=[J[0], S[0]],
            y=[J[1], S[1]],
            z=[J[2], S[2]],
            mode='lines+markers',
            line=dict(color='purple', width=5),
            marker=dict(size=4, color='purple'),
            name='Vector JS'
        ),

        # Vector normal N (de J hacia J+N_unitario)
        go.Scatter3d(
            x=[J[0], J[0] + N_unitario[0]],
            y=[J[1], J[1] + N_unitario[1]],
            z=[J[2], J[2] + N_unitario[2]],
            mode='lines+markers',
            line=dict(color='black', width=5, dash='dash'),
            marker=dict(size=4, color='black'),
            name='Vector normal N'
        ),

        # Vector desde la proyección al punto G (distancia)
        go.Scatter3d(
            x=[proyeccion[0], G[0]],
            y=[proyeccion[1], G[1]],
            z=[proyeccion[2], G[2]],
            mode='lines',
            line=dict(color='red', width=4),
            showlegend=False
        )
    ])

    fig.update_layout(
        scene=dict(
            xaxis_title='X',
            yaxis_title='Y',
            zaxis_title='Z'
        ),
        width=700,
        height=700,
        margin=dict(r=10, l=10, b=10, t=10)
    )

    st.plotly_chart(fig)

# Función para pedir puntos con Streamlit
def pedir_punto_tabla(nombre):
    st.markdown(f"**{nombre}**")
    cols = st.columns(3)
    # Encabezado tabla
    cols[0].markdown("**x**")
    cols[1].markdown("**y**")
    cols[2].markdown("**z**")
    # Inputs
    x = cols[0].number_input("i", value=0.0, key=f"x_{nombre}")
    y = cols[1].number_input("j", value=0.0, key=f"y_{nombre}")
    z = cols[2].number_input("k", value=0.0, key=f"z_{nombre}")
    return [x, y, z]

# Título e instrucciones
st.title("Calculadora y gráfica de la distancia de un punto a un plano")
st.write("Introduce las coordenadas de cada punto (x, y, z):")

# Pedir puntos
st.subheader("Punto G (fuera del plano)")
G = pedir_punto_tabla("G")

st.subheader("Puntos que definen el plano")
J = pedir_punto_tabla("J")
S = pedir_punto_tabla("S")
T = pedir_punto_tabla("T")

# Botón para calcular y mostrar resultado y gráfica
if st.button("Calcular distancia y mostrar gráfica"):
    dist = distancia_punto_a_plano(G, J, S, T)
    if dist is None:
        st.error("Los puntos J, S y T no forman un plano válido (están colineales).")
    else:
        if dist == 0:
            st.success(f"El punto G está en el plano (distancia = 0).")
        else:
            st.success(f"La distancia del punto G al plano es: {dist:.4f}")

        graficar_plano_y_puntos(G, J, S, T)