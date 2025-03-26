import streamlit as st
import requests
from bs4 import BeautifulSoup
import time


def search_papers(query):
    # Google Scholar URL with the search query
    search_url = f"https://scholar.google.com/scholar?q={query}"
    response = requests.get(search_url)

    # Debugging information
    print("Response Status Code:", response.status_code)
    print("Response Headers:", response.headers)
    print("Response Content:", response.text[:500])  # Print only the first 500 characters

    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        papers = []
        for result in soup.find_all('div', class_='gs_ri'):
            title_tag = result.find('h3', class_='gs_rt')
            title = title_tag.text if title_tag else 'No Title'
            link = title_tag.find('a')['href'] if title_tag and title_tag.find('a') else 'No Link'
            snippet = result.find('div', class_='gs_rs').text if result.find('div', class_='gs_rs') else 'No Abstract'
            papers.append({
                'title': title,
                'link': link,
                'snippet': snippet
            })
        return papers
    else:
        st.error(f"Error {response.status_code}: {response.text}")
        return []


def main():
    st.title("Google Scholar Research Paper Search")

    query = st.text_input("Enter a topic or title to search for research papers:")

    if st.button("Search"):
        if query.strip():  # Ensure query is not empty
            st.write("Searching for:", query)
            papers = search_papers(query)

            if papers:
                for paper in papers:
                    st.subheader(paper.get('title', 'No Title'))
                    st.write("Abstract:", paper.get('snippet', 'No Abstract'))
                    st.write("URL:", paper.get('link', 'No Link'))
                    st.write("---")
            else:
                st.write("No papers found.")
        else:
            st.write("Please enter a topic or title to search.")


if __name__ == "__main__":
    main()
