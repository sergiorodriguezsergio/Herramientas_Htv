# Skill: Pick_And_Roll

Esta Skill automatiza la actualización del archivo Excel de rotulación deportiva de Huelva TV.

## Automatización Principal
- **Script**: `scripts/actualizar_pick_and_roll.py`
- **Archivo Destino**: `\\172.16.80.129\g\EXCEL PROGRAMAS\PICK AND ROLL\DATOS PICK AND ROLL.xlsx`

## Reglas de Formato
- **MAYÚSCULAS**: Todo el texto de equipos y resultados.
- **Separadores**: Usar guiones (`-`) para resultados y emparejamientos.
- **Fecha/Hora**: `DD/MM/YY HH:MM`.

## Fuentes de Datos
- **Tercera FEB**: [FEB.es](https://baloncestoenvivo.feb.es/resultados/ligaeba/47/2025)
- **N1 Andaluza**: [FAB](https://www.andaluzabaloncesto.org/competicion-2408/competiciones-fab-25-26) (Grupo A)
