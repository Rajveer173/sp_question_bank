# COMPILER DESIGN - QUESTION BANK & SOLUTIONS
## End-term Exam (50 marks)
### Units 1-6: Complete Theory & Worked Numericals

---

## MARKS DISTRIBUTION
- **Units 1-3:** 20 marks (short answers + 1-2 numericals)
- **Units 4-6:** 30 marks (deeper problems + numericals)

---

# UNIT 1: LANGUAGE PROCESSES & ASSEMBLER (7 marks)

## Q1: Define language processing and list compiler phases.

**Answer:**
Language processing converts a program from source language to target language while preserving meaning.

**Main Compiler Phases:**
1. **Lexical Analysis** – Breaks source into tokens (keywords, identifiers, operators)
2. **Syntax Analysis** – Checks grammar, builds parse tree
3. **Semantic Analysis** – Type checking, scope resolution
4. **Intermediate Code Generation** – Produces TAC (Three-Address Code), trees, or DAGs
5. **Optimization** – Machine-independent & machine-dependent optimizations
6. **Code Generation** – Produces target machine code, register allocation
7. **Assembly & Linking** – Converts to machine code, links libraries

---

## Q2: Differentiate compiler and interpreter.

| Aspect | Compiler | Interpreter |
|--------|----------|-------------|
| **Processing** | Entire source → object code first | Line-by-line execution |
| **Execution** | Separate after compilation | During interpretation |
| **Speed** | Fast execution | Slow (repeated analysis) |
| **Memory** | More (code generation) | Less |
| **Debugging** | Harder (no source at runtime) | Easier (direct access) |
| **Examples** | C, C++, Java | Python, JavaScript, Lisp |

**Use Compiler for:** Performance-critical, embedded systems, large projects  
**Use Interpreter for:** Scripting, rapid prototyping, dynamic typing

---

## Q3: Explain two-pass assembler.

**Answer:**

**What is a two-pass assembler?**
A two-pass assembler processes assembly source code in two complete scans to handle forward references (labels defined later).

**Pass 1: Symbol Definition Phase**
- Scan entire source code
- Maintain location counter (LC) starting at 0
- For each **label**: add to symbol table with current LC value
- For each **instruction**: increment LC by instruction size
- **Output:** Symbol table mapping all labels to their addresses

**Pass 2: Code Generation Phase**
- Scan source again using symbol table from Pass 1
- For each label reference: replace with actual address from symbol table
- Generate machine code for each instruction
- **Output:** Machine code (object file)

**Symbol Table Structure:**
```
Label        Address  Type
START        0x0000   Label
LOOP         0x0008   Label
MAX          0x0014   Data
```

**Why Two Passes?**
- Forward references (using label before defining it) require knowing all label addresses upfront
- Pass 1 collects all label addresses
- Pass 2 can then resolve all references

---

## Q4: NUMERICAL - Symbol Table & Location Counter

**Problem:** Given the assembly code below, construct the symbol table and generate object code.

```
START:    LD    R1, 10       ; Load 10 into R1
          ADD   R1, R2       ; Add R2 to R1
LOOP:     MUL   R1, 2        ; Multiply R1 by 2
          CMP   R1, 100      ; Compare R1 with 100
          JNE   LOOP         ; Jump if not equal
          ST    R1, RESULT   ; Store result
          HLT                ; Halt
RESULT:   .SPACE 4           ; Reserve 4 bytes
```

**Assume:** Each instruction is 2 bytes.

**Solution:**

**PASS 1: Symbol Table Construction**

| Instruction | LC (Address) | Label? |
|------------|------|--------|
| LD R1, 10 | 0x0000 | START |
| ADD R1, R2 | 0x0002 | - |
| MUL R1, 2 | 0x0004 | LOOP |
| CMP R1, 100 | 0x0006 | - |
| JNE LOOP | 0x0008 | - |
| ST R1, RESULT | 0x000A | - |
| HLT | 0x000C | - |
| (space) | 0x000E | RESULT |

**Symbol Table:**
```
Symbol      Address (Hex)   Address (Dec)
START       0x0000          0
LOOP        0x0004          4
RESULT      0x000E          14
```

**PASS 2: Code Generation**

| Address | Instruction | Operand | Machine Code |
|---------|------------|---------|------|
| 0x0000 | LD R1, 10 | - | 10 0A |
| 0x0002 | ADD R1, R2 | - | 20 02 |
| 0x0004 | MUL R1, 2 | - | 30 02 |
| 0x0006 | CMP R1, 100 | - | 40 64 |
| 0x0008 | JNE LOOP | 0x0004 (resolved) | 50 04 |
| 0x000A | ST R1, RESULT | 0x000E (resolved) | 60 0E |
| 0x000C | HLT | - | FF FF |

**Key Points:**
- Forward reference (JNE LOOP) resolved using symbol table: LOOP at 0x0004
- RESULT address: 0x000E used for ST instruction

---

## Q5: Backpatching in One-Pass Assembler

**Theory:**

One-pass assemblers resolve forward references using **backpatching**:

**Algorithm:**
1. When forward reference encountered → add to **Forward Reference Table (FRT)**
2. Output incomplete machine code with placeholder
3. When label defined → look up FRT, fill in actual addresses in previous code

**Forward Reference Table:**
```
Instruction  Reference  Address  Status
JNE LOOP     LOOP       0x0000   Pending
...when LOOP found at 0x0004...
JNE LOOP     LOOP       0x0000   Resolved → update to 0x0004
```

**Example:**
```
0x0000  JNE  LOOP         ; Forward ref - placeholder at 0x0000
0x0002  LD   A, 5
0x0004  LOOP: ADD  A, B   ; Label defined here → backpatch 0x0000 with 0x0004
```

---

# UNIT 2: MACROS & MACRO PROCESSORS (6 marks)

## Q1: Define macro and macro processor. Macro vs Subroutine?

**Answer:**

**Macro:** Named sequence of instructions that can be invoked with parameters. The macro body is **expanded inline** at each call site.

**Macro Processor:** Translates macro calls into expanded code by text substitution.

| Aspect | Macro | Subroutine |
|--------|-------|-----------|
| **Expansion** | Inline (text copy) | Call/return branch |
| **Overhead** | None (compile-time) | Runtime call/return |
| **Code Size** | Larger (multiple copies) | Smaller (one definition) |
| **Speed** | Faster (no branch) | Slower (branch overhead) |
| **Use** | Small, frequent, critical | Large or occasional |

**Example:**
```
Macro definition:
  MACRO INC(R)
    ADD R, 1
  ENDM

Call 1: INC(R1) → expands to: ADD R1, 1
Call 2: INC(R2) → expands to: ADD R2, 1
(Two separate copies generated)

Subroutine would be:
  INC:   ADD R1, 1
         RET
  
  CALL INC    (shared code, branch overhead)
  CALL INC    (branch again)
```

---

## Q2: NUMERICAL - Macro Expansion with Parameters

**Problem:** Given the macro definition and calls below, show the expanded source code.

```
MACRO SWAP(A, B, T)
    MOV   T, A
    MOV   A, B
    MOV   B, T
ENDM

Source calls:
  SWAP(R1, R2, R3)
  SWAP(X, Y, TEMP)
```

**Solution:**

**Macro Expansion Process:**

When macro **SWAP(A, B, T)** is called:
1. Formal parameters: A, B, T
2. Actual arguments replace formal parameters
3. Macro body expanded inline at each call

**Call 1: SWAP(R1, R2, R3)**
- Substitute: A→R1, B→R2, T→R3
```
MOV   R3, R1      ; T = A (save R1 in R3)
MOV   R1, R2      ; A = B (copy R2 to R1)
MOV   R2, R3      ; B = T (copy R3 to R2)
```

**Call 2: SWAP(X, Y, TEMP)**
- Substitute: A→X, B→Y, T→TEMP
```
MOV   TEMP, X     ; T = A
MOV   X, Y        ; A = B
MOV   Y, TEMP     ; B = T
```

**Final Expanded Code:**
```
MOV   R3, R1
MOV   R1, R2
MOV   R2, R3
MOV   TEMP, X
MOV   X, Y
MOV   Y, TEMP
```

**Key Points:**
- Each macro call generates separate copy of code (code duplication)
- Parameter substitution done at assembly-time, not runtime
- Code size increases with multiple macro calls

---

## Q3: Macro Processor Data Structures (MNT, MDT, ALA)

**Answer:**

**Three main tables in a macro processor:**

### 1. Macro Name Table (MNT)
Maps macro names to their definitions.

| Macro Name | MDT Index | Formal Parameters |
|-----------|-----------|-------------------|
| SWAP | 0 | A, B, T |
| MAX | 5 | X, Y |
| MIN | 10 | X, Y |

**Purpose:** Quick lookup of macro definitions

### 2. Macro Definition Table (MDT)
Stores the body of each macro line-by-line.

| Index | Body Line |
|-------|-----------|
| 0 | MOV T, A |
| 1 | MOV A, B |
| 2 | MOV B, T |
| 3 | (ENDM marker) |
| 4 | - |
| 5 | CMP X, Y |
| 6 | JG X_IS_MAX |
| 7 | MOV X, Y |
| 8 | (ENDM marker) |

**Purpose:** Store macro definitions without replicating text

### 3. Argument List Array (ALA)
Stores actual arguments for current macro call.

**For call: SWAP(R1, R2, R3)**
```
ALA[1] = R1
ALA[2] = R2
ALA[3] = R3
```

**Macro Expansion Algorithm:**
```
1. Read macro name from source → lookup in MNT
2. Get MDT index and formal parameter list
3. Read actual arguments from call → fill ALA
4. Scan MDT from stored index
5. For each line in MDT:
   - Replace formal parameters (A, B, T) with ALA values (R1, R2, R3)
   - Output expanded line
   - Stop at ENDM marker
```

---

# UNIT 3: COMPILER PHASES - LEXICAL & SYNTAX ANALYSIS (7 marks)

## Q1: Lexical Analysis - Tokens, Lexemes, Patterns

**Answer:**

**Lexical Analysis** = Breaking source code into meaningful units (tokens)

**Three key concepts:**

1. **Lexeme:** Actual characters in source code
   - Examples: `count`, `42`, `+`, `if`

2. **Token:** Symbolic name representing a lexeme class
   - Examples: IDENTIFIER, NUMBER, PLUS, KEYWORD

3. **Pattern:** Rule describing which lexemes belong to a token
   - Examples: 
     - Identifier pattern: `[a-zA-Z][a-zA-Z0-9]*`
     - Number pattern: `[0-9]+`
     - Plus pattern: `+`

**Example:**
```c
Source: int count = 5 + 3;

Lexeme → Token
int    → KEYWORD
count  → IDENTIFIER
=      → ASSIGN
5      → NUMBER
+      → PLUS
3      → NUMBER
;      → SEMICOLON
```

**Token Definition:**
```
<token-name, attribute-value>

Examples:
<KEYWORD, int>
<IDENTIFIER, count>
<NUMBER, 5>
```

---

## Q2: NUMERICAL - Regular Expression to DFA

**Problem:** Convert the regular expression `(a|b)*abb` to a DFA.

**Solution:**

**Step 1: Understand the regex**
- `(a|b)*` = Zero or more repetitions of 'a' or 'b'
- Followed by exactly `abb`
- Accepted strings: `abb`, `aabb`, `babb`, `aaabb`, `aababb`, etc.

**Step 2: NFA Construction (Thompson's Algorithm)**

The NFA would have states 0-10 with transitions:
```
Start (q0) --ε--> loop part --ε--> (a|b)* part
                                       |
                                    (ε back)
                                       |
                                    abb sequence
                                       |
                                   Accept (qf)
```

Simplified states:
- q0: Start state
- q1-q3: Loop states for (a|b)*
- q4: Saw 'a'
- q5: Saw 'ab'
- q6: Saw 'abb' (accept)

**Step 3: DFA Conversion (Subset Construction)**

**DFA States (after subset construction):**

| DFA State | NFA Closure | Description |
|-----------|---------|-------------|
| q0 | {0,1,2,...} | Start, can match (a\|b)* |
| q1 | {...} | After seeing 'a' |
| q2 | {...} | After seeing 'ab' |
| q3 | {...} | After seeing 'abb' (Accept) |

**DFA Transition Table:**

```
State    Input: a    Input: b
q0       q1          q0          (any char keeps cycling)
q1       q1          q2          (saw 'a', next: b → q2, else restart)
q2       q1          q3          (saw 'ab', next: b → accept)
q3(F)    -           -           (accept state, no more transitions)
```

**Visual DFA:**
```
    a,b
   ↙   ↖
  q0 ──a──> q1 ──b──> q2 ──b──> q3(Accept)
   ↑                    ↑
   └────────────────────┘
        (restart on 'a')
```

**Test Strings:**

| String | Trace | Result |
|--------|-------|--------|
| abb | q0→q1→q2→q3 | ✓ Accept |
| aabb | q0→q1→q1→q2→q3 | ✓ Accept |
| babb | q0→q0→q1→q2→q3 | ✓ Accept |
| ab | q0→q1→q2 | ✗ Reject (not at accept) |
| abba | q0→q1→q2→q3→? | ✗ Reject (no exit from q3) |

---

## Q3: Computing FIRST and FOLLOW Sets

**Theory:**

**FIRST(X)** = Set of terminals that can appear as first symbol in any derivation from X

**FOLLOW(X)** = Set of terminals that can appear immediately after X in some valid sentential form

---

## Q4: NUMERICAL - Compute FIRST and FOLLOW

**Problem:** For the grammar below, compute FIRST and FOLLOW sets.

```
E  → T E'
E' → + T E' | ε
T  → F T'
T' → * F T' | ε
F  → ( E ) | id
```

**Solution:**

### Step 1: Compute FIRST Sets

**FIRST(F):**
- F can derive: `( E )` or `id`
- First symbol can be: `(` or `id`
- **FIRST(F) = {(, id}**

**FIRST(T'):**
- T' can derive: `* F T'` or `ε`
- First symbol: `*` (or nothing if ε)
- **FIRST(T') = {*, ε}**

**FIRST(T):**
- T → F T'
- Start with FIRST(F) = {(, id}
- T' is nullable (has ε), so don't add FIRST(T') here
- **FIRST(T) = {(, id}**

**FIRST(E'):**
- E' → `+ T E'` or `ε`
- First symbol: `+` (or nothing)
- **FIRST(E') = {+, ε}**

**FIRST(E):**
- E → T E'
- Start with FIRST(T) = {(, id}
- T is not nullable, so stop
- **FIRST(E) = {(, id}**

**Summary:**
```
FIRST(E)  = {(, id}
FIRST(E') = {+, ε}
FIRST(T)  = {(, id}
FIRST(T') = {*, ε}
FIRST(F)  = {(, id}
```

### Step 2: Compute FOLLOW Sets

**FOLLOW(E):**
- E is start symbol
- **FOLLOW(E) = {$}** (end of input)
- But also `)` from `( E )` in F
- **FOLLOW(E) = {$, )}**

**FOLLOW(E'):**
- E' appears at end of: E → T E'
- What follows E' is what follows E
- **FOLLOW(E') = {$, )}**

**FOLLOW(T):**
- T appears in: E → T E'
- What follows T: FIRST(E') - {ε} = {+}
- E' is nullable, so also FOLLOW(E) = {$, )}
- **FOLLOW(T) = {+, $, )}**

**FOLLOW(T'):**
- T' appears at end of: T → F T'
- What follows T' is what follows T
- **FOLLOW(T') = {+, $, )}**

**FOLLOW(F):**
- F appears in: T → F T'
- What follows F: FIRST(T') - {ε} = {*}
- T' is nullable, so also FOLLOW(T) = {+, $, )}
- **FOLLOW(F) = {*, +, $, )}**

**Summary:**
```
FOLLOW(E)  = {$, )}
FOLLOW(E') = {$, )}
FOLLOW(T)  = {+, $, )}
FOLLOW(T') = {+, $, )}
FOLLOW(F)  = {*, +, $, )}
```

---

# UNIT 4: SYNTAX DIRECTED TRANSLATION & INTERMEDIATE CODE (10 marks)

## Q1: Three-Address Code (TAC)

**Answer:**

**Three-Address Code** = Intermediate representation where each instruction has **at most 3 operands**.

**Rationale:** 
- Easy to translate to assembly
- Captures control flow and data flow
- Suitable for optimization

**TAC Instruction Forms:**

1. **Binary Operation:**
   ```
   x = y op z
   ```
   Example: `t1 = a + b`

2. **Unary Operation:**
   ```
   x = op y
   ```
   Example: `t2 = -x`

3. **Assignment:**
   ```
   x = y
   ```
   Example: `result = t1`

4. **Conditional Jump:**
   ```
   if x relop y goto L
   ```
   Example: `if i < n goto L1`

5. **Unconditional Jump:**
   ```
   goto L
   ```

6. **Function Call:**
   ```
   param x
   call p, n
   x = call p
   ```

7. **Array Access:**
   ```
   x = a[i]      (load)
   a[i] = x      (store)
   ```

**Example:**
```c
Source: a = b + c * d

TAC:
t1 = c * d         (multiply first, higher precedence)
t2 = b + t1        (then add)
a = t2             (finally assign)
```

---

## Q2: NUMERICAL - TAC Generation for Expressions

**Problem 1:** Generate TAC for: `x = a + b * c - d / e`

**Solution:**

**Step 1: Determine operator precedence & associativity**
- Precedence: `*, /` > `+, -`
- Left associative

**Step 2: Build parse tree** (respecting precedence)
```
           =
          / \
         x   -
            / \
           +   /
          / \ / \
         a  * d  e
           / \
          b   c
```

**Step 3: Postorder traversal & TAC generation**

| Postorder Node | TAC Instruction | Meaning |
|--------|------------------|---------|
| b, c | t1 = b * c | Multiply b and c |
| a, t1 | t2 = a + t1 | Add a to result |
| d, e | t3 = d / e | Divide d by e |
| t2, t3 | t4 = t2 - t3 | Subtract division from addition |
| x, t4 | x = t4 | Assign final result |

**Final TAC:**
```
t1 = b * c
t2 = a + t1
t3 = d / e
t4 = t2 - t3
x = t4
```

---

**Problem 2:** Generate TAC for: `if (x > 5) y = 10; else y = 20;`

**Solution:**

**Method: Backpatching for labels**

| Stmt # | TAC Instruction | Meaning |
|--------|-----------------|---------|
| 1 | if x > 5 goto L1 | If true, jump to L1 |
| 2 | y = 20 | False branch: assign 20 |
| 3 | goto L2 | Skip then part |
| 4 | L1: y = 10 | True branch: assign 10 |
| 5 | L2: | Continue after if-else |

**Explanation:**
- Line 1: Condition check; if true, jump to true branch (L1)
- Line 2: False branch (else)
- Line 3: Unconditional jump to end (L2) to skip true branch
- Line 4: Label and true branch
- Line 5: Label at end

---

**Problem 3:** Generate TAC for: `while (i < n) { sum = sum + a[i]; i = i + 1; }`

**Solution:**

| Stmt # | TAC Instruction | Meaning |
|--------|-----------------|---------|
| 1 | L1: if i >= n goto L2 | Loop condition (negated for false) |
| 2 | t1 = 4 * i | Array index × element size |
| 3 | t2 = a + t1 | Address of a[i] |
| 4 | t3 = *t2 | Load a[i] |
| 5 | t4 = sum + t3 | Add to sum |
| 6 | sum = t4 | Update sum |
| 7 | t5 = i + 1 | Increment i |
| 8 | i = t5 | Update loop counter |
| 9 | goto L1 | Jump back to condition |
| 10 | L2: | Exit loop |

**Key Points:**
- L1: Loop entry (condition check)
- Statements 2-8: Loop body
- Line 9: Unconditional jump to restart loop
- L2: Loop exit

---

## Q3: Syntax-Directed Definition (SDD)

**Theory:**

**SDD** = Grammar with semantic rules (functions) attached to productions.

Each production has:
- **Synthesized attributes** (computed from children)
- **Inherited attributes** (from parent)

**Example SDD for simple expressions:**

```
Production              Semantic Rule
E → E₁ + T             E.val = E₁.val + T.val
E → T                  E.val = T.val
T → T₁ * F             T.val = T₁.val * F.val
T → F                  T.val = F.val
F → ( E )              F.val = E.val
F → num                F.val = num.value
```

**Example:** Evaluate `2 + 3 * 4`

```
Parse tree:
         E
        / \
       E₁  T
       |  / \
       T T₁ F
       |  |  |
       F  F num(4)
       |  |
      num num
      (2)(3)

Evaluation:
F.val = 2
T.val = 2
F.val = 3
T₁.val = 3
F.val = 4
T₁.val = 3 * 4 = 12
E₁.val = 2
E.val = 2 + 12 = 14
```

---

# UNIT 5: CODE OPTIMIZATION (10 marks)

## Q1: Local and Global Optimizations

**Answer:**

### Local Optimizations (within basic block)

**Constant Folding:** Evaluate constant expressions at compile time
```
Before: x = 5 * 3
After:  x = 15
```

**Constant Propagation:** Replace variable with known constant
```
Before: x = 5; y = x + 3;
After:  x = 5; y = 8;
```

**Strength Reduction:** Replace expensive ops with cheaper ones
```
Before: x = y * 2
After:  x = y << 1          (bit shift faster)

Before: x = i * 4
After:  x = i << 2
```

**Dead Code Elimination:** Remove unreachable/unused code
```
Before: x = 5; y = 10; goto L; z = 20; L: print(y);
After:  x = 5; y = 10; goto L; L: print(y);    (z=20 removed)
```

### Global Optimizations (across basic blocks)

**Common Subexpression Elimination:** Avoid recomputing same expression
```
Before: t1 = a + b;
        ...
        t2 = a + b;    (same, but recomputed)

After:  t1 = a + b;
        ...
        t2 = t1;       (reuse result)
```

**Loop Invariant Code Motion:** Move code outside loop
```
Before: while (i < n) {
          t = x * y;       (same every iteration!)
          a[i] = t + i;
          i++;
        }

After:  t = x * y;        (compute once)
        while (i < n) {
          a[i] = t + i;
          i++;
        }
```

---

## Q2: NUMERICAL - Data-Flow Analysis (Reaching Definitions)

**Problem:** Analyze data flow for:
```
B1: x = 5
B2: y = 10
B3: if (x > 0) goto B4 else B5
B4: x = 20
B5: (skip)
B6: z = x + y
```

**Solution:**

**Step 1: Identify basic blocks and CFG**

```
      B1(x=5)
        |
      B2(y=10)
        |
      B3(if)
      / \
    B4   B5
   (x=20)(empty)
      \ /
      B6(z=x+y)
```

**Step 2: Define gen and kill sets**

| Block | gen (generated defs) | kill (killed defs) |
|-------|---------------------|-------------------|
| B1 | {x:1} | {x:4} (x from B4) |
| B2 | {y:2} | {} |
| B3 | {} | {} (no definitions) |
| B4 | {x:4} | {x:1} (x from B1) |
| B5 | {} | {} |
| B6 | {z:6} | {} |

**Step 3: Data-flow equations**

```
For each block B:
  IN[B] = ∪ OUT[P] for all predecessors P
  OUT[B] = gen[B] ∪ (IN[B] - kill[B])
```

**Step 4: Iterative solution**

**Iteration 1:**
```
IN[B1] = {}
OUT[B1] = {x:1}

IN[B2] = {x:1}
OUT[B2] = {x:1, y:2}

IN[B3] = {x:1, y:2}
OUT[B3] = {x:1, y:2}

IN[B4] = {x:1, y:2}
OUT[B4] = {x:4, y:2}

IN[B5] = {x:1, y:2}
OUT[B5] = {x:1, y:2}

IN[B6] = OUT[B4] ∪ OUT[B5] = {x:4, y:2} ∪ {x:1, y:2} = {x:4, x:1, y:2}
OUT[B6] = {x:4, x:1, y:2, z:6}
```

**Iteration 2:** (converges, no changes)

**Final Result:**
```
At B6: z = x + y
  x can be defined at: B1 (value 5) or B4 (value 20)
  y defined at: B2 (value 10)
  
Control-flow sensitive analysis:
  After B4→B6: x from B4, y from B2
  After B5→B6: x from B1, y from B2
```

---

# UNIT 6: CODE GENERATION (10 marks)

## Q1: Code Generation Tasks

**Answer:**

Code generation converts intermediate code (TAC) to target machine code.

**Main Tasks:**

1. **Instruction Selection**
   - Choose appropriate target machine instruction for each TAC statement
   - Consider addressing modes, available operations
   - Example: TAC `t1 = a + b` → Assembly `ADD R1, R2` (register form)

2. **Register Allocation**
   - Assign variables/temporaries to physical registers
   - Minimize register pressure (spill to memory if needed)
   - Maximize reuse (dead values can be overwritten)

3. **Instruction Scheduling**
   - Reorder instructions to avoid pipeline hazards
   - Minimize stalls and branch mispredictions
   - Maximize instruction-level parallelism

4. **Peephole Optimization**
   - Local post-processing on generated code
   - Remove redundant instructions
   - Example: `MOV R1, R2; MOV R2, R1` → eliminate

---

## Q2: NUMERICAL - TAC to Assembly (Register Allocation)

**Problem:** Convert TAC to assembly with register allocation.

Target: 3 registers (R1, R2, R3)

```
TAC:
  t1 = a + b
  t2 = c * d
  t3 = t1 - t2
  result = t3
```

**Solution:**

**Step 1: Live variable analysis**

```
Line 1: t1 = a + b       (a, b are live; t1 defined)
Line 2: t2 = c * d       (c, d are live; t2 defined; a, b dead)
Line 3: t3 = t1 - t2     (t1, t2 are live; t3 defined; c, d dead)
Line 4: result = t3      (result defined; t3 dead)

Live ranges:
  a: line 1 only
  b: line 1 only
  c: line 2 only
  d: line 2 only
  t1: lines 1-3
  t2: lines 2-3
  t3: lines 3-4
```

**Step 2: Register allocation**

```
Since we have 3 registers and max 2 live simultaneously:

  a → R1
  b → R2
  c → R1 (reuse R1; a is dead)
  d → R2 (reuse R2; b is dead)
  t1 → R1 (reuse R1; a is dead after line 1)
  t2 → R2 (reuse R2; c, d dead after line 2)
  t3 → R3
```

**Step 3: Code generation**

| TAC | Register Allocation | Assembly |
|-----|-------------------|----------|
| t1 = a + b | t1→R1, a→R1, b→R2 | LOAD R1, a; LOAD R2, b; ADD R1, R1, R2 |
| t2 = c * d | t2→R2, c→R1, d→R2 | LOAD R1, c; LOAD R2, d; MUL R2, R1, R2 |
| t3 = t1 - t2 | t3→R3, t1→R1, t2→R2 | SUB R3, R1, R2 |
| result = t3 | result, t3→R3 | STORE R3, result |

**Final Assembly:**
```
LOAD   R1, a           ; R1 = a
LOAD   R2, b           ; R2 = b
ADD    R1, R1, R2      ; R1 = a + b (t1)
LOAD   R2, c           ; R2 = c (reuse register)
MUL    R2, R1, R2      ; R2 = (a+b) * c  (ERROR - should be MUL R2, R2, d)

Corrected:
LOAD   R1, a
LOAD   R2, b
ADD    R1, R1, R2      ; R1 = t1
LOAD   R1, c           ; Reload R1 with c (t1 is in use for t3 = t1 - t2)
LOAD   R2, d
MUL    R2, R1, R2      ; R2 = t2
SUB    R3, R1, R2      ; ERROR - R1 has c, not t1!

Corrected allocation:
  t1 → R1 (live through line 3)
  t2 → R2 (live through line 3)
  
LOAD   R1, a
LOAD   R2, b
ADD    R1, R1, R2      ; R1 = t1
LOAD   R3, c
LOAD   R2, d           ; R2 = d (c in R3)
MUL    R2, R3, R2      ; R2 = c * d = t2
SUB    R3, R1, R2      ; R3 = t1 - t2 = t3
STORE  R3, result
```

**Summary:**
- 3 registers sufficient (max 2 simultaneously live)
- No spill needed
- Code size: 7 instructions

---

## Q3: Activation Records & Function Calls

**Theory:**

**Activation Record** = Stack frame storing function state during execution.

**Typical Layout** (stack grows downward):

```
┌─────────────────────┐
│  Return address     │ FP + 4  (saved PC)
├─────────────────────┤
│  Saved FP           │ FP      (previous frame pointer)
├─────────────────────┤
│  Local variable 1   │ FP - 4
├─────────────────────┤
│  Local variable 2   │ FP - 8
├─────────────────────┤
│  Temp storage       │ FP - 12
├─────────────────────┤
│  Outgoing params    │ (for next function call)
└─────────────────────┘ ← SP (Stack Pointer)
```

**Standard Calling Convention (x86-like):**

| Convention Aspect | Detail |
|-------------------|--------|
| **Parameter passing** | Push on stack (right-to-left) or use registers |
| **Return address** | Pushed by CALL; popped by RET |
| **Caller-saved** | EAX, ECX, EDX (caller saves before call) |
| **Callee-saved** | EBX, ESI, EDI, EBP (callee must save/restore) |
| **Return value** | In EAX (or EDX:EAX for 64-bit) |

---

## Q4: NUMERICAL - Activation Record Example

**Problem:** Write prologue, body, and epilogue for function:
```c
int add(int x, int y) {
    int sum = x + y;
    return sum;
}
```

**Solution:**

**Memory Layout:**
```
FP+12  ← Parameter y (4 bytes)
FP+8   ← Parameter x (4 bytes)
FP+4   ← Return address (saved PC, 4 bytes)
FP     ← Saved frame pointer (4 bytes)
FP-4   ← Local variable: sum (4 bytes)
SP     ← Current stack top
```

**Generated Code:**

**Prologue (enter function):**
```
PUSH   FP           ; Save caller's frame pointer
MOV    FP, SP       ; Set up new frame pointer
SUB    SP, SP, 4    ; Allocate 4 bytes for local 'sum'
```

**Function Body:**
```
MOV    EAX, [FP+8]  ; EAX = x (parameter at FP+8)
MOV    ECX, [FP+12] ; ECX = y (parameter at FP+12)
ADD    EAX, ECX     ; EAX = x + y
MOV    [FP-4], EAX  ; Store sum to stack (FP-4)
MOV    EAX, [FP-4]  ; EAX = sum (prepare return value)
```

**Epilogue (exit function):**
```
MOV    SP, FP       ; Deallocate local variables
POP    FP           ; Restore caller's frame pointer
RET                 ; Pop return address and jump
```

**Complete Function:**
```
add:
    PUSH   FP
    MOV    FP, SP
    SUB    SP, SP, 4
    
    MOV    EAX, [FP+8]
    MOV    ECX, [FP+12]
    ADD    EAX, ECX
    MOV    [FP-4], EAX
    MOV    EAX, [FP-4]
    
    MOV    SP, FP
    POP    FP
    RET
```

**Stack Evolution:**

```
Before CALL add:
    SP → [next instruction]    (caller's stack)

After CALL add:
    FP+4 → [return addr]
    FP → [saved FP]
    FP-4 → [space for sum]
    SP → (FP-4)

At RET:
    Return to caller at [FP+4]
    Stack restored to before CALL
```

---

# EXAM STRATEGY & STUDY TIPS

## Time Allocation (50-mark exam, 2 hours = 120 minutes)

| Unit Group | Time | Marks | Strategy |
|-----------|------|-------|----------|
| Units 1-3 | 30 min | 20 | Fast, crisp definitions + quick numericals |
| Units 4-6 | 70 min | 30 | Detailed solutions, show all steps |

## For Units 1-3 (20 marks):
✓ Define terms precisely  
✓ Draw symbol tables, DFAs, parse trees  
✓ Quick numericals (symbol table, DFA construction, FIRST/FOLLOW)  
✓ Answer in 2-3 sentences per definition

## For Units 4-6 (30 marks):
✓ Show detailed steps (parse tree → TAC → assembly)  
✓ Label all temporaries and registers  
✓ Mark IN/OUT sets for data-flow analysis  
✓ Explain rationale (why this optimization, what's the benefit)

## General Tips:
1. **Partial credit:** Examiners award marks for methodology even if final answer wrong
2. **Clarity:** Use diagrams, tables, step-by-step format
3. **Assumptions:** State clearly (e.g., "Assuming 4-byte integers, 3 registers available")
4. **Common mistakes:** 
   - Missing ENDM in macros
   - Forgetting backpatching when computing LAC
   - Wrong precedence in expression parsing
   - Incomplete activation records

---

# QUICK REFERENCE CHECKLIST

## Before Exam:
- [ ] Memorize compiler phases (7)
- [ ] Practice symbol table construction (2-3 examples)
- [ ] Know FIRST/FOLLOW algorithm by heart
- [ ] Practice TAC generation for expressions + loops + conditionals
- [ ] Practice 2-3 register allocation examples
- [ ] Understand activation record layout completely
- [ ] Do 2-3 full mock exams under time pressure

## During Exam:
- [ ] Read all questions first
- [ ] Allocate time: Units 1-3 get 25-30 min, Units 4-6 get 70-75 min
- [ ] Start with your strongest unit
- [ ] For numericals: (1) understand problem (2) show all steps (3) label clearly
- [ ] Leave 5 min for review and checking

---

**END OF QUESTION BANK & SOLUTIONS**
