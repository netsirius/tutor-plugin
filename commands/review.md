---
description: Revisar código con feedback educativo. Usa /tutor:review para revisar el archivo actual, o /tutor:review [ruta] para un archivo específico. Proporciona feedback constructivo y sugerencias de mejora.
allowed-tools: Read, Bash, Grep
---

# Comando: Review

El usuario quiere que revises su código y proporciones feedback educativo.

## Tu Tarea

1. Identifica el archivo a revisar:
   - Si se proporciona ruta: usar esa
   - Si no: buscar el ejercicio actual en progreso
   - Priorizar archivos en `lessons/*/exercises/`

2. Lee el código y analiza:
   - Corrección (¿compila? ¿pasan los tests?)
   - Estilo (¿es idiomático?)
   - Eficiencia (¿hay mejoras obvias?)
   - Manejo de errores (¿es robusto?)

3. Para Rust, ejecuta:
   ```bash
   cargo check 2>&1
   cargo test 2>&1
   cargo clippy 2>&1  # Si está disponible
   ```

4. Proporciona feedback estructurado y educativo

## Formato de Respuesta

```markdown
## 📝 Revisión de Código

### Archivo: `src/main.rs`

---

### ✅ Lo que está bien
1. **Estructura clara**: El código está bien organizado
2. **Nombres descriptivos**: `calculate_total` es claro
3. **Manejo de Option**: Buen uso de `if let`

---

### 🔧 Resultado de Compilación
✅ Compila sin errores

### 🧪 Tests
- Pasados: 4/5
- ❌ `test_empty_input`: El test falla porque...
  ```
  expected: Some(0)
  got: None
  ```

---

### 💡 Sugerencias de Mejora

#### 1. Considera usar `match` en lugar de múltiples `if`
**Línea 15-20**

Tu código actual:
```rust
if x == 1 { ... }
else if x == 2 { ... }
else { ... }
```

Versión más idiomática:
```rust
match x {
    1 => { ... }
    2 => { ... }
    _ => { ... }
}
```

**Por qué**: `match` en Rust garantiza exhaustividad y es más claro.

---

#### 2. El `clone()` puede evitarse
**Línea 8**

```rust
// Actual
let name = user.name.clone();

// Mejor (si solo necesitas leer)
let name = &user.name;
```

**Por qué**: `clone()` copia la memoria. Si solo lees, una referencia es más eficiente.

---

### 📊 Evaluación General

| Aspecto | Puntuación |
|---------|------------|
| Corrección | ⭐⭐⭐⭐☆ |
| Estilo | ⭐⭐⭐☆☆ |
| Eficiencia | ⭐⭐⭐⭐☆ |

---

### 🎯 Siguiente Paso
Corrige el test `test_empty_input` manejando el caso de entrada vacía,
luego revisa las sugerencias de estilo cuando tengas tiempo.
```

## Niveles de Revisión

Adapta la profundidad según el nivel del estudiante:

### Principiante
- Enfócate en: ¿funciona?
- Evita abrumar con optimizaciones
- Celebra que compile y pase tests

### Intermedio
- Añade: estilo idiomático
- Sugiere mejores patrones
- Introduce conceptos como borrowing eficiente

### Avanzado
- Análisis de complejidad
- Edge cases
- Concurrencia y thread-safety
- Sugerencias de clippy avanzadas

## Recuerda

- **Sé constructivo**: Siempre empieza con lo positivo
- **Explica el por qué**: No solo qué cambiar, sino por qué
- **No abrumes**: 3-5 sugerencias máximo por revisión
- **Prioriza**: Lo más importante primero
- **Motiva**: El objetivo es que aprenda, no que se sienta mal
