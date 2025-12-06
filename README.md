# 🔬 Sistema de Lógica Difusa - Triángulo Rectángulo

Sistema de control inteligente basado en lógica difusa tipo Mamdani para el cálculo iterativo de desplazamientos en triángulos rectángulos con objetivo de área específica.

## 📊 Características

- **60 reglas difusas** (10 niveles de error × 6 posiciones)
- **Inferencia Mamdani** con defuzzificación por centroide ponderado
- **Interfaz web interactiva** con visualización en tiempo real
- **Error promedio: 3.08%** comparado con solución analítica exacta

## 🚀 Instalación

```bash
pip install numpy pandas plotly dash dash-bootstrap-components
```

## ▶️ Uso

```bash
python logica_difusa_triangulo.py
```

Abrir en el navegador: `http://127.0.0.1:8050/`

## 🎯 Funcionalidad

El sistema calcula el desplazamiento `Δx` necesario en la base de un triángulo rectángulo para alcanzar un área objetivo mediante:

1. **Fuzzificación**: Error de área y posición actual
2. **Inferencia**: 60 reglas con operador MIN (Mamdani)
3. **Defuzzificación**: Centroide ponderado
4. **Control iterativo**: Convergencia en 8-15 iteraciones

## 📐 Ecuaciones

**Área del triángulo:**
```
A(x) = 0.25 × x²
```

**Solución exacta:**
```
x_final = √(x₀² + 4·ΔA_objetivo)
```

## 📈 Resultados

| x inicial | Δx Exacto | Δx Difuso | Error % |
|-----------|-----------|-----------|---------|
| 0         | 4.000     | 4.000     | 0.0%    |
| 5         | 1.403     | 1.434     | 2.2%    |
| 10        | 0.770     | 0.819     | 6.3%    |

**Promedio de error: 3.08%**

## 🛠️ Tecnologías

- Python 3.x
- NumPy
- Pandas
- Plotly
- Dash
- Dash Bootstrap Components

## 📄 Licencia

MIT

## 👤 Autor

Jheramy Villanueva - Universidad Nacional Mayor de San Marcos
