# Template: Ejercicio

Usa esta plantilla cuando generes ejercicios para el estudiante.

## Estructura de Ejercicio (main.rs)

```rust
// =============================================================================
// EJERCICIO: [Título Descriptivo]
// =============================================================================
// Dificultad: [★ Básico | ★★ Intermedio | ★★★ Avanzado | ★★★★ Reto]
// Tema: [Tema del curriculum]
// Tiempo estimado: [X] minutos
// =============================================================================
//
// DESCRIPCIÓN:
// [Explicación clara del problema a resolver en 2-3 párrafos]
//
// REQUISITOS:
// 1. [Requisito específico 1]
// 2. [Requisito específico 2]
// 3. [Requisito específico 3]
//
// EJEMPLO:
// Entrada: [ejemplo de entrada si aplica]
// Salida esperada: [resultado esperado]
//
// INSTRUCCIONES:
// 1. Lee el código base proporcionado
// 2. Implementa la función [nombre_funcion]
// 3. Ejecuta `cargo test` para verificar tu solución
// 4. Si necesitas ayuda, revisa las pistas al final del archivo
//
// =============================================================================

// Tu código aquí
fn nombre_funcion() {
    todo!("Implementa tu solución")
}

fn main() {
    // Código de prueba para que puedas experimentar
    println!("Ejecuta 'cargo test' para verificar tu solución");

    // Ejemplo de uso
    // let resultado = nombre_funcion(...);
    // println!("Resultado: {:?}", resultado);
}

// =============================================================================
// TESTS - No modifiques esta sección
// =============================================================================

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_caso_basico() {
        // Test del caso más simple
        todo!("Añadir test")
    }

    #[test]
    fn test_caso_normal() {
        // Test de un caso típico
        todo!("Añadir test")
    }

    #[test]
    fn test_caso_edge() {
        // Test de caso límite
        todo!("Añadir test")
    }
}

// =============================================================================
// PISTAS (Solo léelas si te atascas)
// =============================================================================
//
// PISTA 1 (Suave):
// [Orientación general sin revelar la solución]
//
// PISTA 2 (Más directa):
// [Indicación más específica del enfoque]
//
// PISTA 3 (Casi la solución):
// [Pseudocódigo o estructura de la solución]
//
// =============================================================================
```

## Estructura de Cargo.toml

```toml
[package]
name = "ejercicio_[nombre]"
version = "0.1.0"
edition = "2021"

# Añade dependencias si el ejercicio las requiere
[dependencies]
# rand = "0.8"  # Ejemplo: para ejercicios con números aleatorios
```

## Estructura de Solución (solution.rs)

```rust
// =============================================================================
// SOLUCIÓN: [Título del Ejercicio]
// =============================================================================
//
// ¡Spoiler! Solo revisa esto después de intentar resolver el ejercicio.
//
// EXPLICACIÓN DE LA SOLUCIÓN:
// [Descripción de por qué esta solución funciona]
//
// COMPLEJIDAD:
// - Temporal: O(...)
// - Espacial: O(...)
//
// ALTERNATIVAS:
// - [Otra forma de resolver el problema]
// - [Trade-offs de cada enfoque]
//
// =============================================================================

fn nombre_funcion() {
    // Implementación completa
}

// Código de ejemplo de uso
fn main() {
    // Demostración de la solución
}
```

## Niveles de Dificultad

### ★ Básico
- Aplicación directa del concepto recién aprendido
- 1-2 conceptos involucrados
- Código similar a los ejemplos de la lección
- 5-10 minutos

### ★★ Intermedio
- Combinación de 2-3 conceptos
- Requiere adaptar lo aprendido
- Pequeñas decisiones de diseño
- 15-30 minutos

### ★★★ Avanzado
- Múltiples conceptos integrados
- Diseño de solución propia
- Manejo de casos límite
- 30-60 minutos

### ★★★★ Reto
- Problema abierto con múltiples soluciones válidas
- Puede requerir investigación adicional
- Considera optimización y trade-offs
- 1-2 horas

## Notas para el Coach de Práctica

1. **Progresión**: Cada ejercicio debe construir sobre el anterior
2. **Tests claros**: Los tests deben dar feedback útil al fallar
3. **Pistas progresivas**: De vaga a específica, nunca la solución directa
4. **Contexto real**: Usa escenarios aplicables al mundo real
5. **Un concepto nuevo**: Introduce solo una dificultad nueva a la vez
