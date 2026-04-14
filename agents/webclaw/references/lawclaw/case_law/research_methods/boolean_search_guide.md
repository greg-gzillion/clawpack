# Boolean Search Guide for Legal Research

## Overview
Boolean (terms and connectors) searching allows precise legal research by using logical operators to combine search terms. It is more precise than natural language searching.

## Basic Boolean Operators
| Operator | Function | Example |
|----------|----------|---------|
| **AND** | Both terms must appear | "summary judgment" AND "employment discrimination" |
| **OR** | Either term may appear | "wrongful termination" OR "constructive discharge" |
| **NOT** | Excludes term | "hostile environment" NOT "sexual" |

## Proximity Operators
| Operator | Function | Example |
|----------|----------|---------|
| **/s** | Terms in same sentence | "hostile work environment" /s "supervisor" |
| **/p** | Terms in same paragraph | "summary judgment" /p "genuine issue" |
| **/n** | Terms within n words | "constructive" /5 "discharge" |
| **PRE/n** | First term precedes second within n words | "summary" PRE/3 "judgment" |

## Wildcards and Root Expanders
| Operator | Function | Example | Finds |
|----------|----------|---------|-------|
| ***** | Unlimited characters | discriminat* | discriminate, discrimination, discriminatory |
| **!** | Single character | wom!n | woman, women |
| **?** | Optional character | labo?r | labor, labour |

## Phrase Searching
| Operator | Function | Example |
|----------|----------|---------|
| **" "** | Exact phrase | "summary judgment" |
| **{ }** | Exact phrase with punctuation | {res ipsa loquitur} |

## Field Restrictions
| Field | Syntax | Example |
|-------|--------|---------|
| **Court** | court("court name") | court("9th circuit") |
| **Judge** | judge("judge name") | judge("Reinhardt") |
| **Date** | date(YYYY-MM-DD) or after/before | after(2020-01-01) |
| **Jurisdiction** | jurisdiction("state") | jurisdiction("California") |
| **Attorney** | attorney("name") | attorney("Olson") |
| **Docket Number** | docket("number") | docket("19-123") |

## Advanced Search Strings

### Employment Discrimination Example
"hostile work environment" /s (supervisor OR manager) AND "Title VII" AND after(2015-01-01) AND court("9th circuit")

text

### Constitutional Law Example
("First Amendment" OR "free speech") /p (university OR college) AND "student" AND NOT "high school"

text

### Administrative Law Example
"Chevron deference" AND (agency OR EPA OR SEC) AND court("D.C. Circuit") AND after(2020-01-01)

text

## Database-Specific Syntax
| Feature | Westlaw | Lexis | Bloomberg |
|---------|---------|-------|-----------|
| **AND** | AND or & | AND | AND |
| **OR** | OR or space | OR | OR |
| **NOT** | NOT or % | AND NOT | NOT |
| **Sentence** | /s | /s | /s |
| **Paragraph** | /p | /p | /p |
| **Within n words** | /n | /n | /n |
| **Root expander** | ! | * | * |
| **Universal character** | * | ! | * |

## Search Tips
| Tip | Explanation |
|-----|-------------|
| **Start broad, then narrow** | Begin with OR search, refine with AND and NOT |
| **Use parentheses for grouping** | (A OR B) AND C - parentheses control order |
| **Check database-specific syntax** | Westlaw and Lexis have subtle differences |
| **Save successful searches** | Create alerts for recurring research |
| **Review search history** | Track what worked and what didn't |

## Common Mistakes
| Mistake | Correction |
|---------|------------|
| Too many ANDs | Use OR for synonyms; results too narrow |
| No root expander | discriminat* not discriminate |
| Missing parentheses | (A OR B) AND C ? A OR (B AND C) |
| Incorrect proximity | /s is sentence, /p is paragraph |

## Resources
- **Westlaw Search Guide**: https://legal.thomsonreuters.com/en/products/westlaw-edge/search-guide
- **Lexis Search Commands**: https://www.lexisnexis.com/search-commands
- **CourtListener Search Help**: https://www.courtlistener.com/help/search/

---
*Part of Clawpack LawClaw - Case Law Reference*
