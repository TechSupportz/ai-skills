// ════════════════════════════════════════════════════════════
// HOUSE STYLE — copy this whole file to <name>.typ and fill in.
// Everything above `#columns(3, ...)` is the style contract:
// fonts, sizes, palette and macros stay byte-identical across
// sheets. Only the CAPS_PLACEHOLDER words change per cheatsheet.
// ════════════════════════════════════════════════════════════

#set page(paper: "a4", margin: (x: 0.30cm, top: 0.32cm, bottom: 0.62cm), columns: 1,
  footer: context {
    let n = counter(page).get().first()
    set text(size: 5.4pt, fill: rgb("#6f7887"), tracking: 0.04em)
    grid(columns: (1fr, auto),
      align: (left + horizon, right + horizon),
      upper(if n == 1 { "front — TOPIC · TOPIC · TOPIC" }
            else { "back — TOPIC · TOPIC · TOPIC" }),
      upper[COURSE_CODE SHEET_NAME · page #n of #counter(page).final().first()])
  })

// ─── palette ────────────────────────────────────────────────
#let INK  = rgb("#141922")   // near-black, warmer than pure black
#let MUT  = rgb("#6f7887")   // secondary text
#let HAIR = rgb("#e3e6eb")   // hairline rules
#let CODE = rgb("#f5f6f8")   // code block ground

// six accents — rename per course, keep the hexes
#let C_UNIX = rgb("#0f766e")   // teal
#let C_VIM  = rgb("#6d28d9")   // violet
#let C_JAVA = rgb("#b42318")   // red
#let C_TYPE = rgb("#b45309")   // amber
#let C_OOP  = rgb("#1d4ed8")   // blue
#let C_WARN = rgb("#334155")   // slate — meta / checklists

// ─── base typography ────────────────────────────────────────
#set text(font: ("Inter", "Helvetica Neue"), size: 7.0pt, weight: 400,
          fill: INK, tracking: -0.002em)
#set par(leading: 0.41em, justify: false)
#show raw: set text(font: ("SF Mono", "Menlo"), size: 6.15pt)

// code blocks: soft ground, no border
#show raw.where(block: true): it => block(
  width: 100%, fill: CODE, inset: (x: 3.2pt, y: 2.8pt), radius: 2.5pt,
  above: 2.6pt, below: 2.6pt, breakable: false, it)

// ─── components ─────────────────────────────────────────────
// section header: tinted bar + thick left accent (strong landmark)
#let sec(title, color, body) = block(width: 100%, breakable: true, below: 5.1pt, [
  #block(width: 100%, below: 3pt, sticky: true,
    fill: color.lighten(91%), stroke: (left: 2.2pt + color),
    inset: (left: 3.6pt, right: 3pt, y: 2.4pt),
    text(fill: color.darken(12%), weight: 700, size: 6.4pt,
         tracking: 0.055em, upper(title)))
  #body
])

#let sub(color, body) = block(above: 3.2pt, below: 1.6pt, sticky: true,
  text(fill: color, weight: 600, size: 5.9pt, tracking: 0.055em, upper(body)))

// callouts: left accent rule + faint tint
#let note(color, tag, body) = block(width: 100%, above: 2.6pt, below: 2.6pt,
  fill: color.lighten(94%), stroke: (left: 1.2pt + color.lighten(30%)),
  inset: (left: 3.6pt, right: 3pt, y: 2.3pt),
  text(size: 6.1pt, fill: INK)[#text(fill: color, weight: 700, size: 5.4pt,
    tracking: 0.07em)[#tag#h(3pt)]#body])

#let hot(body)  = note(rgb("#b45309"), "REMEMBER", body)
#let warn(body) = note(rgb("#b42318"), "TRAP", body)
#let good(body) = note(rgb("#0f766e"), "DO", body)

// alert: solid header bar, for the two or three things that decide the grade
#let alert(title, body, color: rgb("#b42318")) = block(width: 100%,
  above: 4pt, below: 4pt, breakable: false, radius: 2pt, clip: true,
  stroke: 0.5pt + color, [
  #block(width: 100%, fill: color, inset: (x: 3.4pt, y: 2.4pt),
    text(fill: white, weight: 700, size: 6.1pt, tracking: 0.06em, upper(title)))
  #block(width: 100%, inset: (x: 3.4pt, y: 2.6pt), {
    set par(leading: 0.40em, spacing: 0.40em)
    text(size: 6.1pt, body)
  })
])

// zebra key/value table: term in the left rail, meaning on the right
#let ZEBRA = rgb("#f4f5f8")
#let kv(..rows) = block(breakable: false, {
  set text(fill: MUT)
  show raw: set text(fill: INK, weight: 500)
  table(columns: (auto, 1fr), stroke: none, align: (left, left),
        inset: (x: 2.6pt, y: 1.32pt), column-gutter: 3.5pt, row-gutter: 0pt,
        fill: (_, y) => if calc.odd(y) { ZEBRA },
        ..rows.pos())
})

// numbered step, with the literal command right-aligned
#let step(n, what, cmd) = grid(columns: (8pt, 1fr, auto), align: (left, left, right),
  column-gutter: 2pt,
  text(fill: MUT, weight: 700, size: 6.2pt)[#n], text(size: 6.6pt)[#what], raw(cmd))

#let k(x) = raw(x)

// ─── masthead ───────────────────────────────────────────────
#block(width: 100%, below: 4.6pt, [
  #grid(columns: (1fr, auto), align: (left + bottom, right + bottom),
    [#text(size: 13pt, weight: 800, tracking: -0.03em)[COURSE_CODE]
     #h(4.5pt)
     #text(size: 7.6pt, weight: 500, fill: MUT, tracking: -0.01em)[SHEET_NAME · quick reference]],
    [#text(size: 5.6pt, fill: MUT, weight: 500, tracking: 0.09em)[SCOPE — UNITS N–M]])
  #v(2.4pt)
  #line(length: 100%, stroke: 1.1pt + INK)
])

// ─── thesis box: the one test the whole sheet hangs off ──────
#block(width: 100%, below: 5pt, stroke: 0.5pt + HAIR, radius: 2.5pt,
  inset: (x: 5pt, y: 3.4pt), [
  #grid(columns: (auto, 1fr), column-gutter: 6pt, align: (left + horizon, left + horizon),
    text(weight: 700, size: 6.4pt, tracking: 0.05em)[THE ONE QUESTION],
    text(size: 6.3pt)[The single test that resolves most questions on this paper.])
])

#columns(3, gutter: 0.62em)[

#sec("FIRST SECTION", C_WARN)[
content
]

]
