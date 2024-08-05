import os
import random
import re
import sys
import copy

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    
    # empty dictionary we will add to
    page_probability = {}

    num_links = len(corpus[page])
    total_pages = len(corpus)

    # if the page has no links, return an equal distribution of every page
    if num_links == 0:
        for p in corpus:
            page_probability[p] = 1/ total_pages

        return page_probability
    
    else:

        # probability of clicking a link on the page
        link_prob = damping_factor / num_links
        # probability of picking a page at random
        random_prob = (1 - damping_factor) / len(corpus)

        # probability of every page being picked at random
        for p in corpus:
            page_probability[p] = random_prob

        # probability of a link being clicked at random
        for link in corpus[page]:
            page_probability[link] += link_prob

        return page_probability


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # get the first sample
    current_page = random.choice(list(corpus.keys()))

    # create counting dictionary
    pagerank = {page: 0 for page in corpus}

    # increment current page by 1
    pagerank[current_page] += 1

    for i in range(1, n):
        # get the next page probabilities
        next_page_dict = transition_model(corpus, current_page, damping_factor)

        current_page = random.choices(list(next_page_dict.keys()), weights=list(next_page_dict.values()), k = 1)[0]
        pagerank[current_page] += 1

    pagerank = {page: num / n for page, num in pagerank.items()}

    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    
    page_num = len(corpus)

    # pagerank dictionary
    pagerank = {page: 1 / page_num for page in corpus}

    new_pagerank = pagerank.copy()

    while True:

        for page in corpus:

            rank_sum = 0

            for linked_page in pagerank:
                
                if page in corpus[linked_page]:
                    rank_sum += pagerank[linked_page] / len(corpus[linked_page])
                
                elif not corpus[linked_page]:
                    rank_sum += pagerank[linked_page] / page_num

            new_pagerank[page] = ((1 - damping_factor) / page_num) + (damping_factor * rank_sum)

        if all(abs(new_pagerank[page] - pagerank[page]) < 0.001 for page in pagerank):
            break

        pagerank = new_pagerank.copy()

    return pagerank
        

if __name__ == "__main__":
    main()
