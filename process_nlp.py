import spacy
nlp = spacy.load('en_core_web_md')
from models import RedditPosts
from pycountry import countries
from reddit_api import RedditPosts

country_set = set([country.name for country in countries])
country_set.add("Russia")

nationality_dict = {
    'american' : 'United States of America',
    'canadian' : 'Canada',
    'mexican' : 'Mexico',
    'ecuadorian' : 'Ecuador',
    'egyptian' : 'Egypt',
    'colombian' : 'Colombia',
    'indian' : 'India',
    'french' : 'France',
    'spanish' : 'Spain',
    'polish' : 'Poland',
    'iranian' : 'Iran',
    'ukrainian' : 'Ukraine',
    'russian' : 'Russia',
    'hungarian' : 'Hungary',
    'swedish' : 'Sweden',
    'norwegian' : 'Norway',
    'korean' : 'South Korea',  # Specify if North or South Korea
    'ethiopian' : 'Ethiopia',
    'chinese' : 'China',
    'japanese' : 'Japan',
    'vietnamese' : 'Vietnam',
    'nigerian' : 'Nigeria',
    'afghani' : 'Afghanistan',
    'australian' : 'Australia',
    'turkish' : 'Turkey',
    'german' : 'Germany',
    'israeli' : 'Israel',
    'palestinian' : 'Palestine',
    'italian' : 'Italy',
    'brazilian' : 'Brazil',
    'argentinian' : 'Argentina',
    'chilean' : 'Chile',
    'peruvian' : 'Peru',
    'belgian' : 'Belgium',
    'dutch' : 'Netherlands',
    'portuguese' : 'Portugal',
    'greek' : 'Greece',
    'finnish' : 'Finland',
    'danish' : 'Denmark',
    'icelandic' : 'Iceland',
    'saudi' : 'Saudi Arabia',
    'emirati' : 'United Arab Emirates',
    'qatari' : 'Qatar',
    'bahraini' : 'Bahrain',
    'kenyan' : 'Kenya',
    'south african' : 'South Africa',
    'thai' : 'Thailand',
    'malaysian' : 'Malaysia',
    'singaporean' : 'Singapore',
    'indonesian' : 'Indonesia',
    'filipino' : 'Philippines',
    'pakistani' : 'Pakistan',
    'bangladeshi' : 'Bangladesh',
    'sri lankan' : 'Sri Lanka',
    'nepalese' : 'Nepal',
    'bhutanese' : 'Bhutan',
    'mongolian' : 'Mongolia',
    'jordanian' : 'Jordan',
    'lebanese' : 'Lebanon',
    'syrian' : 'Syria',
    'iraqi' : 'Iraq',
    'kuwaiti' : 'Kuwait',
    'omani' : 'Oman',
    'yemeni' : 'Yemen',
    'new zealander' : 'New Zealand',
    'fijian' : 'Fiji',
    'tongan' : 'Tonga',
    'samoan' : 'Samoa',
    'canadian french' : 'Canada',  # For French-speaking Canadians
    'quebecois' : 'Canada',  # Specific to Quebec
    'british' : 'United Kingdom',
    'irish' : 'Ireland',
    'scottish' : 'Scotland',
    'welsh' : 'Wales',
    'czech' : 'Czech Republic',
    'slovak' : 'Slovakia',
    'romanian' : 'Romania',
    'bulgarian' : 'Bulgaria',
    'albanian' : 'Albania',
    'croatian' : 'Croatia',
    'serbian' : 'Serbia',
    'estonian' : 'Estonia',
    'bosnian' : 'Bosnia and Herzegovina',
    'montenegrin' : 'Montenegro',
    'slovenian' : 'Slovenia',
    'austrian' : 'Austria',
    'swiss' : 'Switzerland',
    'luxembourgish' : 'Luxembourg',
    'liechtensteiner' : 'Liechtenstein',
    'maltese' : 'Malta',
    'cypriot' : 'Cyprus',
    'armenian' : 'Armenia',
    'georgian' : 'Georgia',
    'azerbaijani' : 'Azerbaijan',
    'kazakh' : 'Kazakhstan',
    'uzbek' : 'Uzbekistan',
    'turkmen' : 'Turkmenistan',
    'kyrgyz' : 'Kyrgyzstan',
    'tajik' : 'Tajikistan',
    'north korean' : 'North Korea'
}



def parse_entities(submission_list: list[RedditPosts]):
    for s in submission_list:
        for sub_str in s.title.split(" "):
            title_case_sub_str = sub_str.strip().title()
            if title_case_sub_str in country_set and title_case_sub_str not in s.locations:
                s.locations.append(title_case_sub_str.title())
        doc = nlp(s.title)
        for ent in doc.ents:
            lower_case_ent_text = ent.text.title()
            if lower_case_ent_text in s.locations:
                continue
            if (ent.label_ == 'GPE'):
                s.locations.append(lower_case_ent_text)
            if (ent.label_ == 'NORP'):
                lowercase_norp = ent.text.lower()
                if lowercase_norp in nationality_dict and nationality_dict[lowercase_norp].title() not in s.locations:
                    s.locations.append(nationality_dict[lowercase_norp].title())