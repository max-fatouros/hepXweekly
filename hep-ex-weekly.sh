#!/bin/bash

# Fetch latest HEP-EX related papers from INSPIRE-HEP
API="https://inspirehep.net/api/literature"
QUERY="q=hep-ex"
SORT="sort=mostrecent"
SIZE=25
FIELDS="fields=metadata.title,metadata.abstracts,metadata.arxiv_eprints,metadata.preprint_date,metadata.control_number"

echo "🔍 Fetching latest HEP-EX related papers from INSPIRE-HEP..."

response=$(curl -s "${API}?${QUERY}&${SORT}&size=${SIZE}&${FIELDS}")

count=$(echo "$response" | jq '.hits.hits | length')
if (( count == 0 )); then
  echo "🚫 No HEP-EX papers found."
  exit 0
fi

echo "📚 Found $count recent HEP-EX papers:"
echo "---------------------------------------------"

echo "$response" | jq -r '
  .hits.hits[] |
  {
    title: (.metadata.title[0].title // "❓ No title"),
    abstract: (.metadata.abstracts[0].value // "No abstract available."),
    arxiv: (.metadata.arxiv_eprints[0].value // "N/A"),
    date: (.metadata.preprint_date // "No date"),
    link: ("https://inspirehep.net/literature/" + (.metadata.control_number | tostring))
  } |
  "🔹 \(.title)\n📄 \(.abstract)\n🗓️  \(.date)\n📎 arXiv: \(.arxiv)\n🔗 Link: \(.link)\n"
'
