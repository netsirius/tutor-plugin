---
description: Extend mode for deepening mastered topics. Use /tutor:extend to explore advanced concepts, edge cases, real-world applications, and connections to other topics.
allowed-tools: Read, Write, Bash
---

# Command: Extend

The user wants to go deeper into topics they've already mastered. This mode focuses on advanced understanding, edge cases, real-world applications, and cross-topic connections.

## Your Task

### If called without arguments (`/tutor:extend`):

Show extension opportunities:

```
================================================================================
                          MODO EXTENDER
================================================================================

Extender = Profundizar en lo que ya dominas

  TEMAS DISPONIBLES PARA EXTENDER
  ────────────────────────────────────────────────────────────────────────────

  Solo puedes extender temas con dominio ≥80%

  ✅ DOMINADOS (listos para extender):
  │
  ├── Arrays y Listas                  Dominio: 95%
  │   └── Extensiones disponibles:
  │       • Implementaciones eficientes en memoria
  │       • Arrays dinámicos vs estáticos (trade-offs)
  │       • Skip lists y estructuras avanzadas
  │
  ├── Pilas y Colas                    Dominio: 88%
  │   └── Extensiones disponibles:
  │       • Implementación con arrays circulares
  │       • Double-ended queues (deques)
  │       • Priority queues y heaps
  │
  └── Árboles Binarios                 Dominio: 85%
      └── Extensiones disponibles:
          • Threaded binary trees
          • Árboles de expresión
          • Serialización y deserialización

  🔒 AÚN NO DISPONIBLES:
  │
  ├── Árboles AVL                      Dominio: 60% (necesita ≥80%)
  └── Grafos                           Dominio: 0% (aún no estudiado)

  ────────────────────────────────────────────────────────────────────────────

  Selecciona un tema para ver opciones de extensión, o:

  [A] Ver todas las extensiones disponibles
  [R] Recomendación personalizada

================================================================================
```

### If called with a topic (`/tutor:extend [topic]`):

```
================================================================================
                    EXTENDER: ÁRBOLES BINARIOS
================================================================================

Dominio actual: 85% ✅
Has completado: Conceptos básicos, recorridos, búsqueda, inserción, eliminación

  OPCIONES DE EXTENSIÓN
  ────────────────────────────────────────────────────────────────────────────

  📚 PROFUNDIZAR EN TEORÍA:

    [1] Propiedades matemáticas de árboles binarios
        → Teoremas, demostraciones, análisis formal
        → Dificultad: Alta | Tiempo: 1.5h

    [2] Árboles binarios perfectos vs completos vs llenos
        → Diferencias sutiles, implicaciones en algoritmos
        → Dificultad: Media | Tiempo: 45min

  🔧 IMPLEMENTACIONES AVANZADAS:

    [3] Threaded Binary Trees
        → Eliminar punteros NULL, recorrido sin recursión/pila
        → Dificultad: Alta | Tiempo: 1h

    [4] Serialización y deserialización
        → Guardar/cargar árboles, formatos eficientes
        → Dificultad: Media | Tiempo: 45min

  🌐 APLICACIONES REALES:

    [5] Árboles de expresión
        → Compiladores, calculadoras, parsing
        → Dificultad: Media | Tiempo: 1h

    [6] Árboles de decisión (Machine Learning)
        → Conexión con ML, clasificación
        → Dificultad: Media-Alta | Tiempo: 1.5h

  🔗 CONEXIONES CON OTROS TEMAS:

    [7] De árboles binarios a B-Trees
        → Bases de datos, sistemas de archivos
        → Prerequisito para: Estructuras de almacenamiento
        → Dificultad: Alta | Tiempo: 2h

    [8] De árboles a grafos
        → Generalización, cuándo usar cada uno
        → Prerequisito para: Grafos (tu próximo tema)
        → Dificultad: Media | Tiempo: 30min

  ────────────────────────────────────────────────────────────────────────────

  💡 RECOMENDACIÓN para ti:
     Opción [8] "De árboles a grafos" te preparará para tu próximo tema
     del temario y conectará conceptos.

  Selecciona una opción:

================================================================================
```

### Extension Session Example:

```
================================================================================
                 EXTENSIÓN: THREADED BINARY TREES
================================================================================

Prerrequisitos verificados: ✅ Árboles binarios, ✅ Punteros, ✅ Recorridos

  INTRODUCCIÓN
  ────────────────────────────────────────────────────────────────────────────

  Ya sabes que en un árbol binario muchos nodos tienen punteros NULL
  (hijos que no existen). En un árbol con n nodos hay n+1 punteros NULL.

  ¿Y si usáramos esos punteros NULL para algo útil?

  → Esa es la idea de los Threaded Binary Trees

  CONCEPTO CLAVE
  ────────────────────────────────────────────────────────────────────────────

  En un Threaded Binary Tree:
  • Si left es NULL → apunta al predecesor inorder
  • Si right es NULL → apunta al sucesor inorder

  Ventajas:
  ✅ Recorrido inorder sin recursión ni pila auxiliar
  ✅ Encontrar sucesor/predecesor en O(1) amortizado
  ✅ Aprovecha memoria "desperdiciada"

  Desventajas:
  ❌ Inserción/eliminación más compleja
  ❌ Necesita bits extra para distinguir threads de hijos reales

  VISUALIZACIÓN
  ────────────────────────────────────────────────────────────────────────────

  Árbol binario normal:          Threaded (right threads):

        20                              20
       /  \                            /  \
      10   30                         10   30
     /  \    \                       /  \    \
    5   15   35                     5   15   35
                                    │    │
                                    └→10 └→20  (threads punteados)

  IMPLEMENTACIÓN
  ────────────────────────────────────────────────────────────────────────────

  ```python
  class ThreadedNode:
      def __init__(self, val):
          self.val = val
          self.left = None
          self.right = None
          self.is_thread_left = True   # True si left es thread
          self.is_thread_right = True  # True si right es thread

  def inorder_successor(node):
      # Si right es thread, el sucesor es directo
      if node.is_thread_right:
          return node.right

      # Si right es hijo real, ir al más izquierdo de ese subárbol
      node = node.right
      while not node.is_thread_left:
          node = node.left
      return node
  ```

  ────────────────────────────────────────────────────────────────────────────

  ¿Quieres ver un ejercicio de implementación? [S/n]

================================================================================
```

### Advanced Exercise in Extension Mode:

```
================================================================================
                    EJERCICIO AVANZADO
================================================================================

Nivel: Extensión | Tema: Threaded Binary Trees

  PROBLEMA
  ────────────────────────────────────────────────────────────────────────────

  Implementa la función `inorder_traversal_threaded` que recorre un
  threaded binary tree sin usar recursión ni estructuras auxiliares.

  La función debe:
  1. Empezar desde el nodo más a la izquierda
  2. Seguir los threads para el recorrido
  3. Retornar una lista con los valores en orden

  Firma:
  ```python
  def inorder_traversal_threaded(root: ThreadedNode) -> List[int]:
      pass
  ```

  PISTAS (mostrar solo si las necesitas):
  ────────────────────────────────────────────────────────────────────────────

  [1] Mostrar pista 1 - Cómo empezar
  [2] Mostrar pista 2 - Cómo seguir threads
  [3] Mostrar pista 3 - Cuándo terminar

  Tu solución:
  ────────────────────────────────────────────────────────────────────────────

  > [código del usuario]

================================================================================
```

### Real-World Application Example:

```
================================================================================
            APLICACIÓN REAL: ÁRBOLES DE EXPRESIÓN
================================================================================

  CONTEXTO
  ────────────────────────────────────────────────────────────────────────────

  Cuando escribes una expresión matemática como:
    (3 + 4) * 5 - 2

  Los compiladores y calculadoras la representan como un árbol:

              -
             / \
            *   2
           / \
          +   5
         / \
        3   4

  ¿Por qué? Porque permite:
  • Evaluar en el orden correcto (precedencia automática)
  • Optimizar expresiones
  • Generar código máquina

  EJERCICIO PRÁCTICO
  ────────────────────────────────────────────────────────────────────────────

  Vamos a construir un evaluador de expresiones:

  1. Parsear: "(3 + 4) * 5" → árbol
  2. Evaluar: árbol → 35

  ```python
  class ExprNode:
      pass

  class NumNode(ExprNode):
      def __init__(self, value):
          self.value = value

  class OpNode(ExprNode):
      def __init__(self, op, left, right):
          self.op = op
          self.left = left
          self.right = right

  def evaluate(node):
      if isinstance(node, NumNode):
          return node.value
      elif isinstance(node, OpNode):
          left_val = evaluate(node.left)
          right_val = evaluate(node.right)
          if node.op == '+': return left_val + right_val
          if node.op == '-': return left_val - right_val
          if node.op == '*': return left_val * right_val
          if node.op == '/': return left_val / right_val
  ```

  DESAFÍO:
  Implementa `parse(expression_string)` que convierta un string como
  "(3 + 4) * 5" en el árbol de expresión correspondiente.

  [Ver solución guiada]  [Intentar solo]  [Saltar]

================================================================================
```

### Cross-Topic Connections:

```
================================================================================
              CONEXIÓN: ÁRBOLES → GRAFOS
================================================================================

  INSIGHT CLAVE
  ────────────────────────────────────────────────────────────────────────────

  Un árbol ES un grafo con restricciones especiales:
  • Conexo (todos los nodos alcanzables)
  • Acíclico (sin ciclos)
  • n nodos → n-1 aristas

  COMPARACIÓN
  ────────────────────────────────────────────────────────────────────────────

                    │ ÁRBOL           │ GRAFO
  ──────────────────┼─────────────────┼─────────────────
  Ciclos            │ No              │ Posibles
  Camino único      │ Sí (raíz→nodo)  │ Múltiples posibles
  Raíz              │ Definida        │ No necesaria
  Padre por nodo    │ Exactamente 1   │ 0, 1, o muchos
  BFS/DFS           │ Simples         │ Necesitan visited[]

  CUÁNDO USAR CADA UNO
  ────────────────────────────────────────────────────────────────────────────

  Usa ÁRBOL cuando:
  ✓ Hay jerarquía natural (org chart, sistema de archivos)
  ✓ Relación padre-hijo clara
  ✓ No hay ciclos en el dominio

  Usa GRAFO cuando:
  ✓ Conexiones arbitrarias (redes sociales, mapas)
  ✓ Pueden existir ciclos
  ✓ Múltiples caminos entre nodos

  PREPARACIÓN PARA GRAFOS
  ────────────────────────────────────────────────────────────────────────────

  Lo que ya sabes de árboles que aplica a grafos:
  ✅ BFS (búsqueda en anchura) - ¡igual en grafos!
  ✅ DFS (búsqueda en profundidad) - ¡igual pero con visited!
  ✅ Recursión sobre estructuras - mismo patrón

  Lo nuevo que aprenderás en grafos:
  → Detección de ciclos
  → Caminos más cortos (Dijkstra)
  → Representaciones (matriz vs lista de adyacencia)

  ────────────────────────────────────────────────────────────────────────────

  ¿Quieres empezar con Grafos ahora? [S/n]
  (Tu siguiente tema del temario)

================================================================================
```

## Extension Types

1. **Theoretical Deep Dive**: Mathematical proofs, formal analysis
2. **Advanced Implementation**: Optimizations, variants, edge cases
3. **Real-World Applications**: How it's used in industry
4. **Cross-Topic Connections**: Links to other subjects
5. **Historical Context**: Origins, evolution of the concept
6. **Interview Prep**: Common advanced interview questions

## Prerequisites for Extension

- Topic mastery ≥ 80%
- Core exercises completed
- No critical weak points in the topic

## When to Suggest Extension

- User has mastered a topic and has extra time
- Before moving to advanced topics that build on this one
- User explicitly shows interest in going deeper
- Time permits (not in emergency exam mode)

## Data Updates

After extension:

1. Update `.tutor/topic_status.json` - Mark as EXTENDING or increment mastery
2. Add extension topics to progress tracking
3. Record session with extension flag
4. May unlock advanced exercises/content

## Notes

- Extension should feel like exploration, not obligation
- Always connect to practical applications when possible
- Respect the user's time - extension is optional
- Warn if extending when exam is close (prioritize core material)
- Use the user's `learning_language`
