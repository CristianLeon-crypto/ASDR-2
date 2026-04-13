import sys


# ---- utilidades ----

def primeros_cadena(cadena, primeros, no_terminales):
    resultado = set()
    if cadena == ['ε']:
        resultado.add('ε')
        return resultado
    for simbolo in cadena:
        if simbolo not in no_terminales:
            resultado.add(simbolo)
            return resultado
        else:
            resultado.update(primeros[simbolo] - {'ε'})
            if 'ε' not in primeros[simbolo]:
                return resultado
    resultado.add('ε')
    return resultado


def calcular_primeros(gramatica, no_terminales):
    primeros = {nt: set() for nt in no_terminales}
    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                nuevos = primeros_cadena(prod, primeros, no_terminales)
                antes = len(primeros[nt])
                primeros[nt].update(nuevos)
                if len(primeros[nt]) != antes:
                    changed = True
    return primeros


def calcular_siguientes(gramatica, no_terminales, primeros, simbolo_inicial):
    siguientes = {nt: set() for nt in no_terminales}
    siguientes[simbolo_inicial].add('$')
    changed = True
    while changed:
        changed = False
        for nt, producciones in gramatica.items():
            for prod in producciones:
                if prod == ['ε']:
                    continue
                for i, simbolo in enumerate(prod):
                    if simbolo in no_terminales:
                        beta = prod[i + 1:]
                        antes = len(siguientes[simbolo])
                        if beta:
                            prim_beta = primeros_cadena(beta, primeros, no_terminales)
                            siguientes[simbolo].update(prim_beta - {'ε'})
                            if 'ε' in prim_beta:
                                siguientes[simbolo].update(siguientes[nt])
                        else:
                            siguientes[simbolo].update(siguientes[nt])
                        if len(siguientes[simbolo]) != antes:
                            changed = True
    return siguientes


def calcular_prediccion(gramatica, no_terminales, primeros, siguientes):
    prediccion = {}
    for nt, producciones in gramatica.items():
        for prod in producciones:
            prim = primeros_cadena(prod, primeros, no_terminales)
            if 'ε' in prim:
                pred = (prim - {'ε'}) | siguientes[nt]
            else:
                pred = prim
            prediccion[(nt, tuple(prod))] = pred
    return prediccion


# ---- gramática (tras eliminar recursividad izquierda) ----

gramatica = {
    'S':  [['A', "B'", 'C'], ['D', 'E']],
    'A':  [['dos', "B'", 'tres'], ['ε']],
    "B'": [['cuatro', 'C', 'cinco', "B'"], ['ε']],
    'C':  [['seis', 'A', "B'"], ['ε']],
    'D':  [['uno', 'A', 'E'], ["B'"]],
    'E':  [['tres']],
}
no_terminales = ['S', 'A', "B'", 'C', 'D', 'E']
simbolo_inicial = 'S'

# ---- cálculo de conjuntos ----

primeros   = calcular_primeros(gramatica, no_terminales)
siguientes = calcular_siguientes(gramatica, no_terminales, primeros, simbolo_inicial)
prediccion = calcular_prediccion(gramatica, no_terminales, primeros, siguientes)

print("=" * 65)
print("  EJERCICIO 1 - Conjuntos PRIMEROS, SIGUIENTES y PREDICCIÓN")
print("=" * 65)

print("\n-- Gramática resultante (sin recursividad izquierda):")
for nt, prods in gramatica.items():
    for prod in prods:
        print(f"   {nt} → {' '.join(prod)}")

print("\n-- Conjuntos PRIMEROS:")
for nt in no_terminales:
    print(f"   PRIMEROS({nt}) = {{ {', '.join(sorted(primeros[nt]))} }}")

print("\n-- Conjuntos SIGUIENTES:")
for nt in no_terminales:
    print(f"   SIGUIENTES({nt}) = {{ {', '.join(sorted(siguientes[nt]))} }}")

print("\n-- Conjuntos de PREDICCIÓN:")
for nt, prods in gramatica.items():
    for prod in prods:
        key = (nt, tuple(prod))
        pred = prediccion[key]
        print(f"   PRED({nt} → {' '.join(prod)}) = {{ {', '.join(sorted(pred))} }}")

# ---- verificación LL(1) ----
print("\n-- ¿Es LL(1)?")
es_ll1 = True
for nt in no_terminales:
    prods = gramatica[nt]
    conjs = [prediccion[(nt, tuple(p))] for p in prods]
    for i in range(len(conjs)):
        for j in range(i + 1, len(conjs)):
            inter = conjs[i] & conjs[j]
            if inter:
                es_ll1 = False
                print(f"   ❌ NO es LL(1): '{nt}' tiene conflicto en {sorted(inter)}")
if es_ll1:
    print("   ✅ SÍ es LL(1)")


# ---- ASDR ----

tokens_globales = []
pos_global = 0


def token():
    return tokens_globales[pos_global] if pos_global < len(tokens_globales) else '$'


def emparejar(esperado):
    global pos_global
    if token() == esperado:
        pos_global += 1
    else:
        raise SyntaxError(f"Error: se esperaba '{esperado}', se encontró '{token()}'")


def S():
    t = token()
    if t in prediccion[('S', tuple(['A', "B'", 'C']))]:
        A(); Bp(); C()
    elif t in prediccion[('S', tuple(['D', 'E']))]:
        D(); E()
    else:
        raise SyntaxError(f"Error en S: token inesperado '{t}'")


def A():
    t = token()
    if t in prediccion[('A', tuple(['dos', "B'", 'tres']))]:
        emparejar('dos'); Bp(); emparejar('tres')
    elif t in prediccion[('A', tuple(['ε']))]:
        pass  # ε
    else:
        raise SyntaxError(f"Error en A: token inesperado '{t}'")


def Bp():  # B'
    t = token()
    if t in prediccion[("B'", tuple(['cuatro', 'C', 'cinco', "B'"]))]:
        emparejar('cuatro'); C(); emparejar('cinco'); Bp()
    elif t in prediccion[("B'", tuple(['ε']))]:
        pass  # ε
    else:
        raise SyntaxError(f"Error en B': token inesperado '{t}'")


def C():
    t = token()
    if t in prediccion[('C', tuple(['seis', 'A', "B'"]))]:
        emparejar('seis'); A(); Bp()
    elif t in prediccion[('C', tuple(['ε']))]:
        pass  # ε
    else:
        raise SyntaxError(f"Error en C: token inesperado '{t}'")


def D():
    t = token()
    if t in prediccion[('D', tuple(['uno', 'A', 'E']))]:
        emparejar('uno'); A(); E()
    elif t in prediccion[('D', tuple(["B'"]))]:
        Bp()
    else:
        raise SyntaxError(f"Error en D: token inesperado '{t}'")


def E():
    t = token()
    if t in prediccion[('E', tuple(['tres']))]:
        emparejar('tres')
    else:
        raise SyntaxError(f"Error en E: token inesperado '{t}'")


def analizar_asdr(tokens):
    global tokens_globales, pos_global
    tokens_globales = tokens
    pos_global = 0
    try:
        S()
        return token() == '$'
    except SyntaxError:
        return False


# ---- lectura de archivo ----

if len(sys.argv) > 1:
    with open(sys.argv[1], 'r') as f:
        for linea in f:
            toks = linea.strip().split()
            if not toks:
                continue
            resultado = analizar_asdr(toks)
            estado = "ACEPTADA" if resultado else "RECHAZADA"
            print(f"\n-- Cadena: {' '.join(toks)}")
            print(f"   {estado}")
else:
    print("\n⚠️  Uso: python ejercicio1.py entrada.txt")