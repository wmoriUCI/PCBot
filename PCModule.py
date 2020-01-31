# PC Function Bodies
# William Mori

import json
import requests
import statistics
from collections import defaultdict
from collections import Counter


def generateCurrencyPrintOut(currencyName, currencyList):
    currency_expand_dict = {"jew": "Jeweller's Orb", "chance": "Orb of Chance", "p": "Perandus Coins?",
                          "chrom": "Chromatic Orb", "alt": "Orb of Alteration", "blessed": "Blessed Orb",
                          "chaos": "Chaos Orb", "exa":"Exalted Orb", "mir": "Mirror of Kalandra",
                          "alch": "Orb of Alchemy", "fuse": "Orb of Fusing", "silver": "Silver Coin",
                          "regal": "Regal Orb", "vaal": "Vaal Orb", "gcp":"Gemcutter's Prism", "chisel": "Chisel",
                          "scour": "Scouring Orb"}
    nl = "\n"
    low_c_price = currencyList[0]
    avg_c_price = sum(currencyList) / len(currencyList)
    med_c_price = statistics.median(currencyList)
    modc = Counter(currencyList)
    mod_c_price = modc.most_common(1)[0][0]
    top_c_price = currencyList[-1]
    return f"{currency_expand_dict[currencyName]} pricing:{nl}Lowest: {low_c_price}, Highest:{top_c_price}{nl}" \
           f"Average: {avg_c_price}{nl}Median: {med_c_price}, Mode: {mod_c_price}{nl}" \
           f"Number of listings: {len(currencyList)}{nl}"


def makeLenTenLists(ids):
    yld_list = []
    for i in ids:
        yld_list.append(i)
        if len(yld_list) == 10:
            yield yld_list
            yld_list = []
    yield yld_list


async def searchItem(name, base):
    item_json = {
                "query": {
                        "status": {
                                "option": "online"
                                    },
                        "name": name,
                        "type": base,
                        "stats": [{
                                "type": "and",
                                "filters": []
                                }]
                        },
                "sort": {
                        "price": "asc"
                        }
                }

    poe_url_start = "https://www.pathofexile.com/api/trade/search/Metamorph"

    poe_url_item_get = "https://www.pathofexile.com/api/trade/fetch/"
    
    r = requests.post(poe_url_start, json=item_json)
    q = json.loads(r.text)

    try:
        suffix = "?query=" + q["id"]
    except KeyError:
        return "Invalid item search"

    currency_dict = defaultdict(list)
    for i in makeLenTenLists(q["result"]):
        if len(i) > 0:
            i = ",".join(i)
            final_url = poe_url_item_get + i + suffix
            response = requests.get(final_url)
            d1 = response.json()
            for num in range(len(d1["result"])):
                if d1["result"][num]["listing"]["price"] is not None:
                    currency_dict[d1["result"][num]["listing"]["price"]["currency"]].append(
                        d1["result"][num]["listing"]["price"]["amount"])

    ret_string = ""
    for key, value in currency_dict.items():
        ret_string += generateCurrencyPrintOut(key, value)
    return name + ", " + base + "================" + "\n" + ret_string
