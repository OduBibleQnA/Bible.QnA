import requests
from django.core.cache import cache
from datetime import timedelta
from django.utils import timezone

def get_votd_html(version="NASB1995"):
    cache_key = f"votd_html_{version}"
    cached = cache.get(cache_key)
    if cached:
        return cached

    url = f"https://www.biblegateway.com/votd/get/?format=json&version={version}"
    try:
        response = requests.get(url, timeout=3)
        response.raise_for_status()
        data = response.json()

        html = f"""
        <div class="card h-100">
            <div class="card-header">Verse of the Day</div>
            <div class="card-body">
                <blockquote class="blockquote mb-0">
                    <p>{data['votd']['text']}</p>
                    <footer class="blockquote-footer mt-2 text-muted-light">
                        <cite>{data['votd']['display_ref']}</cite>
                    </footer>
                </blockquote>
            </div>
        </div>
        """

        # Cache until midnight
        now = timezone.localtime()
        midnight = (now + timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0)
        seconds_until_midnight = int((midnight - now).total_seconds())

        cache.set(cache_key, html, timeout=seconds_until_midnight)
        return html

    except Exception:
        fallback = """
        <div class="card h-100">
            <div class="card-header">Verse of the Day</div>
            <div class="card-body text-muted">
                Unable to load the verse. Please visit 
                <a href="https://www.biblegateway.com/votd/" target="_blank">BibleGateway.com</a> 
                to view today's verse.
            </div>
        </div>
        """
        # Cache fallback briefly (e.g., 5 minutes)
        cache.set(cache_key, fallback, timeout=300)
        return fallback
