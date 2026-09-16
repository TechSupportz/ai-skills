# Typst patterns

Block recipes, fit dials and failure modes for the house style in
[`assets/house-style.typ`](../assets/house-style.typ). The macros (`sec`, `sub`, `kv`,
`step`, `note`/`hot`/`warn`/`good`, `alert`, `k`) are defined there — this file is how to
*use* them.

## Block recipes

### Section — the unit of the sheet

```typst
#sec("U11 — INHERITANCE (IS-A)", C_OOP)[
  ...body...
]
```

One idea per `sec`. Title is `UNIT — TOPIC` in caps, so the eye lands on the unit number
when flipping. Colour comes from the accent bound to that topic family, held constant
across every sheet in the course.

### `kv` — the default body

Most content is a term/meaning pair, so reach for `kv` before prose:

```typst
#kv(
 [`super(...)`], [call parent constructor — must be the *first* statement],
 [Inherits], [fields + methods; `private` ones exist but are *not accessible*],
)
```

Left column: the literal token, in `raw` (backticks) when it is code. Right column: one
line, verb-first, no full-sentence padding.

### Callouts — one per section, at most

```typst
#hot[Java is *always pass-by-value*.]        // REMEMBER — the fact that unlocks the topic
#warn[Reassigning a parameter changes nothing for the caller.]  // TRAP — the mistake made under time pressure
#good[Submit early, submit often.]           // DO — the habit worth spending a line on
#alert("Use IS-A, not code reuse", color: C_OOP)[...]  // the two or three things that decide the grade
```

`alert` is loud by design. Three per sheet keeps it loud.

### Code

Fenced blocks with a language tag pick up the soft ground automatically:

````typst
```java
Point a = new Point(0, 0);
Point b = a;       // SAME heap object
b.move(1, 1);      // a.getX() is now 1.0  <- aliasing
```
````

Trailing `//` comments carry the teaching; the code stays the shortest form that shows it.

### Numbered workflow

```typst
#step(1, [Log in], "ssh <user>@pe111.comp.nus.edu.sg")
```

Or, when each step needs its own sub-lines, the zebra table with a narrow index rail:

```typst
#table(columns: (7pt, 1fr), stroke: none, inset: (x: 2.6pt, y: 2.2pt),
  row-gutter: 0pt, fill: (_, y) => if calc.odd(y) { ZEBRA },
  align: (right + horizon, left),
  text(fill: MUT, weight: 700)[1], [Compile *all* files \ #raw("javac *.java")],
)
```

### Diagrams — ASCII inside a raw block

Box-drawing characters in an untagged code block beat any drawing package at this size:

````typst
```
STACK             HEAP
 p ───────────►   [ Polygon | corners ─┐ ]
                                       │
 a ───────┐                            ▼
          └───►   [ Point ] [ Point ] [ Point ]
```
````

Reach for one where the concept is *spatial* — memory layout, a type hierarchy, a
pipeline, a funnel. Comparison tables carry everything else.

## Fit dials

The sheet is done when it fills its pages with no ragged tail. Turn these, in order, and
recompile after each:

1. **Reorder** — move a section to a column where it fits whole. Free.
2. **Cut** — delete the lowest-yield block. The one thing that always improves the sheet.
3. `#set par(leading: ...)` — `0.41em` default, `0.38em` floor.
4. Body `size` — `7.0pt` default, `6.6pt` floor. Below that, printing fails the reader.
5. `#columns` gutter — `0.62em` default, `0.5em` floor.
6. Column count — 3 is the default; 4 only for pure-reference sheets with no code.

Page margins and the `raw` sizes hold at the house values.

## Failure modes

- **Unclosed label** — `<WORD>` in markup is Typst label syntax, not a placeholder. Write
  placeholders as `CAPS_WORD`.
- **Unclosed delimiter** — brackets in `#columns(3)[...]` and `#sec(...)[...]` nest deep.
  When a compile error points at the end of file, the real fault is an earlier unbalanced
  `[`.
- **Math token error** — `$` opens math mode. Write `USD` or wrap in `#raw("$")`.
- **Ragged column bottoms** — a `block` with `breakable: false` (`kv`, `alert`) cannot
  split across a column, so it jumps whole to the next one. Either let it be, or split the
  content into two calls.
- **Font fallback** — the house pairing is Inter (body) + SF Mono (code), with Helvetica
  Neue and Menlo behind them. If `typst compile` warns about an unknown font, install it
  rather than swapping the stack, so every sheet in the course keeps one look.
