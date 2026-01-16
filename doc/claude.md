# English Words - Vocabulary Learning App

## Project Overview

A Next.js-based vocabulary learning application using spaced repetition algorithm to help users efficiently memorize English words. All data is stored locally, no login or backend service required.

### Core Features

- 10,000 most common English words based on Wikipedia word frequency
- Spaced repetition memory system with fuzzing to prevent review clustering
- Click to fetch English definitions in real-time (Free Dictionary API)
- Quick marking system to skip already-known words
- Fully local storage (IndexedDB), privacy-friendly
- PWA support for offline usage
- Support data export/import for backup

---

## Tech Stack

| Category | Technology | Description |
|----------|------------|-------------|
| Framework | Next.js 14 (App Router) | React full-stack framework with static export |
| Styling | Tailwind CSS | Utility-first CSS framework |
| UI Components | shadcn/ui | High-quality, accessible components |
| State Management | Jotai | Primitive and flexible state management |
| Validation | Zod | TypeScript-first schema validation |
| Local Storage | IndexedDB (Dexie.js) | Progress and definition cache |
| PWA | Serwist | Service worker and offline support |
| Deployment | Static Export | Deploy to GitHub Pages / Vercel / Netlify |

### Why These Technologies

- **Next.js 14**: Mature and stable, App Router provides better code organization, static export requires no server
- **Tailwind CSS**: High development efficiency, simple responsive design
- **shadcn/ui**: Beautiful, accessible components, easy to customize
- **Jotai**: Simpler than Redux, more performant than Context, atomic state model
- **Zod**: Runtime validation with TypeScript inference
- **Dexie.js**: Simple IndexedDB wrapper, async operations won't block main thread
- **Serwist**: Modern service worker library for Next.js PWA support

---

## User Flow

### Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                         User Journey                             │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────┐      ┌──────────┐      ┌──────────┐      ┌──────────┐
  │  Browse  │ ───► │  Learn   │ ───► │  Review  │ ───► │ Mastered │
  │  & Mark  │      │   New    │      │   Due    │      │          │
  └──────────┘      └──────────┘      └──────────┘      └──────────┘
       │                 │                 │
       │    Mark known   │   Study cards   │   Recall cards
       │    words to     │   with spaced   │   based on
       │    skip them    │   repetition    │   schedule
       │                 │                 │
       ▼                 ▼                 ▼
  ┌──────────────────────────────────────────────────────────────┐
  │                    Progress saved to IndexedDB                │
  └──────────────────────────────────────────────────────────────┘
```

### Word Status Flow

```
                    ┌─────────────┐
                    │   Unknown   │  (No progress record)
                    │      ○      │
                    └─────────────┘
                          │
           ┌──────────────┼──────────────┐
           │              │              │
           ▼              │              │
    ┌─────────────┐       │       ┌─────────────┐
    │   Skipped   │       │       │  Learning   │
    │      ●      │       │       │      ◐      │
    │ (user knows)│       │       │ (level 0-4) │
    └─────────────┘       │       └─────────────┘
           │              │              │
           │    Click     │    Study     │
           │  "Know It"   │    flow      │
           │              │              │
           │              │              ▼
           │              │       ┌─────────────┐
           │              │       │  Mastered   │
           │              │       │      ★      │
           │              │       │ (level = 5) │
           │              │       └─────────────┘
           │              │              │
           └──────────────┴──────────────┘
                          │
                          ▼
                   Never show in
                   review queue
```

### Status Definitions

| Status | Icon | Description | In Review Queue? |
|--------|------|-------------|------------------|
| Unknown | ○ | Word not yet seen (no progress record) | No |
| Skipped | ● | User marked as "already know" | No |
| Learning | ◐ | Currently learning (level 0-4) | Yes (when due) |
| Mastered | ★ | Reached level 5 through study | No |

### Typical User Journey

1. **First Visit**: User goes to Browse page, quickly marks common words (the, a, is...) as "Know It"
2. **Start Learning**: User selects a word group and begins learning unknown words
3. **Daily Review**: User reviews due words based on spaced repetition schedule
4. **Continuous Progress**: User can always go back to Browse to mark more words or check progress

---

## Coding Standards

### File & Directory Naming

- **Kebab-case**: ALL filenames and folders must be strictly kebab-case
  - ✅ `user-profile.tsx`, `use-window-size.ts`, `api-config.ts`
  - ❌ `UserProfile.tsx`, `useWindowSize.ts`

- **Colocation**: Organize folders by feature module
  - Main component = `index.tsx`
  - Internal sub-components = `components/` subdirectory

### Component Architecture

- **Syntax**: Use `export function ComponentName() {}`. Do not use arrow functions for components
- **Granularity**: Components must be small. Split complex UIs into sub-components (Single Responsibility Principle)
- **Exports**: Use Named Exports only. Do not use `export default`
- **Button Types**: Always specify `type="button"` or `type="submit"`

### TypeScript Guidelines

- **No `any`**: Strictly forbidden. Use `unknown` or Generics if necessary
- **Type Definitions**: Use `type` instead of `interface`
  - ✅ `type ButtonProps = { ... }`
  - ❌ `interface ButtonProps { ... }`
- **Validation**: Use Zod schemas to validate all data from backend or forms

### Naming Conventions

| Entity | Format | Example |
|--------|--------|---------|
| Component Name | PascalCase | `ProductList`, `SubmitButton` |
| Variables/Functions | camelCase | `items`, `getUserData` |
| Hooks | camelCase (prefix `use`) | `useAuth`, `useLocalStorage` |
| Constants | UPPER_SNAKE_CASE | `MAX_RETRY_COUNT`, `API_URL` |
| Types | PascalCase | `UserProps`, `ApiResponse` |
| Files/Directories | kebab-case | `word-card.tsx`, `use-progress.ts` |

- **Boolean Props**: Use prefixes like `is`, `has`, `should` (e.g., `isLoading`, `hasError`)
- **Event Handlers**: Props start with `on` (`onSave`), implementations start with `handle` (`handleSave`)

---

## Data Architecture

### 1. Static Data (Word List) - Lazy Loading

Word data is split into separate JSON files for optimal bundle size and lazy loading.

```
public/
└── data/
    ├── group-1-1000.json
    ├── group-1001-2000.json
    ├── group-2001-3000.json
    ├── group-3001-4000.json
    ├── group-4001-5000.json
    ├── group-5001-6000.json
    ├── group-6001-7000.json
    ├── group-7001-8000.json
    ├── group-8001-9000.json
    └── group-9001-10000.json
```

```typescript
// types/word.ts
export type Word = {
  rank: number;      // Frequency rank 1-10000
  word: string;      // The word
};

export const WORD_GROUPS = [
  '1-1000',
  '1001-2000',
  '2001-3000',
  '3001-4000',
  '4001-5000',
  '5001-6000',
  '6001-7000',
  '7001-8000',
  '8001-9000',
  '9001-10000',
] as const;

export type WordGroup = (typeof WORD_GROUPS)[number];
```

```typescript
// lib/word-loader.ts
const wordCache = new Map<WordGroup, Word[]>();

export async function loadWordGroup(group: WordGroup): Promise<Word[]> {
  // Return cached data if available
  if (wordCache.has(group)) {
    return wordCache.get(group)!;
  }

  // Fetch JSON file
  const res = await fetch(`/data/group-${group}.json`);
  const words: Word[] = await res.json();

  // Cache for future use
  wordCache.set(group, words);
  return words;
}
```

**Benefits**:
- Main bundle stays small (~50KB instead of ~300KB+)
- Only loads word data when user navigates to specific group
- In-memory cache prevents redundant fetches

### 2. Storage Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                       Storage Distribution                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  localStorage (sync, small data, fast read)                     │
│  ├── settings: { theme, dailyNewWords }                         │
│  └── last-group: "1001-2000"                                    │
│                                                                  │
│  IndexedDB via Dexie.js (async, large data)                     │
│  ├── progress: { word -> WordProgress }  (~1MB for 10k words)   │
│  └── definitions: { word -> CachedDefinition }  (up to 50MB)    │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Why IndexedDB for Progress**:
- `localStorage` is synchronous and blocks main thread
- With 10k records, JSON serialization/deserialization causes jank
- IndexedDB is async, won't freeze UI during updates

### 3. Learning Progress (IndexedDB)

```typescript
// lib/db.ts
import Dexie, { type Table } from 'dexie';

export type WordProgress = {
  word: string;         // Primary key
  level: number;        // Mastery level 0-5
  nextReview: number;   // Next review timestamp
  lastReview: number;   // Last review timestamp
  reviewCount: number;  // Total review count
  createdAt: number;    // First learning timestamp
  isSkipped: boolean;   // True if user marked as "already know"
};

export type CachedDefinition = {
  word: string;         // Primary key
  data: DictionaryResponse;
  fetchedAt: number;
};

class WordsDatabase extends Dexie {
  progress!: Table<WordProgress, string>;
  definitions!: Table<CachedDefinition, string>;

  constructor() {
    super('words-app');
    this.version(1).stores({
      progress: 'word, level, nextReview, isSkipped',
      definitions: 'word, fetchedAt',
    });
  }
}

export const db = new WordsDatabase();
```

```typescript
// Zod schema for import/export validation
export const wordProgressSchema = z.object({
  word: z.string(),
  level: z.number().min(0).max(5),
  nextReview: z.number(),
  lastReview: z.number(),
  reviewCount: z.number().min(0),
  createdAt: z.number(),
  isSkipped: z.boolean(),
});

// Derive status from progress data
export type WordStatus = 'unknown' | 'skipped' | 'learning' | 'mastered';

export function getWordStatus(progress: WordProgress | undefined): WordStatus {
  if (!progress) return 'unknown';
  if (progress.isSkipped) return 'skipped';
  if (progress.level >= 5) return 'mastered';
  return 'learning';
}
```

### 4. External API

**Free Dictionary API**:
- URL: `https://api.dictionaryapi.dev/api/v2/entries/en/{word}`
- Free, no API key required
- Returns: phonetics, parts of speech, definitions, examples, synonyms, etc.

---

## Spaced Repetition Algorithm

Using simplified SM-2 algorithm with **fuzzing** to prevent review clustering.

### Mastery Levels

| Level | Base Interval | Description |
|-------|---------------|-------------|
| 0 | 0 days | New word / Forgotten |
| 1 | 1 day | Just learned |
| 2 | 3 days | Initial grasp |
| 3 | 7 days | Basic mastery |
| 4 | 14 days | Proficient |
| 5 | 30 days | Fully mastered |

### User Feedback Options

| Option | Effect |
|--------|--------|
| Again (Forgot) | level = 0 |
| Hard (Difficult) | level = max(0, level - 1) |
| Good (Remembered) | level = min(5, level + 1) |
| Easy (Too simple) | level = min(5, level + 2) |

### Fuzzing (Review Spreading)

**Problem**: Without fuzzing, learning 100 words on Day 1 means 100 reviews due on Day 2, causing "review avalanche".

**Solution**: Add ±10% random variance to review intervals.

```typescript
// lib/spaced-repetition.ts
const BASE_INTERVALS = [0, 1, 3, 7, 14, 30] as const; // Days

export type ReviewQuality = 'again' | 'hard' | 'good' | 'easy';

/**
 * Add ±10% random variance to prevent review clustering
 */
function fuzz(days: number): number {
  if (days === 0) return 0;
  const variance = days * 0.1;
  const offset = (Math.random() - 0.5) * 2 * variance;
  return Math.max(1, days + offset);
}

export function calculateNextReview(level: number): number {
  const baseDays = BASE_INTERVALS[level];
  const fuzzedDays = fuzz(baseDays);
  return Date.now() + fuzzedDays * 24 * 60 * 60 * 1000;
}

export function updateProgress(
  current: WordProgress | undefined,
  word: string,
  quality: ReviewQuality
): WordProgress {
  const now = Date.now();
  const baseLevel = current?.level ?? 0;
  let newLevel: number;

  switch (quality) {
    case 'again':
      newLevel = 0;
      break;
    case 'hard':
      newLevel = Math.max(0, baseLevel - 1);
      break;
    case 'good':
      newLevel = Math.min(5, baseLevel + 1);
      break;
    case 'easy':
      newLevel = Math.min(5, baseLevel + 2);
      break;
  }

  return {
    word,
    level: newLevel,
    nextReview: calculateNextReview(newLevel),
    lastReview: now,
    reviewCount: (current?.reviewCount ?? 0) + 1,
    createdAt: current?.createdAt ?? now,
    isSkipped: false,
  };
}

export function markAsSkipped(word: string): WordProgress {
  const now = Date.now();
  return {
    word,
    level: 5,
    nextReview: Number.MAX_SAFE_INTEGER, // Never review
    lastReview: now,
    reviewCount: 0,
    createdAt: now,
    isSkipped: true,
  };
}
```

### Review Distribution Example

Without fuzzing:
```
Day 1: Learn 100 words
Day 2: 100 reviews due  ← Overwhelming!
Day 4: 100 reviews due
```

With fuzzing (±10%):
```
Day 1: Learn 100 words
Day 2: ~90 reviews due
Day 3: ~10 reviews due  ← Spread out
Day 4: ~85 reviews due
Day 5: ~15 reviews due
```

---

## Page Structure

```
/                    # Home: Dashboard
├── /browse          # Word List (main management page)
├── /learn/[group]   # Learn new words by group
├── /review          # Review due words
└── /settings        # Settings page
```

### Static Export Configuration

For `output: 'export'` mode, dynamic routes require `generateStaticParams`:

```typescript
// app/learn/[group]/page.tsx
import { WORD_GROUPS } from '@/types/word';

export function generateStaticParams() {
  return WORD_GROUPS.map((group) => ({ group }));
}

export default function LearnPage({ params }: { params: { group: string } }) {
  // ...
}
```

### Page Details

#### Home `/`

Dashboard showing:
- Today's due review count (with "Start Review" button)
- Learning statistics (distribution by status)
- Quick entry to continue learning
- Progress overview by word group

```
┌─────────────────────────────────────────────────────────────────┐
│  Dashboard                                                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌─────────────────┐    ┌─────────────────┐                     │
│  │  Due Today      │    │  Total Progress │                     │
│  │     42          │    │   1,234 / 10,000│                     │
│  │ [Start Review]  │    │   ████████░░░░  │                     │
│  └─────────────────┘    └─────────────────┘                     │
│                                                                  │
│  Progress by Group:                                              │
│  1-1000     ████████████████████ 100%                           │
│  1001-2000  ████████░░░░░░░░░░░░  40%                           │
│  2001-3000  ░░░░░░░░░░░░░░░░░░░░   0%                           │
│  ...                                                             │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Browse Page `/browse`

Main word management page with filtering, search, and quick marking.

```
┌─────────────────────────────────────────────────────────────────┐
│  Browse Words                                                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Group: [1-1000 ▼]    Status: [All ▼]    Search: [__________]   │
│                        - All                                     │
│                        - Unknown                                 │
│                        - Learning                                │
│                        - Known (skipped + mastered)              │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  #1    the      ────────────────────────────  [Know It ✓]  ●    │
│  #2    of       ────────────────────────────  [Know It ✓]  ●    │
│  #3    and      ────────────────────────────  [Know It ✓]  ●    │
│  #4    eloquent ────────────────────────────  [Know It  ]  ○    │
│  #5    perhaps  ──────────── Level 3 ───────  [Know It  ]  ◐    │
│                              Next: 5 days                        │
│  #6    master   ──────────── Level 5 ───────  [Know It  ]  ★    │
│                              Mastered                            │
│  ...                                                             │
│                                                                  │
├─────────────────────────────────────────────────────────────────┤
│  ← Prev    Page 1 of 10 (1-100 of 1000)    Next →               │
│                                                                  │
│  Quick Actions:  [Mark Page as Known]  [Start Learning Group]   │
└─────────────────────────────────────────────────────────────────┘
```

**Interactions**:

| Action | Result |
|--------|--------|
| Click word row | Expand to show definition (fetch from API) |
| Click "Know It" checkbox | Toggle: unknown ↔ skipped |
| Click status icon | Show detail popup (level, next review date) |
| "Mark Page as Known" | Batch mark all unknown words on current page |
| "Start Learning Group" | Navigate to `/learn/[group]` |

**Pagination**:
- 100 words per page
- Total 10 pages per group (1000 words)

#### Learn Page `/learn/[group]`

Card-style learning interface for new words.

```
┌─────────────────────────────────────────────────────────────────┐
│  Learning: 1001-2000                          Progress: 15/20   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    ┌─────────────────────┐                      │
│                    │                     │                      │
│                    │      eloquent       │                      │
│                    │                     │                      │
│                    │    [Show Answer]    │                      │
│                    │                     │                      │
│                    └─────────────────────┘                      │
│                                                                  │
│                              or                                  │
│                                                                  │
│                    ┌─────────────────────┐                      │
│                    │  eloquent           │                      │
│                    │  /ˈeləkwənt/  🔊    │                      │
│                    │                     │                      │
│                    │  adj: fluent or     │                      │
│                    │  persuasive in      │                      │
│                    │  speaking or writing│                      │
│                    └─────────────────────┘                      │
│                                                                  │
│         [Again]    [Hard]    [Good]    [Easy]                   │
│          0 days    1 day     3 days    7 days                   │
│                                                                  │
│  Keyboard: 1        2         3         4                       │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

**Flow**:
1. Shows only "unknown" words from selected group
2. User clicks "Show Answer" to reveal definition
3. User selects difficulty to set review schedule
4. Card advances to next word

#### Review Page `/review`

Review words that are due (nextReview <= now).

```
┌─────────────────────────────────────────────────────────────────┐
│  Review                                         Remaining: 42   │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│                    (Same card UI as Learn page)                 │
│                                                                  │
│  Only shows words where:                                        │
│  - status = 'learning'                                          │
│  - nextReview <= Date.now()                                     │
│  - isSkipped = false                                            │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

#### Settings Page `/settings`

- Export progress (download JSON file)
- Import progress (upload JSON file)
- Clear definition cache (free up IndexedDB space)
- Reset all progress (requires confirmation)
- Daily new words count setting

---

## Directory Structure

```
src/
├── app/
│   ├── layout.tsx
│   ├── page.tsx                    # Home/Dashboard
│   ├── browse/
│   │   └── page.tsx                # Browse & mark words
│   ├── learn/
│   │   └── [group]/
│   │       └── page.tsx            # Learn new words
│   ├── review/
│   │   └── page.tsx                # Review due words
│   ├── settings/
│   │   └── page.tsx
│   └── manifest.ts                 # PWA manifest
├── components/
│   ├── word-card/
│   │   ├── index.tsx               # Main WordCard component
│   │   └── components/
│   │       ├── card-front.tsx
│   │       └── card-back.tsx
│   ├── word-list/
│   │   ├── index.tsx               # Word list for Browse page
│   │   └── components/
│   │       ├── word-row.tsx
│   │       ├── status-badge.tsx
│   │       └── pagination.tsx
│   ├── definition-view/
│   │   ├── index.tsx
│   │   └── components/
│   │       ├── phonetic-display.tsx
│   │       └── meaning-list.tsx
│   ├── review-buttons/
│   │   └── index.tsx
│   ├── progress-bar/
│   │   └── index.tsx
│   └── stats-card/
│       └── index.tsx
├── lib/
│   ├── db.ts                       # Dexie.js database setup
│   ├── word-loader.ts              # Lazy load word JSON files
│   ├── api.ts                      # Dictionary API calls
│   ├── audio.ts                    # Audio playback with fallback
│   └── spaced-repetition.ts        # Spaced repetition algorithm
├── stores/
│   ├── progress-store.ts           # Jotai atoms for progress (async)
│   └── settings-store.ts           # Jotai atoms for settings
├── hooks/
│   ├── use-progress.ts
│   ├── use-definition.ts
│   ├── use-word-group.ts           # Load word group data
│   └── use-review-queue.ts
├── types/
│   ├── word.ts
│   ├── progress.ts
│   ├── definition.ts
│   └── settings.ts
└── sw.ts                           # Service worker for PWA
```

---

## Component Design

### WordCard

Main component for learning and review with **prefetching**.

```typescript
// components/word-card/index.tsx
export type WordCardProps = {
  word: string;
  rank: number;
  nextWord?: string;  // For prefetching
  onAnswer: (quality: ReviewQuality) => void;
};

type CardState = 'front' | 'back';

export function WordCard({ word, rank, nextWord, onAnswer }: WordCardProps) {
  const [state, setState] = useState<CardState>('front');
  const { definition, isLoading } = useDefinition(word);

  // Prefetch next word's definition
  usePrefetchDefinition(nextWord);

  // ...
}
```

### Prefetching Strategy

When user is viewing Card N, silently fetch Card N+1's definition:

```typescript
// hooks/use-prefetch-definition.ts
export function usePrefetchDefinition(word: string | undefined) {
  useEffect(() => {
    if (!word) return;

    // Check if already cached
    db.definitions.get(word).then((cached) => {
      if (!cached) {
        // Silently fetch and cache
        fetchDefinition(word).catch(() => {
          // Ignore errors for prefetch
        });
      }
    });
  }, [word]);
}
```

### WordList

Component for Browse page word list.

```typescript
// components/word-list/index.tsx
export type WordListProps = {
  words: Word[];
  progressMap: Map<string, WordProgress>;
  onToggleSkip: (word: string) => void;
  onWordClick: (word: string) => void;
};

export function WordList({ words, progressMap, onToggleSkip, onWordClick }: WordListProps) {
  // ...
}
```

### DefinitionView

Displays word definition:
- Phonetics + pronunciation button
- Part of speech classification
- Definition list
- Example sentences (if available)

### ReviewButtons

Four buttons: Again / Hard / Good / Easy
- Shows next review interval preview
- Supports keyboard shortcuts (1/2/3/4)

---

## Audio Playback with Fallback

When API audio is unavailable or slow, fall back to Web Speech API:

```typescript
// lib/audio.ts

/**
 * Play word pronunciation with fallback to TTS
 */
export async function playPronunciation(
  word: string,
  audioUrl?: string
): Promise<void> {
  // Try API audio first
  if (audioUrl) {
    try {
      const audio = new Audio(audioUrl);
      audio.preload = 'auto';

      await Promise.race([
        audio.play(),
        // Timeout after 3 seconds
        new Promise((_, reject) =>
          setTimeout(() => reject(new Error('Audio timeout')), 3000)
        ),
      ]);
      return;
    } catch (e) {
      console.warn('API audio failed, falling back to TTS:', e);
    }
  }

  // Fallback: Web Speech API (TTS)
  return new Promise((resolve, reject) => {
    if (!window.speechSynthesis) {
      reject(new Error('Speech synthesis not supported'));
      return;
    }

    const utterance = new SpeechSynthesisUtterance(word);
    utterance.lang = 'en-US';
    utterance.rate = 0.9;

    utterance.onend = () => resolve();
    utterance.onerror = (e) => reject(e);

    speechSynthesis.speak(utterance);
  });
}
```

**Benefits**:
- 100% pronunciation coverage (TTS always available)
- No network latency for TTS fallback
- Graceful degradation

---

## State Management with Jotai

Using async atoms with IndexedDB:

```typescript
// stores/progress-store.ts
import { atom } from 'jotai';
import { db, type WordProgress } from '@/lib/db';

// Async atom that reads from IndexedDB
export const progressMapAtom = atom(async () => {
  const allProgress = await db.progress.toArray();
  return new Map(allProgress.map((p) => [p.word, p]));
});

// Writable atom for updates
export const updateProgressAtom = atom(
  null,
  async (get, set, progress: WordProgress) => {
    await db.progress.put(progress);
    // Trigger refresh
    set(progressMapAtom);
  }
);

// Derived atom: words due for review
export const dueWordsAtom = atom(async (get) => {
  const now = Date.now();
  return db.progress
    .where('nextReview')
    .belowOrEqual(now)
    .and((p) => !p.isSkipped && p.level < 5)
    .toArray();
});

// Derived atom: statistics (uses indexed query for performance)
export const statsAtom = atom(async (get) => {
  const [skippedCount, learningCount, masteredCount] = await Promise.all([
    db.progress.where('isSkipped').equals(1).count(),
    db.progress.where('level').below(5).and((p) => !p.isSkipped).count(),
    db.progress.where('level').equals(5).and((p) => !p.isSkipped).count(),
  ]);

  return {
    skipped: skippedCount,
    learning: learningCount,
    mastered: masteredCount,
  };
});
```

```typescript
// stores/settings-store.ts
import { atomWithStorage } from 'jotai/utils';

export type Settings = {
  dailyNewWords: number;
  theme: 'light' | 'dark' | 'system';
};

// Settings stay in localStorage (small, needs sync read)
export const settingsAtom = atomWithStorage<Settings>('settings', {
  dailyNewWords: 20,
  theme: 'system',
});
```

---

## API Integration

### Dictionary API with Robust Validation

```typescript
// lib/api.ts
import { z } from 'zod';
import { db } from './db';

// Schemas with fallback defaults
const phoneticsSchema = z
  .array(
    z.object({
      text: z.string().optional(),
      audio: z.string().url().optional(),
    })
  )
  .catch([]);

const definitionSchema = z.object({
  definition: z.string(),
  example: z.string().optional(),
  synonyms: z.array(z.string()).catch([]),
});

const meaningSchema = z.object({
  partOfSpeech: z.string(),
  definitions: z.array(definitionSchema).catch([]),
});

export const dictionaryResponseSchema = z
  .object({
    word: z.string(),
    phonetic: z.string().optional(),
    phonetics: phoneticsSchema,
    meanings: z.array(meaningSchema).catch([]),
  })
  .transform((data) => ({
    ...data,
    // Ensure at least one phonetic entry
    phonetics:
      data.phonetics.length > 0
        ? data.phonetics
        : data.phonetic
          ? [{ text: data.phonetic }]
          : [],
  }));

export type DictionaryResponse = z.infer<typeof dictionaryResponseSchema>;

export async function fetchDefinition(
  word: string
): Promise<DictionaryResponse | null> {
  // 1. Check IndexedDB cache first
  const cached = await db.definitions.get(word);
  if (cached) return cached.data;

  // 2. Fetch from API
  try {
    const res = await fetch(
      `https://api.dictionaryapi.dev/api/v2/entries/en/${encodeURIComponent(word)}`
    );

    if (!res.ok) {
      if (res.status === 404) {
        // Word not found in dictionary
        return null;
      }
      throw new Error(`API error: ${res.status}`);
    }

    const data = await res.json();
    const parsed = dictionaryResponseSchema.safeParse(data[0]);

    if (!parsed.success) {
      console.error('Invalid API response:', parsed.error);
      return null;
    }

    // 3. Save to cache
    await db.definitions.put({
      word,
      data: parsed.data,
      fetchedAt: Date.now(),
    });

    return parsed.data;
  } catch (error) {
    console.error('Failed to fetch definition:', error);
    return null;
  }
}
```

---

## PWA Support

### Configuration

```typescript
// next.config.js
const withSerwist = require('@serwist/next').default({
  swSrc: 'src/sw.ts',
  swDest: 'public/sw.js',
});

module.exports = withSerwist({
  output: 'export',
  images: {
    unoptimized: true,
  },
});
```

```typescript
// src/sw.ts
import { defaultCache } from '@serwist/next/worker';
import { Serwist } from 'serwist';

const serwist = new Serwist({
  precacheEntries: self.__SW_MANIFEST,
  skipWaiting: true,
  clientsClaim: true,
  navigationPreload: true,
  runtimeCaching: defaultCache,
});

serwist.addEventListeners();
```

```typescript
// app/manifest.ts
import type { MetadataRoute } from 'next';

export default function manifest(): MetadataRoute.Manifest {
  return {
    name: 'English Words',
    short_name: 'Words',
    description: 'Vocabulary learning app with spaced repetition',
    start_url: '/',
    display: 'standalone',
    background_color: '#ffffff',
    theme_color: '#000000',
    icons: [
      {
        src: '/icon-192.png',
        sizes: '192x192',
        type: 'image/png',
      },
      {
        src: '/icon-512.png',
        sizes: '512x512',
        type: 'image/png',
      },
    ],
  };
}
```

**Benefits**:
- Offline access to learned words and cached definitions
- Add to home screen on mobile
- Native app-like experience
- Perfect for subway/airplane study sessions

---

## Data Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                        User Interaction                          │
│                                                                  │
│  Browse Page          Learn Page           Review Page          │
│  - Toggle "Know It"   - Answer cards       - Answer cards       │
│  - View definitions   - View definitions   - View definitions   │
└─────────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────────┐
│                        Jotai Atoms                               │
│                                                                  │
│  progressMapAtom ──────► dueWordsAtom (async, indexed query)    │
│       │                                                          │
│       └─────────────────► statsAtom (async, indexed query)      │
│                                                                  │
│  settingsAtom (localStorage)                                    │
└─────────────────────────────────────────────────────────────────┘
                            │
              ┌─────────────┴─────────────┐
              ▼                           ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│     localStorage        │   │   IndexedDB (Dexie.js)  │
│  - settings             │   │  - progress (indexed)   │
│  - last-group           │   │  - definitions (cached) │
└─────────────────────────┘   └─────────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   Dictionary API        │
                              │  (On-demand fetch)      │
                              └─────────────────────────┘
                                          │
                                          ▼
                              ┌─────────────────────────┐
                              │   Web Speech API        │
                              │  (TTS fallback)         │
                              └─────────────────────────┘
```

---

## Deployment

### Static Export Configuration

```javascript
// next.config.js
const withSerwist = require('@serwist/next').default({
  swSrc: 'src/sw.ts',
  swDest: 'public/sw.js',
});

module.exports = withSerwist({
  output: 'export',
  images: {
    unoptimized: true,
  },
});
```

### Deployment Options

| Platform | Description |
|----------|-------------|
| GitHub Pages | Free, suitable for personal projects |
| Vercel | Free, auto-deployment |
| Netlify | Free, auto-deployment |
| Any Static Hosting | Just upload `out/` directory |

---

## Future Extensions (Optional)

Consider after MVP completion:

1. **Dark Mode**: Follow system or manual toggle
2. **Learning Reminder**: Use Notification API
3. **Learning Statistics Chart**: Use Chart.js or Recharts
4. **Custom Word List**: Users add their own words
5. **Cloud Sync** (optional): Use third-party services like Firebase
6. **E-Factor Algorithm**: Full SM-2 implementation with per-word ease factor

---

## Development Plan

### Phase 1: Foundation
- [ ] Initialize Next.js project with pnpm
- [ ] Configure Tailwind CSS and shadcn/ui
- [ ] Set up Dexie.js database schema
- [ ] Convert word CSV to JSON files in `public/data/`
- [ ] Implement word loader with caching

### Phase 2: Core Features + PWA
- [ ] Implement IndexedDB storage layer with Jotai async atoms
- [ ] Implement Dictionary API integration with Zod validation
- [ ] Implement spaced repetition algorithm with fuzzing
- [ ] Implement audio playback with TTS fallback
- [ ] Set up PWA with Serwist

### Phase 3: Browse Page
- [ ] word-list component with pagination
- [ ] Status filtering and search
- [ ] "Know It" toggle functionality
- [ ] Expandable definition view

### Phase 4: Learn & Review
- [ ] word-card component with prefetching
- [ ] review-buttons component
- [ ] Learn page with group selection
- [ ] Review page with due words queue

### Phase 5: Dashboard & Settings
- [ ] Home dashboard with statistics
- [ ] Settings page (import/export)
- [ ] Progress visualization

### Phase 6: Polish & Deploy
- [ ] Responsive design optimization
- [ ] Keyboard shortcuts support
- [ ] Performance optimization
- [ ] Static export deployment
- [ ] generateStaticParams for dynamic routes

---

## Performance Considerations

### Bundle Size
- Word data split into 10 JSON files (~30KB each)
- Lazy loading on route navigation
- Main bundle stays under 100KB gzipped

### IndexedDB Performance
- Use indexed queries for filtering (`where`, `below`, `equals`)
- Avoid full table scans
- Batch writes when possible

### Jotai Optimization
- Use async atoms for IndexedDB reads
- Avoid derived atoms that iterate over entire dataset
- Consider `atomFamily` if per-word state causes issues

### Prefetching
- Prefetch next card's definition while viewing current
- Cache word group data in memory after first load

---

## References

- [Next.js Documentation](https://nextjs.org/docs)
- [Tailwind CSS Documentation](https://tailwindcss.com/docs)
- [shadcn/ui Documentation](https://ui.shadcn.com)
- [Jotai Documentation](https://jotai.org)
- [Dexie.js Documentation](https://dexie.org)
- [Serwist Documentation](https://serwist.pages.dev)
- [Zod Documentation](https://zod.dev)
- [Free Dictionary API](https://dictionaryapi.dev/)
- [SM-2 Algorithm](https://en.wikipedia.org/wiki/SuperMemo#Description_of_SM-2_algorithm)
- [Web Speech API](https://developer.mozilla.org/en-US/docs/Web/API/Web_Speech_API)
