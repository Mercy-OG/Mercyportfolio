import os
from bs4 import BeautifulSoup
import re

html_files = [f for f in os.listdir('.') if f.endswith('.html')]

def update_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        html = f.read()
    
    soup = BeautifulSoup(html, 'html.parser')
    
    # Replace dashes/hyphens in text nodes
    for text_node in soup.find_all(string=True):
        if text_node.parent.name in ['style', 'script', 'head', 'title', 'meta']:
            continue
        original = str(text_node)
        modified = original.replace('-', ' ').replace('—', ' ').replace('–', ' ')
        modified = modified.replace('  ', ' ')
        if original != modified:
            text_node.replace_with(modified)

    # Add About link to nav menus
    navs = soup.find_all('nav', class_='nav-links')
    for nav in navs:
        about_link = nav.find('a', href='about.html')
        if not about_link:
            home_link = nav.find('a', href='index.html')
            if home_link:
                new_a = soup.new_tag('a', href='about.html')
                new_a.string = 'About'
                home_link.insert_after(new_a)
                home_link.insert_after('\n      ')

    foot_navs = soup.find_all('nav', class_='foot-nav')
    for nav in foot_navs:
        about_link = nav.find('a', href='about.html')
        if not about_link:
            home_link = nav.find('a', href='index.html')
            if home_link:
                new_a = soup.new_tag('a', href='about.html')
                new_a.string = 'About'
                home_link.insert_after(new_a)
                
    foot_col_links = soup.find_all('div', class_='foot-col-links')
    for div in foot_col_links:
        prev_h4 = div.find_previous_sibling('h4')
        if prev_h4 and prev_h4.text == 'Pages':
            about_link = div.find('a', href='about.html')
            if not about_link:
                home_link = div.find('a', href='index.html')
                if home_link:
                    new_a = soup.new_tag('a', href='about.html')
                    new_a.string = 'About'
                    home_link.insert_after(new_a)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(str(soup))

for f in html_files:
    update_file(f)
