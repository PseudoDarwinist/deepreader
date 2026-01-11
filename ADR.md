# Deep Reader - ADR (Architectural Decision Records)

> **What is an ADR?**
> An **Architectural Decision Record** is a document that captures an important architectural decision made along with its context and consequences. It's a pattern used by engineering teams to preserve the "why" behind technical decisions, preventing context loss over time.

> "The why behind code is more valuable than the code itself."

This document captures the reasoning, decisions, and context behind every significant change in this project. When you look at code six months from now and wonder "why is this 80ms and not 50ms?" - the answer should be here.

**See also:** `CLAUDE.md` contains the Intentional Compaction Protocol that ensures this document stays updated.

---

## Animated Typewriter Text Effect - 2026-01-11

### Context & Problem

**User Request:** Implement an animated text effect similar to mattpalmer.io, where words like "educating", "lifting", "hiking" appear to be written in a playful, handwritten style with animation.

**The Inspiration:** Matt Palmer's website shows "matt is" followed by animated handwritten words that cycle through different activities. The words appear to be drawn/written on screen, creating an engaging, personal touch.

**Why This Matters:** The Deep Reader landing page needed more personality and engagement. A static "Master Complex Knowledge" headline doesn't convey the dynamic, transformative nature of the learning experience.

### Decision

Implemented a **typewriter animation with handwritten font** that cycles through phrases describing what Deep Reader does.

**Final Result:**
```
Master Complex Knowledge
Deep Reader is [transforming learning|building understanding|making you smarter|...]
```

### Alternatives Considered

| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|
| **Full SVG Drawing Animation** (like Matt Palmer) | Exact "being drawn" effect, very polished | Requires custom SVG files for each word, needs GSAP DrawSVGPlugin (paid), significant design work | Too much upfront investment for MVP; can upgrade later |
| **CSS-only animation** | No JavaScript, simple | Limited control, can't do typewriter effect smoothly | Couldn't achieve the dynamic word cycling |
| **Typewriter + Handwritten Font** | Works immediately, no external assets, easy to modify words, captures the essence | Not as polished as SVG drawing | **CHOSEN** - Best balance of effort vs. impact |
| **Rough.js generated handwriting** | Programmatic handwritten look | Heavy library, inconsistent results, complex setup | Overkill for this use case |

### Implementation Notes

**Files Modified:**
- `index.html:9` - Added Google Font "Caveat" (handwritten style)
- `index.html:379-468` - CSS for `.animated-text-container`, `.animated-word`, cursor blink, fade animations
- `index.html:1911-1916` - HTML structure in hero section
- `index.html:2822-2897` - JavaScript typewriter engine

**Technical Details:**

1. **Font Choice: Caveat**
   - Why Caveat? It's a clean, readable handwritten font that doesn't look childish. Other options (Pacifico, Dancing Script) felt too decorative.

2. **Timing Values:**
   ```javascript
   typingSpeed = 80       // ms per character when typing
   deletingSpeed = 40     // ms per character when deleting (faster feels natural)
   pauseAfterTyping = 1500  // ms to display complete word
   pauseBetweenWords = 2000 // ms before starting next word
   ```
   - Why 80ms typing? Tested 50ms (too fast, robotic), 100ms (too slow, boring), 80ms feels human.
   - Why faster deletion? Humans delete faster than they type. 40ms makes it feel natural.

3. **Word List:**
   ```javascript
   ['transforming learning', 'building understanding', 'making you smarter', 'unlocking insights', 'teaching deeply']
   ```
   - Each phrase is action-oriented, describes a benefit, fits the brand voice.

4. **Accessibility:**
   - Respects `prefers-reduced-motion` - shows static text instead of animation
   - Cursor uses CSS animation (GPU accelerated, battery friendly)

**How Matt Palmer's Actually Works (for future reference):**
- Each word is a separate SVG file with handwritten-style paths
- Uses GSAP + DrawSVGPlugin to animate stroke paths from 0% to 100%
- Paths have `fill: none`, `stroke-linecap: round`, `stroke-linejoin: round`
- Words cycle every ~2-3 seconds with fade transitions

### Trade-offs Accepted

1. **Not as polished as SVG drawing** - We get 80% of the visual impact with 20% of the effort. Can upgrade later.
2. **Font-dependent** - If Caveat fails to load, falls back to cursive, which is less consistent across browsers.
3. **No actual "drawing" effect** - Characters appear fully formed, not stroke-by-stroke. Acceptable for now.

### Future Considerations

- **Upgrade Path:** If we want the exact Matt Palmer effect later:
  1. Create SVG files for each word (use Figma/Illustrator with a drawing tablet)
  2. Add GSAP and DrawSVGPlugin
  3. Implement stroke animation with `drawSVG: "0%"` to `drawSVG: "100%"`

- **Word Customization:** Words array is easily modifiable. Consider making it dynamic based on user's learning history.

- **Performance:** Current implementation uses `setTimeout` chains. If we add many more animations, consider `requestAnimationFrame` for better performance.

### Change History

- **2026-01-11**: Initial implementation with typewriter effect + Caveat font. Chose this over full SVG approach for faster implementation.

---

## Template for Future Entries

```markdown
## [Feature Name] - YYYY-MM-DD

### Context & Problem
[Why was this needed? What user problem does it solve?]

### Decision
[What approach was chosen? One sentence summary.]

### Alternatives Considered
| Option | Pros | Cons | Why Rejected |
|--------|------|------|--------------|

### Implementation Notes
[Technical details, file changes, non-obvious decisions]

### Trade-offs Accepted
[What compromises were made?]

### Future Considerations
[What might need to change?]

### Change History
- [Date]: [What changed and why]
```
