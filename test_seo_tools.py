from seo_tools import audit_html, keyword_density, tokenize


def test_tokenize_normalizes_words():
    text = "SEO-driven Content, tested twice!"
    assert tokenize(text) == ["seo", "driven", "content", "tested", "twice"]


def test_keyword_density_single_and_multi_word():
    content = "SEO tools improve seo performance. Better SEO tools mean better results."
    densities = keyword_density(content, ["seo", "seo tools", "results"])

    assert densities["seo"] > 0
    assert densities["seo tools"] > 0
    assert densities["results"] > 0


def test_audit_html_flags_missing_items():
    html = """
    <html>
      <head><title>Short</title></head>
      <body>
        <p>Sample content without keyword repetition.</p>
        <img src='a.jpg'>
      </body>
    </html>
    """
    result = audit_html(html, ["technical seo"])

    assert result.checks["title_present"] is True
    assert result.checks["meta_description_present"] is False
    assert result.checks["has_h1"] is False
    assert result.checks["image_alt_coverage_ok"] is False
    assert result.checks["keywords_used"] is False
    assert result.recommendations


def test_audit_html_good_page_scores_high():
    html = """
    <html>
      <head>
        <title>Complete SEO Audit Checklist for Better Search Rankings</title>
        <meta name='description' content='A practical SEO audit checklist covering titles, headings, images, and keyword usage for sustainable ranking growth and stronger click-through rates.'>
      </head>
      <body>
        <h1>Complete SEO Audit Checklist</h1>
        <p>This SEO audit guide helps teams run a complete seo audit with confidence.</p>
        <img src='a.jpg' alt='SEO dashboard'>
      </body>
    </html>
    """
    result = audit_html(html, ["seo audit"])

    assert result.score >= 85
    assert result.checks["title_length_ok"] is True
    assert result.checks["meta_description_length_ok"] is True
    assert result.checks["has_h1"] is True
    assert result.checks["image_alt_coverage_ok"] is True
