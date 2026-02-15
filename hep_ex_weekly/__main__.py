"""
# hep-ex-weekly
"""

import webbrowser
from datetime import (
    datetime,
    timedelta,
)

import feedparser

# --- Config ---
CATEGORY = 'hep-ex'
DAYS_BACK = 7
MAX_RESULTS = 100
AUTHOR_CHAR_LIMIT = 200
API_URL = (
    f"http://export.arxiv.org/api/query?"
    f"search_query=cat:{CATEGORY}"
    f"&sortBy=lastUpdatedDate&sortOrder=descending&max_results=50"
)

# --- Helper Functions ---


def clean_text(text):
    return text.strip().replace('\n', ' ').replace('  ', ' ')


def matches_keywords(text, keywords):
    return any(kw.lower() in text.lower() for kw in keywords)


def shorten_authors(authors, limit=AUTHOR_CHAR_LIMIT):
    full = ', '.join(authors)
    if len(full) <= limit:
        return full
    short = ''
    for name in authors:
        if len(short + name + ', ') > limit:
            break
        short += name + ', '
    return short.rstrip(', ') + ' et al.'


# --- Prompt for filtering keywords ---
print('🔍 Fetching latest hep-ex papers from arXiv...')
print(
    '🔎 Optional: Enter keywords to filter papers'
    ' (e.g. CMS, ATLAS, FCC, ML, GNN). Press Enter to skip.',
)
keyword_input = input('Filter by keywords (comma-separated): ').strip()
keywords = [
    k.strip() for k in keyword_input.split(',')
    if k.strip()
] if keyword_input else []

# --- Fetch & Parse ---
start_date = datetime.now().date() - timedelta(days=DAYS_BACK)
feed = feedparser.parse(API_URL)
entries = feed.entries

# --- Filter Recent & Relevant Papers ---
papers = []
for entry in entries:
    pub_date = datetime.strptime(entry.published, '%Y-%m-%dT%H:%M:%SZ').date()
    if pub_date >= start_date:
        title = clean_text(entry.title)
        summary = clean_text(entry.summary)
        author_list = [author.name for author in entry.authors]
        authors_display = shorten_authors(author_list)
        arxiv_id = entry.id.split('/abs/')[-1]
        pdf_url = next(
            (
                link.href for link in entry.links
                if link.type == 'application/pdf'
            ),
            None,
        )
        announce_type = entry.get('arxiv_announce_type', 'new')

        if keywords and not matches_keywords(title + summary, keywords):
            continue  # Skip if keyword filtering is on and no match

        papers.append({
            'title': title,
            'summary': summary,
            'authors': authors_display,
            'date': pub_date,
            'id': arxiv_id,
            'pdf': pdf_url,
            'announce_type': announce_type,
        })

# --- Display Results ---
if not papers:
    print('🚫 No matching hep-ex papers found.')
    exit(0)

print(
    f"\n📚 Found {len(papers)} hep-ex papers"
    ' published in the last {DAYS_BACK} days:\n',
)

for i, p in enumerate(papers, 1):
    print(f"{i}. {p['title']}")
    print(f"   👨‍🔬 {p['authors']}")
    print(
        f"   🗓️ {p['date']} — arXiv:{p['id']}"
        f"  📌 {p['announce_type']}  🧠 {p['summary'][:200]}...",
    )
    print(f"   🔗 {p['pdf']}\n")

# --- Optional: Open in browser ---
try:
    choice = int(input('Enter number to open PDF, or 0 to exit: '))
    if 1 <= choice <= len(papers):
        webbrowser.open(papers[choice - 1]['pdf'])
except (ValueError, KeyboardInterrupt):
    pass
