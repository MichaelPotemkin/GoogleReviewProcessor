import tldextract


def extract_domain(url: str, include_subdomain: bool = True) -> str:
    """
    Extract the domain from a url

    Parameters:
        url: str
            The url to process
        include_subdomain: bool
            Whether to include the subdomain in the domain output

    Returns:
        str
            The domain of the url
    """
    tld = tldextract.extract(url)
    domain = f"{tld.domain}.{tld.suffix}"
    if tld.subdomain and include_subdomain:
        domain = f"{tld.subdomain}.{domain}"

    return domain
