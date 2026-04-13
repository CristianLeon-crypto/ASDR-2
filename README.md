# Análisis Sintáctico Descendente Recursivo (ASDR)

---

## Ejercicio 1

### Enunciado

Dada la siguiente gramática:

```
S  → A B C | D E
A  → dos B tres | ε
B  → B cuatro C cinco | ε
C  → seis A B | ε
D  → uno A E | B
E  → tres
```

1. Verificar si existe recursividad por la izquierda y eliminarla si es necesario.
2. Calcular los conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN.
3. Determinar si la gramática es LL(1).
4. Implementar el ASDR en Python.

---

### Solución

#### Eliminación de recursividad izquierda

`B → B cuatro C cinco | ε` tiene recursividad izquierda. Se transforma introduciendo `B'`:

```
S  → A B' C | D E
A  → dos B' tres | ε
B' → cuatro C cinco B' | ε
C  → seis A B' | ε
D  → uno A E | B'
E  → tres
```

#### PRIMEROS

| No terminal | PRIMEROS |
|-------------|----------|
| S  | { dos, cuatro, seis, tres, uno, ε } |
| A  | { dos, ε } |
| B' | { cuatro, ε } |
| C  | { seis, ε } |
| D  | { uno, cuatro, ε } |
| E  | { tres } |

#### SIGUIENTES

| No terminal | SIGUIENTES |
|-------------|------------|
| S  | { $ } |
| A  | { cuatro, seis, tres, cinco, $ } |
| B' | { seis, tres, cinco, $ } |
| C  | { cinco, $ } |
| D  | { tres } |
| E  | { tres, $ } |

#### PREDICCIÓN

| Producción | PREDICCIÓN |
|------------|------------|
| S → A B' C | { dos, cuatro, seis, $ } |
| S → D E | { uno, cuatro, tres } |
| A → dos B' tres | { dos } |
| A → ε | { cuatro, seis, tres, cinco, $ } |
| B' → cuatro C cinco B' | { cuatro } |
| B' → ε | { seis, tres, cinco, $ } |
| C → seis A B' | { seis } |
| C → ε | { cinco, $ } |
| D → uno A E | { uno } |
| D → B' | { cuatro, tres } |
| E → tres | { tres } |

#### ¿Es LL(1)?

> ❌ **NO** — `S` tiene conflicto en `{ cuatro }` entre `S → A B' C` y `S → D E`.

---

#### Cómo ejecutar

```bash
python ejercicio1.py entrada.txt
```

Ejemplo de `entrada.txt`:
```
dos tres
seis dos tres
cuatro cinco
```

---

## Ejercicio 2

### Enunciado

Dada la siguiente gramática (sin recursividad izquierda):

```
S → B uno | dos C | ε
A → S tres B C | cuatro | ε
B → A cinco C seis | ε
C → siete B | ε
```

1. Calcular los conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN.
2. Determinar si la gramática es LL(1).
3. Implementar el ASDR en Python.

---

### Solución

#### PRIMEROS

| No terminal | PRIMEROS |
|-------------|----------|
| S | { uno, dos, tres, cuatro, cinco, ε } |
| A | { uno, dos, tres, cuatro, cinco, ε } |
| B | { uno, dos, tres, cuatro, cinco, ε } |
| C | { siete, ε } |

#### SIGUIENTES

| No terminal | SIGUIENTES |
|-------------|------------|
| S | { $, tres } |
| A | { cinco } |
| B | { $, uno, tres, cinco, seis, siete } |
| C | { $, tres, cinco, seis } |

#### PREDICCIÓN

| Producción | PREDICCIÓN |
|------------|------------|
| S → B uno | { uno, dos, tres, cuatro, cinco } |
| S → dos C | { dos } |
| S → ε | { $, tres } |
| A → S tres B C | { uno, dos, tres, cuatro, cinco } |
| A → cuatro | { cuatro } |
| A → ε | { cinco } |
| B → A cinco C seis | { uno, dos, tres, cuatro, cinco } |
| B → ε | { $, uno, tres, cinco, seis, siete } |
| C → siete B | { siete } |
| C → ε | { $, tres, cinco, seis } |

#### ¿Es LL(1)?

> ❌ **NO** — `S` tiene conflicto en `{ dos }` entre `S → B uno` y `S → dos C`.

---

#### Cómo ejecutar

```bash
python ejercicio2.py entrada.txt
```

Ejemplo de `entrada.txt`:
```
dos
uno
cuatro cinco siete seis
tres
```

---

## Ejercicio 3

### Enunciado

Dada la siguiente gramática:

```
S → S uno | A B C
A → dos B C | ε
B → C tres | ε
C → cuatro B | ε
```

1. Verificar si existe recursividad por la izquierda y eliminarla si es necesario.
2. Calcular los conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN.
3. Determinar si la gramática es LL(1).
4. Implementar el ASDR en Python.

---

### Solución

#### Eliminación de recursividad izquierda

`S → S uno | A B C` tiene recursividad izquierda. Con β₁ = `A B C` y α₁ = `uno`, se transforma:

```
S  → A B C S'
S' → uno S' | ε
A  → dos B C | ε
B  → C tres | ε
C  → cuatro B | ε
```

#### PRIMEROS

| No terminal | PRIMEROS |
|-------------|----------|
| S  | { dos, cuatro, tres, uno, ε } |
| S' | { uno, ε } |
| A  | { dos, ε } |
| B  | { cuatro, tres, ε } |
| C  | { cuatro, ε } |

#### SIGUIENTES

| No terminal | SIGUIENTES |
|-------------|------------|
| S  | { $ } |
| S' | { $ } |
| A  | { $, uno, tres, cuatro } |
| B  | { $, uno, tres, cuatro } |
| C  | { $, uno, tres, cuatro } |

#### PREDICCIÓN

| Producción | PREDICCIÓN |
|------------|------------|
| S → A B C S' | { $, dos, cuatro, tres, uno } |
| S' → uno S' | { uno } |
| S' → ε | { $ } |
| A → dos B C | { dos } |
| A → ε | { $, uno, tres, cuatro } |
| B → C tres | { cuatro, tres } |
| B → ε | { $, uno, tres, cuatro } |
| C → cuatro B | { cuatro } |
| C → ε | { $, uno, tres, cuatro } |

#### ¿Es LL(1)?

> ❌ **NO** — `B` tiene conflicto en `{ cuatro, tres }` entre `B → C tres` y `B → ε`.

---

#### Cómo ejecutar

```bash
python ejercicio3.py entrada.txt
```

Ejemplo de `entrada.txt`:
```
dos cuatro tres uno
cuatro tres
dos tres
uno
```