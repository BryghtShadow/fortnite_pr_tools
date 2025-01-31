from mwrogue.auth_credentials import AuthCredentials
from mwrogue.esports_client import EsportsClient

pages_to_make = [
    {
        'match': 'Infobox Player',
        'pages': [
            {
                'pattern': '{}/Tournament Results',
                'text': '{{PlayerTabsHeader}}\n{{PlayerResults|show=everything}}',
            },
            {
                'pattern': 'Tooltip:{}',
                'text': '{{PlayerTooltip}}',
            }
        ]
    },
]

summary = 'Automatically creating subpages/dependent pages'

credentials = AuthCredentials(user_file="bot")
site = EsportsClient('fortnite-esports', credentials=credentials)  # Set wiki

startat_page = 'Myth'
passed_startat = False

for i, page in enumerate(site.pages_using('Infobox Player')):
    if page.name == startat_page:
        passed_startat = True
    if not passed_startat:
        continue
    if page.namespace == 2:
        continue
    text = page.text()
    this_pages = None
    for page_set in pages_to_make:
        if page_set['match'] in text:
            this_pages = page_set['pages']
            break
    if this_pages is None:
        continue
    for item in this_pages:
        subpage = item['pattern'].format(page.name)
        print('Saving page %s...' % page.name)
        site.save_title(subpage, item['text'], summary=summary)
