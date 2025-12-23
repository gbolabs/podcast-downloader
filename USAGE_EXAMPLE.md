# Usage Example with Real Podcast Feed

## The Podcast

**Podcast Name:** Les histoires de Millie D. – RTS
**Description:** Ce podcast s'adresse aux enfants qui ont plein de questions sur le monde qui les entoure...
**Feed URL:** `https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss`
**Total Episodes:** 60 (as of December 2025)

## How to Download Episodes

### 1. Basic Download (30 episodes)

```bash
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss"
```

This will:
- Create a directory named `Les_histoires_de_Millie_D._‐_RTS`
- Download the 30 most recent episodes
- Generate a README.md with metadata

### 2. Download Specific Number of Episodes

Download only 10 episodes:

```bash
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss" -n 10
```

### 3. Save to Specific Directory

Save to your podcasts folder:

```bash
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss" -o ~/podcasts
```

### 4. Combine Options

Download 15 episodes to a specific folder:

```bash
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss" -n 15 -o ~/podcasts
```

## What You'll Get

### Directory Structure

```
Les_histoires_de_Millie_D._‐_RTS/
├── 2025-12-22_Esprit_de_Noël_es_tu_là__‐_Jour_23.mp3
├── 2025-12-21_Sous_le_feu_des_projecteurs__‐_Jour_22.mp3
├── 2025-12-20_La_petite_flamme_du_cœur__‐_Jour_21.mp3
├── 2025-12-19_Ça_sent_le_sapin_pour_les_sapins__‐_Jour_20.mp3
├── 2025-12-18_La_crème_de_la_crème__‐_Jour_19.mp3
└── README.md
```

### README.md Content

The generated README.md will look something like this:

```markdown
# Les histoires de Millie D. ‐ RTS

**Feed URL:** https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss

**Last updated:** 2025-12-23 15:30:45

**Description:**
Ce podcast s'adresse aux enfants qui ont plein de questions sur le monde qui les entoure...

---

## Downloaded Episodes

- [x] Esprit de Noël, es-tu là ? – Jour 23 (Mon, 22 Dec 2025 23:00:00 GMT)
- [x] Sous le feu des projecteurs – Jour 22 (Sun, 21 Dec 2025 23:00:00 GMT)
- [x] La petite flamme du cœur – Jour 21 (Sat, 20 Dec 2025 23:00:00 GMT)
- [x] Ça sent le sapin… pour les sapins ! – Jour 20 (Fri, 19 Dec 2025 23:00:00 GMT)
- [x] La crème de la crème ! – Jour 19 (Thu, 18 Dec 2025 23:00:00 GMT)
- [ ] La petite flamme du cœur – Jour 21 (Sat, 20 Dec 2025 23:00:00 GMT)
- [ ] Ça sent le sapin… pour les sapins ! – Jour 20 (Fri, 19 Dec 2025 23:00:00 GMT)
- [ ] La crème de la crème ! – Jour 19 (Thu, 18 Dec 2025 23:00:00 GMT)
```

## Updating Your Podcast Collection

When new episodes are published, simply run the downloader again:

```bash
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss"
```

The application will:
- Skip episodes that already exist
- Download only the new episodes
- Update the README.md with the new episodes marked as downloaded

## Tips

1. **Use quotes around URLs** with special characters to avoid shell interpretation issues
2. **Start with a small number** (e.g., -n 5) to test before downloading many episodes
3. **Check the README.md** after download to see what was downloaded
4. **Organize by podcast** - Each podcast gets its own directory

## Other Podcasts You Can Try

Here are some other French-language podcasts you might enjoy:

- **RTS Culture:** `https://www.rts.ch/play/radio/la-1ere-prochaine/rss`
- **Swiss Info:** `https://www.swissinfo.ch/eng/rssfeed/podcasts/swissinfo-in-a-minute`

## Troubleshooting

If you encounter issues:

1. **Check the URL** - Make sure it's a valid RSS feed
2. **Verify network** - Ensure you can access the URL in a browser
3. **Check permissions** - Make sure you have write access to the output directory
4. **Review logs** - The application prints detailed progress information

## Example Workflow

```bash
# First download - get 10 episodes
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss" -n 10

# Later, update to get more episodes
python3 podcast_downloader.py "https://www.rts.ch/podcasts-originaux/programmes/les-histoires-de-millie-d/podcast/?flux=rss" -n 20

# The second run will only download the additional 10 episodes
```
