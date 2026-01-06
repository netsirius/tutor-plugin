---
description: Obtener un ejercicio de práctica. Usa /tutor:exercise para un ejercicio del tema actual, o /tutor:exercise [dificultad] donde dificultad puede ser basico, intermedio, avanzado, o reto.
allowed-tools: Read, Write, Bash
---

# Comando: Exercise

El usuario quiere practicar con un ejercicio.

## Tu Tarea

1. Lee `.tutor/progress.json` para conocer:
   - Tema actual del estudiante
   - Nivel de dificultad apropiado
   - Ejercicios ya completados

2. Determina la dificultad:
   - Si se especifica: usar la indicada
   - Si no: calcular según el progreso
     - Pocos ejercicios completados → básico
     - Buen rendimiento → subir nivel
     - Dificultades recientes → mantener o bajar

3. Genera el ejercicio:
   - Crear directorio en `lessons/[modulo]/exercises/ex[num]_[nombre]/`
   - Generar `Cargo.toml` con dependencias necesarias
   - Crear `src/main.rs` o `src/lib.rs` con:
     - Descripción clara del problema
     - Ejemplos de entrada/salida
     - Pistas progresivas (comentadas)
     - Código base con `todo!()`
   - Crear tests en `tests/` o como `#[cfg(test)]`

4. Presenta el ejercicio:
   - Explica el objetivo
   - Indica la dificultad (★ a ★★★★)
   - Muestra cómo ejecutar los tests
   - Recuerda que puede pedir ayuda

## Niveles de Dificultad

### básico (★)
- Aplicación directa del concepto
- 1-2 conceptos involucrados
- ~10 minutos

### intermedio (★★)
- Combinación de conceptos
- Requiere pensar la solución
- ~20-30 minutos

### avanzado (★★★)
- Múltiples conceptos integrados
- Edge cases a considerar
- ~45-60 minutos

### reto (★★★★)
- Problema abierto
- Múltiples soluciones válidas
- Puede requerir investigación
- ~1-2 horas

## Formato del Ejercicio Generado

```rust
// =============================================================================
// Ejercicio: [Título Descriptivo]
// Dificultad: ★★ (Intermedio)
// Tema: [Tema del curriculum]
// Tiempo estimado: 20 minutos
// =============================================================================
//
// DESCRIPCIÓN:
// [Explicación clara del problema a resolver]
//
// EJEMPLO:
// Entrada: [ejemplo]
// Salida esperada: [resultado]
//
// INSTRUCCIONES:
// 1. Implementa la función [nombre]
// 2. Asegúrate de manejar [caso especial]
// 3. Ejecuta `cargo test` para verificar
//
// PISTAS (solo si te atascas):
// Pista 1: [pista suave]
// Pista 2: [pista más directa]
// Pista 3: [casi la solución]
// =============================================================================

fn main() {
    // Tu código aquí
    todo!("Implementa la solución")
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_caso_basico() {
        // Test del caso más simple
    }
}
```

## Recuerda
- El ejercicio debe ser desafiante pero alcanzable
- Incluye siempre tests automatizados
- No reveles la solución, solo pistas progresivas
- Celebra cuando el estudiante complete el ejercicio
