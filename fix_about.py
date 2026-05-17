from bs4 import BeautifulSoup

# Fix About section in about.html and remove from index.html
with open('index.html', 'r', encoding='utf-8') as f:
    index_soup = BeautifulSoup(f.read(), 'html.parser')

# Find the section by searching for the text "The Public Health Professional"
about_section = None
for sec in index_soup.find_all('section'):
    if 'The Public Health Professional' in sec.get_text():
        about_section = sec
        break

if about_section:
    with open('about.html', 'r', encoding='utf-8') as f:
        about_soup = BeautifulSoup(f.read(), 'html.parser')
    
    # Insert it right before the footer
    footer = about_soup.find('footer')
    if footer:
        footer.insert_before(BeautifulSoup(str(about_section), 'html.parser'))
    
    # Remove from index.html
    about_section.decompose()

    with open('about.html', 'w', encoding='utf-8') as f:
        f.write(str(about_soup))

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(str(index_soup))

print("Fixed About section successfully.")
