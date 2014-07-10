import sys
import json
import pdb
import re
import operator

from collections import defaultdict

STATES = {
        'AK': 'Alaska',
        'AL': 'Alabama',
        'AR': 'Arkansas',
        'AS': 'American Samoa',
        'AZ': 'Arizona',
        'CA': 'California',
        'CO': 'Colorado',
        'CT': 'Connecticut',
        'DC': 'District of Columbia',
        'DE': 'Delaware',
        'FL': 'Florida',
        'GA': 'Georgia',
        'GU': 'Guam',
        'HI': 'Hawaii',
        'IA': 'Iowa',
        'ID': 'Idaho',
        'IL': 'Illinois',
        'IN': 'Indiana',
        'KS': 'Kansas',
        'KY': 'Kentucky',
        'LA': 'Louisiana',
        'MA': 'Massachusetts',
        'MD': 'Maryland',
        'ME': 'Maine',
        'MI': 'Michigan',
        'MN': 'Minnesota',
        'MO': 'Missouri',
        'MP': 'Northern Mariana Islands',
        'MS': 'Mississippi',
        'MT': 'Montana',
        'NA': 'National',
        'NC': 'North Carolina',
        'ND': 'North Dakota',
        'NE': 'Nebraska',
        'NH': 'New Hampshire',
        'NJ': 'New Jersey',
        'NM': 'New Mexico',
        'NV': 'Nevada',
        'NY': 'New York',
        'OH': 'Ohio',
        'OK': 'Oklahoma',
        'OR': 'Oregon',
        'PA': 'Pennsylvania',
        'PR': 'Puerto Rico',
        'RI': 'Rhode Island',
        'SC': 'South Carolina',
        'SD': 'South Dakota',
        'TN': 'Tennessee',
        'TX': 'Texas',
        'UT': 'Utah',
'VA': 'Virginia',
        'VI': 'Virgin Islands',
        'VT': 'Vermont',
        'WA': 'Washington',
        'WI': 'Wisconsin',
        'WV': 'West Virginia',
        'WY': 'Wyoming'
}

STATE_INV = {v:k for k, v in STATES.items()}

LARGE_CITIES = {
        "New York": "New York",
        "Los Angeles": "California",
        "Chicago": "Illinois",
        "Houston": "Texas",
        "Philaelphia": "Pennsylvania",
        "Phoenix": "Arizona",
        "San Antonio": "Texas",
        "San Diego": "California",
        "Dallas": "Texas",
        "San Jose": "California",
        "Austin": "Texas",
        "Inianapolis": "Iniana",
        "Jacksonville": "Florida",
        "San Francisco": "California",
        "Columbus": "Ohio",
        "Charlotte": "North Carolina",
        "Fort Worth": "Texas",
        "Detroit": "Michigan",
        "El Paso": "Texas",
        "Memphis": "Tennessee",
        "Seattle": "Washington",
        "Denver": "Colorado",
        "Washington": "District of Columbia",
        "Boston": "Massachusetts",
        "Nashville": "Tennessee",
        "Baltimore": "Maryland",
        "Oklahoma City": "Oklahoma",
        "Louisville": "Kentucky",
        "Portlan": "Oregon",
        "Las Vegas": "Nevada",
        "Milwaukee": "Wisconsin",
        "Albuquerque": "New Mexico",
        "Tucson": "Arizona",
        "Fresno": "California",
        "Sacramento": "California",
        "Long Beach": "California",
        "Kansas City": "Missouri",
        "Mesa": "Arizona",
        "Virginia Beach": "Virginia",
        "Atlanta": "Georgia",
        "Colorado Springs": "Colorado",
        "Omaha": "Nebraska",
        "Raleigh": "North Carolina",
        "Miami": "Florida",
        "Oaklan": "California",
        "Minneapolis": "Minnesota",
        "Tulsa": "Oklahoma",
        "Clevelan": "Ohio",
        "Wichita": "Kansas",
        "Arlington": "Texas",
        "New Orleans": "Louisiana",
        "Bakersfiel": "California",
        "Tampa": "Florida",
        "Honolulu": "Hawaii",
        "Aurora": "Colorado",
        "Anaheim": "California",
        "Santa Ana": "California",
        "St. Louis": "Missouri",
        "Riversie": "California",
        "Corpus Christi": "Texas",
        "Lexington": "Kentucky",
        "Pittsburgh": "Pennsylvania",
        "Anchorage": "Alaska",
        "Stockton": "California",
        "Cincinnati": "Ohio",
        "Saint Paul": "Minnesota",
        "Toleo": "Ohio",
        "Greensboro": "North Carolina",
        "Newark": "New Jersey",
        "Plano": "Texas",
        "Henerson": "Nevada",
        "Lincoln": "Nebraska",
        "Buffalo": "New York",
        "Jersey City": "New Jersey",
        "Chula Vista": "California",
        "Fort Wayne": "Iniana",
        "Orlano": "Florida",
        "St. Petersburg": "Florida",
        "Chanler": "Arizona",
        "Lareo": "Texas",
        "Norfolk": "Virginia",
        "Durham": "North Carolina",
        "Maison": "Wisconsin",
        "Lubbock": "Texas",
        "Irvine": "California",
        "Winston-Salem": "North Carolina",
        "Glenale": "Arizona",
        "Garlan": "Texas",
        "Hialeah": "Florida",
        "Reno": "Nevada",
        "Chesapeake": "Virginia",
        "Gilbert": "Arizona",
        "Baton Rouge": "Louisiana",
        "Irving": "Texas",
        "Scottsale": "Arizona",
        "North Las Vegas": "Nevada",
        "Fremont": "California",
        "Boise": "Iaho",
        "Richmon": "Virginia",
        "San Bernarino": "California",
        "Birmingham": "Alabama",
        "Spokane": "Washington",
        "Rochester": "New York",
        "Des Moines": "Iowa",
        "Moesto": "California",
        "Fayetteville": "North Carolina",
        "Tacoma": "Washington",
        "Oxnar": "California",
        "Fontana": "California",
        "Columbus": "Georgia",
        "Montgomery": "Alabama",
        "Moreno Valley": "California",
        "Shreveport": "Louisiana",
        "Aurora": "Illinois",
        "Yonkers": "New York",
        "Akron": "Ohio",
        "Huntington Beach": "California",
        "Little Rock": "Arkansas",
        "Augusta": "Georgia",
        "Amarillo": "Texas",
        "Glenale": "California",
        "Mobile": "Alabama",
        "Gran Rapis": "Michigan",
        "Salt Lake City": "Utah",
        "Tallahassee": "Florida",
        "Huntsville": "Alabama",
        "Gran Prairie": "Texas",
        "Knoxville": "Tennessee",
        "Worcester": "Massachusetts",
        "Newport News": "Virginia",
        "Brownsville": "Texas",
        "Overlan Park": "Kansas",
        "Santa Clarita": "California",
        "Provience": "Rhoe Islan",
        "Garen Grove": "California",
        "Chattanooga": "Tennessee",
        "Oceansie": "California",
        "Jackson": "Mississippi",
        "Fort Lauerale": "Florida",
        "Santa Rosa": "California",
        "Rancho Cucamonga": "California",
        "Port St. Lucie": "Florida",
        "Tempe": "Arizona",
        "Ontario": "California",
        "Vancouver": "Washington",
        "Cape Coral": "Florida",
        "Sioux Falls": "South Dakota",
        "Springfiel": "Missouri",
        "Peoria": "Arizona",
        "Pembroke Pines": "Florida",
        "Elk Grove": "California",
        "Salem": "Oregon",
        "Lancaster": "California",
        "Corona": "California",
        "Eugene": "Oregon",
        "Palmale": "California",
        "Salinas": "California",
        "Springfiel": "Massachusetts",
        "Pasaena": "Texas",
        "Fort Collins": "Colorado",
        "Haywar": "California",
        "Pomona": "California",
        "Cary": "North Carolina",
        "Rockfor": "Illinois",
        "Alexanria": "Virginia",
        "Esconio": "California",
        "McKinney": "Texas",
        "Kansas City": "Kansas",
        "Joliet": "Illinois",
        "Sunnyvale": "California",
        "Torrance": "California",
        "Brigeport": "Connecticut",
        "Lakewoo": "Colorado",
        "Hollywoo": "Florida",
        "Paterson": "New Jersey",
        "Naperville": "Illinois",
        "Syracuse": "New York",
        "Mesquite": "Texas",
        "Dayton": "Ohio",
        "Savannah": "Georgia",
        "Clarksville": "Tennessee",
        "Orange": "California",
        "Pasaena": "California",
        "Fullerton": "California",
        "Killeen": "Texas",
        "Frisco": "Texas",
        "Hampton": "Virginia",
        "McAllen": "Texas",
        "Warren": "Michigan",
        "Bellevue": "Washington",
        "West Valley City": "Utah",
        "Columbia": "South Carolina",
        "Olathe": "Kansas",
        "Sterling Heights": "Michigan",
        "New Haven": "Connecticut",
        "Miramar": "Florida",
        "Waco": "Texas",
        "Thousan Oaks": "California",
        "Cear Rapis": "Iowa",
        "Charleston": "South Carolina",
        "Visalia": "California",
        "Topeka": "Kansas",
        "Elizabeth": "New Jersey",
        "Gainesville": "Florida",
        "Thornton": "Colorado",
        "Roseville": "California",
        "Carrollton": "Texas",
        "Coral Springs": "Florida",
        "Stamfor": "Connecticut",
        "Simi Valley": "California",
        "Concor": "California",
        "Hartfor": "Connecticut",
        "Kent": "Washington",
        "Lafayette": "Louisiana",
        "Milan": "Texas",
        "Surprise": "Arizona",
        "Denton": "Texas",
        "Victorville": "California",
        "Evansville": "Iniana",
        "Santa Clara": "California",
        "Abilene": "Texas",
        "Athens": "Georgia",
        "Vallejo": "California",
        "Allentown": "Pennsylvania",
        "Norman": "Oklahoma",
        "Beaumont": "Texas",
        "Inepenence": "Missouri",
        "Murfreesboro": "Tennessee",
        "Ann Arbor": "Michigan",
        "Springfiel": "Illinois",
        "Berkeley": "California",
        "Peoria": "Illinois",
        "Provo": "Utah",
        "El Monte": "California",
        "Columbia": "Missouri",
        "Lansing": "Michigan",
        "Fargo": "North Dakota",
        "Downey": "California",
        "Costa Mesa": "California",
        "Wilmington": "North Carolina",
        "Arvaa": "Colorado",
        "Inglewoo": "California",
        "Miami Garens": "Florida",
        "Carlsba": "California",
        "Westminster": "Colorado",
        "Rochester": "Minnesota",
        "Oessa": "Texas",
        "Manchester": "New Hampshire",
        "Elgin": "Illinois",
        "West Joran": "Utah",
        "Roun Rock": "Texas",
        "Clearwater": "Florida",
        "Waterbury": "Connecticut",
        "Gresham": "Oregon",
        "Fairfiel": "California",
        "Billings": "Montana",
        "Lowell": "Massachusetts",
        "Ventura": "California",
        "Pueblo": "Colorado",
        "High Point": "North Carolina",
        "West Covina": "California",
        "Richmon": "California",
        "Murrieta": "California",
        "Cambrige": "Massachusetts",
        "Antioch": "California",
        "Temecula": "California",
        "Norwalk": "California",
        "Centennial": "Colorado",
        "Everett": "Washington",
        "Palm Bay": "Florida",
        "Wichita Falls": "Texas",
        "Green Bay": "Wisconsin",
        "Daly City": "California",
        "Burbank": "California",
        "Richarson": "Texas",
        "Pompano Beach": "Florida",
        "North Charleston": "South Carolina",
        "Broken Arrow": "Oklahoma",
        "Bouler": "Colorado",
        "West Palm Beach": "Florida",
        "Santa Maria": "California",
        "El Cajon": "California",
        "Davenport": "Iowa",
        "Rialto": "California",
        "Las Cruces": "New Mexico",
        "San Mateo": "California",
        "Lewisville": "Texas",
        "South Ben": "Iniana",
        "Lakelan": "Florida",
        "Erie": "Pennsylvania",
        "Tyler": "Texas",
        "Pearlan": "Texas",
        "College Station": "Texas",
}
        

class Tweet(object):
    def __init__(self, text, state):
        self.text = text
        self.state = state

    @classmethod
    def from_json(self, t_json):
        # if t_json['place'] and t_json['place']['country'] == 'United States':
        #     print t_json['place']
        #pdb.set_trace()
        place = t_json.get('place')
        if place == None:
            place = {} 

        full_name = place.get('full_name')
        state = None
        if full_name:
            place_type = place['place_type']
            parts = full_name.split(", ")
            if place_type == 'city':
                if len(parts) == 2:
                    city, state = parts
                    if STATES.has_key(state) == False:
                        state = None
            elif place_type == 'admin':
                if len(parts) == 2:
                    state_name, country = parts
                    if country == 'USA':
                        state = STATE_INV[state_name]
        else:
            loc = t_json['user']['location']
            for part in loc.split(", "):
                if STATES.has_key(part):
                    state = part
                elif STATE_INV.has_key(part):
                    state = STATE_INV[part]
                elif LARGE_CITIES.has_key(part):
                    state = STATE_INV[LARGE_CITIES[part]]


        return Tweet(t_json['text'], state)

    @classmethod
    def is_tweet(self, json):
        return json.has_key('text')

    def analyze_sentiment(self, sentiments):
        sum = 0
        for word in self.text.split(' '):
            word = word.lower()
            word = re.sub(r'[^a-z]', '', word)
            if len(word) == 0:
                continue
            if sentiments.has_key(word):
                sum += sentiments[word]
        return sum

def parse_sentiments(afinnfile):
    scores = {} # initialize an empty dictionary
    for line in afinnfile:
        term, score  = line.split("\t")  # The file is tab-delimited. "\t" means "tab character"
        scores[term] = int(score)  # Convert the score to an integer.

    return scores

def parse_tweets(tweet_file):
    tweets = []
    for line in tweet_file:
        tweet_json = json.loads(line)
        if Tweet.is_tweet(tweet_json):
            tweet = Tweet.from_json(tweet_json)
            tweets.append(tweet)
    return tweets

def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])

    sentiments = parse_sentiments(sent_file)
    tweets = parse_tweets(tweet_file)

    happyness = defaultdict(int)
    for tweet in tweets:
        if tweet.state:
            happyness[tweet.state] = tweet.analyze_sentiment(sentiments)

    # print happyness
    # print sum(happyness.values())
    print max(happyness.iteritems(), key=operator.itemgetter(1))[0]

if __name__ == '__main__':
    main()

