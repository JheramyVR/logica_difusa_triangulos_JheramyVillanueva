"""
Sistema de Lógica Difusa - Triángulo Rectángulo
"""

import numpy as np
import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from dash import Dash, dcc, html, Input, Output, State, callback_context
import dash_bootstrap_components as dbc

# ============================================================================
# CÁLCULOS
# ============================================================================

def area_triangulo(x):
    """Área del triángulo desde origen hasta x"""
    if x <= 0 or x > 12:
        return 0
    return 0.25 * x * x

def calcular_delta_exacto(x_ini, area_adicional=4):
    """Calcula Δx exacto para generar área_adicional desde x_ini"""
    x_final = np.sqrt(x_ini**2 + 4 * area_adicional)
    x_final = min(x_final, 12)
    return x_final - x_ini

# ============================================================================
# LÓGICA DIFUSA
# ============================================================================

def membresia_triangular(x, a, b, c):
    """Función de membresía triangular"""
    if x <= a:
        return 1.0 if a == b else 0.0
    if x >= c:
        return 1.0 if b == c else 0.0
    if a < x <= b:
        return (x - a) / (b - a) if b > a else 1.0
    return (c - x) / (c - b) if c > b else 1.0

class LogicaDifusa:
    """Sistema de lógica difusa"""

    def __init__(self):
        self.definir_sistema()

    def definir_sistema(self):
        """Define conjuntos difusos"""

        # ========== CONJUNTOS PARA ERROR ==========
        self.error_sets = {
            'cero': lambda e: max(0, 1 - abs(e) / 0.03),
            'micro': lambda e: membresia_triangular(abs(e), 0.02, 0.08, 0.2),
            'muy_muy_pequeño': lambda e: membresia_triangular(abs(e), 0.15, 0.35, 0.7),
            'muy_pequeño': lambda e: membresia_triangular(abs(e), 0.5, 0.9, 1.5),
            'pequeño': lambda e: membresia_triangular(abs(e), 1.2, 1.8, 2.8),
            'pequeño_medio': lambda e: membresia_triangular(abs(e), 2.5, 3.5, 4.8),
            'mediano': lambda e: membresia_triangular(abs(e), 4.2, 5.5, 7.5),
            'mediano_grande': lambda e: membresia_triangular(abs(e), 7, 9, 12),
            'grande': lambda e: membresia_triangular(abs(e), 11, 15, 20),
            'muy_grande': lambda e: membresia_triangular(abs(e), 18, 25, 40)
        }

        # ========== CONJUNTOS PARA POSICIÓN ==========
        self.pos_sets = {
            'muy_inicio': lambda x: membresia_triangular(x, 0, 0, 1.5),
            'inicio': lambda x: membresia_triangular(x, 0.8, 2, 3.5),
            'bajo': lambda x: membresia_triangular(x, 2.5, 4, 5.5),
            'medio_bajo': lambda x: membresia_triangular(x, 4.5, 6, 7.5),
            'medio_alto': lambda x: membresia_triangular(x, 6.5, 8, 9.5),
            'alto': lambda x: membresia_triangular(x, 8.5, 10, 12)
        }

        # ========== REGLAS - 60 REGLAS ==========
        self.reglas = {
            # ERROR: cero
            ('cero', 'muy_inicio'): 0,
            ('cero', 'inicio'): 0,
            ('cero', 'bajo'): 0,
            ('cero', 'medio_bajo'): 0,
            ('cero', 'medio_alto'): 0,
            ('cero', 'alto'): 0,

            # ERROR: micro
            ('micro', 'muy_inicio'): 0.12,
            ('micro', 'inicio'): 0.10,
            ('micro', 'bajo'): 0.08,
            ('micro', 'medio_bajo'): 0.06,
            ('micro', 'medio_alto'): 0.05,
            ('micro', 'alto'): 0.04,

            # ERROR: muy_muy_pequeño
            ('muy_muy_pequeño', 'muy_inicio'): 0.35,
            ('muy_muy_pequeño', 'inicio'): 0.30,
            ('muy_muy_pequeño', 'bajo'): 0.25,
            ('muy_muy_pequeño', 'medio_bajo'): 0.20,
            ('muy_muy_pequeño', 'medio_alto'): 0.15,
            ('muy_muy_pequeño', 'alto'): 0.10,

            # ERROR: muy_pequeño
            ('muy_pequeño', 'muy_inicio'): 0.70,
            ('muy_pequeño', 'inicio'): 0.60,
            ('muy_pequeño', 'bajo'): 0.50,
            ('muy_pequeño', 'medio_bajo'): 0.40,
            ('muy_pequeño', 'medio_alto'): 0.30,
            ('muy_pequeño', 'alto'): 0.20,

            # ERROR: pequeño
            ('pequeño', 'muy_inicio'): 1.20,
            ('pequeño', 'inicio'): 1.00,
            ('pequeño', 'bajo'): 0.80,
            ('pequeño', 'medio_bajo'): 0.65,
            ('pequeño', 'medio_alto'): 0.50,
            ('pequeño', 'alto'): 0.35,

            # ERROR: pequeño_medio
            ('pequeño_medio', 'muy_inicio'): 1.90,
            ('pequeño_medio', 'inicio'): 1.60,
            ('pequeño_medio', 'bajo'): 1.30,
            ('pequeño_medio', 'medio_bajo'): 1.00,
            ('pequeño_medio', 'medio_alto'): 0.75,
            ('pequeño_medio', 'alto'): 0.50,

            # ERROR: mediano
            ('mediano', 'muy_inicio'): 2.80,
            ('mediano', 'inicio'): 2.40,
            ('mediano', 'bajo'): 2.00,
            ('mediano', 'medio_bajo'): 1.50,
            ('mediano', 'medio_alto'): 1.10,
            ('mediano', 'alto'): 0.70,

            # ERROR: mediano_grande
            ('mediano_grande', 'muy_inicio'): 3.80,
            ('mediano_grande', 'inicio'): 3.30,
            ('mediano_grande', 'bajo'): 2.80,
            ('mediano_grande', 'medio_bajo'): 2.20,
            ('mediano_grande', 'medio_alto'): 1.60,
            ('mediano_grande', 'alto'): 1.00,

            # ERROR: grande
            ('grande', 'muy_inicio'): 4.80,
            ('grande', 'inicio'): 4.20,
            ('grande', 'bajo'): 3.60,
            ('grande', 'medio_bajo'): 2.80,
            ('grande', 'medio_alto'): 2.00,
            ('grande', 'alto'): 1.30,

            # ERROR: muy_grande
            ('muy_grande', 'muy_inicio'): 6.00,
            ('muy_grande', 'inicio'): 5.20,
            ('muy_grande', 'bajo'): 4.40,
            ('muy_grande', 'medio_bajo'): 3.50,
            ('muy_grande', 'medio_alto'): 2.50,
            ('muy_grande', 'alto'): 1.60,
        }

    def inferir(self, error, x_pos):
        """
        Inferencia difusa Mamdani
        """
        activaciones = []

        for (err_set, pos_set), output in self.reglas.items():
            # Fuzzificación
            grado_error = self.error_sets[err_set](error)
            grado_pos = self.pos_sets[pos_set](x_pos)

            # Inferencia (T-norma MIN de Mamdani)
            activacion = min(grado_error, grado_pos)

            if activacion > 0:
                activaciones.append((activacion, output))

        if not activaciones:
            return 0

        # Defuzzificación: centroide ponderado
        num = sum(act * val for act, val in activaciones)
        den = sum(act for act, _ in activaciones)
        resultado = num / den if den > 0 else 0

        return resultado

    def calcular(self, x_ini, area_objetivo, max_iter=150):
        """
        Calcula desplazamiento iterativo
        """
        x = x_ini
        a_ini = area_triangulo(x_ini)
        a_target = a_ini + area_objetivo

        historial = []

        for i in range(max_iter):
            a_actual = area_triangulo(x)
            error = a_target - a_actual

            historial.append({
                'iter': i,
                'x': x,
                'area': a_actual,
                'error': error
            })

            # Criterio 1: Error suficientemente pequeño (más flexible)
            if abs(error) < 0.02:
                break

            # Criterio 2: Convergencia detectada - no hay mejora significativa
            if i >= 5:
                # Revisar últimas 5 iteraciones
                ultimos_x = [h['x'] for h in historial[-5:]]

                # Si la posición casi no cambia, ya convergió
                variacion_x = max(ultimos_x) - min(ultimos_x)
                if variacion_x < 0.005:
                    break

                # Si el error oscila sin mejorar sustancialmente
                ultimos_errores = [abs(h['error']) for h in historial[-5:]]
                variacion_error = max(ultimos_errores) - min(ultimos_errores)
                if variacion_error < 0.01 and min(ultimos_errores) > 0.01:
                    # Oscila sin mejorar, detener
                    break

            # Criterio 3: Progreso muy lento (estancamiento real)
            if i >= 10:
                # Comparar primeras 3 vs últimas 3 iteraciones
                error_inicial_promedio = np.mean([abs(h['error']) for h in historial[5:8]])
                error_reciente_promedio = np.mean([abs(h['error']) for h in historial[-3:]])

                # Si el error apenas mejoró en las últimas iteraciones, parar
                mejora = error_inicial_promedio - error_reciente_promedio
                if mejora < 0.01:
                    break

            # ========== INFERENCIA DIFUSA ==========
            delta = self.inferir(abs(error), x)

            # Ajustar dirección según el signo del error
            if error < 0:
                delta = -delta

            # Actualizar posición
            x_nuevo = np.clip(x + delta, 0, 12)

            # Criterio 4: Cambio insignificante en x
            if abs(x_nuevo - x) < 0.0001:
                break

            x = x_nuevo

        return x - x_ini, pd.DataFrame(historial)

# ============================================================================
# APLICACIÓN DASH - VISUALIZACION
# ============================================================================

sistema = LogicaDifusa()

app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

app.layout = dbc.Container([
    html.H1("🔬 Sistema de Lógica Difusa - Triángulo Rectángulo",
            className="text-center my-4"),

    html.Div([
        html.H6("✨ 60 reglas ",
                className="text-center text-success mb-3")
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("⚙️ CONFIGURACIÓN"),
                dbc.CardBody([
                    html.Label("Posición inicial (x):"),
                    dcc.Slider(0, 12, 1, value=0, id='x-ini',
                              marks={i: str(i) for i in range(13)}),
                    html.Br(),
                    html.Label("Área adicional objetivo:"),
                    dcc.Slider(1, 10, 0.5, value=4, id='area-obj',
                              marks={i: str(i) for i in range(1, 11)}),
                    html.Br(),
                    dbc.Button("1️⃣ Mostrar Estado Inicial",
                              id='btn-inicial', color="info",
                              className="w-100 mb-2"),
                    dbc.Button("2️⃣ Ejecutar Lógica Difusa",
                              id='btn-ejecutar', color="success",
                              className="w-100"),
                    html.Hr(),
                    html.Div(id='info-resultado')
                ])
            ])
        ], width=3),

        dbc.Col([
            dcc.Graph(id='grafico-principal',
                     style={'height': '600px'})
        ], width=9)
    ], className="mb-4"),

    dbc.Row([
        dbc.Col([
            dcc.Graph(id='grafico-convergencia')
        ], width=6),
        dbc.Col([
            html.Div(id='tabla-comparativa')
        ], width=6)
    ]),

    dcc.Store(id='estado-historial'),
    dcc.Store(id='frame-actual', data=0),
    dcc.Interval(id='interval-animacion',
                interval=300, n_intervals=0,
                disabled=True)
], fluid=True)

@app.callback(
    [Output('grafico-principal', 'figure'),
     Output('info-resultado', 'children'),
     Output('estado-historial', 'data'),
     Output('interval-animacion', 'disabled'),
     Output('frame-actual', 'data')],
    [Input('btn-inicial', 'n_clicks'),
     Input('btn-ejecutar', 'n_clicks'),
     Input('interval-animacion', 'n_intervals')],
    [State('x-ini', 'value'),
     State('area-obj', 'value'),
     State('estado-historial', 'data'),
     State('frame-actual', 'data')]
)
def actualizar_grafico(n_ini, n_ejec, n_intervals, x_ini, area_obj, historial_data, frame):
    ctx = callback_context

    if not ctx.triggered:
        button_id = None
    else:
        button_id = ctx.triggered[0]['prop_id'].split('.')[0]

    fig = go.Figure()

    # Triángulo completo (referencia)
    fig.add_trace(go.Scatter(
        x=[0, 12, 12, 0], y=[0, 0, 6, 0],
        fill='toself', fillcolor='rgba(200,200,200,0.2)',
        line=dict(color='gray', width=1, dash='dash'),
        name='Triángulo total',
        hoverinfo='skip'
    ))

    if button_id == 'btn-inicial' or button_id is None:
        y_ini = 0.5 * x_ini
        a_ini = area_triangulo(x_ini)

        fig.add_trace(go.Scatter(
            x=[0, x_ini, x_ini, 0],
            y=[0, 0, y_ini, 0],
            fill='toself',
            fillcolor='rgba(0,100,255,0.4)',
            line=dict(color='blue', width=3),
            name=f'Estado inicial (x={x_ini})',
            hovertemplate=f'Área inicial: {a_ini:.3f}<extra></extra>'
        ))

        delta_exacto = calcular_delta_exacto(x_ini, area_obj)
        x_exacto = x_ini + delta_exacto
        y_exacto = 0.5 * x_exacto

        fig.add_trace(go.Scatter(
            x=[0, x_exacto, x_exacto, 0],
            y=[0, 0, y_exacto, 0],
            fill='toself',
            fillcolor='rgba(0,255,0,0.3)',
            line=dict(color='green', width=2, dash='dot'),
            name=f'Solución exacta (Δx={delta_exacto:.3f})',
            hovertemplate=f'Área final: {a_ini + area_obj:.3f}<extra></extra>'
        ))

        info = html.Div([
            html.H5("📊 Estado Inicial", className="text-info"),
            html.P(f"✓ x inicial: {x_ini}"),
            html.P(f"✓ Área inicial: {a_ini:.3f}"),
            html.P(f"✓ Área objetivo adicional: {area_obj}"),
            html.Hr(),
            html.H5("📐 Solución Exacta (Fórmula)", className="text-success"),
            html.P(f"✓ Δx necesario: {delta_exacto:.4f}"),
            html.P(f"✓ x final: {x_exacto:.4f}"),
            html.P(f"✓ Área final: {a_ini + area_obj:.3f}")
        ])

        fig.update_layout(
            title="Vista del Triángulo - Estado Inicial",
            xaxis_title="Base (x)",
            yaxis_title="Altura (y)",
            xaxis=dict(range=[-0.5, 13]),
            yaxis=dict(range=[-0.5, 7]),
            showlegend=True
        )

        return fig, info, None, True, 0

    elif button_id == 'btn-ejecutar':
        y_ini = 0.5 * x_ini

        fig.add_trace(go.Scatter(
            x=[0, x_ini, x_ini, 0],
            y=[0, 0, y_ini, 0],
            fill='toself',
            fillcolor='rgba(0,100,255,0.3)',
            line=dict(color='blue', width=2),
            name='Estado inicial'
        ))

        delta_difuso, df_hist = sistema.calcular(x_ini, area_obj)

        info = html.Div([
            html.H5("⏳ Ejecutando animación...", className="text-warning"),
            html.P(f"Total de iteraciones: {len(df_hist)}")
        ])

        return fig, info, df_hist.to_dict('records'), False, 0

    elif button_id == 'interval-animacion':
        if not historial_data or frame >= len(historial_data):
            return actualizar_grafico_final(x_ini, area_obj, historial_data)

        df_hist = pd.DataFrame(historial_data)
        current_frame = min(frame, len(df_hist) - 1)

        y_ini = 0.5 * x_ini
        a_ini = area_triangulo(x_ini)

        fig.add_trace(go.Scatter(
            x=[0, x_ini, x_ini, 0],
            y=[0, 0, y_ini, 0],
            fill='toself',
            fillcolor='rgba(0,100,255,0.2)',
            line=dict(color='blue', width=2),
            name='Inicial'
        ))

        x_current = df_hist.iloc[current_frame]['x']
        y_current = 0.5 * x_current
        a_current = area_triangulo(x_current)

        fig.add_trace(go.Scatter(
            x=[0, x_current, x_current, 0],
            y=[0, 0, y_current, 0],
            fill='toself',
            fillcolor='rgba(255,150,0,0.5)',
            line=dict(color='orange', width=3),
            name=f'Iteración {current_frame}'
        ))

        delta_exacto = calcular_delta_exacto(x_ini, area_obj)
        x_exacto = x_ini + delta_exacto
        y_exacto = 0.5 * x_exacto

        fig.add_trace(go.Scatter(
            x=[0, x_exacto, x_exacto, 0],
            y=[0, 0, y_exacto, 0],
            fill=None,
            line=dict(color='green', width=2, dash='dot'),
            name='Objetivo'
        ))

        error = abs(a_current - (a_ini + area_obj))

        info = html.Div([
            html.H5(f"🎬 Iteración {current_frame + 1}/{len(df_hist)}",
                   className="text-warning"),
            html.P(f"✓ x actual: {x_current:.4f}"),
            html.P(f"✓ Área actual: {a_current:.4f}"),
            html.P(f"✓ Error: {error:.4f}")
        ])

        disabled = current_frame >= len(df_hist) - 1

        fig.update_layout(
            title=f"Animación - Iteración {current_frame + 1}/{len(df_hist)}",
            xaxis_title="Base (x)",
            yaxis_title="Altura (y)",
            xaxis=dict(range=[-0.5, 13]),
            yaxis=dict(range=[-0.5, 7]),
            showlegend=True
        )

        return fig, info, historial_data, disabled, current_frame + 1

    fig.update_layout(
        title="Vista del Triángulo",
        xaxis_title="Base (x)",
        yaxis_title="Altura (y)",
        xaxis=dict(range=[-0.5, 13]),
        yaxis=dict(range=[-0.5, 7]),
        showlegend=True
    )

    return fig, html.Div(), None, True, 0

def actualizar_grafico_final(x_ini, area_obj, historial_data):
    """Muestra el estado final después de la animación"""
    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=[0, 12, 12, 0], y=[0, 0, 6, 0],
        fill='toself', fillcolor='rgba(200,200,200,0.2)',
        line=dict(color='gray', width=1, dash='dash'),
        name='Triángulo total',
        hoverinfo='skip'
    ))

    y_ini = 0.5 * x_ini
    a_ini = area_triangulo(x_ini)

    fig.add_trace(go.Scatter(
        x=[0, x_ini, x_ini, 0],
        y=[0, 0, y_ini, 0],
        fill='toself',
        fillcolor='rgba(0,100,255,0.2)',
        line=dict(color='blue', width=2),
        name='Inicial'
    ))

    df_hist = pd.DataFrame(historial_data)
    delta_difuso, _ = sistema.calcular(x_ini, area_obj)
    x_final = x_ini + delta_difuso
    y_final = 0.5 * x_final

    fig.add_trace(go.Scatter(
        x=[0, x_final, x_final, 0],
        y=[0, 0, y_final, 0],
        fill='toself',
        fillcolor='rgba(255,150,0,0.5)',
        line=dict(color='orange', width=3),
        name=f'Final (Δx={delta_difuso:.3f})'
    ))

    delta_exacto = calcular_delta_exacto(x_ini, area_obj)
    x_exacto = x_ini + delta_exacto
    y_exacto = 0.5 * x_exacto

    fig.add_trace(go.Scatter(
        x=[0, x_exacto, x_exacto, 0],
        y=[0, 0, y_exacto, 0],
        fill=None,
        line=dict(color='green', width=2, dash='dot'),
        name=f'Exacto (Δx={delta_exacto:.3f})'
    ))

    error = abs(delta_difuso - delta_exacto)
    error_pct = (error / abs(delta_exacto)) * 100 if delta_exacto != 0 else 0

    info = html.Div([
        html.H5("✅ Animación Completada", className="text-success"),
        html.P(f"✓ Δx calculado: {delta_difuso:.4f}"),
        html.P(f"✓ x final: {x_final:.4f}"),
        html.P(f"✓ Iteraciones: {len(df_hist)}"),
        html.Hr(),
        html.H5("📊 Comparación"),
        html.P(f"✓ Δx exacto: {delta_exacto:.4f}"),
        html.P(f"✓ Error: {error:.4f}"),
        html.P(f"✓ Error %: {error_pct:.2f}%",
              style={'color': 'green' if error_pct < 5 else 'orange'})
    ])

    fig.update_layout(
        title="Resultado Final - Lógica Difusa",
        xaxis_title="Base (x)",
        yaxis_title="Altura (y)",
        xaxis=dict(range=[-0.5, 13]),
        yaxis=dict(range=[-0.5, 7]),
        showlegend=True
    )

    return fig, info, historial_data, True, 0

@app.callback(
    [Output('grafico-convergencia', 'figure'),
     Output('tabla-comparativa', 'children')],
    [Input('estado-historial', 'data'),
     Input('x-ini', 'value'),
     Input('area-obj', 'value')]
)
def actualizar_extras(historial, x_ini, area_obj):

    if historial:
        df = pd.DataFrame(historial)
        fig_conv = go.Figure()
        fig_conv.add_trace(go.Scatter(
            x=df['iter'], y=df['x'],
            mode='lines+markers',
            name='Posición x',
            line=dict(color='orange', width=3)
        ))

        x_exacto = x_ini + calcular_delta_exacto(x_ini, area_obj)
        fig_conv.add_hline(y=x_exacto, line_dash="dash",
                          line_color="green",
                          annotation_text="Objetivo")

        fig_conv.update_layout(
            title="Convergencia - Lógica Difusa",
            xaxis_title="Iteración",
            yaxis_title="Posición x"
        )
    else:
        fig_conv = go.Figure()
        fig_conv.add_annotation(
            text="Ejecuta el algoritmo para ver la convergencia",
            xref="paper", yref="paper",
            x=0.5, y=0.5, showarrow=False
        )

    datos = []
    for x in range(13):
        delta_exacto = calcular_delta_exacto(x, area_obj)
        delta_difuso, _ = sistema.calcular(x, area_obj)
        dif = abs(delta_difuso - delta_exacto)
        dif_pct = (dif / abs(delta_exacto)) * 100 if delta_exacto != 0 else 0

        datos.append({
            'x': x,
            'Exacto': f'{delta_exacto:.3f}',
            'Difuso': f'{delta_difuso:.3f}',
            'Dif': f'{dif:.3f}',
            'Dif %': f'{dif_pct:.1f}%'
        })

    df_tabla = pd.DataFrame(datos)

    tabla = dbc.Table([
        html.Thead([
            html.Tr([
                html.Th("x"),
                html.Th("Exacto (a)"),
                html.Th("Difuso (b)"),
                html.Th("Diferencia"),
                html.Th("Error %")
            ])
        ]),
        html.Tbody([
            html.Tr([
                html.Td(row['x']),
                html.Td(row['Exacto']),
                html.Td(row['Difuso']),
                html.Td(row['Dif']),
                html.Td(row['Dif %'],
                        style={'color': 'green' if float(row['Dif %'].replace('%', '')) < 5 else 'orange'})
            ]) for _, row in df_tabla.iterrows()
        ])
    ], bordered=True, striped=True, hover=True, size='sm')

    # Calcular promedio de errores porcentuales
    errores_pct = [float(row['Dif %'].replace('%', '')) for _, row in df_tabla.iterrows()]
    promedio_error = np.mean(errores_pct)

    # Crear contenedor con tabla y promedio
    contenido_tabla = html.Div([
        tabla,
        dbc.Card([
            dbc.CardBody([
                html.H5("📊 Promedio de Error (Diferencias)", className="text-center mb-2"),
                html.H3(f"{promedio_error:.2f}%",
                        className="text-center",
                        style={'color': 'green' if promedio_error < 5 else 'orange',
                               'font-weight': 'bold'})
            ])
        ], className="mt-3", color="light")
    ])

    return fig_conv, contenido_tabla

if __name__ == '__main__':
    print("\n" + "="*60)
    print("🚀 SISTEMA DE LÓGICA DIFUSA")
    print("="*60)
    print("✨ 60 reglas")
    print("📊 10 niveles de error × 6 posiciones")
    print("\n🌐 Abriendo en: http://127.0.0.1:8050/")
    print("✅ Presiona Ctrl+C para salir\n")
    app.run(debug=True, use_reloader=False)