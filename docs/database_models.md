# Modelos de base de datos

La API usa SQLAlchemy y crea las tablas automaticamente al iniciar.

## Tabla `diseases`

Guarda la informacion asociada a cada clase del modelo.

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | integer | Identificador primario |
| `class_name` | string | Clase del modelo: `Early_Blight`, `Healthy`, `Late_Blight` |
| `common_name` | string | Nombre comun en espanol |
| `scientific_agent` | string nullable | Agente causal cuando aplica |
| `summary` | text | Resumen de la condicion |
| `causes` | text | Causas o condiciones que favorecen el problema |
| `characteristics` | text | Caracteristicas visuales principales |
| `treatment` | text | Manejo o tratamiento recomendado |
| `prevention` | text | Prevencion y buenas practicas |
| `recommendation` | text | Recomendacion operativa posterior a la prediccion |
| `created_at` | datetime | Fecha de creacion |

## Tabla `predictions`

Guarda el historial de clasificaciones realizadas por la API.

| Campo | Tipo | Descripcion |
| --- | --- | --- |
| `id` | integer | Identificador primario |
| `filename` | string nullable | Nombre del archivo enviado |
| `predicted_class` | string | Clase predicha |
| `confidence` | float | Confianza de la clase ganadora |
| `probabilities` | text | JSON con probabilidades por clase |
| `disease_id` | integer nullable | Relacion con `diseases.id` |
| `created_at` | datetime | Fecha de creacion |

## Datos iniciales

Los datos semilla estan en `app/seed.py` e incluyen:

### Early_Blight

- Nombre comun: Tizon temprano
- Agente: `Alternaria solani`
- Caracteristicas: manchas marrones con anillos concentricos, halo amarillo, inicio frecuente en hojas inferiores.
- Manejo: retiro de hojas muy afectadas cuando sea viable, mejor ventilacion y fungicidas registrados con rotacion de ingredientes activos.

### Healthy

- Nombre comun: Hoja sana
- Agente: no aplica
- Caracteristicas: color verde uniforme y ausencia de lesiones compatibles con tizon temprano o tardio.
- Manejo: no requiere tratamiento fitosanitario por esta clasificacion; mantener monitoreo.

### Late_Blight

- Nombre comun: Tizon tardio
- Agente: `Phytophthora infestans`
- Caracteristicas: lesiones irregulares humedas u oscuras, avance rapido y posible moho blanquecino en el enves.
- Manejo: accion rapida, aislamiento de focos, retiro de material infectado segun protocolo y fungicidas especificos con asesoria tecnica.
