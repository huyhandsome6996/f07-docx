---
name: Warm Empathy Bridge
colors:
  surface: '#fff8f6'
  surface-dim: '#ffcfc5'
  surface-bright: '#fff8f6'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#fff0ee'
  surface-container: '#ffe9e5'
  surface-container-high: '#ffe2dc'
  surface-container-highest: '#ffdad3'
  on-surface: '#360f07'
  on-surface-variant: '#56423e'
  inverse-surface: '#502319'
  inverse-on-surface: '#ffede9'
  outline: '#89726d'
  outline-variant: '#ddc0ba'
  surface-tint: '#9f402d'
  primary: '#89301e'
  on-primary: '#ffffff'
  primary-container: '#a84733'
  on-primary-container: '#ffdcd5'
  inverse-primary: '#ffb4a4'
  secondary: '#a03f2a'
  on-secondary: '#ffffff'
  secondary-container: '#ff866b'
  on-secondary-container: '#741f0c'
  tertiary: '#6b4600'
  on-tertiary: '#ffffff'
  tertiary-container: '#895c09'
  on-tertiary-container: '#ffdeb4'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#ffdad3'
  primary-fixed-dim: '#ffb4a4'
  on-primary-fixed: '#3e0500'
  on-primary-fixed-variant: '#802918'
  secondary-fixed: '#ffdad2'
  secondary-fixed-dim: '#ffb4a3'
  on-secondary-fixed: '#3d0600'
  on-secondary-fixed-variant: '#812815'
  tertiary-fixed: '#ffddb2'
  tertiary-fixed-dim: '#f7bc65'
  on-tertiary-fixed: '#291800'
  on-tertiary-fixed-variant: '#624000'
  background: '#fff8f6'
  on-background: '#360f07'
  surface-variant: '#ffdad3'
typography:
  headline-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Be Vietnam Pro
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  headline-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 17px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: '0'
  body-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
    letterSpacing: '0'
  body-md:
    fontFamily: Be Vietnam Pro
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: '0'
  body-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: '0'
  label-lg:
    fontFamily: Be Vietnam Pro
    fontSize: 15px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.01em
  label-md:
    fontFamily: Be Vietnam Pro
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Be Vietnam Pro
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 14px
    letterSpacing: 0.02em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  margin: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system is crafted for high-school students and their parents navigating emotionally vulnerable conversations within a Zalo Mini App environment. The visual atmosphere is calm, organic, and deeply human—resembling warm paper stationery, gentle editorial guidance, and grounded emotional safety.

### Aesthetic Principles
- **Restrained & Grounded:** Strict avoidance of high-gloss tech tropes, purple-violet neon glows, floating AI mascots, futuristic particles, or noisy gradients. AI acts as a quiet, thoughtful scribe rather than an intrusive machine.
- **Tactile Paper Warmth:** Built on layered cream surfaces and deep earthen typography, creating an intimate space where users feel protected to draft raw thoughts, refine their tone, and review mutual feelings without performance anxiety.
- **Controlled Agency:** The interface never auto-sends or alters text autonomously. Every state makes emotional consent, reversible actions, and user control visibly clear through grounded affordances and reassuring tactile feedback.

## Colors

The palette relies on tactile earthen clays, parchment tones, and muted functional accents. It rejects cold algorithmic blues and harsh monochromes in favor of psychological safety.

### Palette Implementation
- **Canvas Base (`#FFF4E8`):** The master viewport canvas representing natural warm paper. It reduces glare and screen fatigue during difficult emotional states.
- **Card & Workspace Surface (`#FFFFFF`):** High-clarity white reserved for writing sheets, draft cards, bottom sheets, and comparative text blocks to ensure impeccable legibility.
- **Primary Brand Terracotta (`#A84733`):** High-priority actions, primary submit states, and anchored CTA buttons. Paired exclusively with `#FFF4E8` text for contrast and warmth.
- **Secondary Clay Accent (`#C65B43`):** Brand headers, supportive interactive states, active indicators, and expressive text highlights.
- **Tertiary Amber Accent (`#E4AB56`):** Soft focus highlights, emotional tag accents, progress markers, and AI suggestion pips.
- **Primary Ink Typography (`#713D32`):** Rich, deep walnut-brown used for headings, body prose, and core reading content instead of harsh black.
- **Secondary Ink & Subtext (`#475569`):** Balanced slate for descriptive microcopy, metadata, placeholders, character counts, and state guidance.
- **Structured Borders (`#CBD5E1` / `#64748B`):** Subtle dividers use `#CBD5E1` for passive surfaces; high-focus input borders use `#64748B` for crisp, accessible definition.

### Feedback Semantic Tokens
- **Success:** Ink `#166534` over surface `#F0FDF4` (reassurance, sent confirmation, safe tone).
- **Warning:** Ink `#92400E` over surface `#FFFBEB` (caution prompts, tone sensitivity notices).
- **Critical / Error:** Ink `#B91C1C` over surface `#FEF2F2` (loss of connectivity, draft length warnings).
- **Informative:** Ink `#1E40AF` over surface `#EFF6FF` (privacy reminders, AI assistance parameters).

## Typography

The type system standardizes on **Be Vietnam Pro** to deliver native diacritic clarity, natural Vietnamese phrasing, and human warmth. 

### Editorial Guidelines
- **Comfortable Line Height:** All body sizes use a generous 1.45–1.5× line-height ratio, preventing visual crowding when reading emotional, long-form reflections.
- **Reading Hierarchy:** Headings never overwhelm mobile viewports. `headline-lg` caps at `24px` to allow compact Zalo Mini App navigation bars to remain unobtrusive and focused.
- **Accessibility & Weight:** Avoid weights below `400`. Critical body text and user-generated reflections default to `15px` (`body-md`) or `16px` (`body-lg`) to preserve ease of reading for parents and teens alike.

## Layout & Spacing

Designed specifically for the constraints of mobile webviews embedded within the Zalo ecosystem.

### Layout Principles
- **Grid Architecture:** Single-column fluid mobile flow bound to dynamic viewport widths with a consistent `16px` outer margin. Desktop preview/responsive modes constrain max-content width to `480px` centered on `#FFF4E8`.
- **Rhythm & Padding:** Spacing follows a 4px base scale:
  - `space-xs` (4px): Micro gaps between icons and labels.
  - `space-sm` (8px): Spacing between grouped chips and tight metadata.
  - `space-md` (12px): Internal control padding and stacked paragraph separation.
  - `space-lg` (16px): Structural card padding, list item gutters, and section gaps.
  - `space-xl` (24px): Inter-section flow and bottom fixed CTA clearances.
- **Safe Zone Insets:** Respect top navigation app headers and bottom device indicators with an explicit bottom padding buffer of `24px` plus safe-area-inset for fixed CTA panels.

## Elevation & Depth

Visual hierarchy uses physical sheet stacking rather than floating blur effects. The approach conveys trust, containment, and editorial stability.

### Elevation Layers
- **Ground (`#FFF4E8`):** The flat, quiet base canvas. Zero elevation.
- **Layer 1 (Resting Cards & Surfaces):** `#FFFFFF` surface accompanied by a soft, warm ambient drop: `0px 2px 8px rgba(113, 61, 50, 0.05)` and a delicate border `1px solid #CBD5E1`.
- **Layer 2 (Floating Action Trays / Comparison Docks):** Fixed bottom action panels and sliding toolbars use `0px -4px 16px rgba(113, 61, 50, 0.08)` anchored with border-top `1px solid #CBD5E1`.
- **Layer 3 (Modals & Bottom Sheets):** Full overlay sheets sit on a dimming scrim of `rgba(113, 61, 50, 0.40)` with upward elevation: `0px -8px 24px rgba(113, 61, 50, 0.12)`.

## Shapes

The geometric form factor relies on balanced, friendly contours that soften formal friction without appearing childlike.

### Shape Tokens
- **Standard Controls & Cards (`rounded`, 8px–12px):** Default input fields, writing cards, comparison boxes, and tone selector containers use `10px` to `12px` border radius (`rounded-lg`).
- **Interactive Badges & Chips (`rounded-full`, 9999px):** Emotion tags, sentiment indicators, and AI suggestion chips adopt fully pill-shaped contours for distinct tactile pickability.
- **Bottom Drawers & Sheets:** Top edges feature `16px` rounded corners (`rounded-t-2xl`) to evoke a comfortable unfolding letter.

## Components

Every interactive element enforces a minimum physical touch target of `44x44px` to eliminate errant taps during stressful moments.

### 1. Primary & Secondary Buttons
- **Primary CTA:** Height `48px`. Background `#A84733`, text `#FFF4E8`, font `label-lg` (`15px/600`). Radius `12px`. Pressed state darkens to `#8F3B2A`. Full-width layout within sticky bottom bars.
- **Secondary Tone / Action Button:** Height `44px`. Background `#FFFFFF`, border `1.5px solid #CBD5E1`, text `#713D32`. Pressed state transitions to `#FFF4E8`.
- **Ghost / Revert Button:** Minimal visual weight, no border, text `#475569`, underlined on focus, clear tap target of `44px`.

### 2. Emotion & Tone Chips
- **Resting:** Background `#FFFFFF`, border `1px solid #CBD5E1`, text `#475569`, radius `9999px`, padding `6px 14px`.
- **Selected:** Background `#FFF4E8`, border `1.5px solid #C65B43`, text `#713D32`, font weight `600`. Subtle warm glow without neon luminance.

### 3. Writing Surface & Textarea
- **Surface:** Background `#FFFFFF`, border `1px solid #CBD5E1`, radius `12px`, padding `14px 16px`, text `#713D32`.
- **Active / Focused:** Border transitions to `1.5px solid #64748B`. Placeholder text styled in `#475569` at 60% opacity.
- **Metadata Tray:** Embedded character count and emotion status pinned to the bottom right in `label-sm` (`#475569`).

### 4. AI Expression Revision Cards (Side-by-Side / Diff)
- **Container:** Dual surface card on `#FFFFFF`, radius `12px`, separated by a gentle divider `#CBD5E1`.
- **Before (Original Voice):** Tinted header label "Lời nhắn ban đầu" in `#475569`. Content text in `#713D32`.
- **After (Empathetic AI Suggestion):** Tinted header label "Gợi ý diễn đạt ấm áp hơn" in `#C65B43` accompanied by an unobtrusive pen or leaf icon (strictly no robot, sparkle, or sci-fi icons).
- **Tone Explainer:** Subtext block using informational blue (`#EFF6FF` background, `#1E40AF` text) or warm amber (`#FFFBEB`, `#92400E`) clarifying *why* phrasing was softened.

### 5. Checkboxes, Radios, & Confirmations
- **Size:** `20x20px` checkbox/radio centered in a minimum `44x44px` invisible touch target frame.
- **State:** Inactive border `#CBD5E1`. Active fill `#A84733` with `#FFF4E8` checkmark.
- **Confirmation Sheets:** Critical actions (such as sending without AI review or clearing a deeply personal draft) require a deliberate 2-step explicit modal sheet.