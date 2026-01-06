# Template: Mini-Proyecto

Usa esta plantilla cuando generes un proyecto práctico para el estudiante.

## Estructura de Proyecto

```
projects/[nombre-proyecto]/
├── README.md           # Descripción y guía del proyecto
├── Cargo.toml          # Configuración del proyecto
├── src/
│   ├── main.rs         # Punto de entrada
│   └── lib.rs          # Librería (si aplica)
├── tests/
│   └── integration.rs  # Tests de integración
└── docs/
    └── design.md       # Diseño (opcional para proyectos avanzados)
```

## README.md del Proyecto

```markdown
# [Nombre del Proyecto]

## Descripción
[Descripción breve de qué hace el proyecto y por qué es útil]

## Objetivos de Aprendizaje
- [ ] [Concepto 1 que practicarás]
- [ ] [Concepto 2 que practicarás]
- [ ] [Concepto 3 que practicarás]

## Funcionalidades a Implementar

### Fase 1: MVP (Mínimo Producto Viable)
- [ ] [Funcionalidad básica 1]
- [ ] [Funcionalidad básica 2]

### Fase 2: Mejoras
- [ ] [Funcionalidad adicional 1]
- [ ] [Funcionalidad adicional 2]

### Fase 3: Extras (Opcional)
- [ ] [Funcionalidad avanzada 1]
- [ ] [Funcionalidad avanzada 2]

## Requisitos Técnicos
- [Requisito 1: ej. "Usar structs para representar datos"]
- [Requisito 2: ej. "Manejar errores con Result"]
- [Requisito 3: ej. "Implementar trait Display"]

## Ejemplo de Uso

```bash
$ cargo run -- [argumentos]
[Salida esperada]
```

## Guía de Implementación

### Paso 1: Configuración
[Instrucciones para empezar]

### Paso 2: Estructura de datos
[Qué tipos/structs definir]

### Paso 3: Lógica principal
[Cómo abordar la implementación]

### Paso 4: Manejo de errores
[Cómo manejar casos de error]

### Paso 5: Tests
[Qué testear y cómo]

## Recursos Útiles
- [Enlace a documentación relevante]
- [Enlace a crate que podría usar]

## Criterios de Evaluación

| Aspecto | Puntos |
|---------|--------|
| Funcionalidad básica | 40 |
| Manejo de errores | 20 |
| Código limpio | 20 |
| Tests | 20 |
| **Total** | **100** |
```

## Proyectos Sugeridos por Nivel

### Principiante (después de fundamentos)
1. **Calculadora CLI** - Variables, funciones, input/output
2. **Generador de contraseñas** - Strings, random, CLI
3. **Conversor de unidades** - Structs, enums, match

### Intermedio (después de ownership)
1. **Lista de tareas (Todo)** - Vectors, file I/O, structs
2. **Grep simplificado** - File handling, iterators, CLI
3. **JSON parser básico** - Enums, recursión, pattern matching

### Avanzado (después de traits)
1. **HTTP server básico** - Networking, threads, traits
2. **Key-value store** - HashMap, serialización, persistencia
3. **Markdown renderer** - Parser, traits, generics

### Experto (después de async)
1. **Chat server** - async/await, channels, networking
2. **Build tool simple** - File system, procesos, DAG
3. **Mini base de datos** - B-trees, file I/O, indexing

## Notas para el Tutor

1. **Escala apropiada**: El proyecto debe ser completable en 2-4 horas
2. **Fases claras**: Dividir en fases permite progreso visible
3. **No sobre-especificar**: Dejar espacio para decisiones del estudiante
4. **Código de ejemplo**: Proporcionar snippets guía, no soluciones completas
5. **Tests de referencia**: Dar tests que definan el comportamiento esperado
