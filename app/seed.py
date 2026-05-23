from sqlalchemy.orm import Session

from app.models import Disease


DISEASES = [
    {
        "class_name": "Early_Blight",
        "common_name": "Tizon temprano",
        "scientific_agent": "Alternaria solani",
        "summary": "Enfermedad fungica comun en papa que reduce el area fotosintetica y puede afectar rendimiento si avanza sin control.",
        "causes": "Favorecida por humedad alta, periodos de lluvia o rocio, temperaturas templadas a calidas, hojas viejas, estres nutricional y restos de cultivo infectados.",
        "characteristics": "Manchas marrones oscuras con anillos concentricos tipo diana, amarillamiento alrededor de la lesion, inicio frecuente en hojas inferiores y avance hacia la parte superior.",
        "treatment": "Retirar hojas muy afectadas cuando sea viable, mejorar ventilacion del cultivo y aplicar fungicidas registrados para papa segun recomendacion tecnica local, rotando ingredientes activos.",
        "prevention": "Usar semilla sana, rotar cultivos, eliminar residuos infectados, evitar exceso de humedad foliar, mantener nutricion balanceada y monitorear desde etapas tempranas.",
        "recommendation": "Si la prediccion indica tizon temprano con alta confianza, inspecciona hojas bajas y aplica manejo integrado antes de que las lesiones se unan.",
    },
    {
        "class_name": "Healthy",
        "common_name": "Hoja sana",
        "scientific_agent": None,
        "summary": "La hoja no muestra patrones visuales compatibles con tizon temprano o tizon tardio segun las clases entrenadas del modelo.",
        "causes": "No aplica como enfermedad. La sanidad observada puede depender de buen manejo de riego, nutricion, ventilacion y ausencia de inoculo activo.",
        "characteristics": "Coloracion verde uniforme, tejido foliar sin lesiones necroticas extendidas, sin halos amarillos marcados ni manchas acuosas oscuras.",
        "treatment": "No requiere tratamiento fitosanitario por esta clasificacion. Mantener monitoreo y evitar aplicaciones innecesarias.",
        "prevention": "Continuar con vigilancia periodica, riego controlado, fertilizacion balanceada, limpieza de herramientas y control preventivo basado en riesgo climatico.",
        "recommendation": "Una prediccion sana no descarta otros problemas no incluidos en el modelo; revisa campo completo si hay sintomas en otras plantas.",
    },
    {
        "class_name": "Late_Blight",
        "common_name": "Tizon tardio",
        "scientific_agent": "Phytophthora infestans",
        "summary": "Enfermedad agresiva de la papa que puede avanzar rapidamente bajo condiciones frescas y humedas, causando perdidas severas.",
        "causes": "Favorecida por humedad relativa alta, lluvias, neblina, hojas mojadas por varias horas, temperaturas frescas a moderadas e inoculo cercano en plantas o tuberculos infectados.",
        "characteristics": "Lesiones irregulares de aspecto humedo u oscuro, avance rapido, posible moho blanquecino en el enves bajo humedad, colapso de tejido y manchas en bordes o puntas de hojas.",
        "treatment": "Aislar focos, retirar material muy infectado segun protocolo sanitario y aplicar fungicidas especificos registrados con asesoria tecnica urgente, respetando dosis y periodos de carencia.",
        "prevention": "Usar semilla certificada, destruir plantas voluntarias, evitar riego por aspersion nocturno, mejorar drenaje, monitorear clima de riesgo y aplicar programas preventivos cuando corresponda.",
        "recommendation": "Si se detecta tizon tardio, actua rapido: confirma en campo, limita dispersion y consulta un tecnico agricola para un plan de control inmediato.",
    },
]


def seed_diseases(db: Session) -> None:
    for payload in DISEASES:
        exists = db.query(Disease).filter(Disease.class_name == payload["class_name"]).first()
        if exists is None:
            db.add(Disease(**payload))
    db.commit()
